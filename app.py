import streamlit as st
from pathlib import Path
import joblib

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResumeAI | Smart Recruitment",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PATHS AND MODEL
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "resume_classifier.joblib"

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ==============================
   GLOBAL THEME
============================== */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f8fc;
    color: #182230;
}

[data-testid="stAppViewContainer"] {
    background: #f6f8fc;
}

[data-testid="stMain"] {
    background: #f6f8fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* ==============================
   GLOBAL TEXT VISIBILITY
============================== */

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: #182230 !important;
}

.stApp p,
.stApp li,
.stApp label,
.stApp small,
.stApp [data-testid="stMarkdownContainer"] {
    color: #344054;
}

/* Text input, text area and select boxes */
.stApp input,
.stApp textarea {
    color: #182230 !important;
    background-color: #ffffff !important;
    -webkit-text-fill-color: #182230 !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #98a2b3 !important;
    -webkit-text-fill-color: #98a2b3 !important;
}

/* Select boxes */
.stApp [data-baseweb="select"] > div {
    background-color: #ffffff;
    color: #182230;
}

.stApp [data-baseweb="select"] span {
    color: #182230;
}

/* Radio buttons, checkboxes and captions */
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stCheckbox"] label,
.stApp [data-testid="stCaptionContainer"] {
    color: #344054 !important;
}

/* ==============================
   SIDEBAR
============================== */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10152f 0%, #202752 100%);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] input {
    color: #182230 !important;
}

/* ==============================
   HERO BANNER
============================== */

.hero {
    background: linear-gradient(
        120deg,
        #4338ca 0%,
        #6366f1 55%,
        #06b6d4 100%
    );
    padding: 32px;
    border-radius: 22px;
    color: #ffffff;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px rgba(79, 70, 229, 0.18);
}

.hero h1 {
    color: #ffffff !important;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #eef2ff !important;
    font-size: 15px;
    margin-bottom: 0;
}

.hero .small-badge {
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff !important;
}

/* ==============================
   DASHBOARD CARDS
============================== */

.metric-card {
    background: #ffffff;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #e8ebf4;
    box-shadow: 0 5px 18px rgba(31, 41, 55, 0.035);
    min-height: 130px;
}

.metric-label {
    color: #667085 !important;
    font-size: 13px;
    font-weight: 600;
}

.metric-value {
    color: #182230 !important;
    font-size: 29px;
    font-weight: 800;
    margin-top: 12px;
}

.metric-note {
    color: #667085 !important;
    font-size: 12px;
    margin-top: 5px;
}

.section-title {
    color: #182230 !important;
    font-size: 22px;
    font-weight: 750;
    margin-top: 24px;
    margin-bottom: 14px;
}

.info-card {
    background: #ffffff;
    border: 1px solid #e8ebf4;
    border-radius: 16px;
    padding: 22px;
    min-height: 150px;
}

.info-card h3 {
    color: #182230 !important;
    font-size: 17px;
}

.info-card p {
    color: #667085 !important;
    font-size: 13px;
    line-height: 1.7;
}

.small-badge {
    background: #eef2ff;
    color: #4338ca !important;
    display: inline-block;
    border-radius: 20px;
    padding: 5px 11px;
    font-size: 11px;
    font-weight: 700;
}

/* ==============================
   STREAMLIT METRICS
============================== */

div[data-testid="stMetric"] {
    background: #ffffff;
    padding: 18px;
    border: 1px solid #e8ebf4;
    border-radius: 15px;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] label *,
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #182230 !important;
}

/* ==============================
   FILE UPLOADER
============================== */

[data-testid="stFileUploader"] {
    background: #ffffff;
    color: #182230;
}

[data-testid="stFileUploader"] section {
    background: #ffffff;
    border-color: #d0d5dd;
}

[data-testid="stFileUploader"] section * {
    color: #344054 !important;
}

[data-testid="stFileUploader"] button {
    color: #ffffff !important;
}

/* ==============================
   TABLES AND DATAFRAMES
============================== */

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #ffffff;
}

[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
    color: #182230;
}

/* ==============================
   BUTTONS
============================== */

/* Consistent, readable buttons */
.stButton > button,
.stDownloadButton > button {
    background-color: #4f46e5 !important;
    color: #ffffff !important;
    border: 1px solid #4f46e5 !important;
    border-radius: 10px;
    font-weight: 600;
    min-height: 43px;
}

