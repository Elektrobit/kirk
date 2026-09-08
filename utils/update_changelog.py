#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""
Fetch GitHub releases and update doc/changelog.rst.
"""

import argparse
import json
import os
import re
import sys
import urllib.request


def markdown_to_rst(body: str, repo: str = "linux-test-project/kirk") -> str:
    lines = body.splitlines()
    rst_lines = []
    for line in lines:
        m_h = re.match(r"^#{2,4}\s+(.*)", line)
        if m_h:
            title = m_h.group(1).strip()
            rst_lines.append("")
            rst_lines.append(f"**{title}**")
            rst_lines.append("")
            continue

        # Convert Markdown single backticks `code` into RST double backticks ``code``
        line = re.sub(r"`([^`\n]+)`", r"``\1``", line)

        # Wrap bare CLI flags `--some-flag` into ``--some-flag``
        line = re.sub(
            r"(?<![`\w])(--[a-zA-Z0-9_-]+)(?![`\w])",
            r"``\1``",
            line,
        )

        # Format PR links
        line = re.sub(
            r"https://github\.com/([\w-]+)/([\w-]+)/pull/(\d+)",
            r"`#\3 <https://github.com/\1/\2/pull/\3>`__",
            line,
        )
        # Format commit links
        line = re.sub(
            r"https://github\.com/([\w-]+)/([\w-]+)/commit/([0-9a-f]{7,40})",
            r"`\3 <https://github.com/\1/\2/commit/\3>`__",
            line,
        )
        # Format bare 40-char SHA1 commit hashes
        line = re.sub(
            r"(?<![`\w/])([0-9a-f]{40})(?![`\w])",
            rf"`\1 <https://github.com/{repo}/commit/\1>`__",
            line,
        )
        # Format compare links
        line = re.sub(
            r"https://github\.com/([\w-]+)/([\w-]+)/compare/(\S+)",
            r"`\3 <https://github.com/\1/\2/compare/\3>`__",
            line,
        )
        # Format user mentions
        line = re.sub(
            r"(?<!\w)@([a-zA-Z0-9_-]+)",
            r"`@\1 <https://github.com/\1>`__",
            line,
        )
        # Format remaining standalone URLs
        line = re.sub(
            r"(?<![`<])(https?://[^\s`<>]+)(?!`__)",
            r"`\1 <\1>`__",
            line,
        )
        rst_lines.append(line)
    return "\n".join(rst_lines).strip()


def fetch_releases(repo: str) -> list:
    url = f"https://api.github.com/repos/{repo}/releases?per_page=100"
    headers = {
        "User-Agent": "kirk-changelog-updater",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        if not isinstance(data, list):
            raise ValueError(f"Unexpected response from GitHub: {data}")
        return data


def generate_rst(releases: list, repo: str = "linux-test-project/kirk") -> str:
    out_lines = [
        ".. SPDX-License-Identifier: GPL-2.0-or-later\n",
        "Changelog",
        "=========\n",
    ]

    for r in releases:
        tag = r.get("tag_name")
        date = (r.get("published_at") or "")[:10]
        body = (r.get("body") or "").strip()

        header = f"{tag}"
        if date:
            header += f" ({date})"
        out_lines.append(header)
        out_lines.append("-" * len(header))
        out_lines.append("")

        if body:
            out_lines.append(markdown_to_rst(body, repo))
            out_lines.append("")

    return "\n".join(out_lines).rstrip() + "\n"


def run() -> None:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_output = os.path.join(root_dir, "doc", "changelog.rst")

    parser = argparse.ArgumentParser(
        description="Update doc/changelog.rst from GitHub releases."
    )
    parser.add_argument(
        "--repo",
        default="linux-test-project/kirk",
        help="GitHub repository (owner/repo)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=default_output,
        help="Output RST file path (default: doc/changelog.rst)",
    )

    args = parser.parse_args()

    print(f"Fetching releases for {args.repo}...")
    try:
        releases = fetch_releases(args.repo)
    except Exception as e:
        print(f"Error fetching releases: {e}", file=sys.stderr)
        sys.exit(1)

    rst_content = generate_rst(releases, args.repo)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(rst_content)

    print(f"Updated {args.output} ({len(releases)} releases).")


if __name__ == "__main__":
    run()
