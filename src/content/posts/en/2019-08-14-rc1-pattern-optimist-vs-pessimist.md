---
title: "The rc1 pattern: optimist versus pessimist"
description: "An optimistic developer initialises a process as successful. The cheaper habit can become an expensive anomaly once an unexpected event never sets the failure state."
descriptionSource: "written"
pubDate: "2019-08-14"
updatedDate: "2026-10-26"
lang: "en"
originalLang: "de"
translationKey: "wp-83"
provenance: "translation"
translationStatus: "translated-unreviewed"
needsReview: true
draft: false
wpId: 83
author: "Azmir Abdi"
slug: "rc1-pattern-optimist-vs-pessimist"
legacyPath: "/en/blog/2019/rc1-pattern-optimist-vs-pessimist/"
year: 2019
tags:
  - "initial-state"
  - "rc1"
categories:
  - "coding-patterns"
heroImage: "/src/assets/media/2020/06/20200105_104406-e1591303615592-crop.jpg"
heroAlt: ""
editorialRevision: true
---

The German title spells it “Optmist”. That spelling is kept on the original page. Here the word is written as “optimist”.

An optimistic software developer (such people are said to exist) starts from the *goodwill case* and, for example, implements a stateful process with success as the initial value. For instance:

```
class MyProcess {
    state OK;
    ...
}
```

I think I can hear what he is telling himself: `I save myself the explicit setting of this state, which is needed in 99.99% of cases, by simply initialising it that way. If the state should be set differently, no problem, I will do it then.` So far, so good.

Then, one fine day (the optimist has long since moved on), a few data analysts spend several weeks on some anomalies. A few months later someone does suspect a fault in the implementation. An analysis ticket is opened, with the hint that something about the application’s transactions must be wrong. The application claims that some process instances were processed successfully. The data analysis shows, clearly, that this is not so.

Days of reading the code finally expose the fairy tale: an unexpected event stopped the processing and did not implicitly set the status to failure. The optimist’s 99.99% saving caused costs in the higher four figures.

Most people would ask why he went about it that way. Add a faulty rollback implementation and you land in the scene above.

Because it is not obvious to everyone, I am writing down the practice that one may set the state to success only after the last commit. Never before. Before that, it has to be plain that the status was not initialised as success. If you want to force the status to be updated at every step, the status can start as failure. A strict habit, and in the end a sparing one, in large projects. Better still if the initial state is clearly marked as unset, as `NOT_SET`.

```
class MyProcess {
    state NOT_SET;
    ...
}
```

If that state has still not been overwritten at the end of processing, the processing should finish as faulty, the same way any other unexpected state is handled.

In shell and Bash scripts one often initialises a return-code (`rc`) variable at the start of the script with the value 1, which stands for an error. The script ends with `exit rc`. The work happens in between. Only after successful processing is the variable set to 0. That way an OK is reported in that case, and only then.

```
rc = 1 #initiate return code with error
...
do this
change that
commit something else
rc = 0 #set to success
...
exit rc #exit with return code
```

That is why **rc1** seems to me an easy name to remember for this behaviour. I hope an optimist can see it too.

Thanks for your time. Warm regards,
[Azmir Abdi](/en/about/)

PS: I'd be glad to hear from you via [a message](/en/about/#contact).
