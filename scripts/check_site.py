"""Check translation coverage and internal links in a production Hugo build."""

import json
import hashlib
import zipfile
from html.parser import HTMLParser
from pathlib import Path
import tomllib
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.language = None
        self.canonical = None
        self.alternates = {}
        self.redirect = False
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.redirect = True
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "link" and attrs.get("hreflang"):
            self.alternates[attrs["hreflang"]] = attrs["href"]
        self.links.extend(attrs[key] for key in ("href", "src") if attrs.get(key))


def main():
    errors = []
    catalog = tomllib.loads((ROOT / "data" / "downloads.toml").read_text(encoding="utf-8"))
    for download_id, download in catalog.items():
        archive = ROOT / "static" / download["path"]
        published = PUBLIC / download["path"]
        if not archive.is_file() or not published.is_file():
            errors.append(f"Missing source or published archive: {download_id}")
            continue
        checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
        if archive.stat().st_size != download["size"] or checksum != download["sha256"]:
            errors.append(f"Download metadata mismatch: {download_id}")
        if hashlib.sha256(published.read_bytes()).hexdigest() != checksum:
            errors.append(f"Published archive mismatch: {download_id}")
        expected = f"{checksum}  {archive.name}\n"
        for checksum_path in (archive.with_suffix('.zip.sha256'), published.with_suffix('.zip.sha256')):
            if not checksum_path.is_file() or checksum_path.read_text(encoding="ascii") != expected:
                errors.append(f"Invalid checksum file: {checksum_path}")
        try:
            with zipfile.ZipFile(archive) as bundle:
                if bundle.testzip() is not None:
                    errors.append(f"Corrupt ZIP archive: {download_id}")
        except zipfile.BadZipFile:
            errors.append(f"Invalid ZIP archive: {download_id}")
    sources = {}
    messages = {}
    indexes = {}
    home = Page(PUBLIC / "index.html")
    base = urlsplit(home.canonical)

    for language in ("en", "pl"):
        directory = ROOT / "content" / language
        sources[language] = {p.relative_to(directory) for p in directory.rglob("*.md")}
        messages[language] = set(tomllib.loads((ROOT / "i18n" / f"{language}.toml").read_text(encoding="utf-8")))
        prefix = base.path + ("pl/" if language == "pl" else "")
        index_path = PUBLIC / ("pl/index.json" if language == "pl" else "index.json")
        entries = json.loads(index_path.read_text(encoding="utf-8"))
        indexes[language] = set()
        for entry in entries:
            url = entry["url"]
            if not url.startswith(prefix) or (language == "en" and url.startswith(base.path + "pl/")):
                errors.append(f"Wrong language in {language} search index: {url}")
            indexes[language].add(url.removeprefix(prefix))

    for label, groups in (("Markdown files", sources), ("UI translation keys", messages), ("published search entries", indexes)):
        if groups["en"] != groups["pl"]:
            errors.append(f"Mismatched {label}: {groups['en'] ^ groups['pl']}")

    pages = [Page(path) for path in PUBLIC.rglob("*.html")]
    for page in pages:
        relative = page.path.relative_to(PUBLIC)
        if not page.redirect:
            expected_language = "pl" if relative.parts[0] == "pl" else "en"
            if page.language != expected_language:
                errors.append(f"Incorrect HTML language: {relative}")
            if page.path.name != "404.html" and set(page.alternates) != {"en", "pl"}:
                errors.append(f"Missing alternate language link: {relative}")

        for link in page.links:
            url = urlsplit(link)
            if url.scheme and url.scheme not in ("http", "https"):
                continue
            if url.netloc and url.netloc != base.netloc:
                continue
            if not url.path:
                continue
            path = unquote(url.path)
            if path.startswith(base.path):
                target = PUBLIC / path.removeprefix(base.path)
            elif path.startswith("/"):
                errors.append(f"Link outside site base: {relative}: {link}")
                continue
            else:
                target = page.path.parent / path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                errors.append(f"Broken link: {relative}: {link}")

    legacy_paths = {
        "dokumentacja/": "docs/",
        "integracje/": "integrations/",
        "snippety/": "snippets/",
        "dokumentacja/jak-dodawac-tresci/": "docs/adding-content/",
        "integracje/szablon-integracji/": "integrations/writing-an-integration-guide/",
        "snippety/formatowanie-daty/": "snippets/formatting-dates/",
        "blog/start-bazy-wiedzy/": "blog/introducing-the-knowledge-base/",
    }
    for old, new in legacy_paths.items():
        path = PUBLIC / old / "index.html"
        if not path.exists():
            errors.append(f"Missing legacy redirect: {old}")
            continue
        redirect = Page(path)
        if not redirect.redirect or redirect.canonical != home.canonical + "pl/" + new:
            errors.append(f"Incorrect legacy redirect: {old}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(sources['en'])} translated Markdown pairs, matching UI keys and search indexes, links in {len(pages)} HTML files, {len(catalog)} verified downloads.")


if __name__ == "__main__":
    main()
