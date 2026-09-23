#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_root="$repo_root/site"
deploy_root="/home/jeremy/demos"

mkdir -p "$deploy_root/assets/screens"
mkdir -p "$deploy_root/searchcarriers"
cp -f "$site_root/index.html" "$deploy_root/index.html"
cp -f "$site_root/robots.txt" "$deploy_root/robots.txt"
cp -f "$site_root/sitemap.xml" "$deploy_root/sitemap.xml"
cp -f "$site_root/assets/styles.css" "$deploy_root/assets/styles.css"
cp -f "$site_root/assets/app.js" "$deploy_root/assets/app.js"
cp -f "$site_root/assets/project-evidence.json" "$deploy_root/assets/project-evidence.json"
cp -f "$site_root/assets/favicon.svg" "$deploy_root/assets/favicon.svg"
# The vendored estate bar: replace the whole folder so a removed file cannot linger.
rm -rf "$deploy_root/assets/estate-bar"
cp -a "$site_root/assets/estate-bar" "$deploy_root/assets/estate-bar"
cp -f "$site_root/assets/estate-accent.css" "$deploy_root/assets/estate-accent.css"
cp -f "$site_root/searchcarriers/index.html" "$deploy_root/searchcarriers/index.html"
cp -f "$site_root/searchcarriers/styles.css" "$deploy_root/searchcarriers/styles.css"
cp -f "$site_root/searchcarriers/app.js" "$deploy_root/searchcarriers/app.js"
cp -f "$site_root"/assets/screens/*.webp "$deploy_root/assets/screens/"
cp -f "$site_root"/assets/screens/*.webp.json "$deploy_root/assets/screens/"

echo "Deployed catalog shell and the repository-owned SearchCarriers route to $deploy_root."
