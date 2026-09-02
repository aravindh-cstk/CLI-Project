#!/usr/bin/env python3
"""Single source of truth for the CLI docs URL, slug and version-label restructure.

Old scheme                                  New scheme
  V0  /headless-cms/{slug}/old-commands       /headless-cms/{new-slug}/v0
  V1  /headless-cms/{slug}                    /headless-cms/{new-slug}/v1
  V2  /headless-cms/{slug}/beta               /headless-cms/{new-slug}

V2.x.x is going GA, so the V2 doc takes the unsuffixed URL. Slugs that carry no
"cli" anywhere gain a "cli-" prefix. Titles and SEO titles gain a "| V{n}.x.x"
label. The visible H1 stays version-free.

Every other script in the restructure imports from here so the mapping is
derived once. Run this file directly to emit cli-url-map.csv and a summary.

Usage:
  python3 scripts/cli_url_map.py          # print summary, write cli-url-map.csv
  python3 scripts/cli_url_map.py --check  # summary only, no file written
"""

import csv
import json
import os
import re
import sys

from cli_docs_common import ROOT, load_index

BUCKETS = ("GA", "Beta", "old")

VERSION_LABEL = {"old": "V0.x.x", "GA": "V1.x.x", "Beta": "V2.x.x"}
URL_SUFFIX = {"old": "/v0", "GA": "/v1", "Beta": ""}

# Docs whose content is valid for every CLI version, so a single page serves them
# all. These sit in the GA bucket for storage but take the bare URL and carry no
# version label, because a "| V1.x.x" tag on a page a V2 reader is meant to read
# would be wrong. Verified by grepping each one for removed commands, renamed
# flags and V1-only module values, and finding none.
VERSION_AGNOSTIC = frozenset({
    "contentstack-cli-configuration-reference",
    "create-custom-cli-commands",
    "create-custom-cli-plugins",
    "cli-migrate-selected-content-types-using-the-query-export-plugin",
    "cli-query-based-export",
    "cli-taxonomy-migration",
    "uninstall-cli-plugins",
    "cli-update-missing-reference-uids",
    "cli-useful-plugins",
    "cli-change-master-locale",
})

# Docs that only ever described V2 behaviour, so they belong in the Beta bucket
# and take the bare URL with a V2 label, never a /v1 form.
V2_ONLY = frozenset({"cli-for-cs-assets"})

# V1-only docs whose successor is a differently named V2 doc. The bare URL has to
# redirect to the successor rather than back to the /v1 page, because there is no
# V2 page at this slug.
V1_ONLY_SUCCESSOR = {
    "cli-bulk-publish-and-unpublish-content": "bulk-operations-in-cli",
}

# Every version qualifier that has ever been used in a title, seo.title or
# heading on these docs, plus the labels this restructure introduces so the
# transform is idempotent.
VERSION_QUALIFIERS = (
    "V2.x.x Beta",
    "Beta Commands",
    "V2 Beta",
    "Beta",
    "Old Commands",
    "V0.x.x",
    "V1.x.x",
    "V2.x.x",
)

# Trailing brand segment of an seo.title. "Contenstack" is a live typo that gets
# corrected while the field is being rewritten anyway.
BRAND_TAILS = {
    "Contentstack Documentation": "Contentstack Documentation",
    "Contentstack": "Contentstack",
    "Contenstack": "Contentstack",
}

# A trailing pipe segment matching this is probably a version qualifier we have
# not seen before. Better to stop and ask than to append a second label onto it.
VERSIONISH = re.compile(r"^(v\s*\d|beta|old\b|ga$|general availability|version)", re.I)

# Four live seo.title values have no brand segment for the rule to work from, so
# they are written out by hand rather than guessed. Three keep their existing text
# and gain the label plus a brand segment. cli-for-cs-assets has an empty
# seo.title, so it is seeded from the visible H1.
SEO_TITLE_OVERRIDES = {
    ("GA", "branches-migration-use-cases"):
        "Branches | Migration Use Cases | V1.x.x | Contentstack",
    ("old", "branches-migration-use-cases"):
        "Branches | Migration Use Cases | V0.x.x | Contentstack",
    ("GA", "cli-for-cs-assets"): "CLI for CS Assets | V1.x.x | Contentstack",
    ("GA", "useful-plugins"): "Useful Plugins | V1.x.x | Contentstack",
}

CSV_PATH = os.path.join(ROOT, "cli-url-map.csv")


# --------------------------------------------------------------------------
# slugs and urls
# --------------------------------------------------------------------------

def new_slug(slug):
    """Prefix cli- onto a slug that gives no signal it is a CLI doc."""
    return slug if "cli" in slug else f"cli-{slug}"


def _agnostic(slug):
    return slug is not None and new_slug(slug) in VERSION_AGNOSTIC


