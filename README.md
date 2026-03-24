# Anonymous Studio

> PII detection and anonymization platform built with Presidio and Streamlit.

Anonymous Studio helps compliance officers, developers, and researchers detect and anonymize
Personally Identifiable Information (PII) in text data. It provides an interactive web
interface powered by Streamlit and leverages NLP models for entity recognition.

## Features

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━┓
┃Feature                       ┃Status     ┃Issue┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━┩
│PII text detection            │Done       │#3   │
├──────────────────────────────┼───────────┼─────┤
│Allowlists and denylists      │Done       │#25  │
├──────────────────────────────┼───────────┼─────┤
│Confidence threshold tuning   │Done       │#27  │
├──────────────────────────────┼───────────┼─────┤
│Detection rationale view      │In Progress│#26  │
├──────────────────────────────┼───────────┼─────┤
│Entity type selection         │In Progress│#28  │
├──────────────────────────────┼───────────┼─────┤
│Anonymization methods         │Todo       │#4   │
├──────────────────────────────┼───────────┼─────┤
│Save de-identification results│Todo       │#17  │
├──────────────────────────────┼───────────┼─────┤
│MongoDB persistence           │Todo       │#8   │
├──────────────────────────────┼───────────┼─────┤
│Create pipeline cards         │Todo       │#15  │
├──────────────────────────────┼───────────┼─────┤
│Move cards across stages      │Todo       │#16  │
├──────────────────────────────┼───────────┼─────┤
│Visual status indicators      │Todo       │#21  │
├──────────────────────────────┼───────────┼─────┤
│Schedule review appointments  │Todo       │#7   │
├──────────────────────────────┼───────────┼─────┤
│File upload (CSV/text)        │Backlog    │#5   │
├──────────────────────────────┼───────────┼─────┤
│Kanban board                  │Todo       │#6   │
├──────────────────────────────┼───────────┼─────┤
│Audit trail                   │Backlog    │#1   │
├──────────────────────────────┼───────────┼─────┤
│REST API                      │Backlog    │#14  │
├──────────────────────────────┼───────────┼─────┤
│Image PII detection           │Backlog    │#12  │
├──────────────────────────────┼───────────┼─────┤
│Auth and roles                │Backlog    │#2   │
└──────────────────────────────┴───────────┴─────┘
```

## How It Works

```
 ┌────┐            ┌─────────┐     ┌─────────────────┐              ┌─────────┐┌──────────┐
 │User│            │Streamlit│     │Presidio Analyzer│              │NER Model││Anonymizer│
 └─┬──┘            └────┬────┘     └────────┬────────┘              └────┬────┘└────┬─────┘
   │                    │                   │                            │          │      
   │ Paste or type text │                   │                            │          │      
   │───────────────────>│                   │                            │          │      
   │                    │                   │                            │          │      
   │                    │Detect PII entities│                            │          │      
   │                    │──────────────────>│                            │          │      
   │                    │                   │                            │          │      
   │                    │                   │      Run NLP pipeline      │          │      
   │                    │                   │───────────────────────────>│          │      
   │                    │                   │                            │          │      
   │                    │                   │Entities + confidence scores│          │      
   │                    │                   │<───────────────────────────│          │      
   │                    │                   │                            │          │      
   │                    │ Analysis results  │                            │          │      
   │                    │<──────────────────│                            │          │      
   │                    │                   │                            │          │      
   │                    │                   │  Apply operator            │          │      
   │                    │──────────────────────────────────────────────────────────>│      
   │                    │                   │                            │          │      
   │                    │                   De-identified output         │          │      
   │                    │<──────────────────────────────────────────────────────────│      
   │                    │                   │                            │          │      
   │Side-by-side results│                   │                            │          │      
   │<───────────────────│                   │                            │          │      
 ┌─┴──┐            ┌────┴────┐     ┌────────┴────────┐              ┌────┴────┐┌────┴─────┐
 │User│            │Streamlit│     │Presidio Analyzer│              │NER Model││Anonymizer│
 └────┘            └─────────┘     └─────────────────┘              └─────────┘└──────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/cpsc4205-group3/anonymous-studio.git
cd anonymous-studio

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run presidio_streamlit.py
```

The app opens at `http://localhost:8501`.

### Configuration (Optional)

