"""
Authentication System
Handles user and admin authentication
"""

import streamlit as st
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def get_config_val(key, default=""):
    """Retrieve config from Streamlit secrets if available, fallback to os.getenv"""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


# For demo - in production, use proper user database
DEMO_USERS = {
    "user": hashlib.sha256("123".encode()).hexdigest(),
    "john@example.com": hashlib.sha256("john123".encode()).hexdigest(),
}


def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_admin_credentials(username, password):
    """Check if admin credentials are valid"""
    admin_user = get_config_val("ADMIN_USERNAME", "admin")
    admin_pass = get_config_val("ADMIN_PASSWORD", "admin123")
    return username == admin_user and hash_password(password) == hash_password(admin_pass)


def check_user_credentials(email, password):
    """Check if user credentials are valid"""
    password_hash = hash_password(password)
    return email in DEMO_USERS and DEMO_USERS[email] == password_hash


def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'show_admin_login' not in st.session_state:
        st.session_state.show_admin_login = False


def render_login_page():
    """Render the Bauhaus constructivist login page"""
    st.markdown("""
    <div style="text-align: center; padding: 24px 0 16px 0;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 12px;">
            <div class="circle-shape" style="width: 22px; height: 22px; background: #D02020; border: 3px solid #121212;"></div>
            <div style="width: 20px; height: 20px; background: #1040C0; border: 3px solid #121212;"></div>
            <div style="width: 0; height: 0; border-left: 11px solid transparent; border-right: 11px solid transparent; border-bottom: 20px solid #F0C020;"></div>
            <span style="font-family: 'Outfit', sans-serif; font-size: 13px; font-weight: 800; color: #121212; letter-spacing: 3px; text-transform: uppercase; margin-left: 6px;">
                BAUHAUS 1925
            </span>
        </div>
        <h1 style="font-size: 3.2rem; margin: 0; font-weight: 900; letter-spacing: -1px; text-transform: uppercase; color: #121212;">
            ATS RESUME ANALYZER
        </h1>
        <p style="font-family: 'Outfit', sans-serif; color: #444444; font-size: 14px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px;">
            CONSTRUCTIVIST RESUME AUDITING &amp; OPTIMIZATION
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Center the login form inside a Bauhaus card container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.show_admin_login:
            st.markdown("""
            <div style="background: #1040C0; color: #FFFFFF; border: 4px solid #121212; box-shadow: 6px 6px 0px 0px #121212; padding: 16px 20px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div class="circle-shape" style="width: 14px; height: 14px; background: #F0C020; border: 2px solid #121212;"></div>
                    <span style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase;">
                        USER ACCESS AUTHENTICATION
                    </span>
                </div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 500; color: #E0E0E0; margin-top: 4px;">
                    Enter verified credentials to initiate resume compliance scanner
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("user_login_form"):
                email = st.text_input("EMAIL IDENTIFIER", placeholder="user or user@example.com")
                password = st.text_input("SECURITY KEY", type="password", placeholder="Enter key (e.g. 123)")
                login_button = st.form_submit_button("■ INITIALIZE SESSION", use_container_width=True)
                
                if login_button:
                    if check_user_credentials(email, password):
                        st.session_state.authenticated = True
                        st.session_state.is_admin = False
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error("❌ AUTHENTICATION REFUSED // INVALID CREDENTIALS")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Admin login toggle
            if st.button("▲ SWITCH TO ELEVATED ROOT ACCESS", use_container_width=True):
                st.session_state.show_admin_login = True
                st.rerun()
                
        else:
            st.markdown("""
            <div style="background: #F0C020; color: #121212; border: 4px solid #121212; box-shadow: 6px 6px 0px 0px #121212; padding: 16px 20px; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 14px; height: 14px; background: #D02020; border: 2px solid #121212;"></div>
                    <span style="font-family: 'Outfit', sans-serif; font-size: 15px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase;">
                        ROOT / ADMIN ACCESS
                    </span>
                </div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 12px; font-weight: 600; color: #121212; margin-top: 4px;">
                    Elevated system controls & telemetry inspection
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("admin_login_form"):
                username = st.text_input("ROOT USERNAME", placeholder="admin")
                password = st.text_input("ROOT CIPHER KEY", type="password", placeholder="Enter root cipher")
                admin_login_button = st.form_submit_button("■ AUTHENTICATE ROOT", use_container_width=True)
                
                if admin_login_button:
                    if check_admin_credentials(username, password):
                        st.session_state.authenticated = True
                        st.session_state.is_admin = True
                        st.session_state.user_email = "admin"
                        st.rerun()
                    else:
                        st.error("❌ CIPHER MISMATCH // ROOT ACCESS REFUSED")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Back to user login
            if st.button("● RETURN TO STANDARD ACCESS", use_container_width=True):
                st.session_state.show_admin_login = False
                st.rerun()


def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.is_admin = False
    st.session_state.user_email = None
    st.session_state.show_admin_login = False
    st.rerun()


def require_auth():
    """Decorator to require authentication"""
    if not st.session_state.get('authenticated', False):
        render_login_page()
        st.stop()


def require_admin():
    """Decorator to require admin authentication"""
    if not st.session_state.get('is_admin', False):
        st.error("❌ Admin access required")
        st.stop()