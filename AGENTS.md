# Arbeitsregeln für abdi.info

Diese Datei gilt für künftige Änderungen an diesem Repository. Die Migration hat vorhandene Artikel nicht stilistisch neu geschrieben. Die Regeln unten gelten für neue Artikel und für Überarbeitungen, die ausdrücklich beauftragt sind.

## Technik

- Statisches Astro, TypeScript, Content Collections in `src/content.config.ts`. Markdown für Artikel. MDX nur, wenn ein Artikel eine Komponente braucht, die Markdown nicht ausdrücken kann.
- Node `>=24.19.0 <25`, pnpm `11.25.0`. `.node-version` und `packageManager` sind die Quelle. Lokal liegt Node 24.19.0 unter nvm. Der System-Node 20 kann pnpm 11 nicht starten.
- Build-Skripte von `esbuild`, `sharp` und `workerd` stehen in `pnpm-workspace.yaml` unter `allowBuilds`. pnpm 11 liest das nicht mehr aus `package.json`.
- Neue Artikel legt `pnpm new:article <schlüssel> "Deutscher Titel" "English title"` als Entwurf an. Pflichtfelder stehen im Schema. Leere optionale Angaben: kein Bild, leere Tags und Kategorien, `updatedDate` gleich `pubDate`, Beschreibung beim Generator ein Platzhalter, den der Entwurf ersetzt. `draft: true` ist der Normalfall.
- Entwürfe erscheinen nicht in Sitemap, RSS, Suche, Tag-Seiten und Produktionsseiten. `publicPosts` filtert sie immer. Im Dev-Server kann ein Entwurf sichtbar sein.
- Deutsche Beitrags-URLs bleiben ohne `/de/`. Englisch liegt unter `/en/`. Beide Fassungen teilen `translationKey`. Der Sprachwechsel darf nicht auf eine fehlende Seite zeigen.
- Tags und Kategorien haben stabile IDs. Anzeigenamen kommen aus `src/generated/taxonomy.json`. Nur eindeutig gleiche Begriffe zusammenlegen und das im Migrationsbericht oder in einer kurzen Notiz festhalten. Den ungenutzten Tag `openap` nicht still mit `openapi` vereinen.
- Bilder für neue Artikel nach `src/assets/media/{jahr}/{monat}/` legen und im Markdown relativ referenzieren. Dieselbe Datei für beide Sprachen. Alt-Text nur, wenn er vorliegt oder das Bild dafür angesehen wurde. Keine erfundenen Beschreibungen.
- WordPress-Import: `pnpm import:wordpress`. Er liest `.wordpress_backup/` und `.migration-work/uploads-full/` und schreibt beides nicht zurück. Eine Datei mit `editorialRevision: true` oder einem vom gespeicherten `bodyHash` abweichenden Text wird nicht überschrieben. Konflikte landen unter `src/generated/import-conflicts/`.
- `.wordpress_backup/` und `.migration-work/` nicht committen. Keine Entwürfe, privaten Exportdaten, Zugangsdaten oder vollständigen Backups veröffentlichen.
- Impressum und Datenschutz auf Deutsch nicht umformulieren. Layout ja, Wortlaut nein. Englische Fassungen bleiben als Übersetzung gekennzeichnet.
- Kein zweites CMS, keine Datenbank, keine Kommentare, kein Kontaktformular. Kontakt ist eine Nachricht auf LinkedIn an Azmir Abdi, `https://www.linkedin.com/in/azmir-abdi/`. Keine Mailadresse als Kontakt setzen.
- Nicht committen und nicht pushen, solange das nicht ausdrücklich verlangt ist. Produktives DNS und die Domain-Route in `wrangler.jsonc` nicht ohne Freigabe ändern. WordPress und Synology-Verzeichnisse nicht löschen.
- Vorschau-Hosts bleiben `noindex`. Die produktive Indexierung gilt nur für `abdi.info`.

## Veröffentlichung

