import type { ImageMetadata } from "astro";

const modules = import.meta.glob<{ default: ImageMetadata }>("../assets/media/**/*.{jpg,jpeg,png,gif,webp}");

export async function loadImage(pointer: string): Promise<ImageMetadata | null> {
  if (!pointer) return null;
  const file = pointer.replace(/^\/src\/assets\/media\//, "").replace(/^src\/assets\/media\//, "");
  const key = Object.keys(modules).find((candidate) => candidate.endsWith(`/${file}`) || candidate.endsWith(file));
  if (!key) return null;
  const loaded = await modules[key]();
  return loaded.default;
}
