#!/usr/bin/env python3
"""Put the canonical estate bar into demos HTML pages. Idempotent.

Replaces, in order of preference: an existing estate-bar block, the old
<nav class="network-rail">, or the CAD page's <div class="estate"> strip.
If none is present, inserts the bar as the first element of <body>, after a
skip link when one leads the body. Also makes sure <head> loads the vendored
CSS and the demos accent.

    scripts/stamp_estate_bar.py site/index.html /home/jeremy/demos/longbox/index.html
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FRAGMENT = (REPO / "site/assets/estate-bar/fragments/estate-bar.demos.html").read_text().strip()
LINKS = (
    '<link rel="stylesheet" href="/assets/estate-bar/estate-bar.css">\n'
    '  <link rel="stylesheet" href="/assets/estate-accent.css">'
)
OLD = [
    re.compile(r"<!-- estate-bar:start[^>]*-->.*?<!-- estate-bar:end -->", re.S),
    re.compile(r'<nav class="network-rail".*?</nav>', re.S),
    re.compile(r'<div class="estate">\s*<nav.*?</nav>\s*</div>', re.S),
]
BODY = re.compile(r"(<body[^>]*>\s*(?:<a[^>]*class=\"[^\"]*skip[^\"]*\"[^>]*>.*?</a>\s*)?)", re.S | re.I)


def stamp(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    original = html
    for pattern in OLD:
        if pattern.search(html):
            html = pattern.sub(lambda _m: FRAGMENT, html, count=1)
            break
    else:
        if not BODY.search(html):
            raise SystemExit(f"{path}: no <body> tag found")
        html = BODY.sub(lambda m: m.group(1) + FRAGMENT + "\n", html, count=1)
    if "/assets/estate-bar/estate-bar.css" not in html:
        if "</head>" not in html:
            raise SystemExit(f"{path}: no </head> found")
        html = html.replace("</head>", f"  {LINKS}\n</head>", 1)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return "stamped"
    return "already current"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for arg in sys.argv[1:]:
        print(f"{stamp(Path(arg))}: {arg}")
