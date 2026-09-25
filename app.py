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
            <div style="font-family: 'Orbitron', monospace; font-size: 1.25rem; font-weight: 700; color: #00d4ff; letter-spacing: 2px; margin-bottom: 8px;">
                [ 01 // INGEST RESUME ]
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #6b7280; margin-bottom: 12px;">
                FEED PDF DATASTREAM FOR VECTOR TOKENIZATION
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
            <div style="margin-top: 30px; font-family: 'Orbitron', monospace; font-size: 1.05rem; font-weight: 700; color: #ff00ff; letter-spacing: 1.5px; margin-bottom: 6px;">
                [ 02 // RELOCATION MOBILITY ]
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #6b7280; margin-bottom: 8px;">
                INDICATE PHYSICAL / REMOTE VECTOR AVAILABILITY
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
            <div style="font-family: 'Orbitron', monospace; font-size: 1.25rem; font-weight: 700; color: #00ff88; letter-spacing: 2px; margin-bottom: 8px;">
                [ 03 // TARGET SPECIFICATION ]
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #6b7280; margin-bottom: 12px;">
                PASTE RAW JOB DESCRIPTION // EXTRACT COMPLIANCE MATRIX
            </div>
            """,
            unsafe_allow_html=True
        )
        job_description = st.text_area(
            "Paste the complete job description",
            height=140,
            placeholder="> Paste target job posting specification (requirements, tech stack, qualifications)...",
            label_visibility="collapsed"
        )

        st.markdown('<div style="margin-top: 25px;">', unsafe_allow_html=True)
        analyze_button = st.button("⚡ EXECUTE NEURAL SCAN & MATCH", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)




    # ── Analysis ─────────────────────────────────────────────────────────────
    if analyze_button:
        if not uploaded_file:
            st.warning("⚠️ Please upload your resume to continue")
            return
        if not job_description:
            st.warning("⚠️ Please paste the job description to continue")
            return

        with st.spinner("⚡ INITIALIZING NEURAL MATRICES & EXECUTING SCAN..."):

            # Extract text
            try:
                uploaded_file.seek(0)
                resume_text = extract_text_from_pdf(uploaded_file)
            except Exception as e:
                st.error(f"❌ PDF_STREAM_CORRUPTION: {str(e)}")
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
                    st.success("✅ PAYLOAD ARCHIVED // S3 ENCRYPTED VAULT SYNCED")
                except Exception as e:
                    st.warning(f"⚠️ VAULT_UPLOAD_BYPASS: {str(e)}")

            st.info(
                "ℹ️ TELEMETRY_NOTE: Visual or multi-column PDFs can introduce OCR artifacts. "
                "Semantic neural fallbacks were deployed."
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
            <div style="margin-top: 15px; margin-bottom: 20px;">
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #00d4ff; letter-spacing: 3px;">
                    // TELEMETRY READOUT // SCAN COMPLETE //
                </div>
                <h2 style="font-family: 'Orbitron', monospace; font-size: 2.2rem; color: #ffffff; letter-spacing: 3px; margin: 4px 0 0 0;">
                    📈 RESUME COMPLIANCE MATRIX
                </h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="score-label">Current ATS Vector Match</div>', unsafe_allow_html=True)
                st.metric("", f"{similarity_score:.1f}%")
            with col2:
                st.markdown('<div class="score-label">Optimized Potential After Fixes</div>', unsafe_allow_html=True)
                st.metric("", f"{expected_score:.1f}%", delta=f"+{potential_gain:.1f}%", delta_color="normal")

            st.markdown("""
            <div style="font-family: 'Orbitron', monospace; font-size: 1.15rem; color: #00ff88; letter-spacing: 1.5px; margin-top: 25px; margin-bottom: 8px;">
                // SECTION-BY-SECTION TRAJECTORY ANALYSIS
            </div>
            """, unsafe_allow_html=True)
            fig = create_section_impact_chart(sections)
            st.pyplot(fig)
            plt.close()

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("""
            <div style="margin-top: 10px; margin-bottom: 20px;">
                <h2 style="font-family: 'Orbitron', monospace; font-size: 1.8rem; color: #ffffff; letter-spacing: 2px; margin: 0;">
                    🔍 SECTOR-BY-SECTOR DIAGNOSTIC
                </h2>
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #6b7280; letter-spacing: 1.5px; margin-top: 4px;">
                    // GRANULAR COMPONENT AUDIT OF RESUME DEFICITS &amp; HIGH-VALUE TARGETS
                </div>
            </div>
            """, unsafe_allow_html=True)

            for section in sections:
                render_section_card(section)

            st.markdown("---")
            render_pro_tips()


if __name__ == "__main__":
    main()