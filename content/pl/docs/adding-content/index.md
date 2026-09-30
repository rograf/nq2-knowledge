---
title: "Jak dodawać treści do bazy wiedzy"
aliases: [/../dokumentacja/jak-dodawac-tresci/]
description: "Od pliku Markdown do opublikowanego artykułu."
date: 2026-09-29
weight: 1
tags: [markdown, authoring]
---
Każdy artykuł jest plikiem Markdown w `content/en/` (angielski) lub `content/pl/` (polski). Nazwy katalogów i plików są zawsze po angielsku. Wybierz sekcję, dodaj obie wersje materiału i wyślij zmianę na gałąź `master`.

## Wybierz sekcję

| Katalog | Co tu umieszczać |
| --- | --- |
| `docs/` | Instrukcje obsługi i konfiguracji aplikacji |
| `integrations/` | Opisy API, połączeń i wymiany danych |
| `snippets/` | Krótkie, gotowe fragmenty kodu |
| `scripts/` | Kompletne skrypty z konfiguracją i instrukcją użycia |
| `files/` | Wydania aplikacji do pobrania i samodzielnej instalacji |
| `blog/` | Wpisy, aktualności i notatki z rozwoju |

## Utwórz artykuł

Dodaj katalogi `content/en/docs/my-guide/` i `content/pl/docs/my-guide/`, a w każdym plik `index.md`. Identyczna ścieżka pozwala Hugo połączyć tłumaczenia. Polska wersja może zaczynać się tak:

```yaml
---
title: "Moja instrukcja"
description: "Krótki opis widoczny na liście artykułów."
date: 2026-09-29
weight: 10
tags: [configuration]
draft: false
---
```

Pod metadanymi napisz treść. Tytuł strony powstaje z pola `title`, więc kolejne nagłówki zaczynaj od `##`. Hugo zbuduje z nich spis treści.

Pole `weight` ustala kolejność w dokumentacji, integracjach i snippetach. Blog jest sortowany od najnowszego wpisu. `draft: true` ukrywa materiał w publikacji; lokalnie zobaczysz go przez `hugo server -D`.

## Przygotuj tłumaczenie

Wersje językowe mają tę samą ścieżkę i angielskie tagi. Przetłumacz `title`, `description` oraz treść; zachowaj datę i kolejność. Angielski jest dostępny pod głównym adresem strony, polski pod `/pl/`. Przełącznik EN / PL prowadzi do tłumaczenia tego samego artykułu. Jeśli tłumaczenia brakuje, wskazuje stronę główną drugiego języka.

## Dołącz pliki

Pliki PDF, obrazy, przykładowe konfiguracje i archiwa możesz umieszczać obok `index.md`. Linkuj do nich względnie:

```markdown
[Pobierz instrukcję](guide.pdf)
![Widok ustawień aplikacji](settings.png)
```

Te pliki pojawią się razem z artykułem. Wspólne zasoby można przechowywać w `static/`.

## Łącz artykuły

Do odnośników między artykułami używaj shortcode `relref` Hugo. Sprawdza on istnienie strony i uwzględnia bieżący język oraz podkatalog GitHub Pages. Przykład zapisu znajduje się w README repozytorium.

## Opublikuj zmianę

Po zapisaniu pliku wykonaj commit i `git push origin master`. Workflow GitHub Actions zbuduje stronę i opublikuje ją na GitHub Pages. Aktualizacja będzie widoczna po zakończeniu wdrożenia, zwykle po kilku minutach.
