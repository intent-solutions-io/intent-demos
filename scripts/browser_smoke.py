#!/usr/bin/env python3
"""Browser-level smoke test for layout, catalog interaction, and screenshots."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = os.environ.get("DEMOS_BASE_URL", "http://127.0.0.1:4183")
BROWSER_EXECUTABLE = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE", "/snap/bin/chromium")
REVIEW_DIR = Path(__file__).resolve().parents[1] / ".impeccable" / "review"


def inspect_page(page, screenshot: Path) -> None:
    errors: list[str] = []
    page.on("console", lambda message: errors.append(f"console:{message.type}:{message.text}") if message.type == "error" else None)
    page.on("pageerror", lambda error: errors.append(f"page:{error}"))
    page.goto(BASE_URL, wait_until="networkidle")
    page.locator("#hero-title").wait_for(state="visible")

    assert page.locator(".catalog-item").count() == 19
    assert page.locator(".catalog-item:visible").count() == 19
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    assert page.locator('a[href="https://labs.intentsolutions.io/"]').count() >= 1
    assert page.locator('a[href="https://evals.intentsolutions.io/"]').count() >= 1

    previews = page.locator(".feature-screen img, .panel-screen img, .sibling-screen img, .product-grid img")
    assert previews.count() == 8
    for index in range(previews.count()):
        image = previews.nth(index)
        geometry = image.evaluate(
            """element => ({
                rendered: element.getBoundingClientRect().width / element.getBoundingClientRect().height,
                natural: element.naturalWidth / element.naturalHeight,
                fit: getComputedStyle(element).objectFit,
            })"""
        )
        assert abs(geometry["rendered"] - geometry["natural"]) < 0.02, geometry
        assert geometry["fit"] == "contain", geometry

    preview_links = page.locator(".feature-screen, .panel-screen, .sibling-screen, .product-grid > a")
    for index in range(preview_links.count()):
        link = preview_links.nth(index)
        assert link.get_attribute("target") == "_blank"
        assert link.evaluate("element => getComputedStyle(element).touchAction") == "pan-y"

    page.get_by_role("button", name="Systems").click()
    assert page.locator(".catalog-item:visible").count() == 7
    assert page.locator("#filter-status").text_content() == "Showing 7 routes in system work."

    page.locator("#catalog-search").fill("CAD")
    assert page.locator(".catalog-item:visible").count() == 1
    assert page.get_by_role("heading", name="CAD AI Agent").is_visible()

    page.get_by_role("button", name="Show all work").click() if page.locator("#empty-state:visible").count() else None
    page.locator("#catalog-search").fill("")
    page.get_by_role("button", name="All work").click()
    assert page.locator(".catalog-item:visible").count() == 19

    page.goto(f"{BASE_URL}/searchcarriers/", wait_until="networkidle")
    assert page.get_by_role("heading", name="Carrier research that ends in an auditable next action.").is_visible()
    assert page.locator(".sc-skill").count() == 26
    assert page.locator(".sc-skill:visible").count() == 26
    page.get_by_role("button", name="MCP plugins").click()
    assert page.locator(".sc-skill:visible").count() == 5
    assert page.locator("#skill-count").text_content() == "5"
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")

    page.goto(f"{BASE_URL}/#catalog", wait_until="networkidle")
    page.wait_for_function(
        "document.querySelector('#catalog').getBoundingClientRect().top >= document.querySelector('.site-header').getBoundingClientRect().bottom"
    )
    catalog_top = page.locator("#catalog").evaluate("element => element.getBoundingClientRect().top")
    header_bottom = page.locator(".site-header").evaluate("element => element.getBoundingClientRect().bottom")
    assert catalog_top >= header_bottom, {"catalog_top": catalog_top, "header_bottom": header_bottom}

    page.locator("body").press("Tab")
    assert page.evaluate("document.activeElement !== document.body")
    assert not errors, errors
    page.screenshot(path=str(screenshot), full_page=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--mission-control-only", action="store_true", help="Check the independently published Mission Control surface")
    scope.add_argument("--catalog-only", action="store_true", help="Check the catalog and repository-owned demo routes without Mission Control")
    args = parser.parse_args()
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=BROWSER_EXECUTABLE)
        desktop = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        if not args.mission_control_only:
            inspect_page(desktop, REVIEW_DIR / "desktop.png")
        if not args.catalog_only:
            inspect_mission_control(desktop, REVIEW_DIR / "mission-control-desktop.png")
        desktop.close()

        tablet_context = browser.new_context(
            viewport={"width": 1194, "height": 834},
            device_scale_factor=1,
            has_touch=True,
        )
        tablet = tablet_context.new_page()
        if not args.mission_control_only:
            inspect_page(tablet, REVIEW_DIR / "tablet-touch.png")
        if not args.catalog_only:
            inspect_mission_control(tablet, REVIEW_DIR / "mission-control-tablet.png")
        tablet_context.close()

        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        if not args.mission_control_only:
            inspect_page(mobile, REVIEW_DIR / "mobile.png")
        if not args.catalog_only:
            inspect_mission_control(mobile, REVIEW_DIR / "mission-control-mobile.png")
        mobile.close()
        browser.close()

    checked = "Mission Control" if args.mission_control_only else "catalog routes"
    print(f"Browser smoke passed for {checked} at desktop, touch tablet, and mobile; screenshots: {REVIEW_DIR}")


def inspect_mission_control(page, screenshot: Path) -> None:
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(f"{BASE_URL}/mission-control/", wait_until="networkidle")
    assert page.get_by_role("heading", name="Source inventory").is_visible()
    assert page.get_by_role("heading", name="Historical reports · July 11, 2026").is_visible()
    assert page.locator(".freshness").get_attribute("data-state") == "fresh"
    assert page.locator("#digest").input_value().startswith("# Mission Control — current public snapshot")
    assert page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")
    page.screenshot(path=str(screenshot), full_page=True)
    # A normal newer publication must refresh the open page and copied report.
    candidate = page.evaluate("JSON.parse(JSON.stringify(snapshot))")
    old = candidate["published_at"]
    new = (dt.datetime.fromisoformat(old.replace("Z", "+00:00")) + dt.timedelta(seconds=1)).isoformat(timespec="seconds").replace("+00:00", "Z")
    body = page.content().replace(old, new)
    candidate = json.loads(json.dumps(candidate).replace(old, new))
    page.route("**/mission-control/manifest.json", lambda route: route.fulfill(json=candidate))
    page.route("**/mission-control/", lambda route: route.fulfill(body=body, content_type="text/html"))
    # Invalid newer data must not poison the corrected publication's reload guard.
    for field, value in [("revision", None), ("revision", [candidate["source"]["revision"]]), ("observed_at", None),
                         ("observed_at", "2026-02-30T12:00:00Z"),
                         ("observed_at", "2099-01-01T00:00:00Z")]:
        invalid = json.loads(json.dumps(candidate))
        invalid["source"][field] = value
        page.unroute("**/mission-control/manifest.json")
        page.route("**/mission-control/manifest.json", lambda route, request, data=invalid: route.fulfill(json=data))
        page.evaluate("loadFreshness()")
        assert page.evaluate("sessionStorage.getItem('intent-mc-reload-publication')") is None
        assert page.locator("#published").text_content() == old
        assert page.locator(".freshness").get_attribute("data-state") == "stale"
    assert page.evaluate("Number.isNaN(parseClock('2026-02-30T12:00:00Z'))")
    assert page.evaluate("Number.isNaN(parseClock('2026-09-31T12:00:00Z'))")
    assert page.evaluate("Number.isNaN(parseClock('2026-09-17T24:00:00Z'))")
    assert page.evaluate("Number.isFinite(parseClock('2024-02-29T12:00:00+02:00'))")
    page.unroute("**/mission-control/manifest.json")
    page.route("**/mission-control/manifest.json", lambda route: route.fulfill(json=candidate))
    with page.expect_navigation(wait_until="networkidle"):
        page.evaluate("setTimeout(loadFreshness, 0)")
    assert page.locator("#published").text_content() == new
    assert new in page.locator("#digest").input_value()
    assert page.locator(".freshness").get_attribute("data-state") == "fresh"
    # A recent older manifest must not navigate to or relabel an old publication.
    navigations = []
    def record_navigation(frame):
        if frame == page.main_frame:
            navigations.append(frame.url)
    page.on("framenavigated", record_navigation)
    older = json.loads(json.dumps(candidate).replace(new, old))
    page.unroute("**/mission-control/manifest.json")
    page.route("**/mission-control/manifest.json", lambda route: route.fulfill(json=older))
    page.evaluate("loadFreshness()")
    assert not navigations
    assert page.locator("#published").text_content() == new
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    # A server/cache that retains old HTML gets only one reload per candidate.
    later = (dt.datetime.fromisoformat(new.replace("Z", "+00:00")) + dt.timedelta(seconds=1)).isoformat(timespec="seconds").replace("+00:00", "Z")
    repeated = json.loads(json.dumps(candidate).replace(new, later))
    page.unroute("**/mission-control/manifest.json")
    page.unroute("**/mission-control/")
    page.route("**/mission-control/manifest.json", lambda route: route.fulfill(json=repeated))
    page.route("**/mission-control/", lambda route: route.fulfill(body=body.replace(new, old), content_type="text/html"))
    with page.expect_navigation(wait_until="networkidle"):
        page.evaluate("setTimeout(loadFreshness, 0)")
    assert len(navigations) == 1
    assert page.locator("#published").text_content() == old
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    page.evaluate("loadFreshness()")
    assert len(navigations) == 1
    # Alternating older/newer caches cannot reset the attempted-publication guard.
    page.unroute("**/mission-control/manifest.json")
    page.route("**/mission-control/manifest.json", lambda route: route.fulfill(json=candidate))
    page.evaluate("loadFreshness()")
    assert len(navigations) == 1
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    page.unroute("**/mission-control/manifest.json")
    page.route("**/mission-control/manifest.json", lambda route: route.fulfill(json=repeated))
    page.evaluate("loadFreshness()")
    assert len(navigations) == 1
    page.remove_listener("framenavigated", record_navigation)
    page.unroute("**/mission-control/manifest.json")
    page.unroute("**/mission-control/")
    page.evaluate("sessionStorage.removeItem('intent-mc-reload-publication')")
    page.reload(wait_until="networkidle")
    # Regression: an HTTP200 snapshot from July must become visibly stale.
    page.evaluate("snapshot.published_at = '2026-07-11T15:49:17Z'; updateFreshness()")
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    assert "Stale" in page.locator("#freshness-label").text_content()
    page.reload(wait_until="networkidle")
    page.evaluate("snapshot.source.observed_at = new Date().toISOString().replace('Z', ''); updateFreshness()")
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    page.reload(wait_until="networkidle")
    page.evaluate("snapshot.source.revision = null; updateFreshness()")
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    page.evaluate("snapshot = null; updateFreshness()")
    assert page.locator(".freshness").get_attribute("data-state") == "stale"
    assert not errors, errors


if __name__ == "__main__":
    main()
