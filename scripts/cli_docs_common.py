"""Shared Contentstack CMA plumbing for the CLI docs scripts.

The same load_env/request pair was copy-pasted into fetch_cli_docs.py,
push_cli_docs.py, fix_docs_article_headings.py and flatten_v0_v2_nav.py. The
URL restructure adds six more scripts on top of that, so the helpers live here
once. Existing scripts keep their local copies to avoid churning code that is
already known-good.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

REGION_HOST = "https://api.contentstack.io"
DOCS_ARTICLE = "docs_article"
SERVER_REDIRECTS = "server_redirects"
LOCALE = "en-us"

PROD_ENV_UID = "bltfe8376c13fe85b9c"
STAGING_ENV_UID = "blt4a008c3cde35b0c2"
DEVELOPMENT_ENV_UID = "blt92ab7d24e8c52483"
PUBLISH_ENV_UIDS = [STAGING_ENV_UID, DEVELOPMENT_ENV_UID]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "docs", "json", "index.json")


def read_env():
    """Return every key in .env as a dict."""
    path = os.path.join(ROOT, ".env")
    env = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("'\"")
    return env


def staging_auth_header():
    """Basic auth header for the password-protected staging host, or None."""
    env = read_env()
    user, password = env.get("STAG_USERNAME"), env.get("STAG_PASSWORD")
    if not user or not password:
        return None
    import base64
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    return f"Basic {token}"


def load_env():
    """Read the stack credentials out of .env and return CMA request headers."""
    env = read_env()
    api_key = env.get("CONTENTSTACK_DOCS_STACK_API_KEY")
    token = env.get("CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN")
    if not api_key or not token:
        sys.exit("Missing CONTENTSTACK_DOCS_STACK_API_KEY or "
                 "CONTENTSTACK_DOCS_STACK_MANAGEMENT_TOKEN in .env")
    return {"api_key": api_key, "authorization": token,
            "Content-Type": "application/json"}


def request(method, path, headers, body=None, params=None, attempts=5):
    """Call a CMA endpoint, retrying on rate limits and transient network errors.

    403 is retried as well as 429. The publish endpoint returns 403 when it is
    being throttled, not only when a token lacks permission, and a bulk run trips
    that often enough that a single unlucky call would otherwise abort the whole
    pass. A genuine permission error still fails, just after the backoff.
    """
    url = f"{REGION_HOST}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=180) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 403) and attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"HTTP {exc.code} for {method} {url}\n"
                     f"{exc.read().decode('utf-8', 'replace')[:800]}")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < attempts - 1:
                time.sleep(2 ** attempt)
                continue
            sys.exit(f"Network error for {url}: {exc}")
    return None


def get_entry(headers, content_type, uid, version=None):
    params = {"locale": LOCALE, "include_publish_details": "true"}
    if version is not None:
        params["version"] = str(version)
    return request("GET", f"/v3/content_types/{content_type}/entries/{uid}",
                   headers, params=params)["entry"]


def put_entry(headers, content_type, uid, entry):
    return request("PUT", f"/v3/content_types/{content_type}/entries/{uid}",
                   headers, body={"entry": entry}, params={"locale": LOCALE})["entry"]


def publish_entry(headers, content_type, uid, version, env_uids=None):
    body = {
        "entry": {"environments": env_uids or PUBLISH_ENV_UIDS, "locales": [LOCALE]},
        "locale": LOCALE,
        "version": version,
    }
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/publish",
            headers, body=body)


def unpublish_entry(headers, content_type, uid, version, env_uids=None):
    """Take an entry off the given environments. Reversible: publish it again.

    Preferred over deleting an entry when the goal is only to stop serving it, for
    example a redirect whose source now needs to serve a real page.
    """
    body = {
        "entry": {"environments": env_uids or PUBLISH_ENV_UIDS, "locales": [LOCALE]},
        "locale": LOCALE,
        "version": version,
    }
    request("POST", f"/v3/content_types/{content_type}/entries/{uid}/unpublish",
            headers, body=body)


def list_entries(headers, content_type, only=None, page_size=100, progress=False):
    """Page through every entry of a content type, optionally limiting fields."""
    entries, skip = [], 0
    while True:
        params = [("limit", str(page_size)), ("skip", str(skip)),
                  ("include_count", "true"), ("include_publish_details", "true")]
        for field in only or ():
            params.append(("only[BASE][]", field))
        data = request("GET", f"/v3/content_types/{content_type}/entries",
                       headers, params=params)
        page = data.get("entries", [])
        entries.extend(page)
        total = data.get("count", 0)
        if progress:
            print(f"  listed {len(entries)}/{total}", file=sys.stderr, flush=True)
        if not page or len(entries) >= total:
            return entries
        skip += page_size


def is_published_to(entry, env_uid):
    return any(rec.get("environment") == env_uid and rec.get("locale") == LOCALE
               for rec in entry.get("publish_details") or [])


def article_section(entry):
    """Return the article_section dict of an entry, or exit if it has none."""
    for block in entry.get("article_content") or []:
        if "article_section" in block:
            return block["article_section"]
    sys.exit(f"entry {entry.get('uid')} has no article_section block")


def load_index():
    with open(INDEX_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def save_index(index):
    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
