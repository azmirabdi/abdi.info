---
title: "rc1 Pattern - Optmist vs. Pessimist"
description: "Ein optimistisch veranlagter Softwareentwickler (es soll so was anscheinend auch geben) geht von dem goodwill-case aus und implementiert zum Beispiel einen statusbehafteten…"
descriptionSource: "derived-lead"
pubDate: "2019-08-14"
updatedDate: "2021-12-19"
lang: "de"
originalLang: "de"
translationKey: "wp-83"
provenance: "original"
translationStatus: "original"
needsReview: false
draft: false
wpId: 83
wpStatus: "publish"
author: "Azmir Abdi"
slug: "rc1-pattern-optmist-vs-pessimist"
legacyPath: "/blog/2019/rc1-pattern-optmist-vs-pessimist/"
year: 2019
tags:
  - "initial-state"
  - "rc1"
categories:
  - "coding-patterns"
heroImage: "/src/assets/media/2020/06/20200105_104406-e1591303615592-crop.jpg"
heroAlt: ""
wpContentHash: "6e4d4115bc05e059a0f68f49fad789c5f18f3257de94e487b7118b592be2fd75"
bodyHash: "c0aa1aa55482c75acab6126349993fbbd84f0e986046587dd450b67004ab20c4"
editorialRevision: false
---

Ein optimistisch veranlagter Softwareentwickler (es soll so was anscheinend auch geben) geht von dem *goodwill-case* aus und implementiert zum Beispiel einen statusbehafteten Prozess mit dem erfolgreichen Status als initialen Wert. Bsp.:

```
class MyProcess {
    state OK;
    ...
}
```

Ich glaube zu meinen, dass er sich dabei folgendes denkt: `Ich spare mir das im 99,99% der Fällen notwendiges explizites Setzen diesen Zustandes in dem ich es einfach damit initiiere. Falls der Zustand anders gesetzt werden sollte - kein Problem, dann mache ich es eben.` - so weit, so gut.

Doch dann, eines schönen Tages (der Optimist ist schon längst weitergezogen) beschäftigen sich ein paar Datenanalysten mit einigen Anomalien - mehrere Wochen lang. Ein paar Monate später vermutet man doch einen Fehler in der Implementierung. So wird ein Analyse Ticket geöffnet mit dem Hinweis dass da wohl was an der Transaktionen der Anwendung falsch sein müsste. Die Anwendung behauptet, dass einige Prozessinstanzen erfolgreich verarbeitet wurden, die Datenanalyse jedoch eindeutig beweist dass dies nicht der Fall ist.

Die mehrtägige Codeanalyse entblößt endlich das Märchen bei dem ein unerwarteter Ereignis die Verarbeitung stoppte und dabei nicht implizit den Status der Verarbeitung auf Fehler setzte. Es steht fest, der 99,99% Ersparnis des Optimisten hat Kosten in dem höheren vierstelligen Bereich verursacht.

Die Meisten würden sich fragen wieso er wohl so vorgegangen ist. Wenn dazu noch eine fehlerhafte Roll-Back Implementierung hinzu kommt, landet man dabei im oben beschriebenes Szenario.

Weil es eben doch nicht für alle klar ist, beschriebe ich hiermit das *Best Practise* dass man eigentlich den Zustand erst nach dem letzten Commit auf erfolgreich setzen darf. Niemals vorher. Vorher muss klar ersichtlich sein dass der Status nicht imitiert wurde. Wenn man dabei beim jeden Schritt erzwingen möchte dass der Status aktualisiert wird, so könnte der Status anfänglich mit dem Fehler initiiert werden. Ein rigoroses Vorgehen ich, letztendlich aber sehr sparsam - im großen Projekten. Noch besser wäre es wenn initial der Zustand als nicht gesetzt/"NOT_SET" klar gekennzeichnet wurde.

```
class MyProcess {
    state NOT_SET;
    ...
}
```

Sollte dieser Zustand am Ende der Verarbeitung immer noch nicht überschrieben worden sein, dann sollte die Verarbeitung - wie auch sonst mit einem unerwarteten Zustand gehandhabt wird - als fehlerhaft abgeschlossen werden.

Im Shell/Bash Skripten imitiert man oft an dem Skript-Anfang eine return-code (rc) Variable explizit mit dem Wert 1, das wiederum für einen Fehler steht. Das Skript wird mit `exit rc` beendet. Dazwischen findet die Verarbeitung statt. Erst bei einer erfolgreichen Verarbeitung wird die Variable implizit 0 gesetzt. Damit ist es sichergestellt dass in dem Fall - und nur dann - mit einem OK die Verarbeitung quittiert wird.

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

Daher finde ich **rc1** als ein Name dem man sich für dieses Verhalten sehr einfach einprägen kann und hoffe, dass auch ein Optimist dies einsehen kann.

Vielen Dank für Deine Zeit und liebe Grüße,
[Azmir Abdi](/about-me/)

PS: Ich würde mich über einen Kommentar oder eine [Email](mailto:azmir@abdi.info) sehr freuen.
