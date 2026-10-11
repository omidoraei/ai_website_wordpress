#!/usr/bin/env python3
"""
Check that every remote asset URL referenced by the templates is reachable.

Release asset uploads are blocked in the agent sandbox (constitution rule K), so the
kit serves imagery from an immutable git tag. This script is the CI half of that
bargain: it HEAD-tests every unique URL and fails if one stops resolving.

    python3 tools/check_assets.py            # human report
    python3 tools/check_assets.py --json     # machine output
    python3 tools/check_assets.py --offline  # skip the network, list what it would test

Exit codes: 0 = all reachable (200 after redirects), 1 = at least one unreachable.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
URL = re.compile(r"https://[^\"\s]+\.(?:jpg|jpeg|png|webp|avif)")


def collect() -> dict:
    found = {}
    for root, _dirs, names in os.walk(TEMPLATES):
        for fn in sorted(names):
            if not fn.endswith(".json"):
                continue
            path = os.path.join(root, fn)
            for url in URL.findall(open(path, encoding="utf-8").read()):
                found.setdefault(url, []).append(os.path.relpath(path, ROOT))
    return found


def head(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "aurora-kit-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # follow redirects
            # read a byte so the transfer is real, then report the status
            resp.read(1)
            return str(resp.status)
    except urllib.error.HTTPError as exc:
        return str(exc.code)
    except Exception as exc:  # noqa: BLE001 - reported, not raised
        return "ERR:%s" % type(exc).__name__


def curl_head(url: str, timeout: int = 30) -> str:
    out = subprocess.run(
        ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout), url],
        capture_output=True, text=True)
    return out.stdout.strip() or "ERR:curl"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    urls = collect()
    MIN_URLS = 5
    if len(urls) < MIN_URLS:
        print("only %d remote asset URL(s) found in templates/, floor is %d - "
              "a scan of nothing is not a pass (docs/METRICS.md \u00a73)"
              % (len(urls), MIN_URLS))
        return 1

    results = {}
    if not args.offline:
        have_curl = subprocess.run(["which", "curl"], capture_output=True).returncode == 0
        for url in sorted(urls):
            results[url] = curl_head(url) if have_curl else head(url)

    bad = {u: c for u, c in results.items() if c not in ("200",)}
    if args.json:
        print(json.dumps({"checked": len(urls), "unreachable": bad, "results": results},
                         indent=1))
    else:
        print("asset URL check (%s)" % ("offline" if args.offline else "network"))
        for url in sorted(urls):
            status = results.get(url, "not tested")
            print("  %-6s %s" % (status, url))
            print("         used by: %s" % ", ".join(sorted(set(urls[url]))[:3])
                  + (" ..." if len(set(urls[url])) > 3 else ""))
        print("  %d unique URLs, %d unreachable" % (len(urls), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
