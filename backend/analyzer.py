import re
from collections import Counter

SKILLS = {
    "python": ["python"], "javascript": ["javascript", "js"], "typescript": ["typescript"],
    "java": ["java"], "c++": ["c++"], "sql": ["sql"], "fastapi": ["fastapi"],
    "django": ["django"], "flask": ["flask"], "react": ["react"], "tailwind": ["tailwind"],
    "langchain": ["langchain"], "langgraph": ["langgraph"], "llm": ["llm", "large language model", "large language models"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "vector databases": ["vector database", "vector databases", "chromadb", "chroma", "faiss", "qdrant", "pinecone"],
    "embeddings": ["embedding", "embeddings"], "openai": ["openai", "gpt-4", "gpt-5"],
    "transformers": ["transformers", "hugging face"], "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow"], "scikit-learn": ["scikit-learn", "sklearn"],
    "machine learning": ["machine learning", " ml "], "deep learning": ["deep learning"],
    "agents": ["ai agent", "ai agents", "multi-agent", "multi agent", "agentic"],
    "pydantic": ["pydantic"], "docker": ["docker", "containerization"], "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"], "azure": ["azure"], "gcp": ["google cloud"],
    "postgresql": ["postgresql", "postgres"], "sqlite": ["sqlite"], "git": ["git", "github"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous deployment"], "api development": ["rest api", "restful api", "api development"],
    "html/css": ["html", "css"], "streamlit": ["streamlit"], "beautifulsoup": ["beautifulsoup", "beautiful soup"],
    "playwright": ["playwright"], "pytest": ["pytest"], "mcp": ["model context protocol", "mcp"]
}
STOP = set("a an and are as at be by for from has have in into is it its of on or our that the their this to with will you your we role candidate strong ability experience work".split())

def _norm(text: str) -> str:
    return " " + re.sub(r"[^a-z0-9+#./ -]", " ", text.lower()).replace("\n", " ") + " "

def detect_skills(text: str) -> list[str]:
    haystack = _norm(text)
    found = []
    for skill, aliases in SKILLS.items():
        for alias in aliases:
            if f" {alias.lower()} " in haystack or alias.lower() in haystack:
                found.append(skill)
                break
    return sorted(set(found))

def _tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9+#.-]{1,}", text.lower()) if w not in STOP}

def _pct(a: set, b: set) -> int:
    return round(100 * len(a & b) / max(1, len(b)))

def analyze(resume_text: str, job_description: str) -> dict:
    if len(job_description.strip()) < 40:
        raise ValueError("Please enter a job description with at least 40 characters.")
    resume_skills = set(detect_skills(resume_text))
    job_skills = set(detect_skills(job_description))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    # Required/preferred signals are inferred from nearby job-description language.
    required = set()
    preferred = set()
    jd_lower = job_description.lower()
    for skill in job_skills:
        aliases = SKILLS[skill]
        positions = [jd_lower.find(a.lower()) for a in aliases if jd_lower.find(a.lower()) >= 0]
        required_words = ("required", "must have", "must-have", "minimum", "proficient", "strong knowledge")
        preferred_words = ("preferred", "nice to have", "bonus", "ideally", "plus")
        nearby = jd_lower[max(0, min(positions or [0])-100):min(len(jd_lower), (max(positions or [0])+120))]
        if any(w in nearby for w in preferred_words):
            preferred.add(skill)
        elif any(w in nearby for w in required_words):
            required.add(skill)
    if not required:
        required = set(job_skills) - preferred
    skill_score = round(100 * len(matched) / max(1, len(job_skills)))
    r_tokens, j_tokens = _tokens(resume_text), _tokens(job_description)
    semantic_score = _pct(r_tokens, j_tokens)
    exp_patterns = [r"\b\d+\+?\s+years?\b", r"\bentry.level\b", r"\bjunior\b", r"\bfresher\b", r"\bintern(ship)?\b"]
    resume_years = [int(x) for x in re.findall(r"\b(\d+)\+?\s+years?\b", resume_text.lower())]
    job_years = [int(x) for x in re.findall(r"\b(\d+)\+?\s+years?\b", job_description.lower())]
    if job_years:
        experience_score = 100 if resume_years and max(resume_years) >= min(job_years) else (55 if any(re.search(p, resume_text.lower()) for p in exp_patterns[1:]) else 35)
    else:
        experience_score = 75 if re.search(r"\b(intern|internship|junior|fresher|entry.level)\b", job_description.lower()) else 65
    project_terms = {"project", "built", "developed", "implemented", "deployed", "prototype"}
    resume_project_count = sum(1 for term in project_terms if term in resume_text.lower())
    job_project_count = sum(1 for term in project_terms if term in job_description.lower())
    project_score = min(100, 45 + resume_project_count * 9) if job_project_count else min(100, 65 + resume_project_count * 5)
    edu_terms = {"bachelor", "b.tech", "btech", "b.sc", "master", "degree", "b.e.", "education", "graduate"}
    edu_in_jd = any(t in jd_lower for t in edu_terms)
    edu_in_resume = any(t in resume_text.lower() for t in edu_terms)
    education_score = 100 if not edu_in_jd or edu_in_resume else 45
    overall = round(skill_score*.40 + experience_score*.15 + project_score*.15 + education_score*.10 + semantic_score*.20)
    strengths = []
    if matched: strengths.append("Your resume mentions " + ", ".join(matched[:8]) + ", which also appear in the job description.")
    if resume_project_count >= 3: strengths.append("Your resume contains multiple project/action signals; make the outcomes and your individual contribution explicit.")
    if not strengths: strengths.append("The resume text was parsed. Review the extracted skills and add specific evidence for the role's requirements.")
    gaps = []
    for s in sorted(required - resume_skills):
        gaps.append({"skill": s, "priority": "Required signal", "recommendation": f"If you have this experience, add a truthful example of {s} and the result. Otherwise, consider learning it."})
    for s in sorted(preferred - resume_skills):
        gaps.append({"skill": s, "priority": "Preferred signal", "recommendation": f"Consider {s} if it fits your target role; do not list it unless you can substantiate it."})
    for s in sorted((set(missing) - required - preferred)):
        gaps.append({"skill": s, "priority": "Mentioned in job", "recommendation": f"Check whether {s} is genuinely relevant to your experience and target role."})
    improvements = []
    if missing: improvements.append("Address the most relevant missing skills only when you have real evidence; otherwise create a learning project.")
    if "project" in resume_text.lower() or "built" in resume_text.lower():
        improvements.append("For each relevant project, add the problem, your technical approach, and a measurable outcome if you can verify one.")
    else:
        improvements.append("Add a Projects section with 2–3 relevant projects, the stack, your contribution, and verifiable outcomes.")
    improvements.append("Mirror important job-description terminology naturally where it accurately describes your experience.")
    return {
        "overall_match": overall,
        "scores": {"skills": skill_score, "experience": experience_score, "projects": project_score, "education": education_score, "semantic_keyword_overlap": semantic_score},
        "resume_profile": {"detected_skills": sorted(resume_skills), "approximate_years_mentioned": max(resume_years) if resume_years else None, "characters_analyzed": len(resume_text)},
        "job_profile": {"detected_skills": sorted(job_skills), "required_signals": sorted(required), "preferred_signals": sorted(preferred)},
        "matched_skills": matched, "missing_skills": missing, "skill_gaps": gaps,
        "strengths": strengths, "improvements": improvements,
        "score_disclaimer": "Heuristic estimate for guidance only—not a hiring probability or objective measure of candidate quality."
    }