def _v2_only(slug):
    return slug is not None and new_slug(slug) in V2_ONLY


def new_url(slug, bucket):
    ns = new_slug(slug)
    if ns in VERSION_AGNOSTIC or ns in V2_ONLY:
        return f"/headless-cms/{ns}"
    return f"/headless-cms/{ns}{URL_SUFFIX[bucket]}"


def old_url(slug, bucket):
    tail = {"old": "/old-commands", "GA": "", "Beta": "/beta"}[bucket]
    return f"/headless-cms/{slug}{tail}"


def bucket_and_slug(url):
    """Derive (bucket, slug) from either the old or the new URL form.

    Old: .../{slug}, .../{slug}/beta, .../{slug}/old-commands
    New: .../{slug}/v1, .../{slug}, .../{slug}/v0

    The bare form is ambiguous across the two schemes (V1 before, V2 after), so
    it resolves to the bucket that owns the bare URL in each scheme: callers
    reading pre-migration data get "GA", callers reading post-migration data get
    "Beta". Disambiguate with the uid when it matters.
    """
    segments = [seg for seg in (url or "").strip("/").split("/") if seg]
    if not segments:
        return None, None
    last = segments[-1]
    if last == "old-commands" or last == "v0":
        return "old", segments[-2]
    if last == "beta":
        return "Beta", segments[-2]
    if last == "v1":
        return "GA", segments[-2]
    return None, last


# --------------------------------------------------------------------------
# titles and seo titles
# --------------------------------------------------------------------------

def strip_version_qualifier(text):
    """Drop a trailing "| <version qualifier>" segment. Returns (text, matched)."""
    for qualifier in VERSION_QUALIFIERS:
        suffix = f" | {qualifier}"
        if text.endswith(suffix):
            return text[: -len(suffix)].rstrip(), True
    return text, False


def new_title(title, bucket, _slug_hint=None):
    """Append the version label to an entry title.

    Returns None when the title ends in an unrecognized version-looking segment,
    so the caller reports it for review instead of stacking a second label.
    """
    label = VERSION_LABEL[bucket]
    base, matched = strip_version_qualifier(title)
    if _agnostic(_slug_hint):
        return base
    if _v2_only(_slug_hint):
        label = VERSION_LABEL["Beta"]
    if not matched and " | " in title:
        tail = title.rsplit(" | ", 1)[-1].strip()
        if VERSIONISH.match(tail):
            return None
    return f"{base} | {label}"


def clean_heading(heading):
    """Strip a known version qualifier from a visible H1, which stays version-free.

    heading_cleanup.strip_heading_suffix refuses any unrecognized pipe segment,
    which is right for the Beta and old-commands headings it was written for but
    wrong here: "Branches | Migration Use Cases" is a doc name that contains a
    pipe. This only refuses a trailing segment that looks like a version qualifier
    we do not know yet.
    """
    base, matched = strip_version_qualifier(heading)
    if matched:
        return base
    if " | " in heading and VERSIONISH.match(heading.rsplit(" | ", 1)[-1].strip()):
        return None
    return heading


def new_seo_title(seo_title, bucket, slug=None):
    """Insert the version label before the trailing brand segment of an seo.title.

    Falls back to SEO_TITLE_OVERRIDES when the field is empty or has no recognized
    brand segment, and returns None when neither applies, so the caller reports it
    for review instead of inventing a brand segment.
    """
    label = VERSION_LABEL[bucket]
    if _v2_only(slug):
        label = VERSION_LABEL["Beta"]
    override = SEO_TITLE_OVERRIDES.get((bucket, slug))
    if not (seo_title or "").strip():
        return override
    parts = [p.strip() for p in seo_title.split("|")]
    parts = [p for p in parts if p and p not in VERSION_QUALIFIERS]
    if not parts:
        return override
    brand = BRAND_TAILS.get(parts[-1])
    if brand is None:
        return override
    return " | ".join(parts[:-1] + [label, brand])


# --------------------------------------------------------------------------
# the mapping itself
# --------------------------------------------------------------------------

def _read_local_entry(record):
    path = os.path.join(ROOT, "docs", "json", record["json"])
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_docs():
    """Return one record per CLI doc, keyed work order, with old and new values.

    Titles and seo titles come from the local docs/json snapshot. The push script
    re-derives them from the live entry so a doc edited in the CMS since the last
    fetch is still handled correctly.
    """
    index = load_index()
    docs = []
    for record in index["entries"]:
        bucket, slug = record["bucket"], record["slug"]
        entry = _read_local_entry(record)
        seo_title = (entry.get("seo") or {}).get("title") or ""
        docs.append({
            "uid": record["uid"],
            "bucket": bucket,
            "slug": slug,
            "new_slug": new_slug(slug),
            "old_url": record["url"],
            "new_url": new_url(slug, bucket),
            "old_title": entry.get("title") or "",
            "new_title": new_title(entry.get("title") or "", bucket),
            "old_seo_title": seo_title,
            "new_seo_title": new_seo_title(seo_title, bucket, slug),
            "seo_title_overridden": (bucket, slug) in SEO_TITLE_OVERRIDES,
            "json": record["json"],
            "markdown": record["markdown"],
        })
    return docs


