"""
UI Components for ATS Resume Analyzer
Bauhaus Design System Implementation
Form follows function: Geometric purity, constructivist typography,
hard offset shadows, stark black borders, and primary color blocking
(Bauhaus Red #D02020, Bauhaus Blue #1040C0, Bauhaus Yellow #F0C020).
"""

import streamlit as st
import re
from config import (
    APP_TITLE, APP_ICON, APP_VERSION,
    BACKGROUND_COLOR, CARD_COLOR, ACCENT_COLOR, ACCENT_SECONDARY, ACCENT_TERTIARY,
    BORDER_COLOR, DESTRUCTIVE_COLOR, WARNING_COLOR,
    BAUHAUS_RED, BAUHAUS_BLUE, BAUHAUS_YELLOW, BAUHAUS_BLACK, BAUHAUS_WHITE
)


def apply_custom_css():
    """Apply the Bauhaus Design System CSS to Streamlit"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;700;800;900&display=swap');

        /* ── Bauhaus Design Tokens ────────────────────────────────── */
        :root {{
            --bauhaus-bg: #F0F0F0;
            --bauhaus-fg: #121212;
            --bauhaus-card: #FFFFFF;
            --bauhaus-muted: #E0E0E0;
            --bauhaus-red: #D02020;
            --bauhaus-blue: #1040C0;
            --bauhaus-yellow: #F0C020;
            --bauhaus-black: #121212;
            --bauhaus-white: #FFFFFF;
            --bauhaus-border: #121212;
            --font-outfit: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* ── Canvas & Dot Grid Texture ───────────────────────────── */
        .stApp, .main {{
            background-color: var(--bauhaus-bg) !important;
            background-image: radial-gradient(rgba(18, 18, 18, 0.08) 1.5px, transparent 1.5px) !important;
            background-size: 24px 24px !important;
            font-family: var(--font-outfit) !important;
            color: var(--bauhaus-fg) !important;
        }}

        /* ── Constructivist Typography ────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-outfit) !important;
            text-transform: uppercase !important;
            font-weight: 900 !important;
            letter-spacing: -0.5px !important;
            color: var(--bauhaus-fg) !important;
            line-height: 1.05 !important;
        }}

        p, span, label, div {{
            font-family: var(--font-outfit) !important;
            color: var(--bauhaus-fg);
        }}

        /* ── Hard Offset Shadows & Sharp Edges ────────────────────── */
        *, *::before, *::after {{
            border-radius: 0px !important;
        }}

        /* Allow rounded-full for deliberate geometric circles */
        .circle-shape, .rounded-full {{
            border-radius: 9999px !important;
        }}

        /* ── Streamlit Metric Display ─────────────────────────────── */
        [data-testid="stMetricValue"] {{
            font-family: var(--font-outfit) !important;
            font-size: 3.2rem !important;
            font-weight: 900 !important;
            color: var(--bauhaus-fg) !important;
            letter-spacing: -1px !important;
            line-height: 1 !important;
        }}

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] span {{
            font-family: var(--font-outfit) !important;
            font-size: 13px !important;
            font-weight: 800 !important;
            color: var(--bauhaus-fg) !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
        }}

        [data-testid="stMetricDelta"] {{
            font-family: var(--font-outfit) !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
        }}

        .score-label {{
            font-family: var(--font-outfit);
            font-size: 13px;
            font-weight: 800;
            color: var(--bauhaus-fg);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .score-label::before {{
            content: "";
            display: inline-block;
            width: 10px;
            height: 10px;
            background-color: var(--bauhaus-red);
        }}

        /* ── Inputs & Textareas ───────────────────────────────────── */
        .stTextInput>div>div>input, 
        .stTextArea textarea {{
            background-color: var(--bauhaus-white) !important;
            color: var(--bauhaus-fg) !important;
            font-family: var(--font-outfit) !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            border: 3px solid var(--bauhaus-border) !important;
            box-shadow: 4px 4px 0px 0px var(--bauhaus-border) !important;
            padding: 12px 14px !important;
            transition: all 0.15s ease !important;
        }}

        .stTextInput>div>div>input:focus, 
        .stTextArea textarea:focus {{
            border-color: var(--bauhaus-blue) !important;
            box-shadow: 4px 4px 0px 0px var(--bauhaus-blue) !important;
            outline: none !important;
        }}

        /* ── File Uploader ────────────────────────────────────────── */
        [data-testid="stFileUploader"] {{
            background: var(--bauhaus-white) !important;
            border: 3px dashed var(--bauhaus-border) !important;
            box-shadow: 6px 6px 0px 0px var(--bauhaus-border) !important;
            padding: 20px !important;
            transition: all 0.2s ease !important;
        }}

        [data-testid="stFileUploader"]:hover {{
            border-color: var(--bauhaus-red) !important;
            box-shadow: 8px 8px 0px 0px var(--bauhaus-red) !important;
            transform: translateY(-2px);
        }}

        /* ── Buttons (Bauhaus Physical Press) ─────────────────────── */
        .stButton>button {{
            background-color: var(--bauhaus-red) !important;
            color: var(--bauhaus-white) !important;
            font-family: var(--font-outfit) !important;
            font-size: 15px !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            border: 3px solid var(--bauhaus-border) !important;
            box-shadow: 4px 4px 0px 0px var(--bauhaus-border) !important;
            padding: 14px 28px !important;
            transition: all 0.15s ease-out !important;
        }}

        .stButton>button:hover {{
            background-color: #b51a1a !important;
            color: var(--bauhaus-white) !important;
            transform: translateY(-2px) !important;
            box-shadow: 6px 6px 0px 0px var(--bauhaus-border) !important;
        }}

        .stButton>button:active {{
            transform: translate(2px, 2px) !important;
            box-shadow: 0px 0px 0px 0px var(--bauhaus-border) !important;
        }}

        /* ── Bauhaus Cards ────────────────────────────────────────── */
        .section-card {{
            background-color: var(--bauhaus-white) !important;
            border: 4px solid var(--bauhaus-border) !important;
            box-shadow: 8px 8px 0px 0px var(--bauhaus-border) !important;
            padding: 24px !important;
            margin: 22px 0 !important;
            position: relative !important;
            transition: transform 0.2s ease-out !important;
        }}

        .section-card:hover {{
            transform: translateY(-2px);
        }}

        /* Color-blocked status edges */
        .card-good {{
            border-left: 14px solid var(--bauhaus-blue) !important;
        }}

        .card-weak {{
            border-left: 14px solid var(--bauhaus-yellow) !important;
        }}

        .card-missing {{
            border-left: 14px solid var(--bauhaus-red) !important;
        }}

        /* Status Badges */
        .status-badge {{
            font-family: var(--font-outfit);
            font-size: 12px;
            font-weight: 800;
            padding: 5px 12px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border: 2px solid var(--bauhaus-border);
            box-shadow: 3px 3px 0px 0px var(--bauhaus-border);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .badge-good {{
            color: #FFFFFF;
            background-color: var(--bauhaus-blue);
        }}

        .badge-weak {{
            color: #121212;
            background-color: var(--bauhaus-yellow);
        }}

        .badge-missing {{
            color: #FFFFFF;
            background-color: var(--bauhaus-red);
        }}

        /* Diagnostic Box */
        .diag-box {{
            background-color: #FAF8F5;
            border: 2px solid var(--bauhaus-border);
            padding: 16px;
            margin-top: 14px;
        }}

        .diag-title {{
            font-family: var(--font-outfit);
            color: var(--bauhaus-fg);
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .diag-text {{
            font-family: var(--font-outfit);
            color: #222222;
            font-size: 14px;
            font-weight: 500;
            line-height: 1.6;
            margin: 0;
        }}

        .diag-text strong {{
            color: var(--bauhaus-fg) !important;
            font-weight: 800 !important;
            background: var(--bauhaus-yellow);
            padding: 1px 4px;
        }}

        /* ── Sidebar Bauhaus Styling ──────────────────────────────── */
        [data-testid="stSidebar"] {{
            background-color: #E6E6E6 !important;
            border-right: 4px solid var(--bauhaus-border) !important;
        }}

        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {{
            color: var(--bauhaus-fg) !important;
        }}

        /* Alerts */
        .stAlert {{
            background-color: var(--bauhaus-white) !important;
            border: 3px solid var(--bauhaus-border) !important;
            box-shadow: 4px 4px 0px 0px var(--bauhaus-border) !important;
            color: var(--bauhaus-fg) !important;
            font-weight: 600 !important;
        }}

        /* Radio Buttons */
        [data-testid="stRadio"] label {{
            font-family: var(--font-outfit) !important;
            font-weight: 600 !important;
            color: var(--bauhaus-fg) !important;
        }}

        /* Horizontal Divider */
        hr {{
            border: none !important;
            border-top: 4px solid var(--bauhaus-border) !important;
            opacity: 1 !important;
            margin: 28px 0 !important;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the application header with pure Bauhaus constructivist aesthetic"""
    st.markdown(f"""
    <div style="padding: 24px 0 16px 0; border-bottom: 4px solid #121212; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 16px;">
            <!-- Left: Geometric Logo Mark & Title -->
            <div>
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                    <!-- Circle (Red) -->
                    <div class="circle-shape" style="width: 24px; height: 24px; background: #D02020; border: 3px solid #121212;"></div>
                    <!-- Square (Blue) -->
                    <div style="width: 22px; height: 22px; background: #1040C0; border: 3px solid #121212;"></div>
                    <!-- Triangle (Yellow) -->
                    <div style="width: 0; height: 0; border-left: 13px solid transparent; border-right: 13px solid transparent; border-bottom: 24px solid #F0C020; filter: drop-shadow(0 0 0 #121212);"></div>
                    <span style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 13px; letter-spacing: 3px; color: #121212; text-transform: uppercase; margin-left: 6px;">
                        BAUHAUS PROTOCOL // v{APP_VERSION}
                    </span>
                </div>
                <h1 style="font-size: 3.6rem; margin: 0; font-weight: 900; letter-spacing: -1.5px; text-transform: uppercase; color: #121212; line-height: 0.95;">
                    {APP_TITLE}
                </h1>
            </div>
            <!-- Right: Constructivist Manifesto Block -->
            <div style="background: #F0C020; border: 3px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 10px 18px; max-width: 320px;">
                <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; color: #121212;">
                    FORM FOLLOWS FUNCTION
                </div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 600; color: #121212; margin-top: 2px;">
                    Architectural vector analysis for applicant tracking systems.
                </div>
            </div>
        </div>
        <!-- Color Strip Accent -->
        <div style="display: flex; height: 8px; margin-top: 20px; border: 2px solid #121212;">
            <div style="flex: 2; background: #D02020;"></div>
            <div style="flex: 2; background: #1040C0;"></div>
            <div style="flex: 1; background: #F0C020;"></div>
            <div style="flex: 5; background: #121212;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with Bauhaus constructivist aesthetics"""
    with st.sidebar:
        # Top Color-blocked Brand Panel
        st.markdown(f"""
        <div style="background: #1040C0; border: 4px solid #121212; box-shadow: 6px 6px 0px 0px #121212; padding: 18px; margin-bottom: 24px; color: #FFFFFF;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <div class="circle-shape" style="width: 14px; height: 14px; background: #F0C020; border: 2px solid #121212;"></div>
                <span style="font-family: 'Outfit', sans-serif; font-size: 14px; font-weight: 900; letter-spacing: 2px; text-transform: uppercase;">
                    SYSTEM DESIGN
                </span>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 900; letter-spacing: -0.5px; text-transform: uppercase; line-height: 1.1;">
                BAUHAUS 1925
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 500; margin-top: 8px; color: #E0E0E0; line-height: 1.4;">
                Eliminate decorative clutter. Every resume element must serve algorithmic verification.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step-by-Step Architecture
        st.markdown("""
        <div style="background: #FFFFFF; border: 3px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 16px; margin-bottom: 20px;">
            <div style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; color: #121212; margin-bottom: 12px; border-bottom: 2px solid #121212; padding-bottom: 6px;">
                EXECUTION PIPELINE
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="circle-shape" style="width: 22px; height: 22px; background: #D02020; color: #FFF; font-weight: 900; font-size: 11px; display: flex; align-items: center; justify-content: center; border: 2px solid #121212;">1</div>
                    <span style="font-weight: 700; font-size: 13px; text-transform: uppercase;">Upload PDF Resume</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 22px; height: 22px; background: #1040C0; color: #FFF; font-weight: 900; font-size: 11px; display: flex; align-items: center; justify-content: center; border: 2px solid #121212;">2</div>
                    <span style="font-weight: 700; font-size: 13px; text-transform: uppercase;">Paste Job Specs</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 22px; height: 22px; background: #F0C020; color: #121212; font-weight: 900; font-size: 11px; display: flex; align-items: center; justify-content: center; border: 2px solid #121212; transform: rotate(45deg);"><span style="transform: rotate(-45deg);">3</span></div>
                    <span style="font-weight: 700; font-size: 13px; text-transform: uppercase;">Vector Cosine Match</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 22px; height: 22px; background: #121212; color: #FFF; font-weight: 900; font-size: 11px; display: flex; align-items: center; justify-content: center; border: 2px solid #121212;">4</div>
                    <span style="font-weight: 700; font-size: 13px; text-transform: uppercase;">Remedy Deficits</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Design Directives
        st.markdown("""
        <div style="background: #F0C020; border: 3px solid #121212; box-shadow: 4px 4px 0px 0px #121212; padding: 14px 16px;">
            <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; color: #121212; margin-bottom: 8px;">
                GEOMETRIC RULES
            </div>
            <div style="font-size: 12px; font-weight: 600; line-height: 1.6; color: #121212;">
                ■ No floating multi-columns<br>
                ■ Direct keyword alignment<br>
                ■ Plain text over fancy graphics<br>
                ■ Metric quantification in bullets
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_section_card(section):
    """
    Render a section analysis card in Bauhaus constructivist format.
    
    Args:
        section (dict): Section analysis data containing:
            - icon: Emoji icon
            - title: Section name
            - status: 'good', 'weak', or 'missing'
            - recommendation: Recommendation text
            - missing: List of missing elements
    """
    status = section.get('status', 'missing')
    icon = section.get('icon', '📌')
    title = section.get('title', 'Section')
    recommendation = section.get('recommendation', 'No recommendation available.')
    missing = section.get('missing', [])
    
    # Convert markdown bold (**text**) to HTML bold (<strong>text</strong>)
    recommendation_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', recommendation)
    
    # Bauhaus status configurations & geometric corner shapes
    if status == 'good':
        badge_html = '<span class="status-badge badge-good">● ALIGNED</span>'
        card_class = "card-good"
        shape_html = '<div class="circle-shape" style="width: 14px; height: 14px; background: #1040C0; border: 2px solid #121212;"></div>'
        status_accent = "#1040C0"
    elif status == 'weak':
        badge_html = '<span class="status-badge badge-weak">▲ NEEDS WORK</span>'
        card_class = "card-weak"
        shape_html = '<div style="width: 14px; height: 14px; background: #F0C020; border: 2px solid #121212;"></div>'
        status_accent = "#F0C020"
    else:  # missing
        badge_html = '<span class="status-badge badge-missing">■ DEFICIT</span>'
        card_class = "card-missing"
        shape_html = '<div style="width: 14px; height: 14px; background: #D02020; border: 2px solid #121212; transform: rotate(45deg);"></div>'
        status_accent = "#D02020"
    
    st.markdown(f"""
    <div class="section-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #121212; padding-bottom: 12px; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                {shape_html}
                <span style="font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 900; color: #121212; text-transform: uppercase; letter-spacing: -0.5px;">
                    {title}
                </span>
            </div>
            {badge_html}
        </div>
        <div class="diag-box">
            <div class="diag-title">
                <span style="display: inline-block; width: 8px; height: 8px; background: {status_accent};"></span>
                <span>ARCHITECTURAL AUDIT &amp; PRESCRIPTION</span>
            </div>
            <p class="diag-text">
                {recommendation_html}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show missing elements if any
    if missing and len(missing) > 0:
        st.markdown("""
        <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 800; color: #D02020; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px; margin-bottom: 6px;">
            SPECIFICATION DEFICITS DETECTED:
        </div>
        """, unsafe_allow_html=True)
        for item in missing[:5]:
            if item:
                st.markdown(
                    f"<div style='display: flex; align-items: center; gap: 8px; margin: 4px 0;'>"
                    f"<span style='display: inline-block; width: 6px; height: 6px; background: #D02020;'></span>"
                    f"<span style='font-family: \"Outfit\", sans-serif; font-weight: 600; color: #121212;'>{item}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )


def render_pro_tips():
    """Render professional tips section in pure Bauhaus color-blocked composition"""
    st.markdown("""
    <div style="margin-top: 36px; margin-bottom: 20px; border-bottom: 4px solid #121212; padding-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <div class="circle-shape" style="width: 18px; height: 18px; background: #D02020; border: 2px solid #121212;"></div>
            <div style="width: 16px; height: 16px; background: #1040C0; border: 2px solid #121212;"></div>
            <div style="width: 16px; height: 16px; background: #F0C020; border: 2px solid #121212;"></div>
        </div>
        <h2 style="font-size: 2.2rem; color: #121212; margin: 0; font-weight: 900; letter-spacing: -1px;">
            BAUHAUS COMPLIANCE DIRECTIVES
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div style="background: #1040C0; color: #FFFFFF; border: 4px solid #121212; box-shadow: 8px 8px 0px 0px #121212; padding: 22px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px; border-bottom: 2px solid #FFFFFF; padding-bottom: 8px;">
                <div class="circle-shape" style="width: 16px; height: 16px; background: #F0C020; border: 2px solid #121212;"></div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase;">
                    FUNCTIONAL CONSTRUCTORS
                </div>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 13.5px; font-weight: 500; line-height: 1.8;">
                <div>■ <strong>Deploy active verbs:</strong> Engineered, Architected, Spearheaded</div>
                <div>■ <strong>Quantify performance:</strong> Percentages, latency, scale, dollar impact</div>
                <div>■ <strong>Match vocabulary:</strong> Replicate exact keywords from the posting</div>
                <div>■ <strong>Clean hierarchies:</strong> Standard H1-H3 sections with consistent rhythm</div>
                <div>■ <strong>Standard fonts:</strong> Modern geometric or clean sans-serif typefaces</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #D02020; color: #FFFFFF; border: 4px solid #121212; box-shadow: 8px 8px 0px 0px #121212; padding: 22px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 14px; border-bottom: 2px solid #FFFFFF; padding-bottom: 8px;">
                <div style="width: 16px; height: 16px; background: #FFFFFF; border: 2px solid #121212; transform: rotate(45deg);"></div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase;">
                    SYNTACTIC DESTRUCTORS
                </div>
            </div>
            <div style="font-family: 'Outfit', sans-serif; font-size: 13.5px; font-weight: 500; line-height: 1.8;">
                <div>■ <strong>Complex multi-columns:</strong> OCR readers tokenize lines horizontally</div>
                <div>■ <strong>Decorative headers/footers:</strong> Data placed here is often ignored</div>
                <div>■ <strong>Embedded graphics:</strong> Text inside images cannot be parsed</div>
                <div>■ <strong>Tables for formatting:</strong> Creates irregular delimiter artifacts</div>
                <div>■ <strong>Unstandardized titles:</strong> 'My Journey' instead of 'Experience'</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 24px; background: #F0C020; border: 4px solid #121212; box-shadow: 6px 6px 0px 0px #121212; padding: 14px 20px; font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 800; color: #121212; text-transform: uppercase; letter-spacing: 0.5px;">
        ▲ EMPIRICAL FACT: Over 75% of submissions fail machine parsing prior to human review. Eliminate stylistic decoration to maximize parsing fidelity.
    </div>
    """, unsafe_allow_html=True)


def render_score_card(score, label, delta=None):
    """
    Render a Bauhaus constructivist score card.
    
    Args:
        score (float): The score to display
        label (str): Label for the score
        delta (float, optional): Delta value to show
    """
    if delta is not None:
        st.metric(label, f"{score:.1f}%", delta=f"+{delta:.1f}%")
    else:
        st.metric(label, f"{score:.1f}%")