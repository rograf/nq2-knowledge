---
title: "Formatowanie daty po polsku"
description: "Czytelna data z jawną strefą czasową w JavaScript."
date: 2026-09-29
tags: [javascript, daty]
---
`Intl.DateTimeFormat` pozwala formatować daty bez dodatkowych bibliotek.

## Kod

```javascript
const formatDate = new Intl.DateTimeFormat('pl-PL', {
  dateStyle: 'long',
  timeZone: 'Europe/Warsaw',
});

formatDate.format(new Date('2026-09-29T12:00:00Z'));
// „29 września 2026”
```

## Kiedy używać

Jawna strefa czasowa daje spójny wynik niezależnie od ustawień urządzenia. Wartość wejściową przekazuj jako datę ISO z informacją o strefie, np. z końcówką `Z` dla UTC.
