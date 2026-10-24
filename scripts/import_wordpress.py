#!/usr/bin/env python3
"""Repeatable WordPress-to-Markdown import for abdi.info.

Reads the WXR export and the extracted uploads. Does not modify either source.
Re-runs skip files whose body was edited after import (editorialRevision or a
changed body hash). German legal HTML is stored verbatim.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WXR = ROOT / ".wordpress_backup" / "azmirabdi039sblog.WordPress.2026-10-24.xml"
UPLOADS = ROOT / ".migration-work" / "uploads-full"
MEDIA_ROOT = ROOT / "src" / "assets" / "media"
POSTS_DE = ROOT / "src" / "content" / "posts" / "de"
LEGAL_DIR = ROOT / "src" / "content" / "legal"
PAGES_DE = ROOT / "src" / "content" / "pages" / "de"
GENERATED = ROOT / "src" / "generated"
DOCS = ROOT / "docs"
PY_DEPS = ROOT / ".migration-work" / "py"
if PY_DEPS.exists():
    sys.path.insert(0, str(PY_DEPS))

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "wp": "http://wordpress.org/export/1.2/",
}

WP_NS = "{http://wordpress.org/export/1.2/}"
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}"
EXCERPT_NS = "{http://wordpress.org/export/1.2/excerpt/}"

SIZE_SUFFIX = re.compile(r"-(?:\d+x\d+|scaled)(?=-\d|$)")
EDIT_SUFFIX = re.compile(r"-e\d{8,}")
DERIVATIVE_SUFFIX = re.compile(r"-(\d+)x(\d+)(?=\.[A-Za-z0-9]+$)")


def php_unserialize(raw: str):
    data = raw.encode("utf-8")
    index = 0

    def read(n: int) -> bytes:
        nonlocal index
        chunk = data[index : index + n]
        index += n
        return chunk

    def parse():
        nonlocal index
        if index >= len(data):
            raise ValueError("unexpected end")
        kind = chr(data[index])
        index += 1
        if kind == "N":
            index += 1  # ;
            return None
        if kind == "b":
            index += 1  # :
            value = chr(data[index]) == "1"
            index += 2  # digit ;
            return value
        if kind == "i":
            index += 1
            end = data.index(b";", index)
            value = int(data[index:end])
            index = end + 1
            return value
        if kind == "d":
            index += 1
            end = data.index(b";", index)
            value = float(data[index:end])
            index = end + 1
            return value
        if kind == "s":
            index += 1
            end = data.index(b":", index)
            length = int(data[index:end])
            index = end + 2  # :"
            value = read(length)
            index += 2  # ";
            return value.decode("utf-8")
        if kind == "a":
            index += 1
            end = data.index(b":", index)
            count = int(data[index:end])
            index = end + 2  # :{
            result = {}
            for _ in range(count):
                key = parse()
                result[key] = parse()
            index += 1  # }
            return result
        raise ValueError(f"unsupported php type {kind!r} at {index}")

    value = parse()
    return value


def text_of(node, path: str) -> str:
    found = node.find(path)
    return found.text if found is not None and found.text else ""


def metas(item) -> dict[str, str]:
    out = {}
    for meta in item.findall(f"{WP_NS}postmeta"):
        key = text_of(meta, f"{WP_NS}meta_key")
        value = text_of(meta, f"{WP_NS}meta_value")
        out[key] = value
    return out


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def yaml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def has_gps(path: Path) -> bool:
    if path.suffix.lower() not in {".jpg", ".jpeg"}:
        return False
    data = path.read_bytes()
    if data[:2] != b"\xff\xd8":
        return False
    i = 2
    while i < len(data) - 8:
        if data[i] != 0xFF:
            return False
        marker = data[i + 1]
        if marker == 0xDA:
            return False
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        seglen = int.from_bytes(data[i + 2 : i + 4], "big")
        if marker == 0xE1 and data[i + 4 : i + 8] == b"Exif":
            exif = data[i + 10 : i + 2 + seglen]
            if len(exif) < 8:
                return False
            endian = "little" if exif[:2] == b"II" else "big" if exif[:2] == b"MM" else None
            if not endian:
                return False

            def u16(off: int) -> int:
                return int.from_bytes(exif[off : off + 2], endian)

            def u32(off: int) -> int:
                return int.from_bytes(exif[off : off + 4], endian)

            seen: set[int] = set()

            def walk(off: int, depth: int = 0) -> bool:
                if off in seen or off <= 0 or off + 2 > len(exif) or depth > 6:
                    return False
                seen.add(off)
                count = u16(off)
                pos = off + 2
                for _ in range(count):
                    if pos + 12 > len(exif):
                        return False
                    tag = u16(pos)
                    if tag == 0x8825:
                        return True
                    if tag == 0x8769:
                        if walk(u32(pos + 8), depth + 1):
                            return True
                    pos += 12
                nxt = u32(pos) if pos + 4 <= len(exif) else 0
                return walk(nxt, depth + 1) if nxt else False

            try:
                return walk(u32(4))
            except Exception:
                return False
        i += 2 + seglen
    return False


def prepare_bytes(source: Path) -> tuple[bytes, str]:
    """Return bytes to store and a note. GPS-bearing JPEGs lose metadata."""
    raw = source.read_bytes()
    if not has_gps(source):
        return raw, "byte-identical"
    from PIL import Image, ImageOps
    import io

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        buffer = io.BytesIO()
        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")
        try:
            image.save(buffer, format="JPEG", quality="keep")
        except Exception:
            image.save(buffer, format="JPEG", quality=90, subsampling="4:2:0")
        return buffer.getvalue(), "gps-removed-metadata-stripped"


def frontmatter(data: dict) -> str:
    lines = ["---"]
    order = [
        "title",
        "description",
        "descriptionSource",
        "pubDate",
        "updatedDate",
        "lang",
        "originalLang",
        "translationKey",
        "provenance",
        "translationStatus",
        "needsReview",
        "draft",
        "wpId",
        "wpStatus",
        "author",
        "slug",
        "legacyPath",
        "year",
        "tags",
        "categories",
        "heroImage",
        "heroAlt",
        "wpContentHash",
        "bodyHash",
        "editorialRevision",
    ]
    for key in order:
        if key not in data:
            continue
        value = data[key]
        if isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        elif isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {yaml_string(str(item))}")
        elif value is None:
            lines.append(f"{key}: ")
        else:
            lines.append(f"{key}: {yaml_string(str(value))}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def existing_guard(path: Path, wp_hash: str, body: str) -> str | None:
    """Return a skip reason when an existing file must not be overwritten."""
    if not path.exists():
        return None
    current = path.read_text(encoding="utf-8")
    if re.search(r"^editorialRevision:\s*true\s*$", current, re.M):
        return "editorialRevision"
    match = re.search(r'^bodyHash:\s*"?([a-f0-9]+)"?\s*$', current, re.M)
    if match and match.group(1) != sha256_text(body):
        # Body in the file no longer matches the hash this importer would write
        # only when the stored hash differs from the file body. Recompute the
        # stored body and compare with the incoming body.
        stored = current.split("---", 2)
        if len(stored) == 3:
            existing_body = stored[2].lstrip("\n")
            if existing_body != body and match.group(1) != sha256_text(existing_body):
                return "body-edited"
            if existing_body == body:
                return "unchanged"
    wp_match = re.search(r'^wpContentHash:\s*"?([a-f0-9]+)"?\s*$', current, re.M)
    if wp_match and wp_match.group(1) == wp_hash and path.read_text(encoding="utf-8").endswith(body if False else ""):
        stored = current.split("---", 2)
        if len(stored) == 3 and stored[2].lstrip("\n") == body:
            return "unchanged"
    stored = current.split("---", 2)
    if len(stored) == 3:
        existing_body = stored[2].lstrip("\n")
        body_match = re.search(r'^bodyHash:\s*"?([a-f0-9]+)"?\s*$', current, re.M)
        if body_match and body_match.group(1) != sha256_text(existing_body):
            return "body-edited"
        if existing_body == body:
            return "unchanged"
    return None


class MarkdownConverter(HTMLParser):
    def __init__(self, image_resolver):
        super().__init__(convert_charrefs=True)
        self.image_resolver = image_resolver
        self.buffers: list[list[str]] = [[]]
        self.modes: list[str] = ["root"]
        self.pending_caption = False
        self.list_stack: list[str] = []
        self.ol_index: list[int] = []
        self.in_pre = False
        self.skip_depth = 0
        self.gallery_depth = 0
        self.gallery_items: list[str] = []
        self.link_text_start: list[int] = []

    def _append(self, text: str) -> None:
        if self.skip_depth:
            return
        if self.gallery_depth and text.strip() in {"", "\n"}:
            return
        self.buffers[-1].append(text)

    def handle_starttag(self, tag, attrs):
        attr = {key: value or "" for key, value in attrs}
        if tag == "gallery":
            self.gallery_depth += 1
            self.gallery_items = []
            return
        if tag in {"script", "style"}:
            self.skip_depth += 1
            self.modes.append("skip")
            return
        if tag == "br":
            self._append("\n" if self.in_pre else "  \n")
            return
        if tag == "p":
            self._append("\n\n")
            return
        if tag in {"h1", "h2", "h3", "h4", "h5"}:
            level = min(int(tag[1]) + 1, 4) if tag == "h1" else int(tag[1])
            # Keep a single h1 for the layout title. Former h1s become h2.
            if tag == "h1":
                level = 2
            self._append("\n\n" + ("#" * level) + " ")
            return
        if tag == "blockquote":
            self.buffers.append([])
            self.modes.append("blockquote")
            return
        if tag == "cite":
            self._append(" — ")
            return
        if tag in {"strong", "b"}:
            self._append("**")
            self.modes.append("strong")
            return
        if tag in {"em", "i"}:
            self._append("*")
            self.modes.append("em")
            return
        if tag == "a":
            self.modes.append("a:" + self.rewrite_href(attr.get("href", "")))
            self.link_text_start.append(len(self.buffers[-1]))
            self._append("[")
            return
        if tag == "code" and not self.in_pre:
            self._append("`")
            self.modes.append("code")
            return
        if tag == "pre":
            self.in_pre = True
            self._append("\n\n```\n")
            return
        if tag == "ul":
            self.list_stack.append("ul")
            self._append("\n")
            return
        if tag == "ol":
            self.list_stack.append("ol")
            self.ol_index.append(0)
            self._append("\n")
            return
        if tag == "li":
            indent = "  " * max(0, len(self.list_stack) - 1)
            if self.list_stack and self.list_stack[-1] == "ol":
                self.ol_index[-1] += 1
                marker = f"{self.ol_index[-1]}. "
            else:
                marker = "- "
            self._append(f"\n{indent}{marker}")
            return
        if tag == "img":
            self.emit_image(attr)
            return
        if tag == "figcaption":
            self.pending_caption = True
            self._append('\n\n<p class="caption">')
            return
        if tag == "hr":
            self._append("\n\n---\n\n")

    def handle_endtag(self, tag):
        if tag == "gallery":
            self.gallery_depth = max(0, self.gallery_depth - 1)
            if self.gallery_items:
                self._append("\n\n")
                for item in self.gallery_items:
                    self._append(f"- {item}\n")
                self.gallery_items = []
            return
        if tag in {"script", "style"} and self.modes and self.modes[-1] == "skip":
            self.modes.pop()
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag in {"strong", "b"} and self.modes and self.modes[-1] == "strong":
            self._append("**")
            self.modes.pop()
            return
        if tag in {"em", "i"} and self.modes and self.modes[-1] == "em":
            self._append("*")
            self.modes.pop()
            return
        if tag == "code" and not self.in_pre and self.modes and self.modes[-1] == "code":
            self._append("`")
            self.modes.pop()
            return
        if tag == "a" and self.modes and self.modes[-1].startswith("a:"):
            href = self.modes.pop()[2:]
            start = self.link_text_start.pop() if self.link_text_start else 0
            visible = "".join(self.buffers[-1][start:]).strip()
            if visible in {"", "["}:
                del self.buffers[-1][start:]
                return
            self._append(f"]({href})" if href else "](#)")
            return
        if tag == "pre":
            self.in_pre = False
            self._append("\n```\n\n")
            return
        if tag == "blockquote" and self.modes and self.modes[-1] == "blockquote":
            chunk = "".join(self.buffers.pop()).strip()
            self.modes.pop()
            quoted = "\n".join(f"> {line}" if line else ">" for line in chunk.splitlines())
            self._append("\n\n" + quoted + "\n\n")
            return
        if tag in {"ul", "ol"} and self.list_stack:
            kind = self.list_stack.pop()
            if kind == "ol" and self.ol_index:
                self.ol_index.pop()
            self._append("\n")
            return
        if tag == "figcaption" and self.pending_caption:
            self._append("</p>\n\n")
            self.pending_caption = False

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.in_pre:
            self._append(data.replace("\r\n", "\n"))
            return
        text = data.replace("\xa0", " ")
        if not self.pending_caption:
            text = re.sub(r"[ \t]+", " ", text)
        self._append(text)

    def rewrite_href(self, href: str) -> str:
        if not href or href.startswith(("mailto:", "tel:", "#")):
            return href
        parsed = urlparse(href)
        host = parsed.netloc.lower()
        if host in {"abdi.info", "www.abdi.info", "blog.abdi.info", "nas.abdi.info"}:
            if parsed.query.startswith("page_id=2") or parsed.path.rstrip("/").endswith("/about-me"):
                return "/about-me/"
            path = parsed.path or "/"
            if not path.startswith("/"):
                path = "/" + path
            if path.startswith("/wordpress/"):
                path = path[len("/wordpress") :]
            if not path.endswith("/") and "." not in Path(path).name:
                path += "/"
            return path
        return href

    def emit_image(self, attr: dict) -> None:
        src = attr.get("src", "")
        alt = attr.get("alt", "") or ""
        if not src:
            return
        resolved = self.image_resolver(src, attr.get("class", ""))
        if not resolved:
            self._append(f"\n\n<!-- unresolved-image: {src} -->\n\n")
            return
        markdown = f"![{alt}]({resolved})"
        if self.gallery_depth:
            self.gallery_items.append(markdown)
            return
        self._append("\n\n" + markdown + "\n\n")

    def result(self) -> str:
        text = "".join(self.buffers[0])
        text = text.replace("\r\n", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\*\*\s+\*\*", "", text)
        text = re.sub(r"\*\*([^*\n]+?)\s+\*\*", r"**\1**", text)
        text = re.sub(r"(?m)^-\s*$\n?", "", text)
        text = re.sub(r"\)\*{2,}", ")", text)
        return text.strip() + "\n"


def preprocess_html(source: str) -> str:
    text = source.replace("\r\n", "\n")
    text = re.sub(r"<!--\s*wp:gallery\b.*?-->", "<gallery>", text, flags=re.S)
    text = re.sub(r"<!--\s*/wp:gallery\s*-->", "</gallery>", text)
    text = re.sub(r"<!--\s*/?wp:.*?-->", "", text, flags=re.S)
    return text


def strip_tags(value: str) -> str:
    value = re.sub(r"<!--.*?-->", "", value, flags=re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value).replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def lead_description(markdown: str, limit: int = 180) -> str:
    plain = re.sub(r"`{3}[\s\S]*?`{3}", " ", markdown)
    plain = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", plain)
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
    plain = re.sub(r"<[^>]+>", " ", plain)
    plain = plain.replace("*", "").replace("#", "")
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) <= limit:
        return plain
    cut = plain[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def upload_rel_from_url(url: str) -> str | None:
    if not url:
        return None
    parsed = urlparse(url)
    path = unquote(parsed.path)
    marker = "/uploads/"
    if marker not in path:
        return None
    return path.split(marker, 1)[1].lstrip("/")


def basename_key(path: str) -> str:
    return Path(path).name.casefold()


def build_upload_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    if not UPLOADS.exists():
        return index
    for path in UPLOADS.rglob("*"):
        if path.is_file():
            rel = path.relative_to(UPLOADS).as_posix()
            index[rel] = path
            index[rel.casefold()] = path
    return index


def lookup_upload(index: dict[str, Path], rel: str) -> Path | None:
    if rel in index and isinstance(index[rel], Path) and index[rel].is_file():
        return index[rel]
    folded = rel.casefold()
    found = index.get(folded)
    if isinstance(found, Path) and found.is_file():
        return found
    return None


def main() -> None:
    if not WXR.exists():
        raise SystemExit(f"Missing export: {WXR}")
    if not UPLOADS.exists():
        raise SystemExit(f"Missing extracted uploads: {UPLOADS}")

    upload_index = build_upload_index()
    channel = ET.parse(WXR).getroot().find("channel")
    items = channel.findall("item")

    categories = []
    for node in channel.findall(f"{WP_NS}category"):
        categories.append(
            {
                "id": text_of(node, f"{WP_NS}category_nicename"),
                "wpTermId": int(text_of(node, f"{WP_NS}term_id") or 0),
                "nameDe": text_of(node, f"{WP_NS}cat_name"),
            }
        )
    tags = []
    for node in channel.findall(f"{WP_NS}tag"):
        tags.append(
            {
                "id": text_of(node, f"{WP_NS}tag_slug"),
                "wpTermId": int(text_of(node, f"{WP_NS}term_id") or 0),
                "nameDe": text_of(node, f"{WP_NS}tag_name"),
            }
        )

    attachments = {}
    for item in items:
        if text_of(item, f"{WP_NS}post_type") != "attachment":
            continue
        meta = metas(item)
        metadata = {}
        backup = {}
        raw_meta = meta.get("_wp_attachment_metadata", "")
        if raw_meta:
            try:
                metadata = php_unserialize(raw_meta) or {}
            except Exception as error:
                metadata = {"_parse_error": str(error)}
        raw_backup = meta.get("_wp_attachment_backup_sizes", "")
        if raw_backup:
            try:
                backup = php_unserialize(raw_backup) or {}
            except Exception as error:
                backup = {"_parse_error": str(error)}
        post_id = int(text_of(item, f"{WP_NS}post_id"))
        attachments[post_id] = {
            "id": post_id,
            "title": item.findtext("title") or "",
            "alt": meta.get("_wp_attachment_image_alt", ""),
            "caption": text_of(item, CONTENT_NS + "encoded"),
            "attachedFile": meta.get("_wp_attached_file", ""),
            "url": text_of(item, f"{WP_NS}attachment_url"),
            "parent": int(text_of(item, f"{WP_NS}post_parent") or 0),
            "slug": text_of(item, f"{WP_NS}post_name"),
            "metadata": metadata,
            "backup": backup,
        }

    chosen_media: dict[int, dict] = {}
    stored_by_hash: dict[str, str] = {}
    media_report = []

    def choose_and_store(attachment: dict) -> dict | None:
        if attachment["id"] in chosen_media:
            return chosen_media[attachment["id"]]
        meta = attachment["metadata"] if isinstance(attachment["metadata"], dict) else {}
        attached = attachment["attachedFile"]
        directory = str(Path(attached).parent).replace("\\", "/") if attached else ""
        if directory == ".":
            directory = ""
        original_name = meta.get("original_image") if isinstance(meta.get("original_image"), str) else ""
        full_orig = ""
        backup = attachment["backup"] if isinstance(attachment["backup"], dict) else {}
        full = backup.get("full-orig")
        if isinstance(full, dict) and isinstance(full.get("file"), str):
            full_orig = full["file"]
            if "/" not in full_orig and directory:
                full_orig = f"{directory}/{full_orig}"

        candidates = []
        if original_name and directory:
            candidates.append((f"{directory}/{original_name}", "original_image"))
        elif original_name:
            candidates.append((original_name, "original_image"))
        if full_orig:
            candidates.append((full_orig, "full-orig"))
        if attached:
            candidates.append((attached, "attached_file"))

        found = []
        for rel, kind in candidates:
            path = lookup_upload(upload_index, rel)
            found.append({"relativePath": rel, "kind": kind, "exists": path is not None, "path": path})

        existing = [item for item in found if item["exists"]]
        display = None
        notes = []
        explicit_substitute = False
        substitute_reason = ""
        edited = bool(EDIT_SUFFIX.search(attached or ""))
        if edited:
            edit_hit = next((item for item in existing if item["kind"] == "attached_file"), None)
            orig_hit = next((item for item in existing if item["kind"] in {"full-orig", "original_image"}), None)
            if edit_hit:
                display = edit_hit
                explicit_substitute = True
                substitute_reason = "wordpress-editor-crop-without-coordinates"
                notes.append("WordPress image editor crop is displayed because the export has no crop rectangle.")
                if orig_hit:
                    notes.append(f"Uncropped original exists at {orig_hit['relativePath']} and is archived beside the crop.")
            elif orig_hit:
                display = orig_hit
                notes.append("Edited file missing; using the uncropped original.")
        else:
            for kind in ("original_image", "full-orig", "attached_file"):
                hit = next((item for item in existing if item["kind"] == kind), None)
                if hit:
                    display = hit
                    break
            if display and display["kind"] != "original_image" and any(
                item["kind"] == "original_image" and not item["exists"] for item in found
            ):
                explicit_substitute = True
                substitute_reason = "original-image-missing"
                notes.append("Metadata names an original_image that is not in the upload archive.")
            if display and DERIVATIVE_SUFFIX.search(Path(display["relativePath"]).name) and display["kind"] == "attached_file":
                explicit_substitute = True
                substitute_reason = "only-derivative-available"
                notes.append("Only a resized derivative is available.")
            if (
                display
                and display["kind"] == "attached_file"
                and "-scaled" in Path(display["relativePath"]).name
                and not any(item["kind"] == "original_image" and item["exists"] for item in found)
            ):
                explicit_substitute = True
                substitute_reason = "scaled-file-without-original"
                notes.append(
                    "The archive contains a WordPress -scaled file and no full original. "
                    "This file is an explicit substitute."
                )

        if not display:
            # Last resort: largest file sharing the stem.
            stem = Path(attached or attachment["url"]).name
            stem = DERIVATIVE_SUFFIX.sub("", stem)
            stem = stem.replace("-scaled", "")
            best = None
            best_size = -1
            for rel, path in upload_index.items():
                if not isinstance(path, Path):
                    continue
                if stem.casefold() in Path(rel).name.casefold() and path.stat().st_size > best_size:
                    best = path
                    best_size = path.stat().st_size
                    best_rel = rel
            if best:
                display = {"relativePath": best_rel, "kind": "best-available", "exists": True, "path": best}
                explicit_substitute = True
                substitute_reason = "original-missing-best-available"
                notes.append("No metadata original matched; using the largest similarly named file.")

        if not display:
            record = {
                "attachmentId": attachment["id"],
                "status": "missing",
                "attachedFile": attached,
                "url": attachment["url"],
                "notes": ["No file found in the extracted uploads."],
            }
            media_report.append(record)
            chosen_media[attachment["id"]] = record
            return record

        source_path: Path = display["path"]
        data, byte_note = prepare_bytes(source_path)
        digest = sha256_bytes(data)
        if digest in stored_by_hash:
            public_rel = stored_by_hash[digest]
        else:
            filename = Path(display["relativePath"]).name
            # Keep a stable editorial path. Crops stay distinguishable.
            if explicit_substitute and substitute_reason.startswith("wordpress-editor"):
                filename = f"{Path(filename).stem}-crop{Path(filename).suffix.lower()}"
            year_month = "/".join(Path(attached or display["relativePath"]).parts[:2])
            public_rel = f"{year_month}/{filename}".replace("\\", "/")
            target = MEDIA_ROOT / public_rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists() or sha256_bytes(target.read_bytes()) != digest:
                target.write_bytes(data)
            stored_by_hash[digest] = public_rel
            if display["kind"] in {"full-orig", "original_image"} and explicit_substitute:
                pass
            # Archive the true original next to a crop when both exist and differ.
            if edited:
                orig_hit = next((item for item in existing if item["kind"] in {"full-orig", "original_image"} and item["path"] != source_path), None)
                if orig_hit:
                    orig_bytes, orig_note = prepare_bytes(orig_hit["path"])
                    orig_name = Path(orig_hit["relativePath"]).name
                    orig_rel = f"{year_month}/{orig_name}"
                    orig_target = MEDIA_ROOT / orig_rel
                    orig_target.parent.mkdir(parents=True, exist_ok=True)
                    if not orig_target.exists() or sha256_bytes(orig_target.read_bytes()) != sha256_bytes(orig_bytes):
                        orig_target.write_bytes(orig_bytes)
                    notes.append(f"Archived original stored at {orig_rel} ({orig_note}).")

        width = meta.get("width") if isinstance(meta.get("width"), int) else None
        height = meta.get("height") if isinstance(meta.get("height"), int) else None
        record = {
            "attachmentId": attachment["id"],
            "status": "explicit-substitute" if explicit_substitute else "original",
            "substituteReason": substitute_reason or None,
            "sourceKind": display["kind"],
            "sourceRelativePath": display["relativePath"],
            "storedPath": public_rel,
            "bytes": len(data),
            "bytePolicy": byte_note,
            "width": width,
            "height": height,
            "alt": attachment["alt"],
            "notes": notes,
            "parent": attachment["parent"],
            "url": attachment["url"],
            "attachedFile": attached,
        }
        # Map every known derivative URL path to this stored file.
        derivative_paths = set()
        if attached:
            derivative_paths.add(attached)
        file_meta = meta.get("file")
        if isinstance(file_meta, str):
            derivative_paths.add(file_meta)
        sizes = meta.get("sizes") if isinstance(meta.get("sizes"), dict) else {}
        for size in sizes.values():
            if isinstance(size, dict) and isinstance(size.get("file"), str):
                folder = str(Path(attached).parent).replace("\\", "/") if attached else ""
                derivative_paths.add(f"{folder}/{size['file']}" if folder else size["file"])
        if original_name and directory:
            derivative_paths.add(f"{directory}/{original_name}")
        record["legacyUploadPaths"] = sorted(derivative_paths)
        media_report.append(record)
        chosen_media[attachment["id"]] = record
        return record

    by_filename: dict[str, dict] = {}

    def ensure_attachment(attachment: dict) -> dict | None:
        record = choose_and_store(attachment)
        if record and record.get("storedPath"):
            for legacy in record.get("legacyUploadPaths", []):
                by_filename[basename_key(legacy)] = record
                by_filename[legacy.casefold()] = record
        return record

    for attachment in attachments.values():
        ensure_attachment(attachment)

    def resolve_image(src: str, class_name: str = "") -> str | None:
        rel = upload_rel_from_url(src)
        record = None
        if rel and rel.casefold() in by_filename:
            record = by_filename[rel.casefold()]
        elif rel and basename_key(rel) in by_filename:
            record = by_filename[basename_key(rel)]
        else:
            match = re.search(r"wp-image-(\d+)", class_name or "")
            if match:
                record = chosen_media.get(int(match.group(1)))
        if not record or not record.get("storedPath"):
            return None
        return "../../../assets/media/" + record["storedPath"]

    def markdown_from(html_source: str) -> str:
        parser = MarkdownConverter(resolve_image)
        parser.feed(preprocess_html(html_source))
        parser.close()
        return parser.result()

    written = []
    skipped = []
    unresolved = []
    content_counts = {"post": 0, "page": 0}

    POSTS_DE.mkdir(parents=True, exist_ok=True)
    PAGES_DE.mkdir(parents=True, exist_ok=True)
    LEGAL_DIR.mkdir(parents=True, exist_ok=True)

    published_posts = []
    for item in items:
        kind = text_of(item, f"{WP_NS}post_type")
        status = text_of(item, f"{WP_NS}status")
        if kind not in {"post", "page"} or status != "publish":
            continue
        content_counts[kind] += 1
        post_id = int(text_of(item, f"{WP_NS}post_id"))
        raw_html = text_of(item, CONTENT_NS + "encoded")
        title = strip_tags(item.findtext("title") or "")
        slug = text_of(item, f"{WP_NS}post_name")
        link = item.findtext("link") or ""
        path = urlparse(link).path
        if path and not path.endswith("/"):
            path += "/"
        pub = (text_of(item, f"{WP_NS}post_date") or "")[:10]
        updated = (text_of(item, f"{WP_NS}post_modified") or "")[:10]
        excerpt = strip_tags(text_of(item, EXCERPT_NS + "encoded"))
        item_tags = []
        item_categories = []
        for cat in item.findall("category"):
            domain = cat.get("domain")
            nicename = cat.get("nicename") or ""
            if domain == "post_tag":
                item_tags.append(nicename)
            elif domain == "category":
                item_categories.append(nicename)
        meta = metas(item)
        hero = None
        thumb = meta.get("_thumbnail_id")
        if thumb and thumb.isdigit():
            hero = chosen_media.get(int(thumb))
        year_match = re.search(r"/blog/(\d{4})/", path)
        year = int(year_match.group(1)) if year_match else int(pub[:4] or 0)

        if kind == "page" and slug in {"datenschutzerklaerung", "impressum"}:
            if slug == "impressum":
                verbatim = preprocess_html(raw_html).strip()
            else:
                verbatim = raw_html.strip()
            payload = {
                "id": slug,
                "title": title,
                "lang": "de",
                "originalLang": "de",
                "translationKey": f"wp-{post_id}",
                "provenance": "original",
                "translationStatus": "original",
                "needsReview": False,
                "verbatim": True,
                "draft": False,
                "wpId": post_id,
                "slug": slug,
                "legacyPath": path,
                "pubDate": pub,
                "updatedDate": updated,
                "html": verbatim,
            }
            target = LEGAL_DIR / "de" / f"{slug}.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
            if target.exists():
                current = json.loads(target.read_text(encoding="utf-8"))
                if current.get("editorialRevision") is True and current.get("html") != verbatim:
                    skipped.append({"path": str(target.relative_to(ROOT)), "reason": "editorialRevision"})
                elif current.get("html") == verbatim:
                    skipped.append({"path": str(target.relative_to(ROOT)), "reason": "unchanged"})
                else:
                    target.write_text(encoded, encoding="utf-8")
                    written.append(str(target.relative_to(ROOT)))
            else:
                target.write_text(encoded, encoding="utf-8")
                written.append(str(target.relative_to(ROOT)))
            continue

        body = markdown_from(raw_html)
        if "unresolved-image" in body:
            unresolved.append({"wpId": post_id, "slug": slug})
        description = excerpt or lead_description(body)
        description_source = "excerpt" if excerpt else "derived-lead"
        wp_hash = sha256_text(raw_html)
        data = {
            "title": title,
            "description": description,
            "descriptionSource": description_source,
            "pubDate": pub,
            "updatedDate": updated,
            "lang": "de",
            "originalLang": "de",
            "translationKey": f"wp-{post_id}",
            "provenance": "original",
            "translationStatus": "original",
            "needsReview": False,
            "draft": False,
            "wpId": post_id,
            "wpStatus": status,
            "author": "Azmir Abdi",
            "slug": slug,
            "legacyPath": path,
            "tags": item_tags,
            "categories": item_categories,
            "heroImage": f"/src/assets/media/{hero['storedPath']}" if hero and hero.get("storedPath") else "",
            "heroAlt": (hero or {}).get("alt") or "",
            "wpContentHash": wp_hash,
            "editorialRevision": False,
        }
        if kind == "post":
            data["year"] = year
        data["bodyHash"] = sha256_text(body)
        document = frontmatter(data) + "\n" + body
        if kind == "post":
            target = POSTS_DE / f"{pub}-{slug}.md"
        else:
            target = PAGES_DE / f"{slug}.md"
        reason = existing_guard(target, wp_hash, body)
        if reason in {"editorialRevision", "body-edited"}:
            conflict = GENERATED / "import-conflicts" / target.name
            conflict.parent.mkdir(parents=True, exist_ok=True)
            conflict.write_text(document, encoding="utf-8")
            skipped.append({"path": str(target.relative_to(ROOT)), "reason": reason})
        elif reason == "unchanged":
            skipped.append({"path": str(target.relative_to(ROOT)), "reason": reason})
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document, encoding="utf-8")
            written.append(str(target.relative_to(ROOT)))
        if kind == "post":
            published_posts.append(data)

    # Redirects
    exact = {}
    queries = {"p": {}, "page_id": {}, "attachment_id": {}, "cat": {}, "tag": {}}
    cat_by_id = {item["wpTermId"]: item["id"] for item in categories}
    tag_by_id = {item["wpTermId"]: item["id"] for item in tags}

    def add_exact(source: str, target: str) -> None:
        if not source or source == target:
            return
        exact[source] = target

    for item in items:
        kind = text_of(item, f"{WP_NS}post_type")
        status = text_of(item, f"{WP_NS}status")
        if kind not in {"post", "page"} or status != "publish":
            continue
        post_id = text_of(item, f"{WP_NS}post_id")
        link_path = urlparse(item.findtext("link") or "").path
        if link_path and not link_path.endswith("/"):
            link_path += "/"
        key = "page_id" if kind == "page" else "p"
        queries[key][post_id] = link_path
        add_exact(f"/{text_of(item, f'{WP_NS}post_name')}/", link_path)
        add_exact(link_path + "feed/", "/rss.xml")

    for attachment in attachments.values():
        record = chosen_media.get(attachment["id"])
        parent_target = queries["p"].get(str(attachment["parent"])) or queries["page_id"].get(str(attachment["parent"])) or "/"
        queries["attachment_id"][str(attachment["id"])] = parent_target
        if attachment["slug"]:
            add_exact(f"/{attachment['slug']}/", parent_target)
        if record and record.get("storedPath"):
            for legacy in record.get("legacyUploadPaths", []):
                add_exact("/wp-content/uploads/" + legacy, "/media/" + record["storedPath"])
                add_exact("/wordpress/wp-content/uploads/" + legacy, "/media/" + record["storedPath"])

    for tag in tags:
        if not tag["id"]:
            continue
        add_exact(f"/tag/{tag['id']}/", f"/themen/{tag['id']}/")
        add_exact(f"/tag/{tag['id']}/feed/", "/rss.xml")
        queries["tag"][str(tag["wpTermId"])] = f"/themen/{tag['id']}/"
    for category in categories:
        if not category["id"]:
            continue
        add_exact(f"/category/{category['id']}/", f"/archiv/kategorie/{category['id']}/")
        add_exact(f"/category/{category['id']}/feed/", "/rss.xml")
        queries["cat"][str(category["wpTermId"])] = f"/archiv/kategorie/{category['id']}/"

    for feed in ("/feed/", "/feed/rss/", "/feed/rss2/", "/feed/atom/", "/comments/feed/", "/blog/feed/"):
        add_exact(feed, "/rss.xml")
    add_exact("/author/azmir-abdi/", "/about-me/")
    add_exact("/author/azmirabdi/", "/about-me/")
    add_exact("/blog/", "/archiv/")

    redirects = {"exact": exact, "queries": queries}
    GENERATED.mkdir(parents=True, exist_ok=True)
    (GENERATED / "redirects.json").write_text(json.dumps(redirects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    redirect_lines = ["# Generated from the WordPress export. Query URLs are handled by the Worker.", ""]
    for source, target in sorted(exact.items()):
        redirect_lines.append(f"{source} {target} 301")
    (ROOT / "public").mkdir(parents=True, exist_ok=True)
    (ROOT / "public" / "_redirects").write_text("\n".join(redirect_lines) + "\n", encoding="utf-8")

    used_tag_ids = sorted({tag for post in published_posts for tag in post["tags"]})
    used_category_ids = sorted({cat for post in published_posts for cat in post["categories"]})
    taxonomy = {
        "tags": [
            {
                **tag,
                "used": tag["id"] in used_tag_ids,
                "nameEn": TAG_EN.get(tag["id"], tag["nameDe"]),
            }
            for tag in tags
        ],
        "categories": [
            {
                **category,
                "used": category["id"] in used_category_ids,
                "nameEn": CATEGORY_EN.get(category["id"], category["nameDe"]),
            }
            for category in categories
        ],
    }
    (GENERATED / "taxonomy.json").write_text(json.dumps(taxonomy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    legal_hashes = {}
    for path in (LEGAL_DIR / "de").glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        legal_hashes[path.stem] = sha256_text(payload["html"])
    (GENERATED / "legal-hashes.json").write_text(json.dumps(legal_hashes, indent=2) + "\n", encoding="utf-8")

    total_media_bytes = sum(record.get("bytes", 0) for record in media_report if record.get("storedPath"))
    largest = sorted((record for record in media_report if record.get("bytes")), key=lambda item: item["bytes"], reverse=True)[:8]
    inventory = {
        "export": WXR.name,
        "publishedPosts": content_counts["post"],
        "publishedPages": content_counts["page"],
        "attachmentsInExport": len(attachments),
        "mediaStored": len({record.get("storedPath") for record in media_report if record.get("storedPath")}),
        "mediaBytes": total_media_bytes,
        "explicitSubstitutes": [record for record in media_report if record.get("status") == "explicit-substitute"],
        "missingMedia": [record for record in media_report if record.get("status") == "missing"],
        "largestFiles": [
            {"path": record.get("storedPath"), "bytes": record.get("bytes"), "status": record.get("status")}
            for record in largest
        ],
        "unresolvedImagesInBody": unresolved,
        "written": written,
        "skipped": skipped,
        "comments": "Five comments in the export are unapproved or trash spam. None are published.",
        "otherSitesInUploadZip": "uploads/sites/3 and uploads/sites/4 are not referenced by this WXR and were not imported.",
        "unusedTags": [tag["id"] for tag in tags if tag["id"] not in used_tag_ids],
        "openapNote": "The tag openap exists in the export and is used by no post. It was not merged into openapi.",
    }
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "migration-inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "posts": content_counts["post"],
        "pages": content_counts["page"],
        "mediaStored": inventory["mediaStored"],
        "mediaBytes": total_media_bytes,
        "substitutes": len(inventory["explicitSubstitutes"]),
        "missing": len(inventory["missingMedia"]),
        "written": len(written),
        "skipped": len(skipped),
        "redirects": len(exact),
        "over25MiB": [item for item in largest if item.get("bytes", 0) > 25 * 1024 * 1024],
    }, indent=2))


TAG_EN = {
    "artikel": "Article",
    "asyncapi": "AsyncAPI",
    "bdd": "BDD",
    "bpm": "BPM",
    "cdc": "CDC",
    "cucumber": "Cucumber",
    "dantenzentrisch": "data-centric",
    "datengetrieben": "data-driven",
    "dca": "DCA",
    "enterprise-architecture": "Enterprise Architecture",
    "hybrid-konferenz": "hybrid conference",
    "initial-state": "initial state",
    "jax": "JAX",
    "microservices": "Microservices",
    "openap": "OpenAP",
    "openapi": "OpenAPI",
    "rbpm": "rBPM",
    "rc1": "rc1",
    "soa": "SOA",
    "testing": "Testing",
    "vortrag": "Talk",
}

CATEGORY_EN = {
    "agile": "Agile",
    "ai": "AI",
    "allgemein": "General",
    "artikel": "Article",
    "blog": "Blog",
    "coding-patterns": "Coding Patterns",
    "dca": "DCA",
    "ddd": "DDD",
    "microservices": "Microservices",
    "talk": "Talk",
    "testing": "Testing",
    "uncategorized": "Uncategorized",
}


if __name__ == "__main__":
    main()
