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
