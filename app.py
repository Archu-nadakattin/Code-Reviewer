import streamlit as st
import re
import html
from reviewer import review_code


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CodeSense",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# CodeSense testing

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99,102,241,0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(139,92,246,0.08),
            transparent 25%
        ),
        #09090b;

    color: #f4f4f5;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}


/* =========================================================
   HERO
========================================================= */

.hero {
    padding: 10px 0 30px 0;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #818cf8
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #a1a1aa;
    font-size: 16px;
    margin-top: 8px;
}


/* =========================================================
   CODE INPUT
========================================================= */

.input-title {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 12px;
}


/* =========================================================
   REVIEW HEADER
========================================================= */

.review-header {
    margin-top: 35px;
    margin-bottom: 22px;
}

.review-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
}

.review-meta {
    color: #71717a;
    font-size: 14px;
    margin-top: 5px;
}


/* =========================================================
   ANALYSIS CARDS
========================================================= */

.analysis-card {
    min-height: 160px;

    background: linear-gradient(
        145deg,
        rgba(24,24,27,0.96),
        rgba(18,18,21,0.96)
    );

    border: 1px solid #27272a;
    border-radius: 18px;

    padding: 22px;

    margin-bottom: 18px;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.analysis-card:hover {
    transform: translateY(-4px);

    border-color: #6366f1;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.35),
        0 0 20px rgba(99,102,241,0.08);
}

.card-icon {
    font-size: 25px;
    margin-bottom: 10px;
}

.card-heading {
    font-size: 13px;
    font-weight: 800;

    letter-spacing: 1.3px;

    color: #a1a1aa;
}

.card-value {
    font-size: 25px;
    font-weight: 800;

    color: #ffffff;

    margin-top: 8px;
}

.card-description {
    font-size: 13px;
    color: #71717a;

    margin-top: 5px;

    line-height: 1.5;

    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;

    overflow: hidden;
}


/* =========================================================
   CONTENT SECTIONS
========================================================= */

.content-section {
    background: rgba(24,24,27,0.70);

    border: 1px solid #27272a;

    border-radius: 18px;

    padding: 25px;

    margin-top: 20px;
}

.big-section-title {
    font-size: 21px;
    font-weight: 800;

    color: #ffffff;

    margin-bottom: 16px;
}


/* =========================================================
   METRIC BOX
========================================================= */

.metric-box {
    background: #111113;

    border: 1px solid #27272a;

    border-radius: 14px;

    padding: 18px;

    text-align: center;
}

.metric-label {
    color: #71717a;

    font-size: 12px;

    text-transform: uppercase;

    letter-spacing: 1px;
}

.metric-value {
    color: #ffffff;

    font-size: 28px;

    font-weight: 800;

    margin-top: 5px;
}


/* =========================================================
   BUTTON
========================================================= */

.stButton > button {

    width: 100%;

    height: 48px;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color: white;

    border: none;

    font-weight: 700;

    font-size: 15px;

    transition: all 0.2s ease;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 25px rgba(99,102,241,0.30);
}


/* =========================================================
   TEXT AREA
========================================================= */

textarea {

    background: #111113 !important;

    color: #f4f4f5 !important;

    border: 1px solid #27272a !important;

    border-radius: 14px !important;
}


/* =========================================================
   EXPANDER
========================================================= */

[data-testid="stExpander"] {

    background: #111113;

    border: 1px solid #27272a;

    border-radius: 14px;

    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("\\n", "\n")

    text = text.replace("\r", "")

    return text.strip()


def extract_section(text, start, end=None):

    if end:

        pattern = (
            rf"{re.escape(start)}\s*(.*?)"
            rf"(?={re.escape(end)}|$)"
        )

    else:

        pattern = rf"{re.escape(start)}\s*(.*)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return clean_text(match.group(1))

    return ""


def get_score(text):

    match = re.search(
        r"(?:score\s*:?\s*)?"
        r"(\d+(?:\.\d+)?)\s*/\s*(10|100)",
        text,
        re.IGNORECASE
    )

    if match:

        return (
            f"{match.group(1)}/{match.group(2)}"
        )

    return None


def get_complexity(text):

    time_match = re.search(
        r"Time Complexity\s*:?\s*(O\([^)]+\))",
        text,
        re.IGNORECASE
    )

    space_match = re.search(
        r"Space Complexity\s*:?\s*(O\([^)]+\))",
        text,
        re.IGNORECASE
    )

    time_complexity = (
        time_match.group(1)
        if time_match
        else "N/A"
    )

    space_complexity = (
        space_match.group(1)
        if space_match
        else "N/A"
    )

    return time_complexity, space_complexity


def has_issue(text):

    if not text:
        return False

    text = text.lower()

    no_issue_phrases = [
        "no major bugs",
        "no bugs",
        "no major security",
        "no security vulnerabilities",
        "no major performance",
        "no performance issues",
        "no issues detected",
        "none detected"
    ]

    for phrase in no_issue_phrases:

        if phrase in text:
            return False

    return True


# =========================================================
# HERO SECTION
# =========================================================

st.html("""
<div class="hero">

    <div class="hero-title">
        CodeSense
    </div>

    <div class="hero-subtitle">
        AI-powered code review, analysis and refactoring
    </div>

</div>
""")


# =========================================================
# CODE INPUT
# =========================================================

st.html("""
<div class="input-title">
    Code to Review
</div>
""")


code = st.text_area(
    "Code",
    height=300,

    placeholder="""Paste your code here...

Example:

def add(a, b):
    return a + b

print(add(2, 3))""",

    label_visibility="collapsed"
)


language = st.selectbox(
    "Language",

    [
        "Python",
        "Java",
        "C",
        "C++",
        "JavaScript"
    ]
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button("Analyze Code"):

    if not code.strip():

        st.warning(
            "Please enter some code first."
        )

        st.stop()


    # -----------------------------------------------------
    # AI REVIEW
    # -----------------------------------------------------

    with st.spinner(
        "Analyzing your code..."
    ):

        try:

            result = review_code(code)

        except Exception as e:

            st.error(
                f"Review failed: {e}"
            )

            st.stop()


    result_text = clean_text(result)


    # =====================================================
    # EXTRACT SECTIONS
    # =====================================================

    summary = extract_section(
        result_text,
        "SUMMARY",
        "BUGS"
    )

    bugs = extract_section(
        result_text,
        "BUGS",
        "SECURITY"
    )

    security = extract_section(
        result_text,
        "SECURITY",
        "PERFORMANCE"
    )

    performance = extract_section(
        result_text,
        "PERFORMANCE",
        "COMPLEXITY"
    )

    complexity = extract_section(
        result_text,
        "COMPLEXITY",
        "READABILITY"
    )

    readability = extract_section(
        result_text,
        "READABILITY",
        "CODE QUALITY"
    )

    quality = extract_section(
        result_text,
        "CODE QUALITY",
        "REFACTORING NOTES"
    )

    refactor = extract_section(
        result_text,
        "REFACTORING NOTES",
        "REFACTORED CODE"
    )


    # =====================================================
    # REFACTORED CODE
    # =====================================================

    refactored_match = re.search(
        r"REFACTORED CODE\s*"
        r"```(?:python|java|javascript|cpp|c)?\s*"
        r"(.*?)```",

        result_text,

        re.IGNORECASE | re.DOTALL
    )

    if refactored_match:

        refactored_code = clean_text(
            refactored_match.group(1)
        )

    else:

        refactored_code = ""


    # =====================================================
    # DYNAMIC VALUES
    # =====================================================

    readability_score = get_score(
        readability
    )

    if readability_score:

        readability_value = (
            readability_score
        )

    else:

        readability_value = "REVIEW"


    bug_issue = has_issue(bugs)

    security_issue = has_issue(
        security
    )

    performance_issue = has_issue(
        performance
    )


    bugs_value = (
        "REVIEW"
        if bug_issue
        else "0 ISSUES"
    )

    security_value = (
        "REVIEW"
        if security_issue
        else "LOW RISK"
    )

    performance_value = (
        "REVIEW"
        if performance_issue
        else "GOOD"
    )


    time_complexity, space_complexity = (
        get_complexity(complexity)
    )


    # =====================================================
    # REVIEW HEADER
    # =====================================================

    st.html("""
<div class="review-header">

    <div class="review-title">
        Code Review
    </div>

    <div class="review-meta">
        Analysis complete · Python
    </div>

</div>
""")


    # =====================================================
    # CARDS
    # =====================================================

    cards = [

        (
            "🐛",
            "BUGS",
            bugs_value,
            bugs
        ),

        (
            "🔐",
            "SECURITY",
            security_value,
            security
        ),

        (
            "⚡",
            "PERFORMANCE",
            performance_value,
            performance
        ),

        (
            "📖",
            "READABILITY",
            readability_value,
            readability
        ),

        (
            "🧹",
            "CODE QUALITY",
            "REVIEW",
            quality
        ),

        (
            "🔄",
            "REFACTORING",
            "AVAILABLE" if refactor else "NONE",
            refactor
        ),

        (
            "⏱",
            "COMPLEXITY",
            time_complexity,
            (
                f"Time: {time_complexity} · "
                f"Space: {space_complexity}"
            )
        )

    ]


    # =====================================================
    # FIRST ROW
    # =====================================================

    cols = st.columns(4)


    for i in range(4):

        icon, title, value, description = (
            cards[i]
        )

        description = clean_text(
            description
        )

        with cols[i]:

            st.html(f"""
<div class="analysis-card">

    <div class="card-icon">
        {html.escape(icon)}
    </div>

    <div class="card-heading">
        {html.escape(title)}
    </div>

    <div class="card-value">
        {html.escape(value)}
    </div>

    <div class="card-description">
        {html.escape(description[:140])}
    </div>

</div>
""")


    # =====================================================
    # SECOND ROW
    # =====================================================

    cols = st.columns(4)


    for i in range(4, 7):

        icon, title, value, description = (
            cards[i]
        )

        description = clean_text(
            description
        )

        with cols[i - 4]:

            st.html(f"""
<div class="analysis-card">

    <div class="card-icon">
        {html.escape(icon)}
    </div>

    <div class="card-heading">
        {html.escape(title)}
    </div>

    <div class="card-value">
        {html.escape(value)}
    </div>

    <div class="card-description">
        {html.escape(description[:140])}
    </div>

</div>
""")


    # =====================================================
    # OVERVIEW
    # =====================================================

    if summary:

        st.html("""
<div class="content-section">

    <div class="big-section-title">
        Overview
    </div>

</div>
""")

        st.write(summary)


    # =====================================================
    # COMPLEXITY
    # =====================================================

    if complexity:

        st.html("""
<div class="content-section">

    <div class="big-section-title">
        ⏱ Complexity
    </div>

</div>
""")

        col1, col2 = st.columns(2)


        with col1:

            st.html(f"""
<div class="metric-box">

    <div class="metric-label">
        Time Complexity
    </div>

    <div class="metric-value">
        {html.escape(time_complexity)}
    </div>

</div>
""")


        with col2:

            st.html(f"""
<div class="metric-box">

    <div class="metric-label">
        Space Complexity
    </div>

    <div class="metric-value">
        {html.escape(space_complexity)}
    </div>

</div>
""")


        st.write(complexity)


    # =====================================================
    # READABILITY
    # =====================================================

    if readability:

        st.html("""
<div class="content-section">

    <div class="big-section-title">
        📖 Readability
    </div>

</div>
""")

        st.write(readability)


    # =====================================================
    # CODE QUALITY
    # =====================================================

    if quality:

        st.html("""
<div class="content-section">

    <div class="big-section-title">
        🧹 Code Quality
    </div>

</div>
""")

        st.write(quality)


    # =====================================================
    # REFACTORING
    # =====================================================

    if refactor:

        st.html("""
<div class="content-section">

    <div class="big-section-title">
        🔄 Refactoring Suggestions
    </div>

</div>
""")

        st.write(refactor)


    # =====================================================
    # REFACTORED CODE
    # =====================================================

    if refactored_code:

        st.html("""
<div class="content-section">

    <div class="big-section-title">
        Refactored Code
    </div>

</div>
""")

        st.code(
            refactored_code,
            language=language.lower()
        )


    # =====================================================
    # DETAILED ANALYSIS
    # =====================================================

    with st.expander(
        "View Detailed Analysis"
    ):

        st.markdown(
            "### Bugs"
        )

        st.write(bugs)


        st.markdown(
            "### Security"
        )

        st.write(security)


        st.markdown(
            "### Performance"
        )

        st.write(performance)


    # =====================================================
    # SUCCESS
    # =====================================================

    st.success(
        "Code review completed successfully."
    )