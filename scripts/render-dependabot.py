#!/usr/bin/env python3
"""Render a repo's .github/dependabot.yml from configs/dependabot.template.yml.

Keeps only the ecosystems whose manifest files exist in the target repo, so a
shared template never points Dependabot at a manifest that isn't there (which
GitHub reports as failed update jobs in the repo's Dependabot tab).

Usage: render-dependabot.py TEMPLATE REPO_PATH
Prints the rendered YAML to stdout; empty output means no ecosystem applies.
"""

import sys
from pathlib import Path

# Manifest files that activate each ecosystem. github-actions counts when the
# repo has any workflow (the org lint caller guarantees one).
MANIFESTS = {
    "npm": ["package.json"],
    "pip": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
    "maven": ["pom.xml"],
    "gradle": ["build.gradle", "build.gradle.kts"],
    "github-actions": [".github/workflows"],
}


def ecosystems_in(repo: Path) -> set:
    found = set()
    for ecosystem, manifests in MANIFESTS.items():
        if any((repo / m).exists() for m in manifests):
            found.add(ecosystem)
    return found


def render(template: str, keep: set) -> str:
    """Filter `updates:` list items to the kept ecosystems. Template list items
    are simple block maps starting with `- package-ecosystem: "<name>"`."""
    lines = template.splitlines()
    head, blocks, current = [], [], None
    in_updates = False
    for line in lines:
        if line.startswith("updates:"):
            in_updates = True
            head.append(line)
            continue
        if in_updates and line.startswith("  - package-ecosystem:"):
            if current is not None:
                blocks.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
        else:
            head.append(line)
    if current is not None:
        blocks.append(current)

    kept = []
    for block in blocks:
        name = block[0].split('"')[1]
        if name in keep:
            kept.extend(block)
    if not kept:
        return ""
    # Replace the template's header comment with a generated-file notice.
    body = [line for line in head if not line.startswith("#")]
    while body and not body[0].strip():
        body.pop(0)
    header = [
        "# GENERATED from hothsys/.github configs/dependabot.template.yml.",
        "# Do not edit here - edit the template; the org sync workflow opens a",
        "# PR with the change. Only ecosystems with manifests in this repo are",
        "# listed.",
        "",
    ]
    return "\n".join(header + body + kept) + "\n"


def main() -> None:
    template = Path(sys.argv[1]).read_text()
    repo = Path(sys.argv[2])
    sys.stdout.write(render(template, ecosystems_in(repo)))


if __name__ == "__main__":
    main()
