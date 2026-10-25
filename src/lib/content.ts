import { getCollection, type CollectionEntry } from "astro:content";
import taxonomy from "../generated/taxonomy.json";
import type { Lang } from "../i18n.ts";

export type Post = CollectionEntry<"posts">;
export type Page = CollectionEntry<"pages">;
export type Legal = CollectionEntry<"legal">;

export function isPublic(entry: { data: { draft: boolean } }): boolean {
  return import.meta.env.DEV || !entry.data.draft;
}

export function published(entry: { data: { draft: boolean } }): boolean {
  return !entry.data.draft;
}

export async function posts(lang: Lang, includeDrafts = import.meta.env.DEV): Promise<Post[]> {
  const all = await getCollection("posts");
  return all
    .filter((post) => post.data.lang === lang && (includeDrafts || !post.data.draft))
    .sort((a, b) => b.data.pubDate.localeCompare(a.data.pubDate));
}

export async function publicPosts(lang: Lang): Promise<Post[]> {
  return posts(lang, false);
}

export function postPath(post: Post): string {
  const prefix = post.data.lang === "en" ? "/en" : "";
  return `${prefix}/blog/${post.data.year}/${post.data.slug}/`;
}

export function formatDate(iso: string, lang: Lang): string {
  return new Intl.DateTimeFormat(lang === "de" ? "de-DE" : "en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(`${iso}T12:00:00Z`));
}

export function tagName(id: string, lang: Lang): string {
  const tag = taxonomy.tags.find((item) => item.id === id);
  if (!tag) return id;
  return lang === "de" ? tag.nameDe : tag.nameEn;
}

export function categoryName(id: string, lang: Lang): string {
  const category = taxonomy.categories.find((item) => item.id === id);
  if (!category) return id;
  return lang === "de" ? category.nameDe : category.nameEn;
}

export function tagPath(id: string, lang: Lang): string {
  return lang === "de" ? `/themen/${id}/` : `/en/topics/${id}/`;
}

export function categoryPath(id: string, lang: Lang): string {
  return lang === "de" ? `/archiv/kategorie/${id}/` : `/en/archive/category/${id}/`;
}

export function topicsPath(lang: Lang): string {
  return lang === "de" ? "/themen/" : "/en/topics/";
}

export function archivePath(lang: Lang): string {
  return lang === "de" ? "/archiv/" : "/en/archive/";
}

export function aboutPath(lang: Lang): string {
  return lang === "de" ? "/about-me/" : "/en/about/";
}

export function searchPath(lang: Lang): string {
  return lang === "de" ? "/suche/" : "/en/search/";
}

export function homePath(lang: Lang): string {
  return lang === "de" ? "/" : "/en/";
}

export function usedTags(langPosts: Post[]): { id: string; count: number }[] {
  const counts = new Map<string, number>();
  for (const post of langPosts) {
    for (const tag of post.data.tags) counts.set(tag, (counts.get(tag) ?? 0) + 1);
  }
  return [...counts.entries()]
    .map(([id, count]) => ({ id, count }))
    .sort((a, b) => b.count - a.count || a.id.localeCompare(b.id));
}

export function usedCategories(langPosts: Post[]): { id: string; count: number }[] {
  const counts = new Map<string, number>();
  for (const post of langPosts) {
    for (const category of post.data.categories) counts.set(category, (counts.get(category) ?? 0) + 1);
  }
  return [...counts.entries()]
    .map(([id, count]) => ({ id, count }))
    .sort((a, b) => b.count - a.count || a.id.localeCompare(b.id));
}

export function relatedPosts(current: Post, pool: Post[], limit = 3): Post[] {
  const tags = new Set(current.data.tags);
  const categories = new Set(current.data.categories);
  return pool
    .filter((post) => post.id !== current.id && post.data.translationKey !== current.data.translationKey)
    .map((post) => ({
      post,
      score:
        post.data.tags.filter((tag) => tags.has(tag)).length * 2 +
        post.data.categories.filter((category) => categories.has(category)).length,
    }))
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score || b.post.data.pubDate.localeCompare(a.post.data.pubDate))
    .slice(0, limit)
    .map((item) => item.post);
}

export async function translationOf(entry: { data: { translationKey: string; lang: Lang } }): Promise<Post | Page | undefined> {
  const target = entry.data.lang === "de" ? "en" : "de";
  const postMatches = (await getCollection("posts")).filter(
    (item) => item.data.translationKey === entry.data.translationKey && item.data.lang === target,
  );
  const post = postMatches.find((item) => !item.data.draft)
    ?? (import.meta.env.DEV ? postMatches.find((item) => item.data.draft) : undefined);
  if (post) return post;
  return (await getCollection("pages")).find(
    (item) => item.data.translationKey === entry.data.translationKey && item.data.lang === target && !item.data.draft,
  );
}

export async function legalTranslation(entry: Legal): Promise<Legal | undefined> {
  const target = entry.data.lang === "de" ? "en" : "de";
  return (await getCollection("legal")).find(
    (item) => item.data.translationKey === entry.data.translationKey && item.data.lang === target && !item.data.draft,
  );
}

export function absolute(path: string): string {
  return new URL(path, "https://abdi.info").toString();
}

export function showUpdated(pubDate: string, updatedDate?: string): boolean {
  if (!updatedDate || updatedDate === pubDate) return false;
  return updatedDate > pubDate;
}
