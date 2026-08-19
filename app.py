import streamlit as st
from reviewer import review_code

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeSense",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("🧠 CodeSense")

st.write(
    "Paste your code and get a professional AI code review."
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Review Settings")

    review_depth = st.selectbox(
        "Review Depth",
        [
            "Quick Scan",
            "Deep Review"
        ]
    )

    st.divider()

    st.write("### What CodeSense checks")

    st.write("🐞 Bugs")
    st.write("🔐 Security")
    st.write("⚡ Performance")
    st.write("📖 Readability")
    st.write("🧹 Code Quality")
    st.write("🔄 Refactoring")
    st.write("⏱️ Complexity")


# ============================================================
# CODE INPUT
# ============================================================

st.subheader("💻 Your Code")

code = st.text_area(
    "Paste your source code here",
    height=400,
    placeholder="""def calculate_sum(numbers):
    total = 0

    for number in numbers:
        total += number

    return total

print(calculate_sum([1, 2, 3, 4]))
""",
    label_visibility="collapsed"
)


# ============================================================
# REVIEW BUTTON
# ============================================================

if st.button(
    "🚀 Review Code",
    use_container_width=True
):

    if not code.strip():

        st.warning("Please enter some code first.")

    else:

        with st.spinner("🔍 CodeSense is reviewing your code..."):

            result = review_code(
                code,
                review_depth
            )

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        if result["status"] == "ERROR":

            st.error(
                result["message"]
            )

        # ----------------------------------------------------
        # NOT CODE
        # ----------------------------------------------------

        elif result["status"] == "NOT_CODE":

            st.warning(
                "⚠️ The input does not appear to be programming code."
            )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        else:

            st.success(
                "✅ Code review completed!"
            )

            st.divider()

            st.subheader("📋 Code Review")

            st.markdown(
                result["review"]
            )