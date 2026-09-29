# NQ2 Knowledge

A bilingual knowledge base for NQ2, built with Hugo, Markdown, and the local `nq2-style` design system. Includes documentation, integrations, snippets, and a blog. No npm or external theme is required to build the site.

- English: https://rograf.github.io/nq2-knowledge/
- Polish: https://rograf.github.io/nq2-knowledge/pl/

## Local development

Install [Hugo 0.167.0](https://github.com/gohugoio/hugo/releases/tag/v0.167.0) (the standard edition is sufficient), then run:

```sh
hugo server -D
```

Open the address printed by Hugo. `-D` includes drafts. To create a production build and validate it:

```sh
hugo --gc --minify --panicOnWarning --cleanDestinationDir
python scripts/check_site.py
```

The validation script requires Python 3.11 or newer. Generated files go into `public/`, which is excluded from Git. Only use `--cleanDestinationDir` with the default generated output directory; it removes stale generated pages after content moves.

## Repository language

Use **English for directory names, file names, URL paths, tag identifiers, code, comments, commit messages, and repository documentation**. Website content and interface text are available in **English and Polish**. Polish text belongs in `content/pl/` and `i18n/pl.toml`.

## Content structure

```text
content/
  en/
    _index.md
    docs/
      adding-content/index.md
    integrations/
      writing-an-integration-guide/index.md
    snippets/
      formatting-dates/index.md
    blog/
      introducing-the-knowledge-base/index.md
  pl/
    ...                         # same English paths, Polish content

i18n/
  en.toml                       # English interface strings
  pl.toml                       # Polish interface strings
```

English is the default language at the site root; Polish uses `/pl/`. Both languages share the same English paths, for example `/docs/adding-content/` and `/pl/docs/adding-content/`, relative to the GitHub Pages project URL.

## Add or update an article

Create the English article, then create its Polish counterpart at the same relative path:

```sh
hugo new content en/docs/my-guide/index.md
hugo new content pl/docs/my-guide/index.md
```

The archetype uses English headings. Translate the title, description, headings, and body in the Polish file. Matching paths automatically connect the translations in Hugo. Keep dates, weights, and English tag identifiers consistent. Publish both versions together: the build check rejects missing counterparts and mismatched published search entries.

Example front matter:

```yaml
---
title: "Application configuration"
description: "A short summary of the article."
date: 2026-09-29
weight: 10
tags: [configuration]
draft: false
---
```

Start body headings with `##`; the template renders the page title. Blog posts are sorted newest first; other sections use `weight` (lower values first). Drafts and future-dated articles are excluded from production by default.

The language switch links to the translation of the current page, including sections and tags. If a translation is unavailable in a local preview, the switch links to the other language's home page. Each language has its own search index, RSS feed, page metadata, and navigation. Shared styles and scripts are loaded from the site root.

## Links and attachments

Use `relref` to validate links and keep readers in the current language:

```markdown
[Adding content]({{< relref "/docs/adding-content" >}})
```

Place attachments next to `index.md`, using English file names:

```markdown
[Download the guide](guide.pdf)
![Application settings](settings.png)
```

Use relative attachment links without a leading `/`. Place language-specific attachments in the corresponding language bundle. Hugo can share resources between translated bundles; a resource in the current language takes precedence. Common static assets belong in `static/`.

To add a section, create `content/en/section-name/_index.md` and `content/pl/section-name/_index.md` with `title`, `description`, `weight`, and `symbol`. Navigation and home page cards are generated automatically.

Legacy Polish article and section URLs redirect to their new Polish locations through front matter `aliases`. Their `/../` prefix escapes the new `/pl/` language prefix to preserve the original root-level URLs. These legacy strings are retained only for backward compatibility. The old `/blog/` section is now the English blog.

## Interface translations

Add interface strings to both `i18n/en.toml` and `i18n/pl.toml` under matching English keys. Templates use Hugo's `i18n` function; JavaScript receives translated labels through HTML data attributes. Avoid hardcoding interface text in templates or scripts.

See the [Hugo multilingual documentation](https://gohugo.io/content-management/multilingual/) for the directory-based translation model.

## GitHub Pages deployment

The `rograf/nq2-knowledge` repository uses **Settings → Pages → Build and deployment → Source: GitHub Actions** and `master` as its default branch.

```sh
git add .
git commit -m "Update knowledge base content"
git push origin master
```

Every **push to `master`** builds, validates, and deploys both languages. A local commit alone does not trigger GitHub Actions. Pull requests to `master` build and validate without deployment. You can also run the workflow manually on `master`.

Check **Actions → Build and deploy Hugo to Pages** for deployment status. Changes are visible after the workflow completes, usually within a few minutes. No separate token or `gh-pages` branch is needed.

Production builds get the base URL from Pages settings, including the repository subdirectory or a custom domain. Update `baseURL` in `hugo.toml` if the permanent domain changes. Hugo is pinned in `.github/workflows/pages.yml`; use the same version locally.

The workflow follows the [official Hugo GitHub Pages guide](https://gohugo.io/host-and-deploy/host-on-github-pages/).

## Styles

`static/vendor/nq2-style/nq.bootstrap.min.css` is a copy of the built stylesheet from `D:\projects\programopol\nq2-style\dist`. It embeds Space Grotesk. Bootstrap and font licenses are stored alongside it. Site-specific layout styles live in `assets/css/site.css`; templates live in `layouts/`.

After rebuilding `nq2-style`, update the vendored assets with PowerShell:

```powershell
Copy-Item ../nq2-style/dist/nq.bootstrap.min.css static/vendor/nq2-style/
Copy-Item ../nq2-style/dist/BOOTSTRAP-LICENSE.txt static/vendor/nq2-style/
Copy-Item ../nq2-style/dist/OFL.txt static/vendor/nq2-style/
```

Keeping these assets in the repository lets GitHub Actions build the site without access to the neighboring local project.