.stButton > button *,
.stDownloadButton > button * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #3730a3 !important;
    border-color: #3730a3 !important;
}

/* Improve the file uploader text */
[data-testid="stFileUploader"] button {
    background-color: #4f46e5 !important;
    color: #ffffff !important;
}

.stButton > button p,
.stDownloadButton > button p {
    color: inherit !important;
}

/* ==============================
   ALERTS AND EXPANDERS
============================== */

[data-testid="stAlert"] p,
[data-testid="stAlert"] li {
    color: inherit;
}

[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #e8ebf4;
    border-radius: 12px;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #182230 !important;
}

/* ==============================
   FOOTER
============================== */

.footer {
    text-align: center;
    color: #98a2b3 !important;
    font-size: 12px;
    padding-top: 35px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None

model_bundle = load_model()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown("# 🎯 ResumeAI")
    st.caption("SMART RECRUITMENT PLATFORM")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Screen Resumes",
            "Job Matcher",
            "Candidate Comparison",
            "Model Insights",
            "About Project"
        ],
        label_visibility="visible"
    )

    st.markdown("---")

    st.markdown("### 🤖 AI Status")

    if model_bundle is not None:
        st.success("ML model loaded")
    else:
        st.error("Model file not found")

    st.markdown(
        """
        <div style="font-size:12px; color:#c7d2fe;">
        ResumeAI helps recruiters organize resumes and explore
        job-related skills. Always review candidates fairly.
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------
if page == "Dashboard":

    import pandas as pd

    # --------------------------------------------------
    # HERO SECTION
    # --------------------------------------------------

    st.markdown("""
    <div class="hero">
        <span class="small-badge">AI-POWERED RECRUITMENT</span>
        <h1>Find the right talent, smarter.</h1>
        <p>
        Analyze resumes, explore professional categories, and compare
        job-related skills in one workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------
    # MODEL STATISTICS
    # --------------------------------------------------

    accuracy = None
    category_count = 0
    training_count = 0

    if model_bundle:
        accuracy = model_bundle.get("test_accuracy")
        category_count = len(model_bundle.get("categories", []))
        training_count = model_bundle.get("training_samples", 0)

    # Read the latest screening results from the session
    screening_results = st.session_state.get(
        "quick_job_results", []
    )

    results_df = pd.DataFrame(screening_results)

    if not results_df.empty and "Status" in results_df.columns:
        successful_results = results_df[
            results_df["Status"] == "Analyzed"
        ].copy()
    else:
        successful_results = pd.DataFrame()

    resumes_screened = len(successful_results)

    if (
        not successful_results.empty
        and "Skill Match (%)" in successful_results.columns
    ):
        average_match = successful_results[
            "Skill Match (%)"
        ].mean()
    else:
        average_match = None

    # --------------------------------------------------
    # STATISTICS CARDS
    # --------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AI MODEL</div>
            <div class="metric-value">
                {"Ready" if model_bundle else "Offline"}
            </div>
            <div class="metric-note">Classification pipeline</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        accuracy_text = (
            f"{accuracy:.1%}"
            if accuracy is not None
            else "N/A"
        )

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TEST ACCURACY</div>
            <div class="metric-value">{accuracy_text}</div>
            <div class="metric-note">
                Professional-category classification
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CATEGORIES</div>
            <div class="metric-value">{category_count}</div>
            <div class="metric-note">Professional categories</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TRAINING SAMPLES</div>
            <div class="metric-value">{training_count:,}</div>
            <div class="metric-note">Resumes used for training</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------
    # SCREENING OVERVIEW
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">Screening Overview</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Resumes Screened",
        resumes_screened,
        help="Successfully analyzed resumes in the current session."
    )

    s2.metric(
        "Average Skill Match",
        (
            f"{average_match:.1f}%"
            if average_match is not None
            else "N/A"
        ),
        help="Average percentage of selected skills detected."
    )

    s3.metric(
        "Selected Job Role",
        st.session_state.get("quick_job_role", "Not selected")
    )

    # --------------------------------------------------
    # LATEST SCREENING RESULTS
    # --------------------------------------------------

    if not successful_results.empty:

        st.markdown(
            '<div class="section-title">Latest Screening Results</div>',
            unsafe_allow_html=True
        )

        display_columns = [
            column for column in [
                "Resume",
                "Job Role",
                "Predicted Category",
                "Skill Match (%)",
                "Matched Skills",
                "Missing Skills"
            ]
            if column in successful_results.columns
        ]

        st.dataframe(
            successful_results[display_columns].sort_values(
                "Skill Match (%)",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # SKILL MATCH CHART
        # --------------------------------------------------

        st.markdown("### Skill Match Comparison")

        chart_data = successful_results[
            ["Resume", "Skill Match (%)"]
        ].copy()

        chart_data = chart_data.sort_values(
            "Skill Match (%)",
            ascending=False
        ).head(10)

        chart_data = chart_data.set_index("Resume")

        st.bar_chart(
            chart_data,
            y="Skill Match (%)"
        )

        st.caption(
            "The chart displays the top 10 resumes by skill-match "
            "percentage from the latest screening run."
        )

    else:

        st.info(
            "No screening results are available yet. Open Screen Resumes, "
            "upload resumes, and run a screening to see your statistics "
            "and chart here."
        )

    # --------------------------------------------------
    # RECRUITMENT WORKSPACE
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">Your recruitment workspace</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="info-card">
            <h3>📄 Resume Screening</h3>
            <p>
            Upload resumes and classify their professional categories
            using your trained machine-learning model.
            </p>
            <span class="small-badge">TF-IDF + SVM</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Resume Screening",
            use_container_width=True
        ):
            st.session_state["requested_page"] = "Screen Resumes"
            st.rerun()

    with col2:

        st.markdown("""
        <div class="info-card">
            <h3>🎯 Job Matcher</h3>
            <p>
            Compare job requirements with resume text to explore
            keyword overlap and potential skill gaps.
            </p>
            <span class="small-badge">TEXT ANALYSIS</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Job Matcher",
            use_container_width=True
        ):
            st.session_state["requested_page"] = "Job Matcher"
            st.rerun()

    with col3:

        st.markdown("""
        <div class="info-card">
            <h3>📊 Model Insights</h3>
            <p>
            Review classifier evaluation results and inspect
            the confusion matrix generated during training.
            </p>
            <span class="small-badge">MODEL EVALUATION</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "View Model Insights",
            use_container_width=True
        ):
            st.session_state["requested_page"] = "Model Insights"
            st.rerun()

    # --------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">How ResumeAI works</div>',
        unsafe_allow_html=True
    )

    st.info(
        "1. Upload a resume  →  "
        "2. Extract its text  →  "
        "3. Analyze the content  →  "
        "4. Review results and export them."
    )

    st.warning(
        "Important: The trained model predicts professional categories, "
        "not hiring suitability. Skill matching checks for selected "
        "keywords and does not measure overall candidate quality. "
        "Always review resumes manually before making hiring decisions."
    )
