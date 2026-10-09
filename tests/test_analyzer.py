from backend.analyzer import analyze, detect_skills

def test_detects_ai_skills():
    assert {"python", "rag", "langgraph"} <= set(detect_skills("Python, RAG, LangGraph"))

def test_analyze_returns_scores_and_gaps():
    resume = "Python developer. Built a RAG project with FastAPI and LangChain. Education: Bachelor's degree. Projects include deployed API."
    jd = "Required: Python, RAG, FastAPI, AWS. Preferred: LangChain. 2 years experience. Bachelor's degree required."
    result = analyze(resume, jd)
    assert 0 <= result["overall_match"] <= 100
    assert "python" in result["matched_skills"]
    assert "aws" in result["missing_skills"]
    assert set(result["scores"]) == {"skills", "experience", "projects", "education", "semantic_keyword_overlap"}