def load_map(require=True):
    """Return the frozen mapping from cli-url-map.csv.

    load_docs() derives the mapping from docs/json/index.json, which only works
    before the local files are rewritten. Every phase after that reads the CSV
    instead, so the old URLs and titles stay available and each script can be
    re-run against already-migrated files without drifting.
    """
    if not os.path.exists(CSV_PATH):
        if require:
            sys.exit("cli-url-map.csv is missing. Run scripts/cli_url_map.py first, "
                     "before any local file is rewritten.")
        return load_docs()
    with open(CSV_PATH, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    docs = []
    for row in rows:
        docs.append({
            "uid": row["uid"],
            "bucket": row["bucket"],
            "slug": row["slug"],
            "new_slug": row["new_slug"],
            "old_url": row["old_url"],
            "new_url": row["new_url"],
            "old_title": row["old_title"],
            "new_title": row["new_title"],
            "old_seo_title": row["old_seo_title"],
            "new_seo_title": row["new_seo_title"],
            "old_json": f"{row['bucket']}/{row['slug']}.json",
            "new_json": f"{row['bucket']}/{row['new_slug']}.json",
            "old_markdown": f"{row['bucket']}/{row['slug']}.md",
            "new_markdown": f"{row['bucket']}/{row['new_slug']}.md",
            "redirect_from": row["redirect_from"],
            "redirect_to": row["redirect_to"],
        })
    return docs


def by_slug(docs):
    """slug -> {bucket: record}, keyed by both the old and the new slug.

    Content that has already been migrated refers to topics by their new slug, so
    both spellings have to resolve for the link helpers to keep working. A new slug
    is the old slug with a cli- prefix, and check_slug_collisions() proves no new
    slug can shadow a different topic's old slug.
    """
    grouped = {}
    for doc in docs:
        grouped.setdefault(doc["slug"], {})[doc["bucket"]] = doc
    for doc in docs:
        grouped.setdefault(doc["new_slug"], {}).setdefault(doc["bucket"], doc)
    return grouped


def check_slug_collisions(docs):
    """Exit if any new slug equals a different topic's old slug."""
    old_slugs = {d["slug"] for d in docs}
    clashes = sorted({d["new_slug"] for d in docs
                      if d["new_slug"] != d["slug"] and d["new_slug"] in old_slugs})
    if clashes:
        sys.exit(f"FATAL: new slug(s) collide with an existing topic: {clashes}")


def has_v2(docs, slug):
    return "Beta" in by_slug(docs).get(slug, {})


def link_target(docs, target_slug, from_bucket):
    """New URL a doc in from_bucket should use when linking to target_slug.

    Stays inside the same version, falling back to the nearest version that
    exists: a V0 doc linking to a topic with no V0 doc lands on V1, and a V1 doc
    linking to a topic that only has V2 lands on V2.
    """
    available = by_slug(docs).get(target_slug)
    if not available:
        return None
    preference = {
        "old": ("old", "GA", "Beta"),
        "GA": ("GA", "Beta", "old"),
        "Beta": ("Beta", "GA", "old"),
    }[from_bucket]
    for bucket in preference:
        if bucket in available:
            return available[bucket]["new_url"]
    return None


def current_ga_url(docs, target_slug):
    """New URL of the doc that is current GA for a topic: V2 if it exists, else V1."""
    available = by_slug(docs).get(target_slug)
    if not available:
        return None
    for bucket in ("Beta", "GA", "old"):
        if bucket in available:
            return available[bucket]["new_url"]
    return None


def redirects(docs):
    """Old absolute path -> new absolute path, for every URL that stops resolving.

    Skipped deliberately: a V1 doc whose slug does not change and whose topic has
    a V2 doc. Its old URL is byte-identical to the new V2 URL, and server_redirects
    override published pages on this site, so a redirect there would make the new
    GA doc unreachable.
    """
    pairs = []
    for doc in sorted(docs, key=lambda d: (d["slug"], d["bucket"])):
        slug, bucket = doc["slug"], doc["bucket"]
        if bucket == "GA" and has_v2(docs, slug) and doc["new_slug"] == slug:
            continue
        source = f"/docs{old_url(slug, bucket)}"
        if bucket == "GA" and has_v2(docs, slug):
            target = f"/docs/headless-cms/{doc['new_slug']}"
        else:
            target = f"/docs{doc['new_url']}"
        if source == target:
            continue
        pairs.append((source, target))
    return pairs


def cli_slugs(docs):
    return {doc["slug"] for doc in docs}


# --------------------------------------------------------------------------

def index_is_migrated():
    """True once docs/json/index.json holds new-scheme URLs.

    load_docs() derives old-to-new by reading index.json, so it only produces a
    correct mapping before Phase 1 rewrites that file. Afterwards it would derive
    a no-op mapping, which must never overwrite the frozen CSV.
    """
    return any((e.get("url") or "").endswith(("/v0", "/v1"))
               for e in load_index()["entries"])


def main():
    force = "--force" in sys.argv
    if index_is_migrated() and os.path.exists(CSV_PATH) and not force:
        sys.exit("docs/json/index.json already holds new-scheme URLs, so the "
                 "old-to-new mapping can no longer be derived from it. "
                 f"{os.path.relpath(CSV_PATH, ROOT)} is the frozen source of truth "
                 "and was left untouched. Pass --force only if you intend to "
                 "regenerate it from a pre-migration index.json.")

    docs = load_docs()
    check_slug_collisions(docs)
    pairs = redirects(docs)
    grouped = by_slug(docs)

    review = [d for d in docs if d["new_title"] is None or d["new_seo_title"] is None]
    renamed = sorted({d["slug"] for d in docs if d["new_slug"] != d["slug"]})
    skipped = [d for d in docs
               if d["bucket"] == "GA" and has_v2(docs, d["slug"]) and d["new_slug"] == d["slug"]]

    print(f"docs tracked            : {len(docs)}  "
          f"({sum(1 for d in docs if d['bucket'] == 'GA')} GA, "
          f"{sum(1 for d in docs if d['bucket'] == 'Beta')} Beta, "
          f"{sum(1 for d in docs if d['bucket'] == 'old')} old)")
    print(f"topics                  : {len(grouped)}  "
          f"({sum(1 for s in grouped if 'Beta' in grouped[s])} with a V2 doc)")
    print(f"slugs renamed           : {len(renamed)}")
    print(f"redirects               : {len(pairs)}")
    print(f"GA docs with no redirect: {len(skipped)}  (old V1 URL == new V2 URL)")
    print(f"needs manual review     : {len(review)}")

    new_urls = [d["new_url"] for d in docs]
    dupes = {u for u in new_urls if new_urls.count(u) > 1}
    if dupes:
        sys.exit(f"\nFATAL: duplicate new URLs: {sorted(dupes)}")

    redirect_sources = {src for src, _ in pairs}
    collisions = redirect_sources & {f"/docs{u}" for u in new_urls}
    if collisions:
        sys.exit(f"\nFATAL: redirect source would shadow a live page: {sorted(collisions)}")

    overridden = [d for d in docs if d["seo_title_overridden"]]
    if overridden:
        print("\nseo.title values taken from SEO_TITLE_OVERRIDES (no brand segment to "
              "derive from):")
        for doc in overridden:
            print(f"  {doc['bucket']:5} {doc['slug']}")
            print(f"        {doc['old_seo_title']!r} -> {doc['new_seo_title']!r}")

    stale = [d for d in overridden
             if new_seo_title(d["old_seo_title"], d["bucket"]) is not None]
    if stale:
        print("\nWARNING: these overrides are no longer needed, the rule now covers "
              f"them: {[(d['bucket'], d['slug']) for d in stale]}")

    if review:
        print("\nFields needing a hand-written value:")
        for doc in review:
            print(f"  {doc['bucket']:5} {doc['slug']}")
            if doc["new_title"] is None:
                print(f"        title    : {doc['old_title']!r}")
            if doc["new_seo_title"] is None:
                print(f"        seo.title: {doc['old_seo_title']!r}")
        sys.exit("\nFATAL: fill in the values above before continuing.")

    if "--check" in sys.argv:
        return

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["uid", "bucket", "slug", "new_slug", "old_url", "new_url",
                         "old_title", "new_title", "old_seo_title", "new_seo_title",
                         "redirect_from", "redirect_to"])
        lookup = dict(pairs)
        for doc in sorted(docs, key=lambda d: (d["slug"], d["bucket"])):
            source = f"/docs{old_url(doc['slug'], doc['bucket'])}"
            writer.writerow([
                doc["uid"], doc["bucket"], doc["slug"], doc["new_slug"],
                doc["old_url"], doc["new_url"],
                doc["old_title"], doc["new_title"] or "",
                doc["old_seo_title"], doc["new_seo_title"] or "",
                source if source in lookup else "", lookup.get(source, ""),
            ])
    print(f"\nWrote {os.path.relpath(CSV_PATH, ROOT)}")


if __name__ == "__main__":
    main()
