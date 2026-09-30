---
title: "How to add content to the knowledge base"
description: "From a Markdown file to a published article."
date: 2026-09-29
weight: 1
tags: [markdown, authoring]
---
Every article is a Markdown file in `content/en/` (English) or `content/pl/` (Polish). Always use English directory and file names. Choose a section, add both versions of your article, and push your changes to `master`.

## Choose a section

| Directory | What belongs here |
| --- | --- |
| `docs/` | Application instructions and configuration guides |
| `integrations/` | API documentation, connections, and data exchange |
| `snippets/` | Short, reusable code examples |
| `scripts/` | Complete scripts with configuration and usage instructions |
| `files/` | Application releases to download and install yourself |
| `blog/` | Articles, updates, and development notes |

## Create an article

Create `content/en/docs/my-guide/` and `content/pl/docs/my-guide/`, each containing an `index.md` file. Matching paths let Hugo associate the translations. Start the English version with:

```yaml
---
title: "My guide"
description: "A short description displayed in article lists."
date: 2026-09-29
weight: 10
tags: [configuration]
draft: false
---
```

Write the body below the metadata. The page title comes from `title`, so start section headings with `##`. Hugo uses these headings to build the table of contents.

The `weight` field sets the order in documentation, integrations, and snippets. Blog posts appear newest first. `draft: true` excludes an article from publication; preview drafts locally with `hugo server -D`.

## Add the translation

Use the same path and English tags in both versions. Translate `title`, `description`, and the body; keep the date and ordering consistent. English is available at the site root and Polish under `/pl/`. The EN / PL switch opens the translation of the current article. If a translation is missing, it links to the other language's home page.

## Attach files

Place PDFs, images, sample configurations, and archives next to `index.md`. Use relative links:

```markdown
[Download the guide](guide.pdf)
![Application settings](settings.png)
```

These files are published alongside the article. Shared assets can live in `static/`.

## Link articles

Use Hugo's `relref` shortcode for links between articles. It validates the target and respects the current language and the GitHub Pages subdirectory. See the repository README for an example.

## Publish a change

Save the files, commit, and run `git push origin master`. GitHub Actions builds the site and deploys it to GitHub Pages. Changes become visible once deployment finishes, usually within a few minutes.