# --------------------------------------------------
# RESUME SCREENING — QUICK JOB MATCH
# --------------------------------------------------

elif page == "Screen Resumes":

    import re
    from io import BytesIO
    import pandas as pd
    import fitz
    from docx import Document

    st.title("📄 Smart Resume Screening")
    st.write(
        "Choose a job role, select its required skills, and upload "
        "resumes. No lengthy job description required."
    )

    # Suggested skills for each role
    ROLE_SKILLS = {
        "Software Developer": [
            "Python", "C++", "Java", "SQL",
            "Data Structures", "Git", "Problem Solving"
        ],
        "Web Developer": [
            "HTML", "CSS", "JavaScript", "React",
            "Node.js", "SQL", "Git"
        ],
        "AI/ML Engineer": [
            "Python", "Machine Learning", "NumPy",
            "pandas", "scikit-learn", "SQL", "Deep Learning"
        ],
        "Data Analyst": [
            "SQL", "Python", "Excel", "Power BI",
            "Tableau", "pandas", "Statistics"
        ],
        "Data Scientist": [
            "Python", "SQL", "Statistics", "Machine Learning",
            "pandas", "NumPy", "Data Visualization"
        ],
        "Cybersecurity Analyst": [
            "Networking", "Linux", "Cybersecurity",
            "SIEM", "Python", "Incident Response"
        ],
        "HR Executive": [
            "Recruitment", "Communication", "Excel",
            "Interviewing", "HR Management", "Documentation"
        ],
        "Digital Marketing Executive": [
            "SEO", "Social Media", "Google Analytics",
            "Content Writing", "SEM", "Marketing"
        ],
        "Other": [
            "Communication", "Problem Solving",
            "Teamwork", "Python"
        ]
    }

    # Normalize common spelling variations
    SKILL_ALIASES = {
        "python": ["python"],
        "c++": ["c++", "cpp"],
        "java": ["java"],
        "sql": ["sql", "mysql", "postgresql", "sqlite"],
        "data structures": ["data structures", "dsa"],
        "problem solving": ["problem solving", "problem-solving"],
        "html": ["html", "html5"],
        "css": ["css", "css3"],
        "javascript": ["javascript", "java script"],
        "react": ["react", "react.js", "reactjs"],
        "node.js": ["node.js", "nodejs"],
        "git": ["git", "github"],
        "machine learning": ["machine learning", "ml"],
        "numpy": ["numpy"],
        "pandas": ["pandas"],
        "scikit-learn": ["scikit-learn", "sklearn"],
        "deep learning": ["deep learning"],
        "excel": ["excel", "microsoft excel"],
        "power bi": ["power bi", "powerbi"],
        "tableau": ["tableau"],
        "statistics": ["statistics", "statistical analysis"],
        "data visualization": ["data visualization", "data visualisation"],
        "networking": ["networking", "computer networks"],
        "linux": ["linux"],
        "cybersecurity": ["cybersecurity", "cyber security"],
        "siem": ["siem"],
        "incident response": ["incident response"],
        "recruitment": ["recruitment", "talent acquisition"],
        "communication": ["communication", "communication skills"],
        "interviewing": ["interviewing", "interview"],
        "hr management": ["hr management", "human resources"],
        "documentation": ["documentation"],
        "seo": ["seo", "search engine optimization"],
        "social media": ["social media"],
        "google analytics": ["google analytics"],
        "content writing": ["content writing", "copywriting"],
        "sem": ["sem", "search engine marketing"],
        "marketing": ["marketing", "digital marketing"],
        "teamwork": ["teamwork", "team work"]
    }

    # Select a single role
    role = st.selectbox(
        "1. Select the job role",
        list(ROLE_SKILLS.keys())
    )

    # Default skills for the chosen role
    default_skills = ROLE_SKILLS[role]

    selected_skills = st.multiselect(
        "2. Select required skills",
        options=sorted(set(
            skill
            for skills in ROLE_SKILLS.values()
            for skill in skills
        )),
        default=default_skills,
        help="Suggested skills are preselected. Remove or add skills as needed."
    )

    st.caption(
        f"{len(selected_skills)} skill(s) selected for the {role} role."
    )

    # Optional experience requirement
    experience = st.selectbox(
        "3. Minimum experience (optional)",
        [
            "Not specified",
            "Fresher / Entry-level",
            "0–2 years",
            "2–5 years",
            "5+ years"
        ]
    )

    st.caption(
        "Experience is recorded as a requirement but is not automatically "
        "scored in this version. Skill matching is based on resume text."
    )

    st.markdown("### 4. Upload resumes")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="quick_job_resume_upload"
    )

    if st.button("🔍 Screen Resumes", type="primary"):

        if not selected_skills:
            st.warning("Please select at least one required skill.")

        elif not uploaded_files:
            st.warning("Please upload at least one resume.")

        else:
            results = []
            extracted_texts = {}

            for uploaded_file in uploaded_files:
                filename = uploaded_file.name
                resume_text = ""

                try:
                    file_bytes = uploaded_file.getvalue()

                    if filename.lower().endswith(".pdf"):
                        with fitz.open(
                            stream=file_bytes,
                            filetype="pdf"
                        ) as pdf:
                            resume_text = " ".join(
                                page.get_text() for page in pdf
                            )

                    elif filename.lower().endswith(".docx"):
                        document = Document(BytesIO(file_bytes))
                        resume_text = "\n".join(
                            paragraph.text
                            for paragraph in document.paragraphs
                        )

                    elif filename.lower().endswith(".txt"):
                        resume_text = file_bytes.decode(
                            "utf-8",
                            errors="ignore"
                        )

                    resume_text = " ".join(resume_text.split())

                    if not resume_text:
                        results.append({
                            "Resume": filename,
                            "Job Role": role,
                            "Predicted Category": "Unavailable",
                            "Matched Skills": "",
                            "Missing Skills": ", ".join(selected_skills),
                            "Matched Skill Count": 0,
                            "Required Skill Count": len(selected_skills),
                            "Skill Match (%)": 0,
                            "Status": "No text extracted"
                        })
                        continue

                    extracted_texts[filename] = resume_text

                    # Match skills using whole-word/phrase boundaries
                    resume_lower = resume_text.lower()
                    matched = []
                    missing = []

                    for skill in selected_skills:
                        aliases = SKILL_ALIASES.get(
                            skill.lower(),
                            [skill.lower()]
                        )

                        found = any(
                            re.search(
                                r"(?<![a-z0-9])"
                                + re.escape(alias)
                                + r"(?![a-z0-9])",
                                resume_lower
                            )
                            for alias in aliases
                        )

                        if found:
                            matched.append(skill)
                        else:
                            missing.append(skill)

                    match_percentage = (
                        len(matched) / len(selected_skills) * 100
                        if selected_skills else 0
                    )

                    # Keep professional-category prediction separate
                    predicted_category = "Unavailable"

                    if model_bundle:
                        predicted_category = model_bundle["model"].predict(
                            [resume_text]
                        )[0]

                    results.append({
                        "Resume": filename,
                        "Job Role": role,
                        "Predicted Category": predicted_category,
                        "Matched Skills": ", ".join(matched),
                        "Missing Skills": ", ".join(missing),
                        "Matched Skill Count": len(matched),
                        "Required Skill Count": len(selected_skills),
                        "Skill Match (%)": round(match_percentage, 1),
                        "Status": "Analyzed"
                    })

                except Exception as error:
                    results.append({
                        "Resume": filename,
                        "Job Role": role,
                        "Predicted Category": "Unavailable",
                        "Matched Skills": "",
                        "Missing Skills": "",
                        "Matched Skill Count": 0,
                        "Required Skill Count": len(selected_skills),
                        "Skill Match (%)": 0,
                        "Status": f"Error: {str(error)[:100]}"
                    })

            st.session_state["quick_job_results"] = results
            st.session_state["quick_job_role"] = role
            st.session_state["quick_job_skills"] = selected_skills

    # Display results after screening
    if "quick_job_results" in st.session_state:

        results_df = pd.DataFrame(
            st.session_state["quick_job_results"]
        )

        st.markdown("---")
        st.subheader("📊 Screening Results")

        successful = results_df[
            results_df["Status"] == "Analyzed"
        ].copy()

        if not successful.empty:
            successful = successful.sort_values(
                "Skill Match (%)",
                ascending=False
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Resumes Analyzed",
                len(successful)
            )

            col2.metric(
                "Selected Job Role",
                st.session_state["quick_job_role"]
            )

            col3.metric(
                "Average Skill Match",
                f"{successful['Skill Match (%)'].mean():.1f}%"
            )

            st.dataframe(
                successful[
                    [
                        "Resume",
                        "Predicted Category",
                        "Skill Match (%)",
                        "Matched Skills",
                        "Missing Skills",
                        "Status"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            csv_data = results_df.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "⬇️ Download Screening Results (CSV)",
                data=csv_data,
                file_name="resume_screening_results.csv",
                mime="text/csv"
            )

            st.caption(
                "Skill match = percentage of selected skills detected in "
                "the extracted resume text. Missing skills may be present "
                "but expressed differently. This score is not a hiring "
                "probability or a validated measure of candidate quality. "
                "Review resumes manually before making decisions."
            )

        else:
            st.warning(
                "No resumes were analyzed successfully. Check the status "
                "column below for details."
            )

        with st.expander("View all screening records"):
            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True
            )
# --------------------------------------------------
# JOB MATCHER
# --------------------------------------------------

elif page == "Job Matcher":

    st.title("🎯 Job Description Matcher")
    st.write(
        "Explore how closely the text of a resume overlaps with a job "
        "description. This is a keyword-based comparison, not a validated "
        "probability of job success."
    )

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder="Paste responsibilities, required skills, and qualifications..."
    )

    resume_text = st.text_area(
        "Paste resume text",
        height=220,
        placeholder="Paste the candidate's resume text..."
    )

    if st.button("Compare Resume and Job", type="primary"):
        import re
        from collections import Counter

        def extract_keywords(text):
            words = re.findall(r"[a-zA-Z][a-zA-Z+#.]{1,}", text.lower())

            stop_words = {
                "the", "and", "for", "with", "from", "this", "that",
                "you", "your", "our", "are", "was", "were", "will",
                "have", "has", "had", "can", "all", "not", "but",
                "job", "work", "working", "candidate", "role", "team",
                "ability", "strong", "good", "excellent", "required",
                "responsibilities", "experience", "skills"
            }

            return {
                word for word in words
                if word not in stop_words and len(word) > 2
            }

        if not job_description.strip() or not resume_text.strip():
            st.error("Please enter both the job description and resume text.")
        else:
            job_keywords = extract_keywords(job_description)
            resume_keywords = extract_keywords(resume_text)

            matched = sorted(job_keywords & resume_keywords)
            missing = sorted(job_keywords - resume_keywords)

            if job_keywords:
                match_percentage = (
                    len(matched) / len(job_keywords)
                ) * 100
            else:
                match_percentage = 0

            col1, col2, col3 = st.columns(3)

            col1.metric("Keyword Overlap", f"{match_percentage:.1f}%")
            col2.metric("Matched Keywords", len(matched))
            col3.metric("Unmatched Job Keywords", len(missing))

            st.progress(int(match_percentage))

            left, right = st.columns(2)

            with left:
                st.subheader("✅ Keywords Found")
                if matched:
                    st.write(", ".join(matched))
                else:
                    st.write("No shared keywords found.")

            with right:
                st.subheader("🔎 Keywords Not Found")
                if missing:
                    st.write(", ".join(missing))
                else:
                    st.write("All extracted job keywords were found.")

            st.caption(
                "This percentage is the share of extracted job-description "
                "keywords found in the resume. It is not a hiring probability "
                "or a measure of candidate quality."
            )

