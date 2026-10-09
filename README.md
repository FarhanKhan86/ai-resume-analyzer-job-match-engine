# AI Resume Analyzer & Job Match Engine

A portfolio-ready MVP for parsing resumes, analyzing job descriptions, scoring job fit, explaining strengths/gaps, and generating honest resume-improvement suggestions.

## Features
- PDF and DOCX resume upload; TXT job description input
- Extracts skills, projects, experience signals, education signals, and keywords
- Explainable weighted matching: skills (40%), experience (15%), projects (15%), education (10%), semantic keyword overlap (20%)
- Required/preferred skill gap reporting
- Resume improvement suggestions grounded in detected content
- FastAPI backend and Streamlit frontend
- No API key required; all analysis runs locally

> Scores are heuristic indicators, not hiring probabilities. Review extracted content before relying on it. This MVP does not use a hosted LLM or embeddings model; semantic matching is a lightweight local token-overlap baseline.

## Requirements
- Python 3.11+
- Windows, macOS, or Linux

## Run on Windows (PowerShell)
```powershell
cd ai-resume-analyzer-job-match-engine
uv sync
uv run streamlit run frontend/app.py
```
The Streamlit UI calls the local FastAPI API, so start the backend in a second terminal:
```powershell
cd ai-resume-analyzer-job-match-engine
uv run uvicorn backend.main:app --reload
```
Open the Streamlit URL shown in terminal (usually http://localhost:8501). API docs: http://127.0.0.1:8000/docs.

If you prefer pip:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
uvicorn backend.main:app --reload
```
In another terminal run `streamlit run frontend/app.py`.

## API
- `GET /health`
- `POST /analyze` multipart fields: `resume` (PDF/DOCX/TXT) and `job_description` (text)

## Project layout
```text
backend/
  main.py        FastAPI endpoints
  parser.py      PDF/DOCX/TXT extraction
  analyzer.py    Explainable scoring and recommendations
frontend/
  app.py         Streamlit dashboard
tests/
  test_analyzer.py
```

## Next production steps
1. Add robust section-aware resume parsing and user-reviewed structured profile.
2. Add Sentence Transformers embeddings and FAISS/Chroma retrieval.
3. Add authentication, consent, deletion, and encrypted storage if persistence is introduced.
4. Add React frontend and browser extension.
5. Evaluate scores against a labeled test set; avoid using demographic/protected attributes in ranking.
