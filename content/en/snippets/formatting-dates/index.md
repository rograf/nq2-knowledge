---
title: "Formatting dates in Polish"
description: "A readable date with an explicit time zone in JavaScript."
date: 2026-09-29
tags: [javascript, dates]
---
`Intl.DateTimeFormat` formats dates without additional libraries.

## Code

```javascript
const formatDate = new Intl.DateTimeFormat('pl-PL', {
  dateStyle: 'long',
  timeZone: 'Europe/Warsaw',
});

formatDate.format(new Date('2026-09-29T12:00:00Z'));
// "29 września 2026"
```

## When to use it

An explicit time zone produces consistent results regardless of device settings. Pass the input as an ISO date with a time zone, such as the `Z` suffix for UTC. This example intentionally produces a Polish date; use `en-US` as the locale for English output.
