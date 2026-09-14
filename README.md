# Intent Demos

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

`scripts/deploy_local.sh` copies only the versioned catalog files into `/home/jeremy/demos`. It deliberately does not delete or replace the independently managed demo directories already served there.
