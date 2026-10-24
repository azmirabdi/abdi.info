import redirects from "../generated/redirects.json";

interface Env {
  ASSETS: { fetch: (request: Request) => Promise<Response> };
}

const INDEXABLE = new Set(["abdi.info"]);

function normalize(pathname: string): string {
  if (pathname.length > 1 && pathname.endsWith("/")) return pathname;
  if (pathname.includes(".")) return pathname;
  return `${pathname}/`;
}

export function resolveRedirect(url: URL): string | null {
  if (url.hostname === "www.abdi.info") {
    const redirected = new URL(url);
    redirected.hostname = "abdi.info";
    return redirected.toString();
  }
  const search = url.searchParams.get("s");
  if (search && (url.pathname === "/" || url.pathname === "")) {
    return `/suche/?q=${encodeURIComponent(search)}`;
  }
  if (url.searchParams.get("feed")) return "/rss.xml";
  const queries = redirects.queries as Record<string, Record<string, string>>;
  for (const key of ["p", "page_id", "attachment_id", "cat", "tag"] as const) {
    const value = url.searchParams.get(key);
    if (value && queries[key]?.[value]) return queries[key][value];
  }
  const exact = redirects.exact as Record<string, string>;
  const path = normalize(url.pathname);
  return exact[path] || exact[url.pathname] || null;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const target = resolveRedirect(url);
    if (target) {
      const location = target.startsWith("http") ? target : new URL(target, url.origin).toString();
      if (location !== url.toString()) return Response.redirect(location, 301);
    }
    const indexable = INDEXABLE.has(url.hostname);
    if (!indexable && url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", {
        headers: { "Content-Type": "text/plain; charset=utf-8", "X-Robots-Tag": "noindex" },
      });
    }
    const response = await env.ASSETS.fetch(request);
    if (indexable) return response;
    const headers = new Headers(response.headers);
    headers.set("X-Robots-Tag", "noindex, nofollow");
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  },
};
