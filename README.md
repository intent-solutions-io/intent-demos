# Intent Demos

<!-- intent-select-partner:start -->
<p><a href="https://intentsolutions.io/"><img src="assets/brand/claude-select-partner.svg" alt="Intent Solutions: Claude Partner Network Select Services Partner" width="300" height="95" /></a></p>

Intent Solutions is a Claude Partner Network Select Services Partner.
<!-- intent-select-partner:end -->


Source for the catalog at [demos.intentsolutions.io](https://demos.intentsolutions.io/). The site is a proof-first directory of working Intent Solutions systems, public source, and independently verifiable adoption signals.

## Development

```bash
python -m http.server 4183 --directory site
```

Open `http://127.0.0.1:4183`. The production catalog is static; no build step is required.

## Verification

```bash
python scripts/verify_site.py
python scripts/browser_smoke.py
```

The static verifier checks route targets, evidence links, sitemap coverage, screenshots, and document contracts. The browser smoke test exercises filtering and responsive layouts against the local server.

## Catalog Selection

An entry must have a working public route, an inspectable artifact or evidence trail, and a distinct role in the current portfolio. Public adoption—such as installs, stars, forks, or accepted upstream work—determines which work receives prominent placement; it is not required for basic catalog inclusion. Drafts must be labeled, and retired template collections stay out.

## Deployment

`scripts/deploy_local.sh` copies the versioned catalog files, SearchCarriers page and fictional Prospect Prep demonstration into `/home/jeremy/demos`. It preserves independently managed demo directories.

## Fictional Prospect Prep demonstration

The public route is `/prospect-prep-automation/`. Its HTML and PDF are owned here under
`site/prospect-prep-automation/`; private engagement documents are not publication sources.
All people, team relationships, territory labels and example market figures are fictional or illustrative.
The account checklist source is `docs/prospect-prep-account-setup.md`.
Render it through the canonical whiteglove pipeline using the included public-demo theme:

```bash
PROSPECT_PDF_BUILD_DIR=$(mktemp -d)
WHITEGLOVE_THEMES_DIR="$PWD/docs" bash "$HOME/.claude/skills/whiteglove-pdf/scripts/render.sh" \
  --input docs/prospect-prep-account-setup.md \
  --out "$PROSPECT_PDF_BUILD_DIR/account-setup.pdf" --template public-demo
# Complete the review below before copying only the PDF into the public tree.
cp -f "$PROSPECT_PDF_BUILD_DIR/account-setup.pdf" site/prospect-prep-automation/account-setup.pdf
```

Review PDF text, metadata, links, attachments and every page before publishing.
Keep renderer receipts outside the public tree; they contain local paths and are not public artifacts.
Keep real credentials, personal contact details and private engagement identifiers out of these files.
Legacy bookmarks are handled by bounded redirects in the host's existing Caddy configuration;
their private backup and verification receipts stay outside the served tree and Git.

## Mission Control public feed

The catalog repository also owns the public Mission Control projection under
`site/mission-control/` and its installed publisher. This is a deliberately bounded
exception to the independently managed demo directories. See
[the publishing and recovery runbook](scripts/mission-control-runbook.md).

```bash
python -m unittest discover -s scripts -p 'test_mission_control.py' -v
```

Browser smoke checks need a generated Mission Control snapshot rather than the unexpanded
source template. Serve a preview assembled with `mission_control.build_release`, or set
`DEMOS_BASE_URL=https://demos.intentsolutions.io` for the deployed-site verification.