1. Entwurf in beiden Sprachen, verknüpft über `translationKey`.
2. `translationStatus` der Übersetzung erst auf `reviewed` setzen, wenn sie gelesen ist. Bis dahin `translated-unreviewed` und `needsReview: true`.
3. `provenance` ist `original`, `translation` oder `revision`. Eine stilistische Überarbeitung eines alten Artikels ist `revision` und setzt `editorialRevision: true`, damit der Importer sie nicht zurücksetzt.
4. Veröffentlichen heißt `draft: false` und wird nur auf ausdrücklichen Auftrag gesetzt.
5. Danach `pnpm check` und `pnpm dev`. Sitemap und RSS nehmen den Artikel erst dann auf.

## Übersetzung

- Natürliches Deutsch und natürliches Englisch. Keine Wort-für-Wort-Übertragung, keine deutschen Satzbauten im Englischen.
- Stimme, Bedeutung, Humor, Unsicherheit und fachliche Präzision bleiben. Nichts dazuerfinden: keine Erlebnisse, Quellen, Zahlen, Studien.
- Code, URLs, Produktnamen und Zitate bleiben, soweit sie sachlich nötig sind. Ein übersetztes Zitat wird als Übersetzung gekennzeichnet und nicht als geprüfter englischer Originalwortlaut ausgegeben.
- Das historische `pubDate` bleibt. `updatedDate` ist das Änderungsdatum der Quelle, nicht das Datum der Übersetzung.

## Beobachteter Stil

Das Folgende ist an den vorhandenen deutschen Texten abgelesen, nicht an Erinnerungen aus anderen Chats. Zitate und Gastformulierungen, vor allem das WJAX-Abstract und der d1g1tal-Absatz, sind veröffentlichte oder vorgetragene Texte und nicht die einzige Stimme des Blogs.

- Direkte Frage als Einstieg. In `src/content/posts/de/2018-07-22-die-ordnung-ueber-den-haufen-werfen.md`: „Für was stehen überhaupt BPM, SOA und Microservices?“
- Duzen und ein fester Schluss in den älteren Beiträgen. Ebenda und in `src/content/posts/de/2019-08-14-rc1-pattern-optmist-vs-pessimist.md`: „Vielen Dank für Deine Zeit und liebe Grüße“.
- Hörbares Zögern. Im rc1-Beitrag: „Ich glaube zu meinen, dass er sich dabei folgendes denkt“.
- Bedingung statt Behauptung. Im BPM-Artikel: „Ein rBPMS müsste als IT-Anwendung der eigenen unterstützenden Querschnittdomäne … agieren.“
- Kurzer Schlag am Anfang eines späteren Beitrags. In `src/content/posts/de/2025-06-11-endlich-beachtet-jemand-die-details-in-meiner-architektur-doku.md`: „Spoiler: Es war ein AI-Co-Pilot.“
- Wechsel zur förmlichen Ansprache in einem Text von 2025. In `src/content/posts/de/2025-03-01-datenzentrierte-architektur.md`: „Sie wollen wissen, wie das funktioniert? Kontaktieren Sie mich.“
- Ungeschützter Satz, Tippfehler inklusive. In `src/content/posts/de/2017-09-09-hello-world.md`: „war dich nicht ganz positiv.“

## Gewünschte Stimme für neue Texte

Persönlich, direkt, neugierig, reflektiert. Klar und fachlich, ohne akademische Schwere und ohne Werbe- oder Beratungston. Eine eigene Position mit nachvollziehbarer Begründung. Zweifel, Grenzen und Unterscheidungen dürfen stehen bleiben. Fachwörter nur, wenn sie tragen, und beim ersten Mal verständlich.

Westeuropäischer Alltag darf ein Beispiel sein. Er ist nicht der Normalfall der Welt. Keine kulturellen Klischees, keine romantischen Verallgemeinerungen, keine erfundenen biografischen Szenen. Herkunft, Beruf, Familie oder persönliche Erlebnisse nur nennen, wenn sie im Bestand stehen oder ausdrücklich vorgegeben sind. Aus dem Bestand belegt und damit verwendbar: der Name Azmir Abdi, die Adresse im Impressum (Weilderstädter Str. 10, 75395 Ostelsheim), der Blog als persönliche Notizen zu Data-Centric Architecture, AI-native und event-driven Systemen und Knowledge Graphs, Vorträge und die genannten Werkzeuge in den Artikeln. „Wirtschaftsinformatik“ nicht als aktuelle Bezeichnung des Blogs verwenden. Das Porträt auf About nicht mit einer erfundenen Bildbeschreibung versehen.

