# NQ2 Knowledge

Baza wiedzy aplikacji NQ2: Hugo, Markdown i style z `nq2-style`. Zawiera dokumentację, integracje, snippety i blog. Bez npm i bez zewnętrznego motywu.

Docelowy adres: https://rograf.github.io/nq2-knowledge/

## Uruchomienie lokalne

Zainstaluj [Hugo 0.167.0](https://github.com/gohugoio/hugo/releases/tag/v0.167.0) (zwykła wersja wystarczy), a następnie:

```sh
hugo server -D
```

Otwórz adres wypisany przez Hugo. `-D` pokazuje również szkice. Produkcyjny build:

```sh
hugo --gc --minify --panicOnWarning
```

Wynik trafia do `public/`, które jest pomijane w Git.

## Treść i załączniki

```text
content/
  _index.md                     # nagłówek i opis strony głównej
  dokumentacja/
  integracje/
  snippety/
  blog/
    moj-wpis/
      index.md                  # treść i metadane
      schemat.png               # pliki towarzyszące artykułowi
```

Nowy artykuł:

```sh
hugo new content dokumentacja/moja-instrukcja/index.md
```

Uzupełnij `title`, `description`, datę i treść. Ustaw `draft: false`, kiedy materiał jest gotowy. Nagłówki treści zaczynaj od `##`; `#` powstaje z tytułu. Blog sortuje wpisy od najnowszych; pozostałe sekcje korzystają z `weight` (mniejsze wartości najpierw). Przyszłe daty i szkice są domyślnie pomijane w produkcji.

Przykładowe metadane:

```yaml
---
title: "Konfiguracja aplikacji"
description: "Krótki opis materiału."
date: 2026-09-29
weight: 10
tags: [konfiguracja]
draft: false
---
```

Odnośnik między artykułami (Hugo sprawdzi jego cel):

```markdown
[Dodawanie treści]({{< relref "/dokumentacja/jak-dodawac-tresci" >}})
```

Załączniki trzymaj obok `index.md`, np. `[Pobierz PDF](instrukcja.pdf)` i `![Schemat](schemat.png)`. Nie dodawaj początkowego `/` do takich linków — strona działa w podkatalogu GitHub Pages. Każdy artykuł i jego treść trafiają do lokalnej wyszukiwarki. Nie publikuj haseł, tokenów ani prywatnych danych.

Nową sekcję dodasz przez `content/nazwa/_index.md` z `title`, `description`, `weight` oraz `symbol`. Nawigacja i kafelki tworzą się automatycznie.

## GitHub Pages

1. W repozytorium `rograf/nq2-knowledge` wybierz **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Wyślij pliki na `master`:

   ```sh
   git add .
   git commit -m "Initialize NQ2 knowledge site"
   git push -u origin master
   ```

3. W zakładce **Actions** sprawdź workflow **Build and deploy Hugo to Pages**. Po udanym wdrożeniu pojawi się adres strony.

Każdy kolejny **push na `master`** automatycznie buduje i publikuje stronę. Sam lokalny commit nie uruchamia GitHub Actions. Publikacja trwa tyle, ile wykonanie workflow, zwykle kilka minut. Pull requesty do `master` są tylko budowane, bez publikacji. Workflow można też uruchomić ręcznie z `master`.

Adres produkcyjny jest pobierany z ustawień Pages, co uwzględnia podkatalog i ewentualną domenę własną. `baseURL` w `hugo.toml` odpowiada domyślnemu adresowi repozytorium; zaktualizuj go, jeśli zmienisz domenę. Nie potrzeba osobnego tokenu ani gałęzi `gh-pages`.

Workflow oparto na [oficjalnej instrukcji Hugo dla GitHub Pages](https://gohugo.io/host-and-deploy/host-on-github-pages/). Wersja Hugo jest przypięta w `.github/workflows/pages.yml`; aktualizuj ją razem z wersją lokalną.

## Style

`static/vendor/nq2-style/nq.bootstrap.min.css` to skopiowany gotowy arkusz z `D:\projects\programopol\nq2-style\dist`. Zawiera font Space Grotesk. Licencje Bootstrap i fontu są w tym samym katalogu. Własny układ strony jest w `assets/css/site.css`; szablony w `layouts/`.

Aktualizacja stylów w PowerShell, po zbudowaniu projektu `nq2-style`:

```powershell
Copy-Item ../nq2-style/dist/nq.bootstrap.min.css static/vendor/nq2-style/
Copy-Item ../nq2-style/dist/BOOTSTRAP-LICENSE.txt static/vendor/nq2-style/
Copy-Item ../nq2-style/dist/OFL.txt static/vendor/nq2-style/
```

Kopia w repozytorium pozwala budować stronę w GitHub Actions bez dostępu do lokalnego dysku i sąsiedniego projektu.
