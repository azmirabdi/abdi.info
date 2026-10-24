import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const prose = {
  title: z.string(),
  description: z.string().default(""),
  descriptionSource: z.enum(["excerpt", "derived-lead", "written"]).default("written"),
  pubDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  updatedDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  lang: z.enum(["de", "en"]),
  originalLang: z.enum(["de", "en"]),
  translationKey: z.string(),
  provenance: z.enum(["original", "translation", "revision"]).default("original"),
  translationStatus: z.enum(["original", "translated-unreviewed", "reviewed"]).default("original"),
  needsReview: z.boolean().default(false),
  draft: z.boolean().default(false),
  wpId: z.number().optional(),
  wpStatus: z.string().optional(),
  author: z.string().default("Azmir Abdi"),
  slug: z.string(),
  legacyPath: z.string(),
  tags: z.array(z.string()).default([]),
  categories: z.array(z.string()).default([]),
  heroImage: z.string().default(""),
  heroAlt: z.string().default(""),
  wpContentHash: z.string().optional(),
  bodyHash: z.string().optional(),
  editorialRevision: z.boolean().default(false),
};

const posts = defineCollection({
  loader: glob({
    pattern: "**/*.md",
    base: "./src/content/posts",
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.object({
    ...prose,
    year: z.number().int(),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/pages" }),
  schema: z.object(prose),
});

const legal = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/legal" }),
  schema: z.object({
    title: z.string(),
    lang: z.enum(["de", "en"]),
    originalLang: z.enum(["de", "en"]),
    translationKey: z.string(),
    provenance: z.enum(["original", "translation"]),
    translationStatus: z.enum(["original", "translated-unreviewed", "reviewed"]),
    needsReview: z.boolean().default(false),
    verbatim: z.boolean(),
    draft: z.boolean().default(false),
    wpId: z.number().optional(),
    slug: z.string(),
    legacyPath: z.string(),
    pubDate: z.string(),
    updatedDate: z.string().optional(),
    html: z.string(),
    editorialRevision: z.boolean().optional(),
  }),
});

export const collections = { posts, pages, legal };
