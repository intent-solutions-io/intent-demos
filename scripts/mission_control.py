#!/usr/bin/env python3
"""Publish a bounded public projection; never publish private document text."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import fcntl
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REMOTE = "https://github.com/intent-solutions-io/intent-os.git"
BASE = "https://demos.intentsolutions.io/mission-control/"
MAX_AGE = 45 * 60
# Reviewed, public-safe names. Presence means source implementation, NOT deployment.
COMPONENTS = {
    "Repository discovery": "ops/github-repo-collector/refresh.sh",
    "Work reconciliation": "ops/work-sync-reconciler/reconcile.py",
    "Deployment safety": "ops/deploy/deploy-wrapper.sh",
    "Service health projection": "ops/health-projection/collect.py",
    "Capability matrix": "ops/capability-matrix/compose.py",
    "Founder view": "ops/founder-view/compose.py",
    "Operator view": "ops/operator-view/compose.py",
    "Project owner view": "ops/owner-view/compose.py",
    "Agent activity view": "ops/agent-activity-view/compose.py",
}
SERVICES = {
    "Tons of Skills": ("https://tonsofskills.com/healthz", "tonsofskills.com"),
    "Scorecard Echo": ("https://scorecardecho.com/api/health", None),
    "Intent Demos": ("https://demos.intentsolutions.io/", None),
}


def stamp(now: dt.datetime) -> str:
    return now.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def instant(value: str) -> dt.datetime:
    result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return result.astimezone(dt.timezone.utc)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], timeout=60, stderr=subprocess.DEVNULL,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}, text=True,
    ).strip()


def source_snapshot(repo: Path, now: dt.datetime, previous: dict, fetch: bool = True) -> dict:
    try:
        if fetch:
            if not repo.exists():
                repo.mkdir(parents=True, mode=0o700)
                git(repo, "init", "--bare")
                git(repo, "remote", "add", "origin", SOURCE_REMOTE)
            if git(repo, "remote", "get-url", "origin") != SOURCE_REMOTE:
                raise ValueError("unexpected source remote")
            git(repo, "fetch", "--depth=1", "origin", "main")
        revision = git(repo, "rev-parse", "FETCH_HEAD" if fetch else "HEAD")
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("invalid source revision")
        components = []
        for name, path in COMPONENTS.items():
            try:
                git(repo, "cat-file", "-e", f"{revision}:{path}")
                state = "present"
            except subprocess.CalledProcessError:
                state = "absent"
            components.append({"name": name, "state": state})
        return {"revision": revision, "observed_at": stamp(now), "fetch_status": "ok",
                "commit_at": stamp(instant(git(repo, "show", "-s", "--format=%cI", revision))),
                "components": components}
    except (subprocess.SubprocessError, ValueError, OSError):
        # Preserve the LAST GOOD observation clock; a failed fetch never renews it.
        prior = previous.get("source", {}) if isinstance(previous, dict) else {}
        if not isinstance(prior, dict):
            prior = {}
        revision = prior.get("revision")
        if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
            revision = None
        clocks = {}
        for key in ("observed_at", "commit_at"):
            try:
                clocks[key] = stamp(instant(prior[key])) if isinstance(prior.get(key), str) else None
            except ValueError:
                clocks[key] = None
        rows = prior.get("components")
        states = {row["name"]: row.get("state") for row in rows
                  if isinstance(row, dict) and isinstance(row.get("name"), str)} if isinstance(rows, list) else {}
        components = [{"name": name, "state": states[name]} for name in COMPONENTS
                      if states.get(name) in ("present", "absent")]
        return {"revision": revision, **clocks, "fetch_status": "unavailable", "components": components}


def probe(name: str, url: str, expected_service: str | None, now: dt.datetime) -> dict:
    result = {"name": name, "url": url, "observed_at": stamp(now), "state": "unavailable"}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Intent-Mission-Control/1.0", "Cache-Control": "no-cache"})
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read(512 * 1024)
            result["http_status"] = response.status
            if response.status != 200:
                return result
            if expected_service:
                data = json.loads(body)
                if not isinstance(data, dict) or data.get("ok") is not True or data.get("service") != expected_service:
                    return result
            elif name == "Scorecard Echo":
                # This card is explicitly HTTP/API reachability, not game-data freshness.
                data = json.loads(body)
                if not isinstance(data, dict) or data.get("status") not in ("healthy", "ok"):
                    return result
            elif b"Intent Demos" not in body:
                return result
            result["state"] = "reachable"
    except urllib.error.HTTPError as error:
        result["http_status"] = error.code
    except (OSError, ValueError) as error:
        result["error_category"] = "network" if isinstance(error, OSError) else "invalid_response"
    return result


def freshness_errors(data: dict, now: dt.datetime) -> list[str]:
    if not isinstance(data, dict):
        return ["snapshot is not an object"]
    errors = []
    if data.get("schema_version") != 1:
        errors.append("unsupported snapshot")
    source = data.get("source", {})
    if not isinstance(source, dict):
        return ["source is not an object"]
    if source.get("fetch_status") != "ok":
        errors.append("source fetch unavailable")
    revision = source.get("revision")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        errors.append("source revision missing")
    for label, value in [("publication", data.get("published_at")), ("source", source.get("observed_at"))]:
        try:
            age = (now - instant(value)).total_seconds()
            if age > MAX_AGE or age < -120:
                errors.append(f"{label} timestamp stale or invalid")
        except (ValueError, TypeError, AttributeError):
            errors.append(f"{label} timestamp missing or invalid")
    return errors


def current_report(data: dict) -> str:
    source = data["source"]
    lines = ["# Mission Control — current public snapshot", "",
             f"Published (UTC): {data['published_at']}",
             f"Source last successfully checked (UTC): {source['observed_at'] or 'unknown'}",
             f"Source revision: {source['revision'] or 'unknown'}",
             f"Source fetch: {source['fetch_status']}", "",
             "## Program state", "",
             "Implementation is under way. The July 11 design-only / 0%-built report is historical.",
             "This is a public, read-only source inventory and website reachability feed. It is not the private operations console.",
             "Presence in source does not certify deployment, complete phase acceptance, or live service health.", "",
             "## Reviewed source inventory", "", "| Component | Source implementation |", "|---|---|"]
    for component in source["components"]:
        lines.append(f"| {component['name']} | {component['state']} |")
    lines += ["", "## Public website checks", "",
              "These checks verify endpoint reachability and basic response shape from one monitoring location. They do not certify worldwide access, baseball-data freshness, or internal dependencies.", "",
              "| Website | Result | Checked (UTC) |", "|---|---|---|"]
    for service in data["services"]:
        lines.append(f"| {service['name']} | {service['state']} | {service['observed_at']} |")
    lines += ["", "## Historical reports", "",
              "July 11 reports below preserve the decisions and state as recorded then. They are not current implementation claims.", ""]
    for report in data["reports"]:
        lines.append(f"- [{report}]({BASE}reports/{report})")
    return "\n".join(lines) + "\n"


def build_release(destination: Path, data: dict) -> None:
    template_root = ROOT / "site" / "mission-control"
    shutil.copytree(template_root, destination, dirs_exist_ok=True)
    data["reports"] = sorted(p.name for p in (destination / "reports").glob("*.md"))
    digest = current_report(data)
    (destination / "current.md").write_text(digest)
    for name in ("feed.md", "all-reports.md"):
        contents = digest
        if name == "all-reports.md":
            for report in data["reports"]:
                contents += "\n---\n\nHistorical report: " + report + "\n\n" + (destination / "reports" / report).read_text()
        (destination / name).write_text(contents)
    (destination / "llms.txt").write_text(f"# Mission Control\n\nCurrent snapshot: {BASE}current.md\nMachine timestamps: {BASE}manifest.json\nArchive: {BASE}all-reports.md (historical reports are labeled)\n")
    (destination / "manifest.json").write_text(json.dumps(data, indent=2) + "\n")
    page = (destination / "index.html").read_text()
    values = {"PUBLISHED": data["published_at"], "SOURCE_CHECKED": data["source"]["observed_at"] or "unknown",
              "SOURCE_REVISION": data["source"]["revision"] or "unknown", "SOURCE_FETCH": data["source"]["fetch_status"],
              "DIGEST": digest,
              "COMPONENT_ROWS": "".join(f"<tr><td>{html.escape(c['name'])}</td><td>{html.escape(c['state'])} in source</td></tr>" for c in data["source"]["components"]),
              "SERVICE_ROWS": "".join(f"<tr><td><a href='{html.escape(s['url'], quote=True)}'>{html.escape(s['name'])}</a></td><td>{s['state']}</td><td>{s['observed_at']}</td></tr>" for s in data["services"]),
              "ARCHIVE_LINKS": "".join(f"<li><a href='reports/{html.escape(p, quote=True)}'>{html.escape(p.removesuffix('.md'))}</a></li>" for p in data["reports"])}
    for key, value in values.items():
        page = page.replace("{{" + key + "}}", value if key.endswith(("ROWS", "LINKS")) else html.escape(value))
    if re.search(r"\{\{[A-Z_]+\}\}", page):
        raise ValueError("unexpanded template")
    (destination / "index.html").write_text(page)


def publish(deploy: Path, state: Path, source_repo: Path, *, fetch: bool = True) -> dict:
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    state.chmod(0o700)
    with (state / "publish.lock").open("w") as lock:
        # Kernel-owned lease automatically releases after crashes; duplicate triggers wait.
        fcntl.flock(lock, fcntl.LOCK_EX)
        now = dt.datetime.now(dt.timezone.utc)
        previous = {}
        if deploy.is_symlink() and (deploy / "manifest.json").exists():
            try:
                previous = json.loads((deploy / "manifest.json").read_text())
            except (ValueError, OSError):
                # A corrupt prior cache cannot turn a new source observation green.
                previous = {}
        source = source_snapshot(source_repo, now, previous, fetch)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(probe, name, url, expected, now) for name, (url, expected) in SERVICES.items()]
            services = [future.result() for future in futures]
        revision_file = ROOT / ".publisher-revision"
        publisher_revision = revision_file.read_text().strip() if revision_file.exists() else git(ROOT, "rev-parse", "HEAD")
        if not re.fullmatch(r"[0-9a-f]{40}", publisher_revision):
            raise ValueError("publisher revision invalid")
        data = {"schema_version": 1, "published_at": stamp(now), "source": source,
                "publisher_revision": publisher_revision, "max_age_seconds": MAX_AGE,
                "services": services, "reports": []}
        # Public artifacts stay under the existing Caddy-readable tree. Private
        # state, Git credentials, source checkout and legacy tools stay outside it.
        releases = deploy.parent / ".mission-control-releases"
        releases.mkdir(parents=True, exist_ok=True)
        release = Path(tempfile.mkdtemp(prefix="snapshot-", dir=releases))
        try:
            build_release(release, data)
            release.chmod(0o755)
            # Validate the entire candidate before changing what Caddy serves.
            if json.loads((release / "manifest.json").read_text()) != data:
                raise ValueError("candidate verification failed")
        except (ValueError, OSError, TypeError, KeyError):
            shutil.rmtree(release)
            raise
        deploy.parent.mkdir(parents=True, exist_ok=True)
        pending = deploy.parent / ("." + deploy.name + ".next")
        if pending.is_symlink() and pending.resolve().parent == releases.resolve():
            pending.unlink()  # Our own interrupted candidate; the old served snapshot survives.
        elif pending.exists() or pending.is_symlink():
            raise ValueError("unexpected pending deployment; preserve and investigate")
        pending.symlink_to(release)
        if deploy.exists() and not deploy.is_symlink():
            # One-time migration; retain the original unmanaged directory privately.
            backup = state / "legacy-feed"
            if backup.exists():
                pending.unlink()
                raise ValueError("legacy backup already exists; migration refused")
            deploy.rename(backup)
        try:
            os.replace(pending, deploy)
        except OSError:
            if not deploy.exists() and (state / "legacy-feed").exists():
                (state / "legacy-feed").rename(deploy)
            raise
        # Keep a bounded rollback window; never discard the currently served snapshot.
        history = sorted((p for p in releases.glob("snapshot-*")
                          if p.is_dir() and not p.is_symlink() and (p / "manifest.json").is_file()),
                         key=lambda p: p.stat().st_mtime, reverse=True)
        for old in history[96:]:
            if old != deploy.resolve() and old.is_dir() and not old.is_symlink():
                shutil.rmtree(old)
        return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("publish", "check"))
    parser.add_argument("--deploy", type=Path, default=Path.home() / "demos/mission-control")
    parser.add_argument("--state", type=Path, default=Path.home() / ".local/state/intent-mc-public")
    parser.add_argument("--source", type=Path, default=Path.home() / ".local/share/intent-mc-source.git")
    parser.add_argument("--url", default=BASE)
    args = parser.parse_args()
    if args.command == "publish":
        data = publish(args.deploy, args.state, args.source)
        errors = freshness_errors(data, dt.datetime.now(dt.timezone.utc))
    else:
        request = urllib.request.Request(args.url + "manifest.json", headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.load(response)
        errors = freshness_errors(data, dt.datetime.now(dt.timezone.utc))
        with urllib.request.urlopen(args.url, timeout=20) as response:
            page = response.read().decode()
        revision = data.get("source", {}).get("revision") if isinstance(data, dict) and isinstance(data.get("source", {}), dict) else None
        publication = data.get("published_at") if isinstance(data, dict) else None
        if not isinstance(revision, str) or not isinstance(publication, str):
            errors.append("public HTML/manifest revision mismatch")
        elif revision not in page or publication not in page:
            # Separate HTTP requests can straddle an atomic symlink promotion.
            # Retry the pair once, rather than paging on a successful publication.
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.load(response)
            errors = freshness_errors(data, dt.datetime.now(dt.timezone.utc))
            with urllib.request.urlopen(args.url, timeout=20) as response:
                page = response.read().decode()
            source = data.get("source", {}) if isinstance(data, dict) else {}
            revision = source.get("revision") if isinstance(source, dict) else None
            publication = data.get("published_at") if isinstance(data, dict) else None
            if not isinstance(revision, str) or not isinstance(publication, str) or revision not in page or publication not in page:
                errors.append("public HTML/manifest revision mismatch")
    envelope = data if isinstance(data, dict) else {}
    source = envelope.get("source") if isinstance(envelope.get("source"), dict) else {}
    print(json.dumps({"published_at": envelope.get("published_at"), "source_revision": source.get("revision"), "errors": errors}))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({"errors": ["snapshot operation failed"], "error_category": type(error).__name__}))
        raise SystemExit(1)
