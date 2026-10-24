import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://abdi.info",
  trailingSlash: "always",
  output: "static",
  build: {
    format: "directory",
  },
  i18n: {
    defaultLocale: "de",
    locales: ["de", "en"],
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
