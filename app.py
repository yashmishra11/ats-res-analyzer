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
    initial_sidebar_state="collapsed"
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
    
    uploads_enabled = is_uploads_enabled()

    # ── Regular user view ────────────────────────────────────────────────────
    render_header()
    render_sidebar()

    with st.sidebar:
        st.markdown("---")
        st.markdown(f"**Logged in as:** {st.session_state.user_email}")
        if st.button("🚪 Logout", use_container_width=True):
            logout()


    # ── Inputs ───────────────────────────────────────────────────────────────
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <div class="circle-shape" style="width: 16px; height: 16px; background: #D02020; border: 2px solid #121212;"></div>
                <span style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 900; color: #121212; text-transform: uppercase; letter-spacing: 0.5px;">
                    01 // RESUME SPECIFICATION
                </span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 500; color: #444444; margin-bottom: 12px;">
                UPLOAD PDF ARTIFACT FOR VECTOR & KEYWORD EXTRACTION
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
            <div style="margin-top: 26px; display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <div style="width: 14px; height: 14px; background: #F0C020; border: 2px solid #121212; transform: rotate(45deg);"></div>
                <span style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 900; color: #121212; text-transform: uppercase; letter-spacing: 0.5px;">
                    02 // RELOCATION MOBILITY
                </span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 500; color: #444444; margin-bottom: 8px;">
                INDICATE PHYSICAL OR REMOTE AVAILABILITY
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
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <div style="width: 16px; height: 16px; background: #1040C0; border: 2px solid #121212;"></div>
                <span style="font-family: 'Outfit', sans-serif; font-size: 1.15rem; font-weight: 900; color: #121212; text-transform: uppercase; letter-spacing: 0.5px;">
                    03 // TARGET JOB SPECIFICATION
                </span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 500; color: #444444; margin-bottom: 12px;">
                PASTE RAW JOB DESCRIPTION TO EXTRACT COMPLIANCE CRITERIA
            </div>
            """,
            unsafe_allow_html=True
        )
        job_description = st.text_area(
            "Paste the complete job description",
            height=140,
            placeholder="Paste target job posting specification (responsibilities, required skills, qualifications)...",
            label_visibility="collapsed"
        )

        st.markdown('<div style="margin-top: 25px;">', unsafe_allow_html=True)
        analyze_button = st.button("■ EXECUTE ARCHITECTURAL SCAN & MATCH", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)




    # ── Analysis ─────────────────────────────────────────────────────────────
    if analyze_button:
        if not uploaded_file:
            st.warning("⚠️ Please upload your resume to continue")
            return
        if not job_description:
            st.warning("⚠️ Please paste the job description to continue")
            return

        with st.spinner("■ EXECUTING GEOMETRIC & VECTOR ANALYSIS..."):

            # Extract text
            try:
                uploaded_file.seek(0)
                resume_text = extract_text_from_pdf(uploaded_file)
            except Exception as e:
                st.error(f"❌ PDF_EXTRACTION_ERROR: {str(e)}")
                return

            if not resume_text:
                st.error("❌ ZERO_TEXT_PAYLOAD // Unreadable or image-only PDF stream.")
                return

            # Analyze
            sections = analyze_sections(resume_text, job_description, relocation_preference)
            similarity_score, _, _ = calculate_similarity(resume_text, job_description, sections)
            expected_score, potential_gain = calculate_expected_score(similarity_score, sections)

            # S3 upload (only if enabled)
            if uploads_enabled:
                try:
                    uploaded_file.seek(0)
                    file_size = getattr(uploaded_file, 'size', 0)
                    if not file_size:
                        file_size = len(uploaded_file.getvalue())
                    uploaded_file.seek(0)
                    uploaded_url = upload_pdf(uploaded_file)
                    save_resume(
                        uploaded_file.name,
                        uploaded_url,
                        similarity_score,
                        expected_score,
                        st.session_state.user_email,
                        file_size=file_size
                    )
                    st.success("✅ RESUME ARCHIVED // S3 STORAGE SYNCED")
                except Exception as e:
                    st.warning(f"⚠️ S3_STORAGE_BYPASS: {str(e)}")

            st.info(
                "ℹ️ NOTE: Complex visual formatting can impair ATS algorithmic parsing. "
                "Plain constructivist layouts maximize parsing fidelity."
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
            st.markdown("""
            <div style="margin-top: 15px; margin-bottom: 22px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <div class="circle-shape" style="width: 12px; height: 12px; background: #D02020; border: 2px solid #121212;"></div>
                    <span style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 800; color: #121212; letter-spacing: 2px; text-transform: uppercase;">
                        ANALYSIS COMPLETE // VERIFICATION MATRIX
                    </span>
                </div>
                <h2 style="font-size: 2.6rem; color: #121212; letter-spacing: -1px; margin: 0; font-weight: 900;">
                    RESUME COMPLIANCE MATRIX
                </h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2, gap="large")
            with col1:
                st.markdown("""
                <div style="background: #FFFFFF; border: 4px solid #121212; box-shadow: 6px 6px 0px 0px #121212; padding: 18px 24px; margin-bottom: 16px;">
                """, unsafe_allow_html=True)
                st.metric("Current ATS Vector Match", f"{similarity_score:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div style="background: #FFFFFF; border: 4px solid #121212; box-shadow: 6px 6px 0px 0px #121212; padding: 18px 24px; margin-bottom: 16px;">
                """, unsafe_allow_html=True)
                st.metric("Optimized Potential After Fixes", f"{expected_score:.1f}%", delta=f"+{potential_gain:.1f}%", delta_color="normal")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 28px; margin-bottom: 10px;">
                <div style="width: 14px; height: 14px; background: #1040C0; border: 2px solid #121212;"></div>
                <span style="font-family: 'Outfit', sans-serif; font-size: 1.25rem; font-weight: 900; color: #121212; text-transform: uppercase; letter-spacing: 0.5px;">
                    SECTOR-BY-SECTOR TRAJECTORY AUDIT
                </span>
            </div>
            """, unsafe_allow_html=True)
            fig = create_section_impact_chart(sections)
            st.pyplot(fig)
            plt.close()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("""
            <div style="margin-top: 10px; margin-bottom: 22px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                    <div style="width: 14px; height: 14px; background: #F0C020; border: 2px solid #121212; transform: rotate(45deg);"></div>
                    <span style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 800; color: #121212; letter-spacing: 2px; text-transform: uppercase;">
                        GRANULAR BREAKDOWN
                    </span>
                </div>
                <h2 style="font-size: 2.2rem; color: #121212; letter-spacing: -1px; margin: 0; font-weight: 900;">
                    ARCHITECTURAL COMPONENT DIAGNOSTIC
                </h2>
            </div>
            """, unsafe_allow_html=True)

            for section in sections:
                render_section_card(section)

            st.markdown("---")
            render_pro_tips()


if __name__ == "__main__":
    main()