Gelegentlich ein Bild aus Alltag, Handwerk, Kochen, Verkehr, Nachbarschaft, Verwaltung, Reisen oder Zusammenarbeit, wenn es etwas klarer macht. Nicht in jedem Artikel. Nicht mehrere Bilder durcheinander. Danach zurück zur Aussage. Ein hypothetisches Beispiel als solches kennzeichnen. Keine erfundene Anekdote.

Einstiege wechseln zwischen Beobachtung, kurzer Szene, Problem, These oder einer echten offenen Frage. Nicht dieselbe Eröffnung und nicht derselbe Schluss über mehrere Artikel. Ein Text darf mit einer praktischen Folge, einem klaren Gedanken oder einer offenen Frage enden. Keine Pflichtzusammenfassung und keine schematische Rotation von Stilmitteln.

Konkrete Verben, verständliche Substantive, überwiegend aktiv, kurze und längere Sätze im Wechsel. Keine Floskeln wie „in der heutigen schnelllebigen Welt“, „es ist wichtig zu beachten“, „revolutionär“, „Gamechanger“ und kein routinemäßiges „zusammenfassend lässt sich sagen“. Keine künstlichen Gegensätze nach dem Muster „es geht nicht um X, sondern um Y“. Gedankenstriche, rhetorische Fragen und Dreierlisten sparsam.

Fakt, Deutung und Meinung auseinanderhalten. Aktuelle, nachprüfbare Behauptungen mit einer geeigneten Quelle. Keine erfundenen Studien, Zitate, Links oder Zahlen. Unsicherheit stehen lassen. SEO darf Titel und Aufbau verbessern und darf die Aussage nicht verbiegen.

Englische Fassungen behalten Persönlichkeit und Aussage. Redewendungen sinngemäß. Lokale Beispiele behalten und kurz erklären, wenn sie sonst unverständlich sind. Aus einem persönlichen Stück keinen internationalen Werbetext machen.

## Vorläufig, noch zu bestätigen

- Ob neue Texte durchgängig duzen oder, wie manche Texte von 2025, siezen. Der ältere Blog duzt. Die Architekturtexte von 2025 siezen an der Kontaktstelle. Bis zu einer Entscheidung: in einem neuen Artikel eine Anrede halten und nicht mischen.
- Ob der Schluss „Vielen Dank für Deine Zeit und liebe Grüße“ für neue Artikel weitergeführt wird. Er ist ein Merkmal der älteren Texte, keine Vorschrift für jeden künftigen Artikel.
- Ob Hashtag-Zeilen am Ende, wie im Architektur-Doku-Beitrag, gewollt bleiben. Für neue Artikel nicht von sich aus anfügen.

## Ablauf für einen neuen Artikel

1. Thema, Zielgruppe, Kernaussage und vorhandene Notizen aufnehmen.
2. Nur bei einer wesentlichen Lücke nachfragen.
3. Passende vorhandene Artikel auf Stil und interne Links lesen.
4. Aktuelle Fakten recherchieren, wenn die Aussage davon abhängt.
5. Einen vollständigen Entwurf in der beschriebenen Stimme schreiben.
6. Vorhandene Tags bevorzugen. Einen neuen Tag nur mit einem Satz Begründung anlegen und in `taxonomy.json` beide Anzeigenamen ergänzen, sonst zeigt die Seite die ID.
7. Deutsche und englische Fassung mit demselben `translationKey` anlegen. `pnpm new:article` macht das Gerüst.
8. Beschreibung, Slug, Daten und gegebenenfalls Bild und Alt-Text setzen. `descriptionSource: written`, solange die Beschreibung redaktionell ist.
9. Stil, Quellen, Übersetzung, Links und `pnpm check` prüfen.
10. `pnpm dev` starten und die Änderung in wenigen Sätzen zusammenfassen. Entwurf lassen, bis die Veröffentlichung ausdrücklich beauftragt ist.
