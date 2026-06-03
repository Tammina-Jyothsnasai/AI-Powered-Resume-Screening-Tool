import streamlit as st
import base64
import os
import json
import PyPDF2
from pathlib import Path

# === Set Background Image and Text Color ===
def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                color: blue;
            }}
            h1, h2, h3, h4, h5, h6, label, .stTextInput > div > div > input,
            .stTextInput > div > div > label {{
                color: blue !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"⚠️ Background image not found at: {image_path}")

# === Load JSON Data ===
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# === Extract text from PDF ===
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# === Match Resume Text with Job Description ===
def match_jobs(resume_text, job_data):
    matches = []
    for job in job_data:
        skills = [s.strip() for s in job["description"].lower().split(",")]
        if any(skill in resume_text.lower() for skill in skills):
            matches.append(job["title"])
    return matches

# === Main App ===
def main():
    set_background("assets/background.jpg")

    st.title("🧠 Resume Screening Tool")
    st.header("📤 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        resume_path = Path("resumes") / uploaded_file.name
        with open(resume_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ Resume saved as **{uploaded_file.name}**")

        with open(resume_path, "rb") as f:
            resume_text = extract_text_from_pdf(f)

        st.subheader("📄 Resume Preview:")
        st.markdown(
            f"<div style='color:blue; font-size:14px; white-space:pre-wrap'>{resume_text}</div>",
            unsafe_allow_html=True
        )

        # === Load and Match Jobs ===
        job_data = load_json("C:/Users/H6jyo/PycharmProjects/Python/data/jobs.json")
        matched_jobs = match_jobs(resume_text, job_data)

        st.subheader("✅ Recommended Jobs:")
        if not matched_jobs:
            matched_jobs = [job["title"] for job in job_data[:3]]

        for job in job_data:
            if job["title"] in matched_jobs:
                st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 12px;
                            margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);">
                    <h4 style="color: blue;">🔹 {job['title']}</h4>
                    <p><b>🏢</b> {job['company']} — {job['location']}</p>
                    <p><b>💰</b> {job.get('salary', 'Not mentioned')}</p>
                    <p><b>📝</b> {job['description']}</p>
                </div>
                """, unsafe_allow_html=True)

    # === Internship & Hackathon Search ===
    st.header("🔎 Search Opportunities by Domain")
    search_term = st.text_input("Enter domain (e.g., AI, Web, Cybersecurity)")

    if search_term:
        internships = load_json("C:/Users/H6jyo/PycharmProjects/Python/data/internships.json")
        hackathons = load_json("C:/Users/H6jyo/PycharmProjects/Python/data/hackathons.json")

        matched_interns = [i for i in internships if search_term.lower() in i["domain"].lower()]
        matched_hackathons = [h for h in hackathons if search_term.lower() in h["domain"].lower()]

        st.subheader("🎓 Internships:")
        if matched_interns:
            for intern in matched_interns:
                st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4 style="color: blue;">🔹 {intern['name']}</h4>
                    <p><b>🏢</b> {intern['company']} — {intern['location']}</p>
                    <p><b>💰</b> Stipend: {intern['stipend']}</p>
                    <p><b>📝</b> {intern.get('description', 'No description provided')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching internships found.")

        st.subheader("🏆 Hackathons:")
        if matched_hackathons:
            for hack in matched_hackathons:
                st.markdown(f"""
                <div style="background-color: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h4 style="color: blue;">🏁 {hack['name']}</h4>
                    <p><b>🏢</b> {hack['company']} — {hack['location']}</p>
                    <p><b>💰</b> Prize: {hack['prize']}</p>
                    <p><b>📜</b> {hack['certificate']}</p>
                    <p><b>📝</b> {hack.get('description', 'No description provided')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matching hackathons found.")

if __name__ == "__main__":
    os.makedirs("resumes", exist_ok=True)
    main()
