---
title: "A new programming language, “Ubiquitous”: a domain-driven design project report"
description: "A WJAX 2022 talk on ubiquitous language: from the domain, through the architecture, to the code, including what worked and where DDD casts a shadow."
descriptionSource: "written"
pubDate: "2022-11-27"
updatedDate: "2023-03-24"
lang: "en"
originalLang: "de"
translationKey: "wp-259"
provenance: "translation"
translationStatus: "translated-unreviewed"
needsReview: true
draft: false
wpId: 259
author: "Azmir Abdi"
slug: "ubiquitous-a-ddd-project-report"
legacyPath: "/en/blog/2022/ubiquitous-a-ddd-project-report/"
year: 2022
tags: []
categories:
  - "ddd"
  - "talk"
heroImage: "/src/assets/media/2023/03/2022_WJax.jpg"
heroAlt: ""
editorialRevision: false
---

Back at [#WJAX](https://www.linkedin.com/feed/hashtag/?keywords=wjax&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A6996470013696036865), and it is a pleasure every time.

More visitors than ever. So many talks in parallel that you first have to think hard about what to attend. My highlights this time: the domain-storytelling talk by [Henning Schwentner](https://www.linkedin.com/in/ACoAAAFrXiABdt98fd0G5uA4IWGzmGLchTBXN5s); architecture for good testability by [Thomas Much](https://www.linkedin.com/in/ACoAAAQH7-QBxffj7Va1_IMmIi_kfqL_eX-Gayk); Apache Flink by [Frank Lyaruu](https://www.linkedin.com/in/ACoAAAN2_xYByMRDTqf2HqqOWDvlmqArsT_dtdM); DDD architectures by [Stefan Hildebrandt](https://www.linkedin.com/in/ACoAABoWkp0B4443ahbhzcDSoxAN2_A2TSOIWPo); the metaverse by [Thomas Riedel](https://www.linkedin.com/in/ACoAAAefKq0BwLjIN2dh3caf4LlZOu40a0x3-Q0); and of course the keynote “What We Know We Don’t Know” by [Hillel Wayne](https://www.linkedin.com/in/ACoAAAy9lsoBQ05guk4kYdAe7n5jvTHpOGg-Kgo). Thanks to the speakers for the talks.

I was able to give a talk again: “A new programming language, ‘Ubiquitous’: a domain-driven design ([#DDD](https://www.linkedin.com/feed/hashtag/?keywords=ddd&highlightedUpdateUrns=urn%3Ali%3Aactivity%3A6996470013696036865)) project report.” Because the talk took place only that day, I could still build two fitting slides, with sources, from [Henning Schwentner](https://www.linkedin.com/in/ACoAAAFrXiABdt98fd0G5uA4IWGzmGLchTBXN5s) and [Hillel Wayne](https://www.linkedin.com/in/ACoAAAy9lsoBQ05guk4kYdAe7n5jvTHpOGg-Kgo) into my talk. They fitted very well. Thanks for that too.

The abstract of the talk I was able to give at WJAX 2022 in Munich follows. The wording below is a translation of the German abstract, not a separate English original.

"Event, command, boundary, aggregate, … On top of Java, Kotlin, TypeScript, and the rest, a full-stack developer now has to master another language, and an unpronounceable one: “Ubiquitous”. The language is not type-safe. The compiler simply swallows Ubiquitous commands. In IntelliJ we have a small help: the German language pack, because, hard as it is to believe, it covers the language Ubiquitous. A disenchanting matter-of-factness that reveals its joke in more than one context. Or does a software developer shy away from programming sewage-plant software with a ubiquitous language? In this talk I go into domain-driven design (DDD) and the use of ubiquitous language, which is indispensable in it. How do you get from a domain, through a fitting software architecture, to the corresponding code? I report from the project: which DDD methods were well received, how event storming works over Skype, and what we gain from it in development. I show where and how we place the DDD artefacts in the code according to the boundary-control-entity (BCP) pattern. I also show the problems, the shadow side of DDD. Pitfalls you should know if you want to take DDD on."
