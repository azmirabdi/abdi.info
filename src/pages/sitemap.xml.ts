import {
  aboutPath,
  archivePath,
  categoryPath,
  postPath,
  publicPosts,
  searchPath,
  tagPath,
  topicsPath,
  usedCategories,
  usedTags,
  type Post,
} from "../lib/content.ts";

const site = "https://abdi.info";

function url(path: string, alternates: string[] = []) {
  const links = [path, ...alternates.filter((item) => item && item !== path)];
  const xhtml = links
    .map((item) => {
      const lang = item.startsWith("/en/") || item === "/en/" ? "en-GB" : "de-DE";
      return `<xhtml:link rel="alternate" hreflang="${lang}" href="${site}${item}"/>`;
    })
    .join("");
  const xDefault = links.find((item) => !item.startsWith("/en")) ?? links[0];
  return `<url><loc>${site}${path}</loc>${xhtml}<xhtml:link rel="alternate" hreflang="x-default" href="${site}${xDefault}"/></url>`;
}

export async function GET() {
  const german = await publicPosts("de");
  const english = await publicPosts("en");
  const byKey = new Map<string, Post>();
  for (const post of english) byKey.set(post.data.translationKey, post);
  const entries = [
    url("/", ["/en/"]),
    url("/en/", ["/"]),
    url(topicsPath("de"), [topicsPath("en")]),
    url(topicsPath("en"), [topicsPath("de")]),
    url(archivePath("de"), [archivePath("en")]),
    url(archivePath("en"), [archivePath("de")]),
    url(searchPath("de"), [searchPath("en")]),
    url(searchPath("en"), [searchPath("de")]),
    url(aboutPath("de"), [aboutPath("en")]),
    url(aboutPath("en"), [aboutPath("de")]),
    url("/impressum/", ["/en/imprint/"]),
    url("/en/imprint/", ["/impressum/"]),
    url("/datenschutzerklaerung/", ["/en/privacy/"]),
    url("/en/privacy/", ["/datenschutzerklaerung/"]),
  ];
  for (const post of german) {
    const match = byKey.get(post.data.translationKey);
    entries.push(url(postPath(post), match ? [postPath(match)] : []));
    entries.push(url(`/blog/${post.data.year}/`, [`/en/blog/${post.data.year}/`]));
  }
  for (const post of english) entries.push(url(postPath(post), [german.find((item) => item.data.translationKey === post.data.translationKey) ? postPath(german.find((item) => item.data.translationKey === post.data.translationKey)!) : ""]));
  for (const tag of usedTags(german)) entries.push(url(tagPath(tag.id, "de"), [tagPath(tag.id, "en")]));
  for (const tag of usedTags(english)) entries.push(url(tagPath(tag.id, "en"), [tagPath(tag.id, "de")]));
  for (const category of usedCategories(german)) entries.push(url(categoryPath(category.id, "de"), [categoryPath(category.id, "en")]));
  for (const category of usedCategories(english)) entries.push(url(categoryPath(category.id, "en"), [categoryPath(category.id, "de")]));
  const unique = [...new Set(entries)];
  const body = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${unique.join("\n")}\n</urlset>\n`;
  return new Response(body, { headers: { "Content-Type": "application/xml; charset=utf-8" } });
}
