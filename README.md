# What Skills Are Actually in Demand for Data Science Roles Right Now?

An analysis of live job postings from about 3 data sources, cleaned manually, to identify the real, current skill demands for Data Science, Machine Learning, and Data Analyst roles.

## Why this project?

Most "what skills do you need for DS" advice is either years old or based on opinion. This project pulls **live job posting data** from different sources, extracts structured signal from unstructured text, and quantifies what's actually being asked for right now, i.e. skills, tools, experience levels, and how that varies by role type and work arrangement.

## Data sources

| Source | Type | Why included |
|---|---|---|
| [Adzuna](https://developer.adzuna.com/) | General job market API | Broad, high-volume market coverage |
| [The Muse](https://www.themuse.com/developers/api/v2) | Curated/vetted listings | Company-vetted postings, different posting style/quality bar |
| [Arbeitnow](https://www.arbeitnow.com/api/job-board-api) | Remote/EU-focused | Structured tags, remote-work flag, good volume via pagination |

Combining a general-market source, a curated source, and a remote-specialist source gives us a **source diversity**.

## Project phases

Status keys: ✅ Completed · 🔧 Working on · ⏳ Pending
 
| Phase | Status |
|---|---|
| Phase 1: Data collection | ✅ Completed |
| Phase 2: Data cleaning & feature engineering | 🔧 Working on |
| Phase 3: Analysis | ⏳ Pending |
| Phase 4: Presentation & packaging | ⏳ Pending |

**Phase 1: Data collection (4-5 days)**  
Pull postings from all three APIs, filter to DS/ML/Analyst roles, store raw JSON immediately (no on-the-fly processing). Target: 500-1500 postings.

**Phase 2: Data cleaning & feature engineering (3-4 days)**  
Deduplicate, normalize location/salary formats, extract structured features from free text (skills, tools, years of experience, degree requirements, work type).

**Phase 3: Analysis (4-5 days)**  
Skill-frequency analysis, salary distribution by role/seniority/work-type, posting trends over time, and a lightweight model to predict role category or salary bracket from description text.

**Phase 4: Presentation & packaging (3-4 days)**   
Interactive dashboard, deliverable repository with with findings and human interactive results (I bet no one wants to go through configuring venv to get data analysis result), and a short write-up summarizing the most interesting insights.

## Methodology notes

- Matching is **title/tag-first**: a posting only counts as a genuine match if the role title or tags indicate it — description-text matches alone are treated as supporting signal only, since generic phrases (e.g. AI-in-hiring compliance disclaimers) create false positives if trusted on their own.
- Raw and cleaned data are kept as separate files at every stage, so cleaning logic can be re-run without re-fetching.

## Findings

_To be added as analysis progresses._

## Setup
1. Clone the repository
```bash
   git clone https://github.com/abdurahman-abdo/skillscope.git
   cd skillscope
```
2. Install dependencies (uv creates the virtual environment automatically)
```bash
   uv sync
```
3. Check the Jupyter notebooks *since the project is just under development*

**Current data collection results could be accessed at:**
```bash
cd src/skillscope/data/raw
cd src/skillscope/data/cleaned
```

## Directory Structure

```
src/
└── skillscope/
    ├── data/
    │   ├── raw/
    │   │   ├── adzuna.json
    │   │   ├── arbeit.json
    │   │   └── muse.json
    │   └── cleaned/
    │       ├── adzuna.csv
    │       ├── arbeit.csv
    │       └── muse.csv
    ├── fetch/
    │   ├── fetch_adzuna.py
    │   ├── fetch_arbeit.py
    │   └── fetch_muse.py
    ├── clean/
    │   ├── clean_adzuna.py
    │   ├── clean_arbeit.py
    │   └── clean_muse.py
    ├── __init__.py
    ├── main.ipynb      # Notebook where new algorithms and logics are experimented at
    ├── utils.py        # basic utility functions reused multiple times like load_file, save_file...
    ├── matching.py     # matching, and data extraction related algorithms
    └── config.py       # configuration variables like: paths and API keys loaded from env
```