from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.parser import extract_resume_text
from backend.analyzer import analyze

app = FastAPI(title="AI Resume Analyzer & Job Match Engine", version="0.1.0",
              description="Local, explainable resume/job matching MVP. Uploaded files are processed in memory.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
                   allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "AI Resume Analyzer & Job Match Engine"}

@app.post("/analyze")
async def analyze_resume(resume: UploadFile = File(...), job_description: str = Form(...)):
    try:
        content = await resume.read()
        resume_text = extract_resume_text(resume.filename or "resume.txt", content)
        result = analyze(resume_text, job_description)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await resume.close()
