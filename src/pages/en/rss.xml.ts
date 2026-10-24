import rss from "@astrojs/rss";
import { postPath, publicPosts } from "../../lib/content.ts";

export async function GET(context: { site: URL }) {
  const posts = await publicPosts("en");
  return rss({
    title: "Azmir Abdi",
    description: "Data-centric architecture, AI-native and event-driven.",
    site: context.site,
    trailingSlash: true,
    customData: "<language>en-GB</language>",
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: new Date(`${post.data.pubDate}T12:00:00Z`),
      description: post.data.description,
      link: postPath(post),
    })),
  });
}
