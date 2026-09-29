---
title: "Jak dodawać treści do bazy wiedzy"
description: "Od pliku Markdown do opublikowanego artykułu."
date: 2026-09-29
weight: 1
tags: [markdown, redakcja]
---
Każdy artykuł jest plikiem Markdown w katalogu `content/`. Wybierz sekcję, dodaj materiał i wyślij zmianę na gałąź `master`.

## Wybierz sekcję

| Katalog | Co tu umieszczać |
| --- | --- |
| `dokumentacja/` | Instrukcje obsługi i konfiguracji aplikacji |
| `integracje/` | Opisy API, połączeń i wymiany danych |
| `snippety/` | Krótkie, gotowe fragmenty kodu |
| `blog/` | Wpisy, aktualności i notatki z rozwoju |

## Utwórz artykuł

Dodaj katalog, np. `content/dokumentacja/moja-instrukcja/`, a w nim plik `index.md`:

```yaml
---
title: "Moja instrukcja"
description: "Krótki opis widoczny na liście artykułów."
date: 2026-09-29
weight: 10
tags: [konfiguracja]
draft: false
---
```

Pod metadanymi napisz treść. Tytuł strony powstaje z pola `title`, więc kolejne nagłówki zaczynaj od `##`. Hugo zbuduje z nich spis treści.

Pole `weight` ustala kolejność w dokumentacji, integracjach i snippetach. Blog jest sortowany od najnowszego wpisu. `draft: true` ukrywa materiał w publikacji; lokalnie zobaczysz go przez `hugo server -D`.

## Dołącz pliki

Pliki PDF, obrazy, przykładowe konfiguracje i archiwa możesz umieszczać obok `index.md`. Linkuj do nich względnie:

```markdown
[Pobierz instrukcję](instrukcja.pdf)
![Widok ustawień aplikacji](ustawienia.png)
```

Te pliki pojawią się razem z artykułem. Wspólne zasoby można przechowywać w `static/`.

## Łącz artykuły

Do odnośników między artykułami używaj shortcode `relref` Hugo. Sprawdza on istnienie strony i uwzględnia podkatalog GitHub Pages. Przykład zapisu znajduje się w README repozytorium.

## Opublikuj zmianę

Po zapisaniu pliku wykonaj commit i `git push origin master`. Workflow GitHub Actions zbuduje stronę i opublikuje ją na GitHub Pages. Aktualizacja będzie widoczna po zakończeniu wdrożenia, zwykle po kilku minutach.
