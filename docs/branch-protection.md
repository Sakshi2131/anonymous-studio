# Branch Protection Rules — Recommended Settings

This document describes the GitHub branch protection rules that should be
configured for the `main` branch via **Settings → Branches → Branch
protection rules** (or the newer **Settings → Rules → Rulesets**).

The rules below balance good software-engineering practice with the
practical realities of a four-person college capstone team.

---

## Rule: Protect `main`

**Applies to:** `main`

### 1. Require a pull request before merging

| Setting | Value | Rationale |
|---------|-------|-----------|
| Required approving reviews | **1** | Ensures at least one teammate reviews every change. A higher number would bottleneck a four-person team. |
| Dismiss stale pull request approvals when new commits are pushed | **Yes** | Forces re-review after the author updates code, preventing stale approvals from sneaking in unreviewed changes. |
| Require review from Code Owners | **Yes** | Leverages the `CODEOWNERS` file so domain experts review the code they own. |

### 2. Require status checks to pass before merging

| Status check | Required? | Rationale |
|--------------|-----------|-----------|
| `lint-and-test` (CI workflow) | **Yes** | Catches syntax errors, style violations, and test regressions before they reach `main`. |
| `Analyze (python)` (CodeQL) | **Yes** | Prevents merging code with known security vulnerabilities. |

| Setting | Value | Rationale |
|---------|-------|-----------|
| Require branches to be up to date before merging | **Yes** | Ensures the PR is tested against the latest `main`, avoiding integration surprises. |

### 3. Other settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| Require conversation resolution before merging | **Yes** | Ensures all review comments are addressed, promoting thorough reviews. |
| Do not allow bypassing the above settings | **Yes** | Even admins and repository owners must follow the same rules, building good habits. |
| Restrict who can push to matching branches | **No** | Not needed — requiring a PR already prevents direct pushes. |
| Require signed commits | **No** | Adds friction without proportional security benefit for a student project. |
| Require linear history | **No** | Merge commits are fine; forcing rebase adds complexity for newer Git users. |
| Allow force pushes | **No** | Protects shared history from accidental rewrites. |
| Allow deletions | **No** | Prevents accidental deletion of the main branch. |

---

## How to Apply These Rules (Classic Branch Protection)

1. Go to **Settings → Branches** in the GitHub repository.
2. Click **Add classic branch protection rule**.
3. Set **Branch name pattern** to `main`.
4. Enable each setting as listed above.
5. Click **Create**.

> GitHub also offers the newer **Rulesets** UI under **Settings → Rules →
> Rulesets**. The same settings are available there, but the classic
> branch protection path above is simpler for a first-time setup.

> **Note:** Some settings (e.g., requiring CODEOWNERS review) require the
> `CODEOWNERS` file to exist in the repository — see `.github/CODEOWNERS`.
