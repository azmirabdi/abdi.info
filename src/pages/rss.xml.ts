import rss from "@astrojs/rss";
import { publicPosts, postPath } from "../lib/content.ts";

export async function GET(context: { site: URL }) {
  const posts = await publicPosts("de");
  return rss({
    title: "Azmir Abdi",
    description: "Data-Centric Architecture, AI-native und event-driven.",
    site: context.site,
    trailingSlash: true,
    customData: "<language>de-DE</language>",
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: new Date(`${post.data.pubDate}T12:00:00Z`),
      description: post.data.description,
      link: postPath(post),
    })),
  });
}
