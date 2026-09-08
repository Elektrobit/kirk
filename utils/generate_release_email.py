#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""
Generate a release announcement email for the LTP mailing list.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request


def get_current_version() -> str:
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        from libkirk import __version__
        return __version__
    except Exception:
        return "4.2.0"


def fetch_release_notes(version: str, repo: str = "linux-test-project/kirk") -> str:
    tag = f"v{version.lstrip('v')}"
    url = f"https://api.github.com/repos/{repo}/releases/tags/{tag}"
    headers = {
        "User-Agent": "kirk-email-generator",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("body", "").strip()
    except Exception:
        pass

    # Fallback to git log
    try:
        log = subprocess.check_output(
            ["git", "log", "--no-merges", "--pretty=format:* %s", f"{tag}~10..{tag}"],
            text=True,
        ).strip()
        return log
    except Exception:
        return ""


def get_author_name() -> str:
    try:
        name = subprocess.check_output(["git", "config", "user.name"], text=True).strip()
        if name:
            return name
    except Exception:
        pass
    return "The Kirk Maintainers"


def generate_email(version: str, repo: str = "linux-test-project/kirk") -> str:
    tag = f"v{version.lstrip('v')}"
    raw_version = version.lstrip("v")
    notes = fetch_release_notes(version, repo)
    author = get_author_name()

    email_lines = [
        "To: ltp@lists.linux.it",
        f"Subject: [ANNOUNCE] kirk release {tag}",
        "",
        "Hi everyone,",
        "",
        f"I am pleased to announce the release of kirk {tag}.",
        "",
        "kirk is the test runner framework for the Linux Test Project (LTP).",
        "The release is available on PyPI:",
        f"    https://pypi.org/project/kirk/{raw_version}/",
        "",
        "You can install or upgrade using pip:",
        "    pip install --upgrade kirk",
        "",
    ]

    if notes:
        email_lines.append("Key changes in this release:")
        email_lines.append("----------------------------")
        email_lines.append(notes)
        email_lines.append("")

    email_lines.extend([
        "Best regards,",
        author,
        "",
    ])

    return "\n".join(email_lines)


def run() -> None:
    default_version = get_current_version()

    parser = argparse.ArgumentParser(
        description="Generate release announcement email."
    )
    parser.add_argument(
        "-v",
        "--version",
        default=default_version,
        help=f"Release version (default: {default_version})",
    )
    parser.add_argument(
        "--repo",
        default="linux-test-project/kirk",
        help="GitHub repository (default: linux-test-project/kirk)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    email_text = generate_email(args.version, args.repo)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(email_text)
        print(f"Announcement email written to {args.output}")
    else:
        print(email_text)


if __name__ == "__main__":
    run()
