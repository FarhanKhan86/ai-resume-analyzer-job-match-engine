
import html
import json
import requests
import streamlit as st

st.set_page_config(
    page_title="NEXUS | Resume Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# FUTURISTIC UI THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080b14;
        --panel: rgba(18, 24, 42, 0.78);
        --border: rgba(150, 160, 255, 0.17);
        --text: #eef0ff;
        --muted: #8d97b5;
        --purple: #9b7bff;
        --cyan: #51e5ff;
        --green: #57f2bb;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse at 12% 10%,
                rgba(100, 62, 210, 0.19), transparent 35%),
            radial-gradient(ellipse at 88% 24%,
                rgba(0, 180, 220, 0.11), transparent 32%),
            #080b14;
    }

    [data-testid="stHeader"] {
        background: rgba(8, 11, 20, 0.65);
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes floatGlow {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 12px rgba(81,229,255,.12); }
        50% { box-shadow: 0 0 28px rgba(81,229,255,.3); }
    }

    @keyframes rotateBorder {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 35px;
        border: 1px solid var(--border);
        border-radius: 24px;
        background: linear-gradient(
            125deg,
            rgba(108, 76, 210, .18),
            rgba(15, 25, 47, .88) 55%,
            rgba(24, 83, 108, .15)
        );
        animation: fadeUp .75s ease both;
    }

    .hero:after {
        content: "";
        position: absolute;
        width: 250px;
        height: 250px;
        right: -80px;
        top: -100px;
        border-radius: 50%;
        border: 1px solid rgba(155,123,255,.2);
        box-shadow:
            0 0 0 30px rgba(155,123,255,.025),
            0 0 0 60px rgba(81,229,255,.02);
        pointer-events: none;
    }

    .eyebrow {
        color: var(--cyan);
        font-size: 11px;
        letter-spacing: 3px;
        font-weight: 800;
        text-transform: uppercase;
    }

    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        color: #f4f2ff;
        font-size: clamp(32px, 4vw, 54px);
        line-height: 1.1;
        letter-spacing: -2px;
        margin: 16px 0 12px;
    }

    .gradient-text {
        background: linear-gradient(90deg, #b39aff, #62e9ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .hero p {
        color: #a5afcb;
        font-size: 15px;
        line-height: 1.8;
        max-width: 650px;
    }

    .hero-chip {
        display: inline-block;
        margin-top: 14px;
        margin-right: 8px;
        padding: 8px 12px;
        border-radius: 30px;
        border: 1px solid var(--border);
        background: rgba(255,255,255,.035);
        color: #c9d1ed;
        font-size: 11px;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        color: #f0efff;
        font-size: 21px;
        font-weight: 700;
        margin: 24px 0 5px;
    }

    .section-subtitle {
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 18px;
    }

    .glass-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 14px;
        backdrop-filter: blur(16px);
        animation: fadeUp .6s ease both;
        transition: transform .25s ease,
                    border-color .25s ease,
                    box-shadow .25s ease;
    }

    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(155,123,255,.55);
        box-shadow: 0 12px 40px rgba(0,0,0,.22);
    }

    .card-label {
        color: #929dbd;
        font-size: 11px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-weight: 700;
    }

    .big-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: #f4f2ff;
        margin-top: 10px;
    }

    .muted {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.8;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--green);
        margin-right: 8px;
        box-shadow: 0 0 12px var(--green);
    }

    .ring-wrap {
        display: flex;
        justify-content: center;
        padding: 15px 0 20px;
    }

    .score-ring {
        width: 205px;
        height: 205px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: conic-gradient(
            from -90deg,
            #a58aff 0%,
            #51e5ff var(--score),
            rgba(255,255,255,.07) var(--score),
            rgba(255,255,255,.07) 100%
        );
        position: relative;
        animation: fadeUp .9s ease both;
        box-shadow: 0 0 35px rgba(155,123,255,.12);
    }

    .score-ring:before {
        content: "";
        position: absolute;
        inset: 9px;
        border-radius: 50%;
        background: #101426;
        border: 1px solid rgba(255,255,255,.06);
    }

    .score-content {
        position: relative;
        text-align: center;
        z-index: 1;
    }

    .score-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 47px;
        line-height: 1.2;
        font-weight: 700;
        color: #fff;
    }

    .score-caption {
        font-size: 10px;
        letter-spacing: 2px;
        color: var(--cyan);
        text-transform: uppercase;
    }

    .skill-chip {
        display: inline-block;
        padding: 8px 11px;
        margin: 4px 4px 4px 0;
        background: rgba(81,229,255,.07);
        border: 1px solid rgba(81,229,255,.2);
        border-radius: 9px;
        color: #a5efff;
        font-size: 12px;
        transition: all .2s ease;
    }

    .gap-chip {
        display: inline-block;
        padding: 8px 11px;
        margin: 4px 4px 4px 0;
        background: rgba(255,174,99,.07);
        border: 1px solid rgba(255,174,99,.2);
        border-radius: 9px;
        color: #ffc58e;
        font-size: 12px;
    }

    .insight {
        border-left: 2px solid var(--purple);
        background: rgba(155,123,255,.06);
        border-radius: 0 12px 12px 0;
        padding: 13px 15px;
        margin: 10px 0;
        color: #cbd1e8;
        font-size: 13px;
        line-height: 1.7;
    }

    .step-number {
        display: inline-flex;
        width: 30px;
        height: 30px;
        align-items: center;
        justify-content: center;
        background: rgba(155,123,255,.13);
        border: 1px solid rgba(155,123,255,.3);
        border-radius: 9px;
        color: #c3b2ff;
        font-weight: 700;
        margin-right: 10px;
    }

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        border: 1px solid rgba(183,158,255,.4);
        background: linear-gradient(100deg, #7854e8, #526cdb);
        color: white;
        font-weight: 700;
        transition: all .25s ease;
    }

    .stButton > button:hover {
        border-color: #a8eaff;
        box-shadow: 0 0 24px rgba(119,101,255,.3);
        transform: translateY(-2px);
        color: white;
    }

    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(155,123,255,.45);
        border-radius: 14px;
        padding: 12px;
        background: rgba(155,123,255,.035);
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        background: rgba(9,13,26,.8);
        color: #eef0ff;
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        background: rgba(18,24,42,.5);
    }

    hr {
        border-color: rgba(150,160,255,.12);
    }

    @media (prefers-reduced-motion: reduce) {
        *, *:before, *:after {
            animation: none !important;
            transition: none !important;
            scroll-behavior: auto !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">✦ PERSONAL CAREER INTELLIGENCE</div>
        <h1>Know your value.<br>
        <span class="gradient-text">Match your next move.</span></h1>
        <p>
            Turn your resume into actionable career intelligence.
            Discover your strengths, measure job alignment, and
            identify the skills that can help you move forward.
        </p>
        <span class="hero-chip">✦ AI-POWERED ANALYSIS</span>
        <span class="hero-chip">◈ EXPLAINABLE MATCHING</span>
        <span class="hero-chip">⌘ LOCAL PROCESSING</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="margin:22px 0 8px;color:#91a0c2;font-size:11px;
    letter-spacing:2px;font-weight:700;">
        <span class="status-dot"></span> ANALYSIS WORKSPACE
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# INPUT PANEL
# --------------------------------------------------
with st.container(border=True):
    st.markdown(
        '<div class="section-title">01 / Configure your analysis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Upload your resume and '
        'provide the target job description.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("⚙ Backend settings", expanded=False):
        api_url = st.text_input(
            "FastAPI URL",
            "http://127.0.0.1:8000",
        )

    col_resume, col_job = st.columns([0.85, 1.15], gap="large")

    with col_resume:
        st.markdown("**02 / Your resume**")
        resume = st.file_uploader(
            "Drop your resume here",
            type=["pdf", "docx", "txt"],
            help="Maximum file size depends on your backend configuration.",
        )

        if resume:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="card-label">FILE READY</div>
                    <div style="margin-top:10px;color:#b9a8ff;
                    font-weight:700;overflow-wrap:anywhere;">
                        ✦ {html.escape(resume.name)}
                    </div>
                    <div class="muted">
                        {resume.size / 1024:.1f} KB · Ready for analysis
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_job:
        st.markdown("**03 / Target opportunity**")
        jd = st.text_area(
            "Job description",
            height=235,
            placeholder=(
                "Paste the job description here...\n\n"
                "Include responsibilities, required skills, "
                "experience, and preferred qualifications."
            ),
        )

    analyze_btn = st.button(
        "✦  RUN INTELLIGENCE ANALYSIS",
        type="primary",
        use_container_width=True,
    )

# --------------------------------------------------
# API CALL
# --------------------------------------------------
if analyze_btn:
    if not resume:
        st.error("Please upload a resume first.")
    elif len(jd.strip()) < 40:
        st.error("Please enter a more complete job description (at least 40 characters).")
    else:
        try:
            with st.spinner("Analyzing profile signals and job alignment..."):
                response = requests.post(
                    f"{api_url.rstrip('/')}/analyze",
                    files={
                        "resume": (
                            resume.name,
                            resume.getvalue(),
                            resume.type or "application/octet-stream",
                        )
                    },
                    data={"job_description": jd},
                    timeout=90,
                )

            if response.status_code != 200:
                try:
                    detail = response.json().get("detail", "Analysis failed.")
                except ValueError:
                    detail = "The backend returned an unexpected response."
                st.error(str(detail))
            else:
                st.session_state["analysis"] = response.json()
                st.success("Analysis complete.")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to FastAPI. Make sure the backend "
                f"is running. Details: {exc}"
            )
        except ValueError:
            st.error("The backend returned invalid JSON.")

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
data = st.session_state.get("analysis")

if data:
    overall = max(0, min(100, int(data.get("overall_match", 0))))
    scores = data.get("scores", {})
    matched = data.get("matched_skills", [])
    gaps = data.get("skill_gaps", [])
    strengths = data.get("strengths", [])
    improvements = data.get("improvements", [])

    st.markdown(
        """
        <div class="section-title">04 / Intelligence report</div>
        <div class="section-subtitle">
            Your resume-to-role analysis, broken into explainable signals.
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_col, summary_col = st.columns([0.8, 1.2], gap="large")

    with score_col:
        st.markdown(
            f"""
            <div class="glass-card" style="text-align:center;">
                <div class="card-label">OVERALL MATCH ESTIMATE</div>
                <div class="ring-wrap">
                    <div class="score-ring"
                         style="--score:{overall}%;">
                        <div class="score-content">
                            <div class="score-value">{overall}%</div>
                            <div class="score-caption">Match index</div>
                        </div>
                    </div>
                </div>
                <div class="muted">
                    Heuristic estimate for guidance only—not a hiring
                    probability or objective measure of candidate quality.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with summary_col:
        st.markdown(
            '<div class="glass-card">'
            '<div class="card-label">MATCH BREAKDOWN</div>',
            unsafe_allow_html=True,
        )

        for label, value in scores.items():
            try:
                value = max(0, min(100, int(value)))
            except (TypeError, ValueError):
                value = 0

            st.markdown(
                f'<div style="display:flex;justify-content:space-between;'
                f'margin-top:15px;margin-bottom:7px;color:#cdd4ee;'
                f'font-size:12px;">'
                f'<span>{html.escape(label.replace("_", " ").title())}</span>'
                f'<b>{value}%</b></div>',
                unsafe_allow_html=True,
            )
            st.progress(value / 100)

        st.markdown("</div>", unsafe_allow_html=True)

    # Skill comparison
    skill_col, gap_col = st.columns(2, gap="large")

    with skill_col:
        st.markdown(
            '<div class="section-title">05 / Skill alignment</div>',
            unsafe_allow_html=True,
        )

        chips = "".join(
            f'<span class="skill-chip">{html.escape(str(skill))}</span>'
            for skill in matched
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">SKILLS FOUND IN BOTH</div>
                <div style="margin-top:14px;">
                    {chips if chips else
                    '<span class="muted">No shared skills detected.</span>'}
                </div>
                <div class="muted" style="margin-top:16px;">
                    Skills detected by the current skill dictionary.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with gap_col:
        st.markdown(
            '<div class="section-title">06 / Skill gaps</div>',
            unsafe_allow_html=True,
        )

        gap_chips = "".join(
            f'<span class="gap-chip">{html.escape(str(g.get("skill", "Unknown")))}</span>'
            for g in gaps
        )

        st.markdown(
            f"""
            <div class="glass-card">
                <div class="card-label">MISSING OR UNCONFIRMED</div>
                <div style="margin-top:14px;">
                    {gap_chips if gap_chips else
                    '<span class="muted">No gaps detected by the current skill dictionary.</span>'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for gap in gaps:
            with st.expander(
                f"{gap.get('skill', 'Skill')} · {gap.get('priority', 'Review')}"
            ):
                st.write(gap.get("recommendation", ""))

    # Insights
    st.markdown(
        '<div class="section-title">07 / Career insights</div>',
        unsafe_allow_html=True,
    )

    insight_col, plan_col = st.columns(2, gap="large")

    with insight_col:
        st.markdown(
            '<div class="card-label">WHY YOU MAY BE A MATCH</div>',
            unsafe_allow_html=True,
        )
        if strengths:
            for item in strengths:
                st.markdown(
                    f'<div class="insight">✦ {html.escape(str(item))}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No strengths were returned by the analyzer.")

    with plan_col:
        st.markdown(
            '<div class="card-label">YOUR IMPROVEMENT ROADMAP</div>',
            unsafe_allow_html=True,
        )
        if improvements:
            for i, item in enumerate(improvements, 1):
                st.markdown(
                    f'<div style="display:flex;align-items:flex-start;'
                    f'margin:12px 0;color:#cbd1e8;font-size:13px;'
                    f'line-height:1.7;">'
                    f'<span class="step-number">{i:02}</span>'
                    f'<span>{html.escape(str(item))}</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.write("No improvement suggestions were returned.")

    # Profile details: use JSON output instead of general st.write.
    st.markdown(
        '<div class="section-title">08 / Profile diagnostics</div>',
        unsafe_allow_html=True,
    )

    profile_col, job_col = st.columns(2, gap="large")

    with profile_col:
        with st.expander("◈ Extracted resume profile"):
            st.json(data.get("resume_profile", {}))

    with job_col:
        with st.expander("◈ Extracted job profile"):
            st.json(data.get("job_profile", {}))

    st.download_button(
        "↓  EXPORT ANALYSIS REPORT",
        data=json.dumps(data, indent=2, ensure_ascii=False),
        file_name="resume_match_report.json",
        mime="application/json",
        use_container_width=True,
    )

else:
    # Initial state
    st.markdown(
        """
        <div class="glass-card" style="text-align:center;padding:40px 20px;">
            <div style="font-size:42px;animation:floatGlow 4s ease-in-out infinite;">
                ◈
            </div>
            <div style="font-family:'Space Grotesk',sans-serif;
            font-size:22px;color:#e9e7ff;margin:15px 0 8px;">
                Your next opportunity starts here.
            </div>
            <div class="muted">
                Upload your resume, paste a job description, and run the
                analysis to reveal your matching skills and improvement plan.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="text-align:center;margin-top:45px;padding:20px;
    border-top:1px solid rgba(150,160,255,.12);">
        <div style="color:#9b8bd1;font-size:11px;letter-spacing:2px;">
            RESUME INTELLIGENCE SYSTEM
        </div>
        <div class="muted" style="margin-top:8px;">
            Built with Python · FastAPI · Streamlit
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
