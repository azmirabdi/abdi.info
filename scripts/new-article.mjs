#!/usr/bin/env node
import { mkdir, writeFile } from "node:fs/promises";
import { existsSync } from "node:fs";

const key = process.argv[2];
const titleDe = process.argv[3];
const titleEn = process.argv[4];
if (!key || !titleDe || !titleEn) {
  console.error('Usage: pnpm new:article <translation-key> "German title" "English title"');
  process.exit(1);
}

const today = new Date().toISOString().slice(0, 10);
const slug = (value) => value
  .toLowerCase()
  .replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss")
  .normalize("NFKD").replace(/[\u0300-\u036f]/g, "")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const slugDe = slug(titleDe);
const slugEn = slug(titleEn);
const year = today.slice(0, 4);

function frontmatter(fields) {
  return `---\n${Object.entries(fields).map(([name, value]) => {
    if (Array.isArray(value)) return `${name}: []`;
    if (typeof value === "boolean") return `${name}: ${value}`;
    if (typeof value === "number") return `${name}: ${value}`;
    return `${name}: ${JSON.stringify(value)}`;
  }).join("\n")}\n---\n\n`;
}

const shared = {
  description: "Entwurf ohne Beschreibung.",
  descriptionSource: "written",
  pubDate: today,
  updatedDate: today,
  originalLang: "de",
  translationKey: key,
  needsReview: true,
  draft: true,
  author: "Azmir Abdi",
  tags: [],
  categories: [],
  heroImage: "",
  heroAlt: "",
  editorialRevision: false,
};

const dePath = `src/content/posts/de/${today}-${slugDe}.md`;
const enPath = `src/content/posts/en/${today}-${slugEn}.md`;
for (const path of [dePath, enPath]) {
  if (existsSync(path)) {
    console.error(`Refusing to overwrite ${path}`);
    process.exit(1);
  }
}
await mkdir("src/content/posts/de", { recursive: true });
await mkdir("src/content/posts/en", { recursive: true });
await writeFile(dePath, frontmatter({
  ...shared,
  title: titleDe,
  lang: "de",
  provenance: "original",
  translationStatus: "original",
  slug: slugDe,
  legacyPath: `/blog/${year}/${slugDe}/`,
  year: Number(year),
}) + "Schreib den Artikel hier.\n");
await writeFile(enPath, frontmatter({
  ...shared,
  title: titleEn,
  lang: "en",
  provenance: "translation",
  translationStatus: "translated-unreviewed",
  slug: slugEn,
  legacyPath: `/en/blog/${year}/${slugEn}/`,
  year: Number(year),
}) + "Write the English version here. Mark translated quotations as translations.\n");
console.log(dePath);
console.log(enPath);
