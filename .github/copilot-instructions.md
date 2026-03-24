# GitHub Copilot Instructions

## Project Overview
Anonymous Studio is a **PII (Personally Identifiable Information) detection and anonymization** application built with:
- **Streamlit** — interactive web UI
- **Microsoft Presidio** — NLP-based PII detection engine
- **spaCy / Flair / Stanza / HuggingFace** — named-entity recognition models
- **Azure AI Language** — cloud-based PII detection (optional)
- **OpenAI** — synthetic data generation (optional)

## Repository Layout
| File | Purpose |
|------|---------|
| `presidio_streamlit.py` | Main Streamlit app entry point |
| `presidio_helpers.py` | Analyzer/anonymizer helpers shared by the app and tests |
| `presidio_nlp_engine_config.py` | NLP engine configuration |
| `flair_recognizer.py` | Custom Flair-based entity recognizer |
| `azure_ai_language_wrapper.py` | Azure AI Language PII service wrapper |
| `openai_fake_data_generator.py` | OpenAI-based synthetic data generator |
| `test_streamlit.py` | Pytest tests for core analyze/anonymize logic |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container image definition |

## Coding Conventions
- **Python 3.10**, PEP 8 style, max line length **120** characters.
- Use `flake8` for linting (`E9, F63, F7, F82` are hard errors; everything else is a warning).
- All new logic should include docstrings.
- Avoid committing API keys, passwords, or any credentials — use environment variables (`.env` / `os.getenv`).
- Prefer Presidio's built-in recognizer interfaces when adding new entity types.

## Testing
- Tests live in `test_streamlit.py` and use **pytest**.
- Tests require large NLP model downloads; run locally, not in CI without caching.
- To run: `pytest test_streamlit.py -v`

## Security Considerations
- This app handles sensitive PII data; never log raw user text.
- Encrypt keys (`st_encrypt_key`) must be treated as secrets.
- Azure / OpenAI credentials are read from environment variables — never hard-code them.
- CodeQL scans run on every push/PR and weekly via `.github/workflows/codeql.yml`.
