#!/usr/bin/env python3
"""Fail-closed checks for the static catalog and its deployed route targets."""

from __future__ import annotations

import os
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = REPO_ROOT / "site"
DEPLOY_ROOT = Path(os.environ.get("DEMOS_DEPLOY_ROOT", "/home/jeremy/demos"))


class CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.catalog_items = 0
        self.hrefs: list[str] = []
        self.assets: list[str] = []
        self.has_canonical = False
        self.has_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = (values.get("class") or "").split()
        if tag == "article" and "catalog-item" in classes:
            self.catalog_items += 1
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"])
        if tag in {"img", "script"} and values.get("src"):
            self.assets.append(values["src"])
        if tag == "link" and values.get("href"):
            if values.get("rel") == "canonical" and values["href"] == "https://demos.intentsolutions.io/":
                self.has_canonical = True
            if values.get("rel") == "stylesheet":
                self.assets.append(values["href"])

    def handle_data(self, data: str) -> None:
        if "Intent Demos | Working systems with receipts" in data:
            self.has_title = True


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def route_target(href: str) -> Path:
    parsed = urlparse(href)
    path = parsed.path.lstrip("/")
    target = DEPLOY_ROOT / path
    if href.endswith("/"):
        target /= "index.html"
    return target


def main() -> int:
    failures: list[str] = []
    html_path = SITE_ROOT / "index.html"
    html = html_path.read_text(encoding="utf-8")
    parser = CatalogParser()
    parser.feed(html)

    require(parser.has_title, "expected page title is missing", failures)
    require(parser.has_canonical, "canonical URL is missing or incorrect", failures)
    require(parser.catalog_items == 19, f"expected 19 catalog routes, found {parser.catalog_items}", failures)
    require("n8n" not in html.lower(), "n8n appears in the catalog source", failures)
    require("Why these 19 are here" in html, "catalog selection rubric is missing", failures)
    searchcarriers = (SITE_ROOT / "searchcarriers" / "index.html").read_text(encoding="utf-8")
    require(
        searchcarriers.count('class="sc-skill"') == 26,
        "SearchCarriers page must list all 26 packages",
        failures,
    )
    require(
        "Grok Build, Claude Code, and other MCP clients" in searchcarriers,
        "SearchCarriers page must state the tested multi-model boundary",
        failures,
    )
    require(
        "hosted Grok Bot needs an authenticated Streamable HTTP deployment" in searchcarriers,
        "SearchCarriers page must state the hosted Grok Bot transport boundary",
        failures,
    )
    require(
        "Capability brief, not a customer success story" in searchcarriers,
        "SearchCarriers capability boundary is missing",
        failures,
    )
    require(
        "https://github.com/jeremylongshore/searchcarriers-tools" in searchcarriers,
        "SearchCarriers public source link is missing",
        failures,
    )
    require(
        'href="https://searchcarriers.com/lander"' in searchcarriers,
        "SearchCarriers product link is missing",
        failures,
    )
    require(
        'href="https://searchcarriers.com/docs/api"' in searchcarriers,
        "SearchCarriers API documentation link is missing",
        failures,
    )
    evidence = json.loads((SITE_ROOT / "assets" / "project-evidence.json").read_text())
    require(len(evidence["personal"]) == 5, "expected five ranked personal source projects", failures)
    require(len(evidence["organization"]) == 6, "expected six organization source projects", failures)
    require(evidence["observed_on"] == "2026-09-17", "source snapshot date changed without review", failures)
    for project in evidence["personal"] + evidence["organization"]:
        require(project["html_url"] in parser.hrefs, f"missing source project: {project['name']}", failures)
    for project in evidence["personal"]:
        require(f'{project["stargazers_count"]:,} stars' in html, f"star count drift: {project['name']}", failures)
    require("Stars show public interest, not customers" in html, "metric limitations missing", failures)

    required_links = {
        "https://tonsofskills.com/",
        "https://github.com/jeremylongshore/tons-of-skills-marketplace",
        "https://skills.sh/b/jeremylongshore/tons-of-skills-marketplace",
        "https://labs.intentsolutions.io/",
        "https://evals.intentsolutions.io/",
        "https://learn.intentsolutions.io/",
        "https://oma.intentsolutions.io/",
    }
    missing_links = sorted(required_links.difference(parser.hrefs))
    require(not missing_links, f"required proof/network links missing: {missing_links}", failures)

    # The top network strip is vendored from intent-solutions-landing/estate-bar.
    # The canonical checker verifies the vendored files against their manifest and
    # that the page carries exactly the canonical demos bar: labels, order, hrefs.
    vendor = SITE_ROOT / "assets" / "estate-bar"
    bar_check = subprocess.run(
        [sys.executable, str(vendor / "check_estate_bar.py"), "--site", "demos",
         "--vendor", str(vendor), str(SITE_ROOT / "index.html")],
        capture_output=True, text=True, check=False,
    )
    require(bar_check.returncode == 0, f"estate bar drift: {bar_check.stderr.strip()}", failures)
    require("/assets/estate-bar/estate-bar.css" in html, "estate bar stylesheet is not linked", failures)
    require("/assets/estate-accent.css" in html, "estate bar accent stylesheet is not linked", failures)

    local_demo_hrefs = sorted(
        href for href in set(parser.hrefs)
        if href.startswith("/") and not href.startswith("/assets/") and href != "/"
    )
    # The demo folders are served from the deploy root and are not in this repo,
    # so CI cannot see them. Say so rather than pass silently or fail falsely.
    deployed_routes_checked = DEPLOY_ROOT.is_dir()
    if deployed_routes_checked:
        for href in local_demo_hrefs:
            require(route_target(href).is_file(), f"deployed route target missing for {href}", failures)

    for asset in sorted(set(parser.assets)):
        if asset.startswith("/"):
            require((SITE_ROOT / asset.lstrip("/")).is_file(), f"local asset missing: {asset}", failures)

    screens = sorted((SITE_ROOT / "assets" / "screens").glob("*.webp"))
    require(len(screens) == 8, f"expected 8 live screenshots, found {len(screens)}", failures)
    for screen in screens:
        require(screen.with_suffix(screen.suffix + ".json").is_file(), f"provenance sidecar missing: {screen.name}", failures)

    sitemap_path = SITE_ROOT / "sitemap.xml"
    root = ET.parse(sitemap_path).getroot()
    sitemap_urls = {node.text for node in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    require("https://demos.intentsolutions.io/" in sitemap_urls, "root URL missing from sitemap", failures)
    for href in local_demo_hrefs:
        expected = f"https://demos.intentsolutions.io{href}"
        require(expected in sitemap_urls, f"catalog route missing from sitemap: {href}", failures)

    robots = (SITE_ROOT / "robots.txt").read_text(encoding="utf-8")
    require("https://demos.intentsolutions.io/sitemap.xml" in robots, "robots.txt does not advertise sitemap", failures)

    if failures:
        print("Intent Demos verification failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Verified: {parser.catalog_items} catalog routes, {len(screens)} screenshots, {len(sitemap_urls)} sitemap URLs.")
    if not deployed_routes_checked:
        print(f"NOTE: deploy root {DEPLOY_ROOT} is absent; deployed route targets were NOT checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
