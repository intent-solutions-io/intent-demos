#!/usr/bin/env python3
"""Browser-level smoke test for layout, catalog interaction, and screenshots."""

from __future__ import annotations

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

    assert page.locator(".catalog-item").count() == 18
    assert page.locator(".catalog-item:visible").count() == 18
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
    assert page.locator(".catalog-item:visible").count() == 6
    assert page.locator("#filter-status").text_content() == "Showing 6 routes in system work."

    page.locator("#catalog-search").fill("CAD")
    assert page.locator(".catalog-item:visible").count() == 1
    assert page.get_by_role("heading", name="CAD AI Agent").is_visible()

    page.get_by_role("button", name="Show all work").click() if page.locator("#empty-state:visible").count() else None
    page.locator("#catalog-search").fill("")
    page.get_by_role("button", name="All work").click()
    assert page.locator(".catalog-item:visible").count() == 18

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
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=BROWSER_EXECUTABLE)
        desktop = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        inspect_page(desktop, REVIEW_DIR / "desktop.png")
        desktop.close()

        tablet_context = browser.new_context(
            viewport={"width": 1194, "height": 834},
            device_scale_factor=1,
            has_touch=True,
        )
        tablet = tablet_context.new_page()
        inspect_page(tablet, REVIEW_DIR / "tablet-touch.png")
        tablet_context.close()

        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
        inspect_page(mobile, REVIEW_DIR / "mobile.png")
        mobile.close()
        browser.close()

    print(f"Browser smoke passed at desktop, touch tablet, and mobile; screenshots: {REVIEW_DIR}")


if __name__ == "__main__":
    main()
