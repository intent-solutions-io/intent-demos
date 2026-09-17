#!/usr/bin/env python3
"""Bounded public HTTPS diagnostics through Globalping; not browser or all-ISP proof."""

import argparse
import datetime as dt
import json
import time
import urllib.request

API = "https://api.globalping.io/v1/measurements"
COUNTRIES = ("US", "DE", "GB", "IN", "BR", "JP", "AU", "ZA")
TARGETS = ("tonsofskills.com", "www.tonsofskills.com")


def request(url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "IntentSolutions-RegionalMonitor/1.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)


def evaluate(measurement, expected=COUNTRIES):
    errors, rows = [], []
    if not isinstance(measurement, dict) or measurement.get("status") != "finished":
        return {"ok": False, "errors": ["measurement incomplete or unavailable"], "results": []}
    results = measurement.get("results")
    if not isinstance(results, list):
        return {"ok": False, "errors": ["malformed measurement results"], "results": []}
    seen = set()
    for item in results:
        if (not isinstance(item, dict) or not isinstance(item.get("probe"), dict)
                or not isinstance(item.get("result"), dict)
                or not isinstance(item["result"].get("tls"), dict)
                or not isinstance(item["result"].get("rawBody"), str)
                or not isinstance(item["probe"].get("country"), str)):
            errors.append("malformed country result")
            continue
        country = item.get("probe", {}).get("country")
        result = item.get("result", {})
        if country in seen:
            errors.append("duplicate country result")
        seen.add(country)
        passed = (result.get("status") == "finished" and result.get("statusCode") == 200
                  and result.get("tls", {}).get("authorized") is True
                  and "tons of skills" in result.get("rawBody", "").lower())
        rows.append({"country": country, "http_status": result.get("statusCode"),
                     "tls_trusted": result.get("tls", {}).get("authorized") is True,
                     "state": "reachable" if passed else "failed_or_unverified"})
        if not passed:
            errors.append(f"{country}: HTTPS/content check failed")
    if seen != set(expected):
        errors.append("requested countries not completely observed")
    return {"ok": not errors, "errors": errors, "results": rows}


def measure(target):
    if target not in TARGETS:
        raise ValueError("target is not allowlisted")
    created = request(API, {"target": target, "type": "http", "measurementOptions": {
        "protocol": "HTTPS", "request": {"method": "GET", "path": "/"}},
        "locations": [{"country": country, "limit": 1} for country in COUNTRIES]})
    if not isinstance(created, dict) or not isinstance(created.get("id"), str):
        raise ValueError("invalid measurement identity")
    measurement_id = created["id"]
    if not measurement_id.isalnum():
        raise ValueError("invalid measurement identity")
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        time.sleep(2)
        data = request(API + "/" + measurement_id)
        if not isinstance(data, dict) or data.get("status") != "in-progress":
            result = evaluate(data)
            return {"target": target, "measurement_id": measurement_id, **result}
    return {"target": target, "measurement_id": measurement_id, "ok": False,
            "errors": ["measurement timed out"], "results": []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=TARGETS, default=TARGETS[0])
    args = parser.parse_args()
    try:
        result = measure(args.target)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {"target": args.target, "ok": False, "errors": ["regional measurement unavailable"],
                  "error_category": type(error).__name__, "results": []}
    result["checked_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    print(json.dumps(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
