import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { existsSync } from "node:fs";

function fail(message) {
  console.error(message);
  process.exitCode = 1;
}

const dePosts = (await readdir("src/content/posts/de")).filter((name) => name.endsWith(".md"));
const enPosts = (await readdir("src/content/posts/en")).filter((name) => name.endsWith(".md"));
const migratedPairs = 15;
if (dePosts.length < migratedPairs) fail(`Expected at least ${migratedPairs} German posts, found ${dePosts.length}`);
if (enPosts.length < migratedPairs) fail(`Expected at least ${migratedPairs} English posts, found ${enPosts.length}`);
if (dePosts.length !== enPosts.length) fail(`German and English post counts differ: ${dePosts.length} vs ${enPosts.length}`);

const hashes = JSON.parse(await readFile("src/generated/legal-hashes.json", "utf8"));
for (const [slug, expected] of Object.entries(hashes)) {
  const payload = JSON.parse(await readFile(`src/content/legal/de/${slug}.json`, "utf8"));
  const actual = createHash("sha256").update(payload.html).digest("hex");
  if (actual !== expected) fail(`German legal text changed: ${slug}`);
  if (!payload.verbatim) fail(`${slug} is no longer marked verbatim`);
}

const redirects = JSON.parse(await readFile("src/generated/redirects.json", "utf8"));
const exact = redirects.exact;
for (const [source, target] of Object.entries(exact)) {
  let cursor = target;
  const seen = new Set([source]);
  for (let hop = 0; hop < 5; hop += 1) {
    if (!exact[cursor]) break;
    if (seen.has(cursor)) {
      fail(`Redirect loop at ${source} -> ${cursor}`);
      break;
    }
    seen.add(cursor);
    cursor = exact[cursor];
  }
}

let unresolved = 0;
for (const file of dePosts) {
  const text = await readFile(`src/content/posts/de/${file}`, "utf8");
  unresolved += (text.match(/unresolved-image/g) || []).length;
  if (text.includes("<!-- wp:")) fail(`WordPress block comment left in ${file}`);
}
if (unresolved) fail(`${unresolved} unresolved images`);

if (!existsSync("src/worker/index.ts")) fail("Worker missing");
if (!existsSync("public/robots.txt")) fail("robots.txt missing");
if (process.exitCode) {
  console.error("Migration checks failed.");
} else {
  console.log(`Migration checks passed: ${dePosts.length} DE posts, ${enPosts.length} EN posts, ${Object.keys(exact).length} redirects.`);
}
