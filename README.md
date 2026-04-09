# cv-processor

Backend REST API for a bilingual CV semantic matching system. Receives pre-extracted CV text strings from the frontend (OCR is handled on the FE side), matches them against job postings using multilingual sentence embeddings, and returns ranked candidate results alongside a TF-IDF keyword baseline score for comparison.

> **Skripsi:** Perancangan Sistem Filtering Kandidat Berdasarkan Kualifikasi Menggunakan Analisis Semantik Berbasis Machine Learning pada Data Curriculum Vitae

---

## Tech Stack

| Layer | Library / Tool | Purpose |
|---|---|---|
| Web Framework | `Flask` | REST API server |
| Auth | Static UUID token in `.env` | Simple Bearer token auth |
| NLP Preprocessing | `langdetect`, `re`, `unicodedata` | Text cleaning, language detection |
| Skill Extraction | `spaCy` + custom bilingual skill list | Rule-based NER for skills |
| Embedding Model | `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) | Cross-lingual sentence embeddings |
| Similarity | `scikit-learn` (`cosine_similarity`) | Compute semantic match scores |
| Baseline | `scikit-learn` (`TfidfVectorizer`) | TF-IDF keyword matching — always returned alongside semantic score |
| Data Store | `SQLite` (via `SQLAlchemy`) | Job descriptions — read-only from API |
| Env/Config | `python-dotenv` | Token & config management |
| CORS | `flask-cors` | Allow cross-origin requests from the FE |

---

## Project Structure

```
backend/
├── app.py                      # Flask entry point
├── config.py                   # Env vars, token, model name
├── requirements.txt
├── seed/
│   ├── schema.sql              # Idempotent CREATE TABLE statement
│   └── jobs_seed.sql           # INSERT OR IGNORE seed data (5 industries)
│
├── middleware/
│   └── auth.py                 # Static Bearer token validation
│
├── routes/
│   ├── match.py                # POST /api/match
│   ├── jobs.py                 # GET /api/jobs, GET /api/jobs/<id>
│   └── health.py               # GET /api/health
│
├── services/
│   ├── preprocessing.py        # Text cleaning & normalization
│   ├── extraction.py           # Rule-based skill & section extraction
│   ├── embedding_service.py    # Sentence embeddings (loaded once at startup)
│   └── baseline_service.py     # TF-IDF keyword matching (paper baseline)
│
├── models/
│   └── db_models.py            # SQLAlchemy Job model
│
└── utils/
    └── response_utils.py       # Standardised JSON response helpers
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r backend/requirements.txt
python -m spacy download xx_ent_wiki_sm
```

### 2. Configure environment

```bash
cp backend/.env.example backend/.env
# Edit backend/.env — set APP_TOKEN to a real UUID
```

### 3. Initialise the database

```bash
cd backend
sqlite3 app.db < seed/schema.sql
sqlite3 app.db < seed/jobs_seed.sql
```

### 4. Run

```bash
# Development
python backend/app.py

# Production
gunicorn -w 1 -b 0.0.0.0:5000 backend/app:app
```

---

## Docker

```bash
cp backend/.env.example backend/.env
# Edit backend/.env — set APP_TOKEN to a real UUID
docker compose up --build
```

The entrypoint script automatically applies schema and seed data on first run. The SQLite database is stored on a named Docker volume and persists across container restarts.

Service available at: `http://localhost:5000/api/health`

---

## API Endpoints

All endpoints except `/api/health` require: `Authorization: Bearer <token>`

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/health` | Liveness check — no auth required |
| `GET` | `/api/jobs` | List job postings (supports `industry`, `page`, `limit` query params) |
| `GET` | `/api/jobs/<job_id>` | Get full job detail |
| `POST` | `/api/match` | Batch CV matching — returns ranked candidates with semantic and keyword scores |

### POST /api/match

Accepts a `job_id` and a list of candidates with pre-extracted `cv_text`. Returns candidates ranked by `semantic_score` descending. Every result includes both the semantic score and the TF-IDF keyword score side by side for direct comparison.

**Grade thresholds** (based on `semantic_score`):

| Score | Grade |
|---|---|
| ≥ 80 | High Match |
| 60–79 | Medium Match |
| < 60 | Low Match |

---

## Scoring

`semantic_score = (skills_score × 0.4) + (experience_score × 0.4) + (education_score × 0.2)`

The `score_comparison` block in every result contains:
- `semantic_score` — weighted cosine similarity from multilingual sentence embeddings (0–100)
- `keyword_score` — TF-IDF bag-of-words cosine similarity score (0–100)
- `improvement` — `semantic_score − keyword_score` (quantifies the gain from semantic over keyword matching)
