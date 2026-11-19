## 🚦 Development Workflow & Standards

To maintain clean repository histories and automate issue tracking, all work across this organization should adhere to the following development lifecycle.

### 1. 🎫 Issue Creation
Usually each task (feature, bug, or refactor) should begin with an Issue.
* Use the corresponding issue template (`bug.md`, `enhancement.md`, `refactor.md`).
* Ensure every issue defines a clear **Problem** and a **Proposal/Expected Behavior**.

### 2. 🌿 Branch Naming Convention
Branches must be lowercase, use hyphens, and include the issue number (if applicable).
* **Format:** `<type>/#<issue-number>-<short-description>`
* **Examples:** 
  * `feat/#12-add-billing`
  * `fix/#45-resolve-session-timeout`
  * `refactor/#19-clean-auth-service`

### 🏗️ 3. Commit Messages & PR Titles
Follow the **Conventional Commits** specification. Use the imperative, lowercase mood.
* **Format:** `<type>(<optional-scope>): <description>`
* **Types:**
  * `feat`: A new user-facing feature.
  * `fix`: A bug fix or patch.
  * `refactor`: Structural code changes without changing external behavior.
  * `docs`: Documentation edits only (e.g., README updates).
  * `chore`: Build steps, package updates, or project configuration changes.

### 🔗 4. Pull Requests & Automated Closing
To close an issue automatically upon merging a pull request, you **must** include a closing keyword inside the **PR description/body** (not the title).
* **Format:** `Closes #<issue-number>`
* For multiple issues inside one PR, list them cleanly on separate lines:
  ```text
  Closes #14
  Closes #15
  ```

### 🧹 5. Linting & Formatting

All repos run the org's shared lint workflow on every PR. It auto-detects the stack and runs:

* **Python** - [Ruff](https://docs.astral.sh/ruff/) (`ruff check` + `ruff format --check`)
* **JavaScript / TypeScript** - [Biome](https://biomejs.dev/) (`biome ci`)
* **Java** - [Spotless](https://github.com/diffplug/spotless) with google-java-format (activates when a `pom.xml` or Gradle build exists)

**Adding it to a repo** takes one workflow file at `.github/workflows/lint.yml`:

```yaml
name: Lint
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
jobs:
  lint:
    uses: hothsys/.github/.github/workflows/reusable-lint.yml@v2
    permissions:
      contents: read
```

Plus a repo-root copy of the matching config from this repo: `configs/ruff.toml`, `configs/biome.json`, or both. Local copies keep your editor and CI on the same rules; refresh them when the org configs change. Per-repo overrides (e.g. an older Ruff `target-version`) belong in the repo's copy.

Multi-stack repos need nothing extra: the workflow runs each linter on the matching files, so a JS frontend and a Python backend are both checked in one PR.

**Dependabot:** settings live in `configs/dependabot.template.yml` here. `sync-dependabot.yml` renders each repo's `.github/dependabot.yml` filtered to the ecosystems that repo actually uses, and opens a PR when a repo drifts. Do not hand-edit a repo's dependabot.yml - edit the template. Manifest ecosystems (pip, npm, maven, gradle) check daily so advisories become fix PRs within a day; `github-actions` checks weekly. Dependabot alerts and security updates are enabled per repo under Settings > Code security and analysis, so known-CVE PRs also fire between version-update runs.
### 🛡️ 6. Security audit

Every repo runs the org's shared CVE audit daily. It scans every dependency manifest and lockfile with [osv-scanner](https://google.github.io/osv-scanner/) against the OSV.dev database (PyPI, npm, Maven Central, GitHub Actions, ...), opens one `Security audit` issue when it finds known vulnerabilities, keeps that issue updated, and closes it when the repo scans clean.

**Adding it to a repo** takes one workflow file at `.github/workflows/security-audit.yml`:

```yaml
name: Security Audit
on:
  schedule:
    - cron: 'MM HH * * *'  # daily; stagger the time per repo
  workflow_dispatch:
jobs:
  audit:
    uses: hothsys/.github/.github/workflows/reusable-security-audit.yml@v2
    permissions:
      contents: read
      issues: write
```

**README:** new repos start from `docs/README-template.md` (Description, Features, Documentation in `docs/`, License).
