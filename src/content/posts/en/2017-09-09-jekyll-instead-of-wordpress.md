---
title: "Jekyll instead of WordPress"
description: "Why this blog started on Jekyll: no database, static pages, and a comment experiment with Staticman that later led back to WordPress."
descriptionSource: "written"
pubDate: "2017-09-09"
updatedDate: "2026-10-26"
lang: "en"
originalLang: "de"
translationKey: "wp-151"
provenance: "translation"
translationStatus: "translated-unreviewed"
needsReview: true
draft: false
wpId: 151
author: "Azmir Abdi"
slug: "jekyll-instead-of-wordpress"
legacyPath: "/en/blog/2017/jekyll-instead-of-wordpress/"
year: 2017
tags: []
categories:
  - "blog"
heroImage: ""
heroAlt: ""
editorialRevision: true
---

`In the beginning was the idea … and because the idea was so "innovative", it found its creation in cyberspace.`

- Does the internet still need a blog?
- Does the internet need my blog?

Be that as it may, here I sit, typing how it came about …

A few thoughts kept following me, and I could not find them online, so I opened a blog of my own. I am very curious what time will make of the impression.

So, off we go.

## The topics …

… were set by those thoughts:

- IT architecture
- BPM
- Enterprise architecture
- Java

## Choosing the technology

[WordPress](https://en.wordpress.com/) is more or less the standard for blogs, and I chose [Jekyll](http://jekyllrb.com/). Roughly for these reasons:

- No database server required
- A remarkably simple template mechanism
- Static content only
- [GitHub Pages](https://pages.github.com/) and [GitLab Pages](https://gitlab.com/pages) each support [Jekyll](http://jekyllrb.com/) with their own deployment pipeline

There are plenty of articles online arguing for [Jekyll](http://jekyllrb.com/). One example is from [Smashing Magazine](https://www.smashingmagazine.com/2014/08/build-blog-jekyll-github-pages/).

## [Disqus](https://disqus.com) versus [Staticman](https://staticman.net/)

What about comments, though? Are comments not *the* reason to set up a blog, so that you receive the community’s response to your own thoughts? `Web 2.0`. But running [WordPress](https://en.wordpress.com/), which allows dynamic content, only for the comment function …?

The next search followed: `comments for Jekyll sites`. Hits:

- [Disqus](https://disqus.com)
  - Stores the comments, through its own SaaS in the USA, overseas, per page (URL), and loads them inside an embedded div.
- [Staticman](https://staticman.net/)
  - Runs a git-push service in which every comment is stored as a new file on the matching paths in the site’s source code, in the site’s GitHub repository. GitHub notices the change and starts a new deployment.

I prefer [Staticman](https://staticman.net/) because it is `cool`. IT people like complicated flows. And then all the comments lie in the source code, which really is many times better than [Disqus](https://disqus.com).

## [GitLab Pages](https://gitlab.com/pages) versus [GitHub Pages](https://pages.github.com/)

What is interesting is that, in [GitLab Pages](https://gitlab.com/pages) versus [GitHub Pages](https://pages.github.com/), GitLab actually offers far more functions and a modern CI pipeline. Together with [Staticman](https://staticman.net/), though, it was out of the question, because a new deployment took several minutes on account of the whole Docker container. On [GitHub Pages](https://pages.github.com/) it was only a few seconds.

Try it, and leave a comment.

1. In the background the public [Staticman](https://staticman.net/) service is called with the HTTP POST form, and it in turn stores a new file for your comment with `git push`. See the [GitHub comments repository](https://github.com/azabdi/azabdi.github.io/tree/master/_data/comments/).
2. GitHub starts a new deployment and …
3. … when you reload the page, your comment should appear.

## Conclusion

Once the comment function was embedded, the rest was done quickly. I enjoyed setting it up, and the thought of how simply a new blog post can be added (once the blog stands) pleases me even more. I hope there will be something worth reading for you as well.

### Note added on 4 June 2020

A field report on Staticman: it was not entirely positive. Some comments were not taken over as the article intended, so the blog was migrated to WordPress after all. A thesis is easily overturned when it rests on only one pillar.

---

The original article, whose Jekyll-generated content can be seen on GitHub Pages, is here: [https://azabdi.github.io/](https://azabdi.github.io/). Thanks for your time. Warm regards,
[Azmir Abdi](/en/about/)

PS: I'd be glad to hear from you via [a message](/en/about/#contact).
