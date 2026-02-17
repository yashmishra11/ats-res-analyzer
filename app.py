"""
ATS Resume Analyzer - Main Application
Streamlit-based tool for analyzing resume-job match scores
WITH USER AUTHENTICATION AND ADMIN DASHBOARD
"""

import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

# Import custom modules
from nltk_setup import setup_nltk
from ui_components import (
    apply_custom_css, render_header, render_sidebar,
    render_section_card, render_pro_tips
)
from text_extractors import extract_text_from_pdf
from similarity_calculator import calculate_similarity, calculate_expected_score
from section_analyzer import analyze_sections
from visualization import create_section_impact_chart

from s3_utils import upload_pdf
from database import init_db, save_resume, is_uploads_enabled

# Authentication and admin
from auth import init_session_state, render_login_page, logout
from admin_dashboard import render_admin_dashboard

# Initialize
init_db()
setup_nltk()
init_session_state()

# Page configuration
st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()


def main():
    """Main application logic"""

    # ── Auth gate ────────────────────────────────────────────────────────────
    if not st.session_state.get('authenticated', False):
        render_login_page()
        return

    # ── Admin view ───────────────────────────────────────────────────────────
    if st.session_state.get('is_admin', False):
        render_admin_dashboard()
        return

    # ── Regular user view ────────────────────────────────────────────────────
    render_header()
    render_sidebar()

    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**Logged in as:** {st.session_state.user_email}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # Check upload status (shows warning but never blocks analysis)
    uploads_enabled = is_uploads_enabled()
    if not uploads_enabled:
        st.warning(
            "**.** "
        )

    # ── Inputs ───────────────────────────────────────────────────────────────
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            """
            <style>
                .upload-resume-heading {
                    font-size: 1.5rem;
                }
                .relocation-section {
                    margin-top: 50px;  /* Increased spacing */
                }
            </style>
            <div class="upload-resume-heading">
                📄 Upload Resume
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            "Drag and drop your resume here",
            type=['pdf'],
            help="Upload your resume in PDF format for analysis",
            label_visibility="collapsed"
        )
        st.markdown(
            """
            <div class="relocation-section">
                📍 Willing to relocate?
            </div>
            """,
            unsafe_allow_html=True
        )
        relocation_choice = st.radio(
            "relocation",
            options=["Yes", "No", "Not specified"],
            index=2,
            horizontal=True,
            label_visibility="collapsed"
        )
        relocation_preference = (
            True if relocation_choice == "Yes"
            else False if relocation_choice == "No"
            else None
        )

    with col2:
        st.markdown(
            """
            <style>
                .job-description-heading {
                    font-size: 1.5rem;
                }
                .analyze_button {
                    margin-top: 50px;
                }
            </style>
            <div class="job-description-heading">
                💼 Job Description
            </div>
            """,
            unsafe_allow_html=True
        )
        job_description = st.text_area(
            "Paste the complete job description",
            height=40,
            placeholder="Copy and paste the job posting here, including requirements, responsibilities, and qualifications...",
            label_visibility="collapsed"
        )

        # Create a container for the button with spacing
        st.markdown('<div class="analyze_button">', unsafe_allow_html=True)
        analyze_button = st.button("🔍 Analyze Resume Match", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)




    # ── Analysis ─────────────────────────────────────────────────────────────
    if analyze_button:
        if not uploaded_file:
            st.warning("⚠️ Please upload your resume to continue")
            return
        if not job_description:
            st.warning("⚠️ Please paste the job description to continue")
            return

        with st.spinner("👀 Analyzing your resume..."):

            # Extract text
            try:
                uploaded_file.seek(0)
                resume_text = extract_text_from_pdf(uploaded_file)
            except Exception as e:
                st.error(f"❌ Error reading PDF: {str(e)}")
                return

            if not resume_text:
                st.error("❌ Could not extract text from PDF. Please try another file.")
                return

            # Analyze
            sections = analyze_sections(resume_text, job_description, relocation_preference)
            similarity_score, _, _ = calculate_similarity(resume_text, job_description, sections)
            expected_score, potential_gain = calculate_expected_score(similarity_score, sections)

            # S3 upload (only if enabled)
            if uploads_enabled:
                try:
                    uploaded_file.seek(0)
                    uploaded_url = upload_pdf(uploaded_file)
                    save_resume(
                        uploaded_file.name,
                        uploaded_url,
                        similarity_score,
                        expected_score,
                        st.session_state.user_email
                    )
                    st.success("✅ Resume saved!")
                except Exception as e:
                    st.warning(f"⚠️ S3 upload error (analysis still works): {str(e)}")

            st.info(
                "ℹ️ Visual PDFs may affect section extraction. "
                "The analyzer uses semantic fallbacks where possible."
            )

            # Auto-scroll
            components.html("""
                <script>
                    setTimeout(function() {
                        const main = window.parent.document.querySelector('section.main');
                        if (main) { main.scrollBy({ top: 600, behavior: 'smooth' }); }
                    }, 100);
                </script>
            """, height=0)

            # ── Results ──────────────────────────────────────────────────────
            st.markdown("---")
            st.markdown("## 📈 Analysis Results")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="score-label">Current Match Score</div>', unsafe_allow_html=True)
                st.metric("", f"{similarity_score:.1f}%")
            with col2:
                st.markdown('<div class="score-label">Expected After Improvements</div>', unsafe_allow_html=True)
                st.metric("", f"{expected_score:.1f}%", delta=f"+{potential_gain:.1f}%", delta_color="normal")

            st.markdown("#### Section-by-Section Impact Analysis")
            fig = create_section_impact_chart(sections)
            st.pyplot(fig)
            plt.close()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("## 🔍 Section-by-Section Analysis")
            st.markdown("*Detailed breakdown of what needs attention in your resume*")

            for section in sections:
                render_section_card(section)

            st.markdown("---")
            render_pro_tips()


if __name__ == "__main__":
    main()