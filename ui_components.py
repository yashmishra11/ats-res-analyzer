"""
UI Components for ATS Resume Analyzer
Cyberpunk / Glitch Design System Implementation
High-tech, low-life aesthetic: Void black, neon glow, scanlines, chamfered HUD panels.
"""

import streamlit as st
import re
from config import (
    APP_TITLE, APP_ICON, APP_VERSION,
    BACKGROUND_COLOR, CARD_COLOR, ACCENT_COLOR, ACCENT_SECONDARY, ACCENT_TERTIARY,
    BORDER_COLOR, DESTRUCTIVE_COLOR, WARNING_COLOR
)


def apply_custom_css():
    """Apply the Cyberpunk / Glitch Design System CSS to Streamlit"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Orbitron:wght@600;700;800;900&family=Share+Tech+Mono&display=swap');

        /* ── Design Tokens ────────────────────────────────────────── */
        :root {{
            --cyber-bg: #0a0a0f;
            --cyber-card: #12121a;
            --cyber-muted: #1c1c2e;
            --cyber-fg: #e0e0e0;
            --cyber-muted-fg: #6b7280;
            --neon-green: #00ff88;
            --neon-magenta: #ff00ff;
            --neon-cyan: #00d4ff;
            --neon-red: #ff3366;
            --neon-amber: #ffa500;
            --cyber-border: #2a2a3a;
            --font-head: 'Orbitron', monospace;
            --font-tech: 'Share Tech Mono', monospace;
            --font-body: 'JetBrains Mono', monospace;
        }}

        /* ── CRT Scanlines Overlay ────────────────────────────────── */
        .stApp::before {{
            content: " ";
            display: block;
            position: fixed;
            top: 0; left: 0; bottom: 0; right: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 0, 0, 0.28) 2px,
                rgba(0, 0, 0, 0.28) 4px
            );
            pointer-events: none;
            z-index: 999999;
            opacity: 0.65;
        }}

        /* ── Base App & Background Circuit Grid ───────────────────── */
        .stApp, .main {{
            background-color: var(--cyber-bg) !important;
            background-image: 
                linear-gradient(rgba(0, 255, 136, 0.035) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 136, 0.035) 1px, transparent 1px) !important;
            background-size: 40px 40px !important;
            font-family: var(--font-body) !important;
            color: var(--cyber-fg) !important;
        }}

        /* ── Typography & Headers ─────────────────────────────────── */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-head) !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            color: #ffffff !important;
        }}

        p, span, label, div {{
            font-family: var(--font-body);
        }}

        /* ── Glitch Animation & Effects ───────────────────────────── */
        @keyframes cyberGlitch {{
            0%, 100% {{ transform: translate(0); }}
            10% {{ transform: translate(-2px, 1px); }}
            20% {{ transform: translate(2px, -1px); }}
            30% {{ transform: translate(-1px, -1px); }}
            40% {{ transform: translate(1px, 2px); }}
            50% {{ transform: translate(-1px, 1px); }}
        }}

        @keyframes rgbShiftPulse {{
            0%, 100% {{
                text-shadow: -2px 0 var(--neon-magenta), 2px 0 var(--neon-cyan), 0 0 12px rgba(0, 255, 136, 0.5);
            }}
            50% {{
                text-shadow: 2px 0 var(--neon-magenta), -2px 0 var(--neon-cyan), 0 0 20px rgba(0, 255, 136, 0.7);
            }}
        }}

        @keyframes blinkCursor {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}

        @keyframes neonPulseGlow {{
            0%, 100% {{
                box-shadow: 0 0 6px var(--neon-green), 0 0 15px rgba(0, 255, 136, 0.3);
            }}
            50% {{
                box-shadow: 0 0 12px var(--neon-green), 0 0 25px rgba(0, 255, 136, 0.6);
            }}
        }}

        .cyber-glitch {{
            animation: cyberGlitch 3s infinite alternate-reverse, rgbShiftPulse 2.5s infinite;
        }}

        .cyber-cursor {{
            display: inline-block;
            width: 8px;
            height: 1.1em;
            background: var(--neon-green);
            vertical-align: middle;
            margin-left: 4px;
            animation: blinkCursor 0.8s step-end infinite;
            box-shadow: 0 0 8px var(--neon-green);
        }}

        /* ── Metric Display (HUD Stats) ───────────────────────────── */
        [data-testid="stMetricValue"] {{
            font-family: var(--font-head) !important;
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            color: var(--neon-green) !important;
            text-shadow: 0 0 12px rgba(0, 255, 136, 0.6) !important;
            letter-spacing: 1px !important;
        }}

        [data-testid="stMetricDelta"] {{
            font-family: var(--font-tech) !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
        }}

        .score-label {{
            font-family: var(--font-tech);
            font-size: 13px;
            color: var(--neon-cyan);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .score-label::before {{
            content: ">>";
            color: var(--neon-green);
            font-weight: bold;
        }}

        /* ── Inputs & Textareas (Terminal Prompt) ──────────────────── */
        .stTextInput>div>div>input, 
        .stTextArea textarea {{
            background-color: var(--cyber-card) !important;
            color: var(--neon-green) !important;
            font-family: var(--font-tech) !important;
            font-size: 14px !important;
            border: 1px solid var(--cyber-border) !important;
            border-radius: 0px !important;
            clip-path: polygon(0 6px, 6px 0, calc(100% - 6px) 0, 100% 6px, 100% calc(100% - 6px), calc(100% - 6px) 100%, 6px 100%, 0 calc(100% - 6px)) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stTextInput>div>div>input:focus, 
        .stTextArea textarea:focus {{
            border-color: var(--neon-green) !important;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.4), inset 0 0 5px rgba(0, 255, 136, 0.2) !important;
            outline: none !important;
        }}

        /* ── File Uploader ────────────────────────────────────────── */
        [data-testid="stFileUploader"] {{
            background: var(--cyber-card);
            border: 1px dashed rgba(0, 255, 136, 0.4);
            padding: 16px;
            clip-path: polygon(0 8px, 8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px));
            transition: border 0.3s;
        }}

        [data-testid="stFileUploader"]:hover {{
            border-color: var(--neon-green);
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.25);
        }}

        /* ── Cyberpunk Buttons ────────────────────────────────────── */
        .stButton>button {{
            background: transparent !important;
            color: var(--neon-green) !important;
            font-family: var(--font-tech) !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            border: 1.5px solid var(--neon-green) !important;
            border-radius: 0px !important;
            clip-path: polygon(0 8px, 8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px)) !important;
            padding: 12px 24px !important;
            box-shadow: 0 0 8px rgba(0, 255, 136, 0.25) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stButton>button:hover {{
            background: var(--neon-green) !important;
            color: #0a0a0f !important;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.8), 0 0 35px rgba(0, 255, 136, 0.4) !important;
            transform: translateY(-1px);
        }}

        .stButton>button:active {{
            transform: translateY(1px);
            box-shadow: 0 0 5px rgba(0, 255, 136, 0.9) !important;
        }}

        /* Secondary Button (Admin Toggle / Alt Actions) */
        .cyber-btn-secondary {{
            border-color: var(--neon-magenta) !important;
            color: var(--neon-magenta) !important;
            box-shadow: 0 0 8px rgba(255, 0, 255, 0.3) !important;
        }}

        .cyber-btn-secondary:hover {{
            background: var(--neon-magenta) !important;
            color: #0a0a0f !important;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.8) !important;
        }}

        /* ── Cyber Section Cards (Chamfered HUD) ──────────────────── */
        .section-card {{
            background-color: var(--cyber-card) !important;
            border: 1px solid var(--cyber-border) !important;
            clip-path: polygon(0 12px, 12px 0, calc(100% - 12px) 0, 100% 12px, 100% calc(100% - 12px), calc(100% - 12px) 100%, 12px 100%, 0 calc(100% - 12px));
            padding: 22px !important;
            margin: 18px 0 !important;
            position: relative;
            transition: all 0.25s ease;
        }}

        .section-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 18px rgba(0, 255, 136, 0.15);
        }}

        /* Chamfer Card Status Indicators */
        .card-good {{
            border-left: 4px solid var(--neon-green) !important;
            box-shadow: -4px 0 12px rgba(0, 255, 136, 0.3);
        }}

        .card-weak {{
            border-left: 4px solid var(--neon-amber) !important;
            box-shadow: -4px 0 12px rgba(255, 165, 0, 0.3);
        }}

        .card-missing {{
            border-left: 4px solid var(--neon-red) !important;
            box-shadow: -4px 0 12px rgba(255, 51, 102, 0.3);
        }}

        /* Status Badges */
        .status-badge {{
            font-family: var(--font-tech);
            font-size: 12px;
            font-weight: 700;
            padding: 4px 10px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .badge-good {{
            color: var(--neon-green);
            border: 1px solid var(--neon-green);
            background: rgba(0, 255, 136, 0.08);
            box-shadow: 0 0 8px rgba(0, 255, 136, 0.35);
        }}

        .badge-weak {{
            color: var(--neon-amber);
            border: 1px solid var(--neon-amber);
            background: rgba(255, 165, 0, 0.08);
            box-shadow: 0 0 8px rgba(255, 165, 0, 0.35);
        }}

        .badge-missing {{
            color: var(--neon-red);
            border: 1px solid var(--neon-red);
            background: rgba(255, 51, 102, 0.08);
            box-shadow: 0 0 8px rgba(255, 51, 102, 0.35);
        }}

        /* Terminal Diagnostic Block */
        .diag-box {{
            background-color: #0b0b13;
            border: 1px solid rgba(0, 212, 255, 0.25);
            padding: 14px;
            margin-top: 12px;
            font-family: var(--font-tech);
        }}

        .diag-title {{
            color: var(--neon-cyan);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .diag-text {{
            color: #d1d5db;
            font-size: 13.5px;
            line-height: 1.6;
            margin: 0;
        }}

        .diag-text strong {{
            color: var(--neon-green) !important;
            font-weight: 700 !important;
            text-shadow: 0 0 6px rgba(0, 255, 136, 0.5) !important;
        }}

        /* ── Sidebar Cyber Styling ────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background-color: #0d0d14 !important;
            border-right: 1px solid var(--cyber-border) !important;
        }}

        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {{
            color: var(--neon-cyan) !important;
        }}

        /* Alerts & Infoboxes */
        .stAlert {{
            background-color: var(--cyber-card) !important;
            border: 1px solid var(--neon-cyan) !important;
            color: var(--cyber-fg) !important;
            font-family: var(--font-tech) !important;
        }}

        /* Radio Buttons */
        [data-testid="stRadio"] label {{
            font-family: var(--font-tech) !important;
            color: var(--cyber-fg) !important;
        }}

        /* Horizontal Divider */
        hr {{
            border-color: rgba(0, 255, 136, 0.18) !important;
            box-shadow: 0 0 8px rgba(0, 255, 136, 0.1) !important;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the application header with cyberpunk styling"""
    st.markdown(f"""
    <div style="text-align: center; padding: 25px 0 15px 0;">
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #00d4ff; letter-spacing: 4px; margin-bottom: 6px;">
            // NODE_CONNECTED: ATS_OPTIMIZER_CORE_v3.0 //
        </div>
        <h1 class="cyber-glitch" style="font-size: 3.2rem; margin: 0; font-weight: 900; letter-spacing: 4px;">
            {APP_ICON} {APP_TITLE}
        </h1>
        <div style="font-family: 'Share Tech Mono', monospace; color: #6b7280; font-size: 13px; letter-spacing: 2px; margin-top: 8px;">
            [ NEURAL PARSER ] :: HEURISTIC RESUME-JOB COMPLIANCE ENGINE <span class="cyber-cursor"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


def render_sidebar():
    """Render the sidebar with cyberpunk terminal aesthetics"""
    with st.sidebar:
        st.markdown(f"""
        <div style="border: 1px solid #00d4ff; padding: 12px; background: #12121a; margin-bottom: 20px;">
            <div style="font-family: 'Orbitron', monospace; font-size: 14px; color: #00d4ff; font-weight: 700; letter-spacing: 1px;">
                {APP_ICON} SYSTEM PROTOCOL
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #00ff88; margin-top: 6px;">
                STATUS: ONLINE [v{APP_VERSION}]
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #8e8e93; margin-top: 8px; line-height: 1.4;">
                Advanced telemetry for bypassing corporate ATS algorithmic gatekeepers.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #ff00ff; letter-spacing: 1.5px; margin-bottom: 8px;">
            [ 01 // EXECUTION WORKFLOW ]
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        `> STEP 1:` **FEED RESUME** (PDF Stream)  
        `> STEP 2:` **INGEST TARGET JD** (Job Posting)  
        `> STEP 3:` **TRIGGER VECTOR SCAN** (Cosine / Match)  
        `> STEP 4:` **OPTIMIZE DEFICITS** (Recommendations)
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #00d4ff; letter-spacing: 1.5px; margin-bottom: 8px;">
            [ 02 // HUD DIRECTIVES ]
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        - `[+]` Standardize token headings
        - `[+]` Inject high-density keywords
        - `[+]` Quantify impact coefficients
        - `[-]` Eliminate graphic artifacts
        """)


def render_section_card(section):
    """
    Render a section analysis card in Cyberpunk HUD Chamfer format.
    
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
    
    # Cyberpunk status configurations
    if status == 'good':
        badge_html = '<span class="status-badge badge-good">[✓ SYS_OPTIMAL]</span>'
        card_class = "card-good"
        code_tag = "SYS_OK"
    elif status == 'weak':
        badge_html = '<span class="status-badge badge-weak">[⚠ SYS_WARN]</span>'
        card_class = "card-weak"
        code_tag = "DEFICIT_DETECTED"
    else:  # missing
        badge_html = '<span class="status-badge badge-missing">[✗ CRIT_DEFICIT]</span>'
        card_class = "card-missing"
        code_tag = "SECTOR_ABSENT"
    
    st.markdown(f"""
    <div class="section-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(42, 42, 58, 0.6); padding-bottom: 10px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.2rem;">{icon}</span>
                <span style="font-family: 'Orbitron', monospace; font-size: 1.15rem; font-weight: 700; color: #ffffff; letter-spacing: 1px;">
                    {title}
                </span>
            </div>
            {badge_html}
        </div>
        <div class="diag-box">
            <div class="diag-title">
                <span>&gt; DIAGNOSTIC // {code_tag}</span>
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
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #ff3366; letter-spacing: 1px; margin-top: 4px;">
            [ CRITICAL DEFICIT LIST: ]
        </div>
        """, unsafe_allow_html=True)
        for item in missing[:5]:
            if item:
                st.markdown(f"`[-]` <span style='font-family: \"Share Tech Mono\"; color: #e0e0e0;'>{item}</span>", unsafe_allow_html=True)


def render_pro_tips():
    """Render professional tips section in Cyberpunk terminal layout"""
    st.markdown("""
    <div style="margin-top: 25px;">
        <h2 style="font-family: 'Orbitron', monospace; font-size: 1.6rem; color: #00d4ff; letter-spacing: 2px;">
            ⚡ HUD PROTOCOLS: ATS BYPASS TACTICS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #12121a; border: 1px solid #00ff88; padding: 16px; clip-path: polygon(0 8px, 8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px));">
            <div style="font-family: 'Orbitron', monospace; color: #00ff88; font-size: 14px; font-weight: 700; margin-bottom: 10px; letter-spacing: 1px;">
                [+] SYSTEM OPTIMIZERS
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; line-height: 1.8; color: #e0e0e0;">
                <div>&gt; DEPLOY ACTIVE VERBS [Engineered, Architected, Spearheaded]</div>
                <div>&gt; INJECT METRIC COEFFICIENTS [%, latency, scale]</div>
                <div>&gt; SYNCHRONIZE JD KEYWORDS EXACTLY</div>
                <div>&gt; ENFORCE CLEAN PARSING SCHEMAS</div>
                <div>&gt; UTILIZE CANONICAL SECTION LABELS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #12121a; border: 1px solid #ff3366; padding: 16px; clip-path: polygon(0 8px, 8px 0, calc(100% - 8px) 0, 100% 8px, 100% calc(100% - 8px), calc(100% - 8px) 100%, 8px 100%, 0 calc(100% - 8px));">
            <div style="font-family: 'Orbitron', monospace; color: #ff3366; font-size: 14px; font-weight: 700; margin-bottom: 10px; letter-spacing: 1px;">
                [-] PARSER CORRUPTORS
            </div>
            <div style="font-family: 'Share Tech Mono', monospace; font-size: 12px; line-height: 1.8; color: #e0e0e0;">
                <div>&gt; AVOID MULTI-COLUMN COMPLEX LAYOUTS</div>
                <div>&gt; PURGE HEADERS, FOOTERS &amp; FLOATING TEXT BOXES</div>
                <div>&gt; FORBID EMBEDDED TABLES AND IMAGES</div>
                <div>&gt; REJECT OBSOLETE NON-STANDARD FONTS</div>
                <div>&gt; PREVENT SYNTACTIC NOISE &amp; OVERFLOW</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 15px; border-left: 3px solid #00d4ff; padding: 8px 12px; background: rgba(0, 212, 255, 0.05); font-family: 'Share Tech Mono', monospace; font-size: 12px; color: #00d4ff;">
        // ALERT: Over 75% of submissions are rejected at the parsing boundary before human evaluation. Optimize precision.
    </div>
    """, unsafe_allow_html=True)


def render_score_card(score, label, delta=None):
    """
    Render a cyberpunk score card with optional delta.
    
    Args:
        score (float): The score to display
        label (str): Label for the score
        delta (float, optional): Delta value to show
    """
    st.markdown(f'<div class="score-label">{label}</div>', unsafe_allow_html=True)
    if delta is not None:
        st.metric("", f"{score:.1f}%", delta=f"+{delta:.1f}%")
    else:
        st.metric("", f"{score:.1f}%")