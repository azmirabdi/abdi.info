---
title: "Freeing the AI Agents"
description: "Does it take a new platform to run AI agents? A look back at CloudLand on 20 May 2026 at Heide Park Soltau."
descriptionSource: "written"
pubDate: "2026-05-26"
updatedDate: "2026-05-26"
lang: "en"
originalLang: "de"
translationKey: "cloudland-2026-befreiung-der-ki-agenten"
provenance: "translation"
translationStatus: "translated-unreviewed"
needsReview: true
draft: false
author: "Azmir Abdi"
slug: "freeing-the-ai-agents"
legacyPath: "/en/blog/2026/freeing-the-ai-agents/"
year: 2026
tags:
  - "vortrag"
  - "datengetrieben"
  - "dca"
categories:
  - "talk"
  - "ai"
heroImage: "/src/assets/media/2026/05/cloudland-2026-befreiung-der-ki-agenten.jpg"
heroAlt: "Poster for the Cloud Native Festival, 19 to 22 May 2026 at Heide Park Soltau. The title Die Befreiung der KI-Agenten in magenta, Azmir Abdi beside it, adorsys and CloudLand below."
editorialRevision: false
---

Does it really take a new platform to run AI agents?

That was the question at CloudLand, on 20 May 2026 at Heide Park Soltau. The festival ran from 19 to 22 May. The talk was called "Die Befreiung der KI-Agenten".

AI agents are everywhere right now. First copilots, then workflows, then agents on some rack, a vector database, a framework, and at some point a platform of their own. At the start it feels like unchecked growth. Once it becomes useful, it is supposed to run in production. Available, highly available, secure. In the end, the people who already run the other software are supposed to run this too.

The new platforms usually sit on top. They do not fit what a DevOps team already has. I do not think it has to be that way.

An agent is a piece of software. It needs a language model, a prompt, tools, and knowledge from the company. That sits closer to a microservice than the black box of a finished platform suggests. Where Kubernetes is already running, an agent like this can be described and rolled out. GitOps, secrets, observability. The pod is not magic.

What is missing is context. Without knowledge from the company, the agent stays a conversation. Where I work, we describe that knowledge semantically, with ontologies. Semantic data products make access easier, because the interface is already specified. It also works more plainly, with tables, PDFs, or a wiki.

On the slide, the specification was a custom resource. Capabilities, competency questions, model, prompt, knowledge base, owner. A business domain can hold the same description on a canvas. I call it the Semantic Agent Canvas. Or straight into Git as YAML. Flux or Argo CD takes it from there. The metadata lands in a registry, and the registry itself is a graph. Then you can see where the agent runs, and also what it is for and which other agent to ask.

In the demo, one agent did not answer the request itself. It passed it on. There was no more magic than that. One image, several specifications.

I have a German phrase for it: betrieblich integrierte KI, AI that belongs to ordinary operations. The same platform as for the microservices. The domain owns the agent and keeps it current. The models sit behind a gateway. For chat, an external model is often enough. For employee data, I want something that runs locally. Prompt injection and data leakage are better checked in one place. I did not show MCP. It fits the same registry.

Five portals for the same team are too many. Agents here, data products there, the repository in Backstage, the API in API management. The cluster can carry the workloads.

I had filled in the canvas and the competency questions live for the first time in September, at the [Big Bang AI Festival](/en/blog/2025/semantic-data-products-at-the-big-bang-ai-festival/). How business domains provide their own data was the subject at [DevLand](/en/blog/2026/javaland-and-devland-2026/) in March. The architecture around it is in [Data-Centric Architecture](/en/blog/2025/data-centric-architecture/).
