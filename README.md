# abdi.info

Statischer Blog, migriert aus WordPress. Die Website und der Build hängen nicht mehr an WordPress, seiner API oder der Synology. Neuer Inhalt sind Dateien in diesem Repository.

Für eine spätere Sitzung: Branch `migrate/astro-blog`, Stand der Migration in `docs/migration-report.md`, Arbeitsregeln in `AGENTS.md`. `.wordpress_backup/` und `.migration-work/` sind gitignoriert und dürfen nicht veröffentlicht werden. Es ist noch nichts committet. DNS ist nicht umgestellt.

## Architektur

Astro 7 schreibt vollständig statisches HTML nach `dist/`. Ein kleiner Cloudflare Worker in `src/worker/index.ts` beantwortet davor Query-Redirects, leitet `www` auf die Apex-Domain und setzt auf allen Hosts außer `abdi.info` `noindex`. Gehashte Dateien unter `/_astro/` und die Originalmedien unter `/media/` gehen am Worker vorbei.

```
src/content/posts/{de,en}/     Artikel, Markdown
src/content/pages/{de,en}/     About
src/content/legal/{de,en}/     Impressum und Datenschutz, deutsch als HTML-String
src/assets/media/              redaktionelle Originale
src/generated/                 Redirects, Taxonomie, Legal-Hashes, Import-Konflikte
src/styles/global.css          Designvariablen
public/_redirects              Pfad-Redirects, vom Importer geschrieben
public/robots.txt              Produktionsregeln; Vorschau ersetzt der Worker
scripts/import_wordpress.py    wiederholbarer Import
scripts/new-article.mjs        Gerüst für einen neuen Artikel
scripts/check-migration.mjs    Mengen, Legal-Hash, Redirect-Schleifen
scripts/copy-media.mjs         kopiert Originale nach dist/media
wrangler.jsonc                 Workers Static Assets, keine Custom Domain
```

Es gibt kein CMS und keine Datenbank. Suche filtert die bereits ausgelieferte Artikelliste im Browser. Ohne JavaScript bleibt die volle Liste sichtbar. Tag- und Kategoriefilter sind normale Links.

## Voraussetzungen

- Node `>=24.19.0 <25`. Auf diesem Rechner: `nvm use` liest `.nvmrc` (`24.19.0`). Node 20 kann pnpm 11 nicht starten (`node:sqlite` fehlt).
- pnpm `11.25.0`, festgelegt in `package.json` als `packageManager`. `pnpm-workspace.yaml` setzt `pmOnFail: error` und erlaubt die Build-Skripte von `esbuild`, `sharp` und `workerd`.

```sh
nvm use
pnpm install
pnpm dev
```

Der Dev-Server bindet an `127.0.0.1`, Port 4321, solange der frei ist.

## Prüfung und Build

```sh
pnpm check    # astro check und scripts/check-migration.mjs
pnpm build    # dist/ plus Kopie der Originale nach dist/media
pnpm preview  # das gebaute dist an 127.0.0.1
pnpm preview:cf   # wrangler dev, inklusive Worker-Redirects und echtem 404
```

`astro preview` wendet den Worker und `_redirects` nicht an. Query-URLs und den HTTP-Status 404 dort prüfen, wo der Worker läuft.

## Artikel und Sprachen

```sh
pnpm new:article mein-schluessel "Deutscher Titel" "English title"
```

Das legt zwei Entwürfe an, verknüpft über `translationKey`. `draft` bleibt `true`, bis die Veröffentlichung ausdrücklich beauftragt ist. Entwürfe fehlen in Sitemap, RSS, Suche, Themen und Produktion.

Felder, die der Generator setzt und die das Schema verlangt: `title`, `description`, `pubDate`, `lang`, `originalLang`, `translationKey`, `slug`, `legacyPath`, `year`. Ohne optionales Bild bleibt `heroImage` leer und die Seite zeigt keins. Ohne Tags bleibt die Liste leer. `updatedDate` wird nur angezeigt, wenn es nach `pubDate` liegt.

Deutsche Beiträge: `/blog/{jahr}/{slug}/`. Englische: `/en/blog/{jahr}/{slug}/`. Dieselbe Jahreszahl. Im Sprachschalter steht DE immer links und EN rechts. Sprach- und Farbschema-Schalter teilen sich dasselbe Aussehen: die aktive Hälfte hat einen leichten orangenen Grund und einen orangefarbenen Rand, außen rund und zur anderen Hälfte hin gerade. Fehlt die andere Fassung, ist das kein Link. Der Hinweis „English translation, not yet editorially reviewed.“ wird nicht angezeigt.

Tags: stabile ID, Anzeigename in `src/generated/taxonomy.json` (`nameDe`, `nameEn`). Seiten unter `/themen/{id}/` und `/en/topics/{id}/`. Kategorien unter `/archiv/kategorie/{id}/` und `/en/archive/category/{id}/`. Das Menü verlinkt die Übersicht, nicht jeden Tag. Die Übersicht zeigt zuerst Tags mit mehr als einem Artikel, danach alle.

## Bilder

Redaktionelle Dateien liegen unter `src/assets/media` und werden unverändert kopiert nach `dist/media`, damit alte Upload-URLs auf stabile Pfade zeigen. Astro erzeugt beim Build zusätzlich responsive Bilder unter `/_astro/`. Die sind nicht die Quelle.

Der Importer nimmt aus den Attachment-Metadaten bevorzugt das Original, sonst die beste vorhandene Datei, und kennzeichnet Ersatz in `docs/migration-inventory.json`. Dateien mit GPS-EXIF werden ohne diese Koordinaten neu gespeichert. Alles andere bleibt byte-identisch. Sprachfassungen referenzieren dieselbe Datei.