# --------------------------------------------------
# CANDIDATE COMPARISON
# --------------------------------------------------

elif page == "Candidate Comparison":

    st.title("⚖️ Candidate Comparison")
    st.write("Compare two resume texts side by side.")

    candidate1 = st.text_area(
        "Candidate A — Resume Text",
        height=230
    )

    candidate2 = st.text_area(
        "Candidate B — Resume Text",
        height=230
    )

    if st.button("Compare Candidates", type="primary"):
        if not candidate1.strip() or not candidate2.strip():
            st.error("Please enter resume text for both candidates.")
        else:
            import re

            def words(text):
                return set(
                    re.findall(r"[a-zA-Z][a-zA-Z+#.]{1,}", text.lower())
                )

            words_a = words(candidate1)
            words_b = words(candidate2)
            common = words_a & words_b

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Candidate A")
                st.metric("Unique Words", len(words_a))
                st.metric("Words Shared With B", len(common))

            with col2:
                st.subheader("Candidate B")
                st.metric("Unique Words", len(words_b))
                st.metric("Words Shared With A", len(common))

            st.info(
                "Word counts are descriptive only. They do not establish "
                "which candidate is better qualified."
            )

# --------------------------------------------------
# MODEL INSIGHTS
# --------------------------------------------------

elif page == "Model Insights":

    st.title("📊 Model Insights")
    st.write("Review the evaluation output from your trained classifier.")

    if model_bundle:
        st.metric(
            "Held-Out Test Accuracy",
            f"{model_bundle['test_accuracy']:.2%}"
        )

        st.metric(
            "Training Samples",
            model_bundle["training_samples"]
        )

        st.metric(
            "Testing Samples",
            model_bundle["testing_samples"]
        )

        st.subheader("Professional Categories")
        st.write(", ".join(model_bundle["categories"]))

        confusion_path = PROJECT_DIR / "models" / "confusion_matrix.png"

        if confusion_path.exists():
            st.subheader("Confusion Matrix")
            st.image(
                str(confusion_path),
                caption="Predicted versus actual professional categories",
                use_container_width=True
            )
    else:
        st.error(
            "The model could not be loaded. Please run "
            "`python src/train_model.py` first."
        )

# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

elif page == "About Project":

    st.title("ℹ️ About ResumeAI")

    st.markdown("""
    ResumeAI is a machine-learning-assisted recruitment prototype.

    **Technology stack**
    - Python
    - Streamlit
    - Scikit-learn
    - TF-IDF text vectorization
    - Linear Support Vector Machine (SVM)
    - PyMuPDF for PDF text extraction
    - python-docx for DOCX text extraction

    **Current capabilities**
    - Professional-category classification
    - PDF, DOCX, and TXT resume uploads
    - Keyword overlap analysis against job descriptions
    - Side-by-side resume text comparison
    - CSV export
    - Model evaluation visualization

    **Limitations**

    The training dataset labels resumes by professional category.
    It does not label candidates as suitable or unsuitable for a specific
    vacancy. The keyword matcher is a simple text-overlap tool, not a
    validated hiring score.

    Use this application to assist human review, not to make automatic
    hiring or rejection decisions.
    """)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    ResumeAI • Machine Learning Recruitment Prototype • Built with Python
</div>
""", unsafe_allow_html=True)