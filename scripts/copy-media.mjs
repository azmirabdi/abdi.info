import { cp, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";

const source = "src/assets/media";
const target = "dist/media";
if (!existsSync(source)) {
  console.log("No editorial media to copy.");
  process.exit(0);
}
await mkdir("dist", { recursive: true });
await cp(source, target, { recursive: true });
console.log(`Copied editorial originals to ${target}`);
