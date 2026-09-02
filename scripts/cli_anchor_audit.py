#!/usr/bin/env python3
"""WI-4 anchor audit, corrected.

Verified renderer behavior (from the live DOM of /docs/headless-cms/cli-authentication):
  H2 and H3 are wrapped in  <div id="<slug>" class="group heading-with-copy ...">
  followed by <h2 class="... docs-h3 ...">  or  <h3 class="... docs-h4 ...">.
  H4 renders as a bare <h4> with NO id, NO anchor, and NO right-nav entry.

So an anchor that targets an H4 heading cannot be fixed by rewriting the href.
The heading has to be promoted to H3.

Read-only.
"""
import concurrent.futures as cf
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "docs", "markdown")
HOST = "https://www.contentstack.com"
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
UA = {"User-Agent": "Mozilla/5.0"}

index = json.load(open(os.path.join(ROOT, "docs", "json", "index.json")))
url2md, url2title = {}, {}
for e in index["entries"]:
    url2md["/docs" + e["url"]] = e["markdown"]
    url2title["/docs" + e["url"]] = e["title"]
md2url = {}
for u, m in url2md.items():
    md2url.setdefault(m, u)

# ---- authoritative ids from the rendered page ----
HEADING_DIV = re.compile(
    r'<div id="([^"]+)" class="group heading-with-copy[^"]*">\s*<h([23])[^>]*>(.*?)</h\2>', re.S)


def rendered(url):
    try:
        html = urllib.request.urlopen(
            urllib.request.Request(HOST + url, headers=UA), timeout=180
        ).read().decode("utf-8", "replace")
    except Exception as exc:
        return None, str(exc)
    out = []
    for m in HEADING_DIV.finditer(html):
        out.append((m.group(1), int(m.group(2)),
                    re.sub(r"<[^>]+>", "", m.group(3)).strip()))
    return out, None


# ---- local markdown headings, fence aware ----
def local_headings(relpath):
    out, fence = [], False
    p = os.path.join(MD, relpath)
    if not os.path.exists(p):
        return out
    for n, line in enumerate(open(p, encoding="utf-8"), 1):
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), n))
    return out


def slug(text):
    """Approximate the renderer: ':' and most punctuation dropped, '/' and space -> '-'."""
    s = text.lower().replace("/", " ")
    s = re.sub(r"`", "", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


# ---- collect anchor links ----
records = []
for dp, _d, fs in os.walk(MD):
    for fn in sorted(fs):
        if not fn.endswith(".md"):
            continue
        rel = os.path.relpath(os.path.join(dp, fn), MD)
        if not rel.startswith(("Version 1", "Version 2")):
            continue
        for n, line in enumerate(open(os.path.join(dp, fn), encoding="utf-8"), 1):
            for m in LINK.finditer(line):
                href = m.group(2)
                if "#" not in href:
                    continue
                base, frag = href.split("#", 1)
                if not frag.strip():
                    continue
                records.append((rel, n, m.group(1), href, base.rstrip("/"), frag.strip()))

pages = set()
for rel, _n, _t, _h, base, _f in records:
    pages.add(md2url[rel] if base == "" and rel in md2url else base if base in url2md else None)
pages.discard(None)

print(f"fetching {len(pages)} rendered pages ...", file=sys.stderr)
ren, errs = {}, {}
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    fut = {ex.submit(rendered, u): u for u in sorted(pages)}
    for f in cf.as_completed(fut):
        u = fut[f]
        got, err = f.result()
        if err or not got:
            errs[u] = err or "no heading divs found"
        ren[u] = got or []
for u, e in sorted(errs.items()):
    print(f"  WARN {u}: {e}", file=sys.stderr)

# ---- evaluate ----
rows = []
for rel, line, text, href, base, frag in records:
    if base == "":
        url = md2url.get(rel)
        kind = "same-page"
    elif base in url2md:
        url = base
        kind = "cross-doc"
    else:
        continue
    if not url or url not in ren or not ren[url]:
        continue
    have = {i.lower(): (lvl, t) for i, lvl, t in ren[url]}
    if frag.lower() in have:
        continue

    tgt_rel = url2md.get(url, rel)
    hs = local_headings(tgt_rel)
    cause, action, rec = "unknown", "", ""

    hit = next(((lvl, ht) for lvl, ht, _ln in hs if slug(ht) == frag.lower()), None)
    if hit and hit[0] >= 4:
        cause = f'target heading "{hit[1]}" is H{hit[0]}'
        action = "promote heading to H3"
        rec = ""
    else:
        cands = [(lvl, ht) for lvl, ht, _ln in hs
                 if lvl in (2, 3) and (slug(ht) in frag.lower() or frag.lower() in slug(ht))]
        if cands:
            cands.sort(key=lambda c: -len(slug(c[1])))
            lvl, ht = cands[0]
            cause = f'stale anchor, closest H{lvl} heading is "{ht}"'
            action = "rewrite href"
            rec = f"{base}#{slug(ht)}"
        else:
            # is the text present at H4 under a different slug?
            h4 = [ht for lvl, ht, _ln in hs if lvl >= 4
                  and any(w in slug(ht) for w in frag.lower().split("-")[:2])]
            if h4:
                cause = f'no H2/H3 match, nearest content is H4 "{h4[0]}"'
                action = "promote heading to H3, then link to it"
            else:
                cause = "no matching heading at any level in target"
                action = "needs author decision"
    rows.append(dict(src=rel, line=line, kind=kind, text=text, href=href, base=base,
                     frag=frag, target=url2title.get(url, tgt_rel),
                     cause=cause, action=action, rec=rec))

rows.sort(key=lambda r: (r["src"], r["line"]))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "notes", "reports", "anchors.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(rows, open(out, "w"), indent=1)
print("wrote " + out, file=sys.stderr)
print(f"\nbroken anchor links: {len(rows)}", file=sys.stderr)
print(f"distinct broken hrefs: {len(set(r['href'] for r in rows))}", file=sys.stderr)
import collections
for a, n in collections.Counter(r["action"] for r in rows).most_common():
    print(f"  {n:3d}  {a}", file=sys.stderr)
