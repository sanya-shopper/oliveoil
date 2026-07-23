# Bottling the Sun

A small, static, dependency-free website that researches one question:
**what would it take to start a mom-and-pop olive oil business in Upstate
New York** — sourcing US-grown oil, bottling and labeling it, and selling it?

It is built as a gift and as a genuine learning/research tool: attractive to
read, but every important claim is footnoted so the reader can check the
source themselves.

Live site: **https://sanya-shopper.github.io/oliveoil/**

## What's inside

| Page | Covers |
|------|--------|
| `index.html` | Overview + chapter map |
| `landscape.html` | The ~$3B US market, imports vs. domestic, headroom |
| `sourcing.html` | Who grows/mills US oil, bulk & private-label suppliers |
| `pricing.html` | Price history, where to watch prices, a 500 ml cost stack, RFQ how-to |
| `bottling.html` | FDA registration, NY Article 20-C license, labeling, dark glass |
| `marketing.html` | Channels, distributor fees, tasting rooms, DTC, marketing angles |
| `players.html` | Cobram/COR, Graza, estate artisans, big importers |
| `resources.html` | Full bibliography grouped by topic + method & photo credits |

## Design & tech

- Plain HTML + one CSS file (`css/style.css`) + one tiny JS file (`js/site.js`).
- **No frameworks, no CDNs, no external fonts, no tracking** — everything ships
  in the repo, so it loads fast, works offline, and leaks nothing to third
  parties.
- Photography is fetched from **Wikimedia Commons** under permissive licenses
  (CC0 / public domain / CC BY / CC BY-SA), scaled for the web. Attribution,
  license, source URL, and checksums are in `assets/photos/CREDITS.md`.
- The olive-branch mark and decorative branch are original SVGs.

## Repo layout

```
index.html + 7 chapter pages   the site
css/style.css                  the whole design system
js/site.js                     nav toggle, active link, footer year
assets/svg/                    favicon + brand/decoration SVGs
assets/photos/                 licensed photography + CREDITS.md
refs/                          research notes + the photo-fetch script (provenance)
.nojekyll                      tell GitHub Pages to serve files as-is
```

## Building / previewing locally

No build step. To preview:

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Refetching photos

`refs/fetch_photos.py` re-pulls the images from Wikimedia Commons and rewrites
`assets/photos/CREDITS.md` and `credits.json` with fresh provenance:

```sh
python3 refs/fetch_photos.py
```

## A note on accuracy

Prices and market figures are dated July 2026 snapshots and **will drift**;
olive oil is a volatile commodity. Nothing here is legal, financial, or
business advice — regulations must be confirmed with the FDA and the NYS
Department of Agriculture & Markets. Sources are dated and linked so they can
be re-checked.