Create a `.env` file in the project root for optional services:

```bash
# Azure AI Language (optional PII detection backend)
TA_KEY=YOUR_TEXT_ANALYTICS_KEY
TA_ENDPOINT=YOUR_TEXT_ANALYTICS_ENDPOINT

# OpenAI synthetic data generation (optional)
OPENAI_TYPE="Azure"          # or "openai"
OPENAI_KEY=YOUR_OPENAI_KEY
OPENAI_API_VERSION="2023-05-15"
AZURE_OPENAI_ENDPOINT=YOUR_AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_DEPLOYMENT=text-davinci-003

# Allow users to download additional NLP models at runtime
ALLOW_OTHER_MODELS=true

# MongoDB Atlas (persistence layer — see docs/mongodb-setup.md)
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=anonymous_studio
```

## Running with Docker

```bash
docker build -t anonymous-studio .
docker run -p 7860:7860 anonymous-studio
```

## Testing

```bash
pytest test_streamlit.py -v
```

## NER Models

| Package | Model | Best For |
|---------|-------|----------|
| spaCy | `en_core_web_lg` | General-purpose, fast |
| HuggingFace | `obi/deid_roberta_i2b2` | Medical/clinical text |
| HuggingFace | `StanfordAIMI/stanford-deidentifier-base` | Healthcare de-identification |
| Flair | `ner-english-large` | High-accuracy NER |
| Stanza | `en` | Academic/research NLP |
| Azure AI | Cloud PII service | Production-scale, managed |

Models are swappable at runtime via the sidebar dropdown.

## Project Structure

| File | Description |
|------|-------------|
| `presidio_streamlit.py` | Main Streamlit application |
| `presidio_helpers.py` | Analyzer and anonymizer helper functions |
| `presidio_nlp_engine_config.py` | NLP engine configuration |
| `flair_recognizer.py` | Custom Flair-based entity recognizer |
| `azure_ai_language_wrapper.py` | Azure AI Language PII wrapper |
| `openai_fake_data_generator.py` | OpenAI synthetic data generator |
| `mongo_persistence.py` | MongoDB connection and persistence helpers |
| `test_streamlit.py` | Pytest test suite |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container image definition |
| `docs/` | Project documentation (setup guides, sprint planning, team info) |

## Roadmap

```
Anonymous Studio
 ├─Done
 │  ├─PII text detection (#3)
 │  ├─Allowlists and denylists (#25)
 │  └─Confidence threshold tuning (#27)
 ├─In Progress
 │  ├─Detection rationale view (#26)
 │  └─Entity type selection (#28)
 ├─Sprint 2 (Todo)
 │  ├─Anonymization methods (#4)
 │  ├─Save de-id results (#17)
 │  ├─MongoDB persistence (#8)
 │  ├─Pipeline cards (#15)
 │  ├─Kanban workflow (#16)
 │  └─Status indicators (#21)
 └─Backlog
    ├─File upload (#5)
    ├─Kanban board (#6)
    ├─Audit trail (#1)
    ├─REST API (#14)
    ├─Auth and roles (#2)
    └─Image PII detection (#12)
```

## Sprint Workflow

This project uses GitHub Issues and Projects for sprint planning:

- **Labels**: Issues are tagged with Sprint (`sprint-1`, `sprint-2`), Type (`feat`, `bug`),
  and MoSCoW (`must-have`, `should-have`, `nice-to-have`) labels.
- **Issue templates**: Use the provided templates for bug reports, user stories, and sprint
  tasks when creating new issues.
- **Pull requests**: Follow the PR template checklist before requesting review.
- **Project board**: Track issue status from Backlog -> Todo -> In Progress -> In Review -> Done.



## Team

| Member | Role | Sprint 2 Focus |
|--------|------|----------------|
| Carley Fant (51nk0r5w1m) | Lead Developer & Database Engineer | MongoDB persistence, data layer (#8, #17, #4) |
| Diamond Hogans | UI/UX Developer | Detection rationale, badges (#26, #21, #28) |
| Sakshi Patel | Frontend Developer | Card management, table views (#15, #20, #28) |
| Elijah Jenkins | Configuration & Integration | Workflow, thresholds, allow/deny lists (#16, #20, #15, |

## License

This project is for educational purposes as part of CPSC 4205.
