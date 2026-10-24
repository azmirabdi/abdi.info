# Migrationsbericht abdi.info

Stand: 24. Oktober 2026. Branch `migrate/astro-blog`. Es wurde nichts committet, nichts gepusht und kein DNS geändert. WordPress auf der Synology bleibt unangetastet.

## Mengenvergleich

| Quelle | Export | Übernommen |
| --- | --- | --- |
| Veröffentlichte Beiträge | 15, alle `publish` | 15 deutsche Markdown-Dateien plus 15 englische Übersetzungen |
| Seiten | 3 (`about-me`, Impressum, Datenschutz) | 3, deutsch unverändert im Inhalt; englische Fassungen zusätzlich |
| Anhänge im Export | 63 | 56 gespeicherte Mediendateien nach Inhaltsabgleich |
| Kommentare | 5 | 0. Alle sind Spam im Papierkorb oder nicht freigegeben |
| Entwürfe und private Beiträge | 0 | 0 |
| `custom_css` | 1 (Argent, blendet `.site-info` aus) | nicht als Inhalt übernommen |
| Menüeinträge | 6 | als eigene Navigation neu gebaut, nicht als WordPress-Menü |

Der Export ist `azmirabdi039sblog.WordPress.2026-10-24.xml`, WordPress 6.1.1, WXR 1.2, Sprache `de-DE`. Es gibt kein Polylang und kein WPML. Alle Originaltexte sind deutsch. Die englischen Fassungen sind Übersetzungen mit `translationStatus: translated-unreviewed` und `needsReview: true`.

Medien: 40 825 386 Bytes in `src/assets/media`. Keine Datei über 25 MiB. Größte Datei: `2020/12/DSC_3384.jpg`, 2 497 148 Bytes. Cloudflare Workers Static Assets erlaubt derzeit 25 MiB pro Datei und zehntausende Dateien. 56 Dateien und rund 41 MB liegen darunter. Eine Verkleinerung der Originale ist dafür nicht nötig. Der Build erzeugt davon getrennte responsive WebP-Dateien unter `/_astro/`.

Redirects: 1243 Pfade in `public/_redirects` und `src/generated/redirects.json`. Query-URLs (`?p=`, `?page_id=`, `?attachment_id=`, `?cat=`, `?tag=`, `?s=`, `?feed=`) liegen zusätzlich im Worker, weil `_redirects` keine Query-Strings vergleicht.

## URL-Entscheidung

Deutsche Beitrags-URLs bleiben `/blog/{jahr}/{slug}/` ohne Sprachpräfix. Englische Beiträge liegen unter `/en/blog/{jahr}/{übersetzter-slug}/` mit dem historischen Jahr. Seiten: `/about-me/`, `/impressum/`, `/datenschutzerklaerung/`. Englisch: `/en/about/`, `/en/imprint/`, `/en/privacy/`. Startseiten: `/` und `/en/`. Der Sprachwechsel verlinkt nur, wenn die andere Fassung existiert.

Der deutsche Slug `hello-world` bleibt. Die englische Fassung heißt `jekyll-instead-of-wordpress`. Der Tippfehler „Optmist“ bleibt im deutschen Titel und Slug `rc1-pattern-optmist-vs-pessimist`. Die englische URL schreibt `optimist`.

## Was nicht still verschwunden ist

- Literaturverweise wie `[1]` und `[2]` sind keine Shortcodes. Sie bleiben Text oder Links.
- Leere Bildblöcke ohne `src` (Beitrag 130) werden nicht als fehlendes Medium geführt.
- Fotos, die am AsyncAPI-Beitrag hängen, aber nicht im HTML stehen, wurden nicht in den Artikel eingefügt. Sie liegen im Medienbestand, damit alte Upload-URLs weiterleiten.
- Galerien sind Markdown-Listen. Leere Listenzeilen aus leeren Gallery-Items wurden entfernt.
- Nachgestellte `****` aus leeren `<strong>` im JAX-2022-Beitrag wurden entfernt. Der sichtbare Satz bleibt.
- Das kaputte Emphasis im SOA-Zitat des BPM-Artikels bleibt im deutschen Original: `***SOA setzt au***f Wiederverwendung.` Die englische Fassung erklärt den Satz und lässt die Bruchstelle sichtbar.

## Fehlende Originale

`missingMedia` ist leer. Es fehlt keine referenzierte Datei im Export. 28 Anhang-Einträge sind ausdrücklich Ersatz, weil das Archiv kein Volloriginal enthält. Mehrere WordPress-IDs zeigen auf dieselbe gespeicherte Datei. Es sind 25 `-scaled`-Dateien ohne vorhandenes Original und 3 Editor-Zuschnitte ohne Koordinaten im Export. Die unbeschnittene Datei liegt daneben, wenn sie im Archiv war. Der Zuschnitt wird angezeigt, weil das Export keine Crop-Rechtecke enthält.

Ersatzdateien, Grund `scaled-file-without-original`, sofern nicht unten als Zuschnitt genannt:

