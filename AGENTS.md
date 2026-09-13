# Repository Guidelines

## Project Structure & Module Organization

`site/` is the deployable static catalog. The page shell lives in `site/index.html`; reusable styles and browser behavior belong in `site/assets/`. Live-site captures and their provenance sidecars live in `site/assets/screens/`. `scripts/` contains verification and the bounded local deployment command. Product and Impeccable context live in `PRODUCT.md`, `DESIGN.md`, and `.impeccable/`.

## Build, Test, and Development Commands

- `python -m http.server 4183 --directory site` serves the catalog locally.
- `python scripts/verify_site.py` checks routes, assets, screenshots, sitemap entries, and required proof links.
- `python scripts/browser_smoke.py` exercises filters and responsive layouts in Chromium and writes ignored review captures.
- `scripts/deploy_local.sh` copies only the catalog shell into `/home/jeremy/demos`; it preserves every demo subdirectory.

## Coding Style & Naming Conventions

Use two-space indentation in HTML, CSS, and JavaScript. Prefer semantic HTML, focused data attributes, kebab-case CSS classes, and plain browser APIs. Keep the squared, proof-led visual language documented in `DESIGN.md`. Metrics require a source link and an `as of` date. Never infer a customer, employer, or partner relationship from an open-source contribution.

## Testing Guidelines

Run both verification scripts for any catalog or interaction change. The browser smoke test must pass at 1440px and 390px without console errors or horizontal overflow. Keep catalog counts and sitemap routes synchronized. Name future Python tests `test_*.py`.

## Commit & Pull Request Guidelines

Use conventional commits such as `feat: add proof source` or `fix: restore mobile filter`. Work on a feature branch. Pull requests should explain the visitor-facing change, list verification commands, and include desktop/mobile captures for visual changes. Push and verify the repository plus live URL before closing the Beads issue.
