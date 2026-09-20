#!/usr/bin/env bash
# Vendor the canonical Intent Solutions estate bar into site/assets/estate-bar/.
#
# The bar's single source is intent-solutions-landing/estate-bar/. This copies it
# at a pinned commit and verifies every file against the canonical manifest, so a
# vendored copy can never silently differ. Never hand-edit the vendored files;
# scripts/verify_site.py fails if they stop matching the manifest.
#
#   scripts/sync_estate_bar.sh                 # latest main
#   scripts/sync_estate_bar.sh <commit-sha>    # a specific commit
set -euo pipefail
repo="jeremylongshore/intent-solutions-landing"
ref="${1:-main}"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="$repo_root/site/assets/estate-bar"

sha="$(curl -fsSL "https://api.github.com/repos/$repo/commits/$ref" | python3 -c 'import json,sys; print(json.load(sys.stdin)["sha"])')"
base="https://raw.githubusercontent.com/$repo/$sha/estate-bar"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT

curl -fsSL "$base/manifest.sha256" -o "$tmp/manifest.sha256"
while read -r _digest rel; do
  mkdir -p "$tmp/$(dirname "$rel")"
  curl -fsSL "$base/$rel" -o "$tmp/$rel"
done < "$tmp/manifest.sha256"
for extra in check_estate_bar.py fonts/OFL.txt; do
  mkdir -p "$tmp/$(dirname "$extra")"
  curl -fsSL "$base/$extra" -o "$tmp/$extra"
done
(cd "$tmp" && sha256sum --check --quiet manifest.sha256)

rm -rf "$dest"; mkdir -p "$dest"
cp -a "$tmp/." "$dest/"
printf 'source: https://github.com/%s/tree/%s/estate-bar\ncommit: %s\n' "$repo" "$sha" "$sha" > "$dest/SOURCE"
echo "estate bar vendored from $repo@$sha into site/assets/estate-bar/"