## Gestaltung

Variablen in `src/styles/global.css`. Heller Grund `#F7F3EC`, Überschriften `#141210`, Oberfläche `#3A342E`, Artikelfließtext `#4A433C`. Akzentfläche `#C66A32`. Linktext im Hellen ist `#9A4E22`, weil `#C66A32` auf dem Grund nur etwa 3,45:1 erreicht und für Text nicht reicht. Dunkel: Grund `#161411`, Akzenttext `#E8A36E`, Artikelfließtext `#EFE8E0`. Zwei Schriften, lokal über Fontsource: Newsreader für Namen, Überschriften und Artikeltitel, Source Sans 3 für Menü und Fließtext, mit Versalziffern. Die Spalte ist `68ch`. Artikelbilder sind so breit wie die Artikelspalte, Höhe proportional. Abstand davor und danach ist `0.875rem`. Auf der Startseite liegen Einleitung, „Zuletzt“ und „Weitere Artikel“ in `.home-column` (`40rem`), zentriert. Dieselbe Spalte haben Über mich, Themen, Archiv, Suche und die darunterliegenden Tag-, Kategorie- und Jahresseiten. Der Seitentitel dort ist ein kleiner Vorspann und danach die Überschrift, wie auf der Startseite. Die Suche filtert die schon geladene Liste; ausgeblendete Einträge brauchen `display: none`, weil die Listenpunkte sonst als Raster sichtbar bleiben. Kontakt auf der Seite ist eine LinkedIn-Nachricht an Azmir Abdi, nicht die Mailadresse. Die Straße im Impressum ist Weilderstädter Str. 10. Tags sind klein und in der gedämpften Farbe des Hinweises unter dem Namen. Jede `h2` hat als Padding eine halbe Zeile davor und eine viertel Zeile danach.

Die öffentliche Bezeichnung folgt dem LinkedIn-Profil: Data-Centric Architecture, AI-native, event-driven, Knowledge Graphs. „Wirtschaftsinformatik“ nicht wieder als Blog-Untertitel setzen. Der vollständige LinkedIn-About-Text ist ohne Anmeldung abgeschnitten; nicht aus dem Fragment weiterschreiben.

Der Netzwerk-Graph liegt fest hinter allen Seiten. Alle 500 Pixel Scrollweg beginnt ein neues Netz, horizontal verschoben und mit anderer Knotenlage. Es lässt sich nicht ausblenden. Jeder Punkt läuft langsam ein kleines Rechteck ab, etwa einmal in 36 Sekunden. Die Linien werden zwischen den aktuellen Punkten gezeichnet und folgen dieser Bewegung. `prefers-reduced-motion` hält die Punkte still und folgt nur dem Scrollen. Bei inaktivem Tab läuft die Animation nicht.

Die erste Farbe folgt `prefers-color-scheme`. Eine manuelle Wahl liegt in `localStorage` unter `theme` und wird vor dem ersten Paint gesetzt.

Unter 760 px wird die Navigation ein Klappmenü. Der Knopf zeigt ein Burger-Icon, geöffnet ein X. „Menü“ und „Schließen“ stehen nur für Screenreader im Knopf, die Icons sind `aria-hidden`.

## Import

```sh
pnpm import:wordpress
```

Liest den WXR und `.migration-work/uploads-full`. Schreibt die Quellen nicht um. Überspringt Dateien mit `editorialRevision: true` oder einem Text, dessen Hash nicht mehr zum gespeicherten `bodyHash` passt. Grenzen: keine stillen stilistischen Überarbeitungen, keine Übernahme von `uploads/sites/3` und `sites/4`, keine Kommentare, kein Zusammenlegen von `openap` und `openapi`.

## Deployment

Secrets in GitHub: `CLOUDFLARE_API_TOKEN` und `CLOUDFLARE_ACCOUNT_ID`. Der Workflow `.github/workflows/ci.yml` prüft Pull Requests und Pushes. `wrangler deploy` läuft bei Push auf `main` und bei `workflow_dispatch`. Es gibt keine Route für `abdi.info`. Ein Deploy landet auf `workers.dev` und bleibt `noindex`.

Domain erst nach Freigabe: in `wrangler.jsonc` eine Route oder Custom Domain für `abdi.info` und `www.abdi.info` ergänzen, DNS beim Registrar auf Cloudflare zeigen lassen, Zertifikat abwarten, `https://abdi.info/?p=8` und eine unbekannte URL mit `curl -I` prüfen. Bis dahin zeigt die Domain weiter auf die Synology.

Zurück zur bisherigen Website: die Worker-Route entfernen oder das DNS auf den bisherigen Synology-Eintrag stellen. WordPress nicht deinstallieren. Dieses Repository löscht nichts auf der NAS. Die Exporte bleiben in `.wordpress_backup/`.

Redirects pflegen: Pfade in `scripts/import_wordpress.py` erzeugen, oder einen einzelnen Pfad in `src/worker/index.ts` und `public/_redirects` gleichlautend eintragen. Query-Ziele nur im Worker. Nach einer Änderung `pnpm preview:cf` und `curl -I` gegen den lokalen Worker.

## Abhängigkeiten

```sh
nvm use
pnpm update --interactive
pnpm check
pnpm build
```

Vor einem größeren Astro-Sprung die Release-Notes lesen. `markdown.gfm` in der Astro-Konfiguration nicht wieder als Top-Level-Schlüssel setzen. Sätteri, der Standardprozessor von Astro 7, erzeugt die Überschriften-IDs. Ein eigener Rehype-Plugin ist dafür nicht eingebunden.
