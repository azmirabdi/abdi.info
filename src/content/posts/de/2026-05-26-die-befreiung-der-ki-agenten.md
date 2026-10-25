---
title: "Die Befreiung der KI-Agenten"
description: "Braucht es für KI-Agenten eine neue Plattform? Rückblick auf die CloudLand am 20. Mai 2026 im Heide Park Soltau."
descriptionSource: "written"
pubDate: "2026-05-26"
updatedDate: "2026-05-26"
lang: "de"
originalLang: "de"
translationKey: "cloudland-2026-befreiung-der-ki-agenten"
provenance: "original"
translationStatus: "original"
needsReview: false
draft: true
author: "Azmir Abdi"
slug: "die-befreiung-der-ki-agenten"
legacyPath: "/blog/2026/die-befreiung-der-ki-agenten/"
year: 2026
tags:
  - "vortrag"
  - "datengetrieben"
  - "dca"
categories:
  - "talk"
  - "ai"
heroImage: "/src/assets/media/2026/05/cloudland-2026-befreiung-der-ki-agenten.jpg"
heroAlt: "Plakat zum Cloud Native Festival, 19. bis 22. Mai 2026 im Heide Park Soltau. In Magenta der Titel Die Befreiung der KI-Agenten, daneben Azmir Abdi, unten adorsys und CloudLand."
editorialRevision: false
---

Braucht es für KI-Agenten wirklich eine neue Plattform?

Darum ging es auf der CloudLand, am 20. Mai 2026 im Heide Park Soltau. Das Festival lief vom 19. bis 22. Mai. Der Vortrag hieß „Die Befreiung der KI-Agenten“.

KI-Agenten sind gerade überall. Zuerst Copilots, dann Workflows, dann Agenten auf irgendeinem Rack, eine Vektor-Datenbank, ein Framework, und irgendwann eine eigene AI-Plattform. Am Anfang fühlt sich das an wie Wildwuchs. Sobald es nützlich wird, soll es produktiv laufen. Verfügbar, hochverfügbar, sicher. Betreiben soll es am Ende, wer die andere Software schon betreibt.

Die neuen Plattformen liegen meist obendrauf. Sie fügen sich nicht in das, was ein DevOps-Team schon hat. Ich glaube, das muss nicht so sein.

Ein Agent ist ein Stück Software. Er braucht ein Sprachmodell, einen Prompt, Werkzeuge und Wissen aus dem Unternehmen. Das liegt näher an einem Microservice, als die Black Box einer fertigen Plattform vermuten lässt. Wo schon Kubernetes läuft, lässt sich so ein Agent beschreiben und ausrollen. GitOps, Secrets, Observability. Der Pod ist kein Zauber.

Was fehlt, ist der Kontext. Ohne Unternehmenswissen bleibt der Agent eine Unterhaltung. Bei uns beschreiben wir dieses Wissen semantisch, mit Ontologien. Semantic Data Products machen den Zugriff leichter, weil die Schnittstelle schon spezifiziert ist. Es geht auch schlichter, mit Tabellen, PDFs oder einem Wiki.

Auf der Folie war die Spezifikation eine Custom Resource. Capabilities, Competency Questions, Modell, Prompt, Knowledge Base, Owner. Dieselbe Beschreibung kann der Fachbereich auf einer Canvas festhalten. Ich nenne sie Semantic Agent Canvas. Oder direkt als YAML in Git. Flux oder Argo CD übernimmt den Rest. Die Metadaten landen in einer Registry, und die ist selbst ein Graph. Dann sieht man, wo der Agent läuft, und auch, wofür er da ist und welchen anderen Agenten man fragen kann.

In der Demo hat ein Agent die Anfrage nicht selbst beantwortet, sondern weitergereicht. Mehr Magie war da nicht. Ein Image, mehrere Spezifikationen.

Dafür habe ich ein deutsches Wort. Betrieblich integrierte KI. Dieselbe Plattform wie für die Microservices. Die Domäne besitzt den Agenten und hält ihn aktuell. Die Modelle hängen hinter einem Gateway. Fürs Chatten reicht oft ein externes Modell. Für Mitarbeiterdaten will ich etwas, das lokal läuft. Prompt Injection und Datenabfluss prüft man besser an einer Stelle. MCP habe ich nicht vorgeführt. Es passt an dieselbe Registry.

Fünf Portale für dasselbe Team sind zu viel. Agenten hier, Data Products dort, das Repository in Backstage, die API im API-Management. Der Cluster kann die Workloads tragen.

Den Canvas und die Competency Questions hatte ich im September auf dem [Big Bang KI Festival](/blog/2025/semantic-data-products-auf-dem-big-bang-ki-festival/) zum ersten Mal live ausgefüllt. Wie Fachdomänen ihre Daten selbst bereitstellen, war im März das Thema auf der [DevLand](/blog/2026/javaland-und-devland-2026/). Die Architektur drumherum steht in [Datenzentrierte Architektur](/blog/2025/datenzentrierte-architektur/).
