# Contributing to Anonymous Studio

Thank you for contributing! This guide describes the branching strategy,
pull-request workflow, and review expectations adopted by the capstone team.

---

## Branching Strategy

| Branch | Purpose | Who can push directly? |
|--------|---------|------------------------|
| `main` | Production-ready code. Always deployable. | **Nobody** — changes arrive only through approved PRs. |
| `feature/<short-name>` | New features or enhancements. | The developer who owns the feature. |
| `bugfix/<short-name>` | Bug fixes. | The developer who owns the fix. |
| `docs/<short-name>` | Documentation-only changes. | Any team member. |

### Naming examples

```
feature/add-redaction-highlights
bugfix/fix-nlp-model-load
docs/update-readme
```

## Pull-Request Workflow

1. **Create a branch** from `main` using the naming convention above.
2. **Make small, focused commits.** Each commit should do one logical thing.
3. **Open a Pull Request** against `main` when your work is ready for review.
   - Fill in the PR template (if present) or write a short description of
     *what* changed and *why*.
   - Link the related GitHub Issue (e.g., `Closes #42`).
4. **Automated checks run automatically:**
   - **CI** — flake8 lint + pytest (see `.github/workflows/ci.yml`).
   - **CodeQL** — security & code-quality scan.
5. **Request a review** from at least one teammate. CODEOWNERS will
   auto-assign reviewers for files they own.
6. **Address review feedback** by pushing new commits to the same branch.
7. **Merge** once the PR has:
   - At least **1 approving review**.
   - All required status checks passing.
   - No unresolved review conversations.

> **Tip:** Prefer *Squash and merge* to keep `main` history clean, but
> regular merge commits are also acceptable.

## Code-Review Guidelines

- Be constructive and specific — suggest fixes, not just problems.
- Approve only after verifying the change does what the PR says it does.
- Look for:
  - PII or secrets accidentally committed.
  - Missing or broken tests.
  - Style issues not caught by flake8.

## Coding Standards

- **Python 3.10**, PEP 8 style, max line length **120** characters.
- Run `flake8` locally before pushing:
  ```bash
  flake8 . --max-line-length=120
  ```
- Add docstrings to all new functions and classes.
- Never commit API keys, passwords, or credentials — use environment
  variables (`os.getenv`).

## Running Tests Locally

```bash
pip install -r requirements.txt
pytest test_streamlit.py -v
```

> Tests require large NLP model downloads. The CI runner skips them
> gracefully; run the full suite locally before opening a PR.
