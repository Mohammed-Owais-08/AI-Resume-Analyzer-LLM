import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.analyzer import analyze_resume
import re

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("📄 AI Resume Analyzer & Job Match System")

st.markdown(
    """
    ### 🚀 AI-Powered Resume Intelligence Platform

    Optimize resumes for ATS systems, identify skill gaps,
    and improve job matching using LLM-powered analysis.
    """
)

st.divider()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
        This AI-powered application compares resumes with job
        descriptions and provides:

        - ATS Match Score
        - Skill Gap Analysis
        - Resume Strengths
        - Improvement Suggestions
        """
    )

    st.info("Powered by Llama 3.3 + Groq API")

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

with col2:

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

# ---------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------

if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        with st.spinner("AI is analyzing your resume..."):

            # Extract Resume Text
            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            # Analyze Resume
            result = analyze_resume(
                resume_text,
                job_description
            )

        st.success("Analysis Complete")

        # ---------------------------------------------------
        # PARSE AI RESPONSE
        # ---------------------------------------------------

        sections = {
            "MATCH_SCORE": [],
            "MATCHING_SKILLS": [],
            "MISSING_SKILLS": [],
            "STRENGTHS": [],
            "IMPROVEMENTS": [],
            "FINAL_RECOMMENDATION": []
        }

        current_section = None

        for line in result.splitlines():

            line = line.strip()

            if "MATCH_SCORE:" in line:
                current_section = "MATCH_SCORE"
                continue

            elif "MATCHING_SKILLS:" in line:
                current_section = "MATCHING_SKILLS"
                continue

            elif "MISSING_SKILLS:" in line:
                current_section = "MISSING_SKILLS"
                continue

            elif "STRENGTHS:" in line:
                current_section = "STRENGTHS"
                continue

            elif "IMPROVEMENTS:" in line:
                current_section = "IMPROVEMENTS"
                continue

            elif "FINAL_RECOMMENDATION:" in line:
                current_section = "FINAL_RECOMMENDATION"
                continue

            if current_section and line:
                sections[current_section].append(line)

        # ---------------------------------------------------
        # MATCH SCORE
        # ---------------------------------------------------

        st.subheader("📊 ATS Match Score")

        score_text = "\n".join(
            sections.get("MATCH_SCORE", ["0"])
        )

        score_match = re.search(
            r"\b\d{1,3}\b",
            score_text
        )

        score = (
            int(score_match.group())
            if score_match else 0
        )

        st.progress(score / 100)

        st.metric(
            label="Match Score",
            value=f"{score}%"
        )

        if score >= 80:
            st.success(
                f"Excellent Match: {score}%"
            )

        elif score >= 60:
            st.warning(
                f"Moderate Match: {score}%"
            )

        else:
            st.error(
                f"Low Match: {score}%"
            )

        st.divider()

        # ---------------------------------------------------
        # SKILLS SECTION
        # ---------------------------------------------------

        col3, col4 = st.columns(2)

        # MATCHING SKILLS

        with col3:

            st.subheader("✅ Matching Skills")

            matching_skills = sections.get(
                "MATCHING_SKILLS",
                []
            )

            if matching_skills:

                for skill in matching_skills:

                    skill = skill.replace("-", "").strip()

                    if skill:
                        st.success(skill)

            else:
                st.info(
                    "No matching skills found."
                )

        # MISSING SKILLS

        with col4:

            st.subheader("❌ Missing Skills")

            missing_skills = sections.get(
                "MISSING_SKILLS",
                []
            )

            if missing_skills:

                for skill in missing_skills:

                    skill = skill.replace("-", "").strip()

                    if skill:
                        st.error(skill)

            else:
                st.success(
                    "No missing skills detected."
                )

        st.divider()

        # ---------------------------------------------------
        # RESUME STRENGTHS
        # ---------------------------------------------------

        st.subheader("💪 Resume Strengths")

        strengths = sections.get(
            "STRENGTHS",
            []
        )

        if strengths:

            for item in strengths:

                item = item.replace("-", "").strip()

                if item:
                    st.info(item)

        else:
            st.warning(
                "No strengths identified."
            )

        # ---------------------------------------------------
        # IMPROVEMENTS
        # ---------------------------------------------------

        st.subheader("🛠 Suggested Improvements")

        improvements = sections.get(
            "IMPROVEMENTS",
            []
        )

        if improvements:

            for item in improvements:

                item = item.replace("-", "").strip()

                if item:
                    st.warning(item)

        else:
            st.success(
                "No major improvements suggested."
            )

        # ---------------------------------------------------
        # FINAL RECOMMENDATION
        # ---------------------------------------------------

        st.subheader("🎯 Final Recommendation")

        recommendations = sections.get(
            "FINAL_RECOMMENDATION",
            []
        )

        if recommendations:

            for item in recommendations:

                item = item.replace("-", "").strip()

                if item:
                    st.write(item)

        else:
            st.info(
                "No recommendation generated."
            )

    else:

        st.warning(
            "Please upload a resume and paste a job description."
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Built with Streamlit, Llama 3.3, and Groq API"
)