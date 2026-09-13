#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_root="$repo_root/site"
deploy_root="/home/jeremy/demos"

mkdir -p "$deploy_root/assets/screens"
cp -f "$site_root/index.html" "$deploy_root/index.html"
cp -f "$site_root/robots.txt" "$deploy_root/robots.txt"
cp -f "$site_root/sitemap.xml" "$deploy_root/sitemap.xml"
cp -f "$site_root/assets/styles.css" "$deploy_root/assets/styles.css"
cp -f "$site_root/assets/app.js" "$deploy_root/assets/app.js"
cp -f "$site_root/assets/favicon.svg" "$deploy_root/assets/favicon.svg"
cp -f "$site_root"/assets/screens/*.webp "$deploy_root/assets/screens/"
cp -f "$site_root"/assets/screens/*.webp.json "$deploy_root/assets/screens/"

echo "Deployed catalog shell to $deploy_root without modifying demo subdirectories."