- `2020/06/20200527_214017-scaled-1.jpg`
- `2020/06/20200606_215620-scaled-1.jpg`
- `2020/06/20200606_215653-scaled-1.jpg`
- `2019/05/20200606_215710-scaled-1.jpg`
- `2019/05/20200606_215722-scaled-1.jpg`
- `2019/05/20200606_215727-scaled-1.jpg`
- `2019/05/20200606_215730-scaled-1.jpg`
- `2019/05/20200606_215742-scaled-1.jpg`
- `2019/05/20200606_215747-scaled-1.jpg`
- `2020/09/Jax2020_OliverAzmir-scaled-1.jpg`
- `2020/09/Jax2020_OliverAzmir_2-scaled-1.jpg`
- `2020/09/20200910_124333-scaled-1.jpg`
- `2020/10/20200908_150210-scaled-1.jpg`
- `2020/10/20200909_090446-scaled-1.jpg`
- `2020/10/20200909_091157-scaled-1.jpg`
- `2020/10/20200909_142530-scaled-1.jpg`
- `2020/10/20200910_100906-scaled-1.jpg`
- `2020/10/20200910_124311-scaled-1.jpg`
- `2020/10/20200910_124759-scaled-1.jpg`
- `2020/10/20200910_124818-scaled-1.jpg`
- `2020/10/IMG_0186-scaled-1.jpg`
- `2020/10/IMG_0189-scaled-1.jpg`
- `2020/10/IMG_0198-scaled-1.jpg`

Zuschnitte, Grund `wordpress-editor-crop-without-coordinates`:

- `2019/08/20200419_114015-e1591303370820-crop.jpg`
- `2020/06/20200105_104406-e1591303615592-crop.jpg`
- `2019/05/IMG_9938-1-scaled-e1591474640407-crop.jpg`

JPEGs mit GPS-EXIF wurden beim Speichern ohne diese Koordinaten neu geschrieben (`bytePolicy: gps-removed-metadata-stripped`). Dateien ohne GPS bleiben byte-identisch. Koordinaten stehen nicht im Inventar. 14 der Ersatz-Einträge tragen diese Kennzeichnung. Die Entscheidung ist eine Datenschutz-Ausnahme gegenüber bitidentischen Originalen.

`uploads/sites/3` und `uploads/sites/4` im ZIP gehören nicht zu diesem WXR und wurden nicht importiert. Darunter liegen auch Bilder zu lena-abdi. Der Tag `openap` hat keinen Beitrag und wurde nicht mit `openapi` zusammengelegt. Er hat keine eigene Seite.

## Menschliche Prüfung

Inhalt:

- Alle 15 englischen Beiträge und die englischen Seiten About, Impressum und Datenschutz sind ungelesene Übersetzungen.
- Das Zitat aus der d1g1tal Agenda im englischen Artikel „IT at different speeds“ ist als Übersetzung gekennzeichnet, nicht als geprüfter englischer Originalwortlaut.
- Das Ubiquitous-Abstract ist eine Übersetzung des deutschen Abstracts.
- Der englische Slug korrigiert „Optmist“ zu „optimist“. Der deutsche Titel nicht.
- Alt-Texte wurden nicht erfunden. Leere Alt-Texte aus WordPress bleiben leer, auch beim Porträt auf About.
- Angehängte, aber nicht eingebettete AsyncAPI-Fotos sind nur über alte URLs erreichbar, nicht im Artikel.

Recht, ohne Anspruch auf eine rechtliche Prüfung:

- Die deutschen Texte von Impressum und Datenschutz sind 1:1 aus dem Export, inklusive Tippfehlern wie „gerieng“. Der Hash steht in `src/generated/legal-hashes.json`. `node scripts/check-migration.mjs` vergleicht ihn.
- Die englischen Rechtstexte ersetzen die deutschen nicht. Sie glätten Tippfehler und sind als Übersetzung markiert.
- Der Datenschutz beschreibt Kommentare, Kommentar-Cookies, Login, „Angemeldet bleiben“, ein Kontaktformular und lokal gehostetes Font Awesome. Die neue Website hat davon nichts. Kontakt ist `mailto`. Eine Theme-Wahl liegt in `localStorage`, nicht in den beschriebenen Cookies.
- Der Hosting-Wechsel zu Cloudflare steht nicht im deutschen Text. Das kann Auftragsverarbeitung und ein Drittland betreffen. Der deutsche Text wurde deshalb nicht geändert.
- Quelle e-recht24.de bleibt stehen.

## Offene Punkte

- Übersetzungen gegenlesen.
- Rechtstext nach dem Hosting-Wechsel selbst entscheiden.
- Domain `abdi.info` erst nach Freigabe an den Worker hängen. `wrangler.jsonc` hat keine Custom-Domain-Route.
- Vorschau-Hosts und `workers.dev` senden `X-Robots-Tag: noindex, nofollow` und eine sperrende `robots.txt`. Das ist erst mit `wrangler dev` geprüft, nicht in Produktion.
- Im Bestand gibt es keine Tabelle. Die Tabellen-CSS ist vorhanden und an einem echten Artikel nicht geprüft.
- `maymert.com` wurde nicht im Quelltext gelesen. Der Graph folgt der schriftlichen Beschreibung. `schwaebits.de` wurde gestalterisch nicht ausgewertet. ArtByCooper lieferte die Idee zentraler Farbvariablen, nicht die Farben.

## Durchgeführte Prüfung

- `pnpm exec astro check`: 0 Fehler, nach den Korrekturen an Slugs, Graph und RSS.
- `pnpm build`: 120 Seiten, Bildoptimierung abgeschlossen, Medien nach `dist/media` kopiert.
- `node scripts/check-migration.mjs`: 15/15 Beiträge, Legal-Hashes, keine Redirect-Schleife in den exakten Pfaden, keine `unresolved-image`, keine Gutenberg-Kommentare.
- Visuelle und Redirect-Prüfung: siehe den Abschluss im Chat. Nur dort genannte Läufe gelten.
