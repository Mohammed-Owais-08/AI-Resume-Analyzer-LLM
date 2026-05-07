from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

def analyze_resume(resume_text, job_description):

    prompt = f"""
    Analyze the resume against the job description.

    Return the response EXACTLY in this format:

    MATCH_SCORE:
    MATCHING_SKILLS:
    MISSING_SKILLS:
    STRENGTHS:
    IMPROVEMENTS:
    FINAL_RECOMMENDATION:

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    prompt = f"""
        You are an ATS Resume Analyzer.

        Analyze the resume against the job description.

        IMPORTANT:
        Return ONLY in the following format.

        MATCH_SCORE:
        <number only>

        MATCHING_SKILLS:
                - skill 1
                - skill 2

        MISSING_SKILLS:
                - skill 1
                - skill 2

        STRENGTHS:
                - point 1
                - point 2

        IMPROVEMENTS:
                - point 1
                - point 2

        FINAL_RECOMMENDATION:
                - final recommendation

        Resume:
                {resume_text}

        Job Description:
                {job_description}
        """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return completion.choices[0].message.content