# NQ2 Knowledge

A bilingual knowledge base for NQ2, built with Hugo, Markdown, and the local `nq2-style` design system. Includes documentation, integrations, snippets, scripts, downloadable application releases, and a blog. Visitors can download NQ2 and install it themselves. No npm or external theme is required to build the site.

- English: https://rograf.github.io/nq2-knowledge/
- Polish: https://rograf.github.io/nq2-knowledge/pl/

## Install Hugo

Hugo builds this documentation website. It is not required to run the NQ2 application.

### Windows

Install Hugo Extended using Windows Package Manager:

```powershell
winget install Hugo.Hugo.Extended
```

Open a new terminal if necessary, then verify the installation:

```powershell
hugo version
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install hugo
```

Verify the installation:

```bash
hugo version
```

### macOS

With Homebrew installed, run:

```bash
brew install hugo
```

Verify the installation:

```bash
hugo version
```

### Match the project version

This project is validated with **Hugo 0.167.0**, the version pinned in `.github/workflows/pages.yml`. Package managers may install a different version; Ubuntu and Debian repositories in particular may provide an older release that cannot build this project. Check `hugo version` before continuing. To match the build environment, download the appropriate binary from the [Hugo 0.167.0 release](https://github.com/gohugoio/hugo/releases/tag/v0.167.0) and make it available on your `PATH`. The standard edition is sufficient; Extended also works.

See the [official Hugo installation documentation](https://gohugo.io/installation/) for platform-specific details.

## Local development

After installing Hugo, run the following command from the repository root:

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
      installing-nq2/index.md
    integrations/
      writing-an-integration-guide/index.md
    snippets/
      formatting-dates/index.md
    scripts/
      _index.md
    files/
      nq2-1-0-0/index.md
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

## Scripts and application downloads

Use `content/en/scripts/` and `content/pl/scripts/` for complete scripts with prerequisites, configuration, and usage instructions. Add actual script files as page attachments; reserve `snippets/` for short examples.

Application release pages belong in `content/en/files/` and `content/pl/files/`. Both languages use a single shared archive in `static/downloads/nq2/VERSION/`.

To prepare another release:

1. Add its ZIP to a new version directory under `static/downloads/nq2/`. Keep published version files unchanged so existing links remain reproducible.
2. Calculate the archive's SHA-256 with `Get-FileHash PATH -Algorithm SHA256` and its byte size with `(Get-Item PATH).Length`.
3. Create a matching `.zip.sha256` file containing `HASH`, two spaces, and the ZIP file name, followed by a newline.
4. Add an entry to `data/downloads.toml` with a unique ID, `name`, `path` (relative to `static/`), `size` in bytes, and lowercase `sha256`.
5. Create matching English and Polish release pages. Include the download card with the ID from the catalog:

   ```text
   {{< download "nq2-1-0-0-arm64-local" >}}
   ```

6. Describe the package and its changelog in both languages. Link to the shared installation guide with `relref "/docs/installing-nq2"` instead of repeating setup instructions on every release page. Keep Node.js, system dependencies, Mosquitto, checksum verification, and startup instructions in that guide. Use a lower `weight` to put a newer release above older releases.
7. Build and run the validation script. It checks the archive size, checksum, ZIP integrity, published copy, and links.

The ZIP and checksum file are published by Hugo as static assets. Links work from both languages and under the GitHub Pages repository subdirectory. Adding a file locally does not make it publicly downloadable until the user reviews, commits, and pushes the changes.

## GitHub Pages deployment

The `rograf/nq2-knowledge` repository uses **Settings → Pages → Build and deployment → Source: GitHub Actions** and `master` as its default branch.

AI-assisted changes must remain local for review. The user controls commits and pushes; an agent must not perform either unless explicitly requested for the current changes.

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

`static/vendor/nq2-style/nq.bootstrap.min.css` is a copy of the built stylesheet. It embeds Space Grotesk. Bootstrap and font licenses are stored alongside it. Site-specific layout styles live in `assets/css/site.css`; templates live in `layouts/`.

After rebuilding `nq2-style`, update the vendored assets with PowerShell:

```powershell
Copy-Item ../nq2-style/dist/nq.bootstrap.min.css static/vendor/nq2-style/
Copy-Item ../nq2-style/dist/BOOTSTRAP-LICENSE.txt static/vendor/nq2-style/
Copy-Item ../nq2-style/dist/OFL.txt static/vendor/nq2-style/
```

Keeping these assets in the repository lets GitHub Actions build the site without access to the neighboring local project.

Navigation uses a local SVG subset of `@hugeicons/core-free-icons` 4.2.2 in `layouts/partials/icons/`. The original icon names are recorded in the files, and the MIT license is preserved in `static/vendor/hugeicons/LICENSE.md`. No icon CDN or npm installation is needed to build the site. Header appearance is defined in `assets/css/navigation.css`; dropdown and mobile-menu interactions are in `static/js/navigation.js`.

## Ownership, license, and testing status

**NQ2 is owned by Rafał Rogulski. Copyright © 2026 Rafał Rogulski. All rights reserved.**

NQ2 is proprietary software. Making its code or installation packages publicly accessible does not make it open source or grant permission to modify or redistribute it.

You may download the official application package, install it, and run it on your own devices or devices you administer. You may adjust the settings exposed by the application and its configuration files for that installation. This permission does not transfer ownership or grant rights to the application source code.

Unless you have prior written permission from Rafał Rogulski, you may not modify the application code, create derivative versions, redistribute or republish its source code or application packages, sublicense it, or sell copies. These restrictions apply to the original NQ2 code and materials owned by Rafał Rogulski, subject to rights that cannot be restricted under applicable law and any applicable hosting-platform terms.

**The application is in the testing phase.** It may contain defects, change without notice, or stop working. It is provided **“as is” and “as available,” without warranties of any kind**, to the fullest extent permitted by applicable law. No guarantee is given regarding correct operation, availability, security, compatibility, data preservation, fitness for a particular purpose, continued development, updates, or support. Use it at your own risk and keep backups of important data.

To the fullest extent permitted by applicable law, Rafał Rogulski is not liable for loss or damage arising from the use of, or inability to use, NQ2. This statement does not exclude liability or rights that applicable law does not allow to be excluded.

Third-party software, fonts, and other dependencies remain subject to their respective licenses; the restrictions above do not replace or limit those licenses. In this repository, Bootstrap's license is in `static/vendor/nq2-style/BOOTSTRAP-LICENSE.txt`, and the Space Grotesk font license is in `static/vendor/nq2-style/OFL.txt`.
