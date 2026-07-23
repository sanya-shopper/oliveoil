#!/usr/bin/env python3
"""
fetch_photos.py — pull openly-licensed olive photos from Wikimedia Commons.

Why this exists:
  The site wants real inline photography but the repo must stay self-contained
  (no hotlinking) and every image must carry clean license + provenance. This
  queries the Commons API, keeps only permissively-licensed files (CC0 / public
  domain / CC BY / CC BY-SA), downloads a web-sized thumbnail (<=1600px) so the
  repo stays lean, records sha256 + source URL + license + artist + access date
  in assets/photos/credits.json, and writes a human-readable CREDITS.md.

  No local malware scanner is available on this box; images are JPEG/PNG served
  from the Wikimedia CDN (trusted) and we record sha256 for auditability.

Usage:  python3 refs/fetch_photos.py
Last updated: 2026-07-23 (Pacific)
"""
import json, hashlib, os, sys, time, urllib.parse, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "photos")
OUT = os.path.abspath(OUT)
API = "https://commons.wikimedia.org/w/api.php"
UA  = "oliveoil-static-site/1.0 (gift research project; sanya.shopper@gmail.com)"
ACCESSED = "2026-07-23"

# slot name -> search query. Keepers use their proven query string verbatim so
# they reproduce; weaker slots were re-queried for cleaner, non-branded shots.
QUERIES = {
    "grove":      "olive grove landscape",     # keeper: rolling grove vista (hero)
    "branch":     "olives on branch tree",     # keeper: olives + leaves on blue sky
    "tree":       "olive tree orchard",        # keeper: aerial orchard rows
    "mill":       "olive oil mill press",      # keeper: modern stainless mill
    "harvest":    "olive harvest hands",       # retry: people picking, not just tools
    "bottle":     "olive oil bottle dark glass", # retry: generic dark bottle
    "pour":       "extra virgin olive oil drizzle spoon", # retry: actual oil, not artifact
    "food":       "olive oil bread dipping",   # new: warm food/tasting shot
    "olives":     "olives wooden bowl table",  # new: still-life olives
}

OK_LICENSES = ("cc0", "public domain", "pd", "cc-by", "cc by", "cc-by-sa", "cc by-sa")

def api(params):
    params = dict(params); params["format"] = "json"
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def license_ok(short):
    s = (short or "").lower()
    return any(tok in s for tok in OK_LICENSES)

def clean(html):
    # extmetadata values can carry a little HTML; strip crudely
    import re
    txt = re.sub(r"<[^>]+>", "", html or "")
    return " ".join(txt.split())

def fetch_slot(slot, query, want=1):
    data = api({
        "action": "query", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": 12,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|mime|size",
        "iiurlwidth": 1600,
    })
    pages = (data.get("query") or {}).get("pages") or {}
    # search order isn't preserved in dict; sort by search index
    items = sorted(pages.values(), key=lambda p: p.get("index", 999))
    got = []
    for p in items:
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            continue
        mime = ii.get("mime", "")
        if mime not in ("image/jpeg", "image/png"):
            continue
        meta = ii.get("extmetadata") or {}
        short = (meta.get("LicenseShortName") or {}).get("value", "")
        if not license_ok(short):
            continue
        thumb = ii.get("thumburl")
        if not thumb or ii.get("thumbwidth", 0) < 1000:
            continue
        ext = ".jpg" if mime == "image/jpeg" else ".png"
        got.append({
            "slot": slot,
            "query": query,
            "title": p.get("title", ""),
            "thumburl": thumb,
            "descurl": ii.get("descriptionurl", ""),
            "license": clean(short),
            "license_url": (meta.get("LicenseUrl") or {}).get("value", ""),
            "artist": clean((meta.get("Artist") or {}).get("value", "")),
            "credit": clean((meta.get("Credit") or {}).get("value", "")),
            "description": clean((meta.get("ImageDescription") or {}).get("value", ""))[:240],
            "ext": ext,
        })
        if len(got) >= want:
            break
    return got

def download(entry, idx):
    fname = f"{entry['slot']}{'' if idx == 0 else idx}{entry['ext']}"
    path = os.path.join(OUT, fname)
    req = urllib.request.Request(entry["thumburl"], headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        blob = r.read()
    with open(path, "wb") as f:
        f.write(blob)
    entry["file"] = f"assets/photos/{fname}"
    entry["bytes"] = len(blob)
    entry["sha256"] = hashlib.sha256(blob).hexdigest()
    entry["accessed"] = ACCESSED
    return entry

def main():
    os.makedirs(OUT, exist_ok=True)
    records = []
    for slot, query in QUERIES.items():
        try:
            cands = fetch_slot(slot, query, want=1)
        except Exception as e:
            print(f"  ! {slot}: query failed: {e}", file=sys.stderr)
            continue
        if not cands:
            print(f"  - {slot}: no permissively-licensed match", file=sys.stderr)
            continue
        try:
            rec = download(cands[0], 0)
            records.append(rec)
            print(f"  + {slot}: {rec['file']} ({rec['bytes']//1024} KB) [{rec['license']}]")
        except Exception as e:
            print(f"  ! {slot}: download failed: {e}", file=sys.stderr)
        time.sleep(0.5)

    with open(os.path.join(OUT, "credits.json"), "w") as f:
        json.dump(records, f, indent=2)

    with open(os.path.join(OUT, "CREDITS.md"), "w") as f:
        f.write("# Photo credits & provenance\n\n")
        f.write(f"All images fetched {ACCESSED} from Wikimedia Commons, scaled to web size.\n")
        f.write("Licenses are permissive (CC0 / public domain / CC BY / CC BY-SA); attribution below.\n\n")
        for r in records:
            f.write(f"## {r['file']}\n")
            f.write(f"- Source: {r['descurl']}\n")
            f.write(f"- License: {r['license']}  {r['license_url']}\n")
            f.write(f"- Artist/credit: {r['artist'] or r['credit'] or 'see source page'}\n")
            f.write(f"- Description: {r['description']}\n")
            f.write(f"- sha256: {r['sha256']}\n")
            f.write(f"- accessed: {r['accessed']}\n\n")
    print(f"\nWrote {len(records)} photos + credits to {OUT}")

if __name__ == "__main__":
    main()
