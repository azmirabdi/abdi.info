---
title: "Jekyll statt Wordpress"
description: "`Am Anfang war die Idee … und weil die Idee so \"innovativ\" war, fand sie im Cyberspace ihre Schöpfung.` - Braucht das Internet noch einen Blog? - Braucht Internet meinen Blog? Wie…"
descriptionSource: "derived-lead"
pubDate: "2017-09-09"
updatedDate: "2026-10-26"
lang: "de"
originalLang: "de"
translationKey: "wp-151"
provenance: "revision"
translationStatus: "original"
needsReview: false
draft: false
wpId: 151
wpStatus: "publish"
author: "Azmir Abdi"
slug: "hello-world"
legacyPath: "/blog/2017/hello-world/"
year: 2017
tags: []
categories:
  - "blog"
heroImage: ""
heroAlt: ""
wpContentHash: "1c8dc0f1e3b19b0b89200d0383032965c9c739aedea95ef208235cfbe084a8c7"
bodyHash: "82a2fad34b9288ce462ab512685446ddacdd1552018a4e72dd88b6dd49fb01d8"
editorialRevision: true
---

`Am Anfang war die Idee … und weil die Idee so "innovativ" war, fand sie im Cyberspace ihre Schöpfung.`


- Braucht das Internet noch einen Blog?

- Braucht Internet meinen Blog?

Wie dem auch sei, jetzt sitze ich hier und tippe, wie es dazu kam …

Da mich ein paar Gedanken verfolgten und ich diese online nicht vorfinden konnte, kam ich dazu, einen eigenen Blog zu eröffnen. Die Zeit, auf die ich sehr gespannt bin, wird den Eindruck offenbaren.

Also los geht es.

## Die Themen …
… waren durch die o.g. Gedanken gesetzt:


- IT-Architektur

- BPM

- Enterprise Architecture

- Java

## Technologieauswahl
[Wordpress](https://de.wordpress.com/) ist quasi der Standard für Blogs und ich habe mich für [Jekyll](http://jekyllrb.com/) entschieden. Ungefähr aus folgenden Gründen:


- Kein Datenbank-Server notwendig

- Phänomenal einfacher Template-Mechanismus

- Nur statische Inhalte

- [GitHub Pages](https://pages.github.com/) und [GitLab Pages](https://gitlab.com/pages) unterstützen [Jekyll](http://jekyllrb.com/) jeweils mit eigener Deployment Pipeline

Online gibt es etliche Artikel, die Argumente pro [Jekyll](http://jekyllrb.com/) bringen. Zum Beispiel vom [smashingmagazine](https://www.smashingmagazine.com/2014/08/build-blog-jekyll-github-pages/).

## [Discus](https://disqus.com) vs. [Staticman](https://staticman.net/)
Doch wie sieht es mit den Kommentaren aus? Sind Kommentare nicht DER Grund, einen Blog aufzusetzen – um die Rückmeldungen auf eigene Gedanken von der Community zu erhalten?! `Web 2.0`.
Aber nur wegen der Kommentarfunktion doch [Wordpress](https://de.wordpress.com/), das dynamische Inhalte ermöglicht, zu betreiben …?

Die nächste Recherche folgte: `Kommentare für Jekyll Seiten`.
Treffer:


- [`Discus`](https://disqus.com)


  - Speichert über eigenes SAAS in USA die Kommentare in Übersee je Seite (URL) und lädt diese innerhalb eines eigebetteten Div.


- [`Staticman`](https://staticman.net/)


  - Betreibt einen Git Push Dienst bei dem jeder Kommentar als neue Datei auf die entsprechenden Pfade im Seiten-Quellcode auf GitHub Repository der Seite gespeichert wird. GitHub realisiert Änderungen und startet ein neues Deployment.

Ich bevorzuge [staticman](https://staticman.net/) weil es `cool` ist. ITler mögen komplexe Abläufe! Außerdem liegen alle Kommentare dann in Sourcecode, was im Vergleich zum [discus](https://disqus.com) tatsächlich um ein Vielfaches besser ist.

## [GitLab Pages](https://gitlab.com/pages) vs. [GitHub Pages](https://pages.github.com/)
Interessant ist, dass im [GitLab Pages](https://gitlab.com/pages) vs. [GitHub Pages](https://pages.github.com/) eigentlich GitLab weitaus mehr Funktionen und eine moderne CI-Pipeline anbietet, aber dafür im Zusammenspiel mit [staticman](https://staticman.net/) nicht in Frage kommt, da ein neues Deployment aufgrund des gesamten Docker-Containers mehrere Minuten benötigt.
Beim [GitHub Pages](https://pages.github.com/) sind es nur wenige Sekunden.

Probiere es mal aus, und hinterlasse einen Kommentar.


1. Im Hintergrund wird [staticman](https://staticman.net/) public Service mit dem HTTP POST Formular aufgerufen, das wiederum per `git push` für deinen Kommentar eine neue Datei ablegt. Siehe [GitHub Comments Repository](https://github.com/azabdi/azabdi.github.io/tree/master/_data/comments/).

2. GitHub startet ein neues Deployment und …

3. … wenn du die Seite neu lädst, sollte dein Kommentar erscheinen.

## Fazit
Nachdem die Kommentarfunktion eingebettet war, ist der Rest schnell erledigt. Mir hat das Aufsetzten Spaß bereitet und der Gedanke, wie einfach ein neuer Blog-Post (nachdem der Blog steht) hinzugefügt werden kann, bereitet mir umso mehr Freude. Ich hoffe, dass auch für Dich etwas Lesenswertes dabei zu finden sein wird.

### Nachtrag 04.06.2020
Erfahrungsbericht mit Staticman: war dich nicht ganz positiv. Einige Kommentare wurden nicht wie im Artikel beabsichtigt übernommen - also wurde der Blog doch auf Wordpress migriert! So kann eine These leicht gestürzt werden wenn sie bloß auf eine Säule basiert.

---

Original Artikel dessen mit Jakyll generierter Inhalt auf github pages gesichtet werden kann findet ihr hier: [https://azabdi.github.io/](https://azabdi.github.io/).Vielen Dank für Deine Zeit und liebe Grüße,
[Azmir Abdi](/about-me/)

PS: Ich freue mich über eine [Nachricht](/about-me/#kontakt).
