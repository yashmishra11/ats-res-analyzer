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
    """Render the cyberpunk terminal login page"""
    st.markdown("""
    <div style="text-align: center; padding: 25px 0 10px 0;">
        <div style="font-family: 'Share Tech Mono', monospace; font-size: 13px; color: #00d4ff; letter-spacing: 3px; margin-bottom: 8px;">
            // TERMINAL_AUTH_GATEWAY // NODE_ID: 0x889F //
        </div>
        <h1 class="cyber-glitch" style="font-size: 3rem; margin: 0; font-weight: 900; letter-spacing: 4px;">
            ATS RESUME ANALYZER
        </h1>
        <p style="font-family: 'Share Tech Mono', monospace; color: #8e8e93; font-size: 1rem; letter-spacing: 2px; margin-top: 6px;">
            NEURAL GATEKEEPER BYPASS SYSTEM <span class="cyber-cursor"></span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Center the login form inside a cyber card container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.show_admin_login:
            st.markdown("""
            <div style="background: #12121a; border: 1px solid #00ff88; box-shadow: 0 0 15px rgba(0, 255, 136, 0.2); padding: 18px 24px 10px 24px; clip-path: polygon(0 12px, 12px 0, calc(100% - 12px) 0, 100% 12px, 100% calc(100% - 12px), calc(100% - 12px) 100%, 12px 100%, 0 calc(100% - 12px)); margin-bottom: 15px;">
                <div style="font-family: 'Orbitron', monospace; font-size: 15px; color: #00ff88; font-weight: 700; letter-spacing: 2px; margin-bottom: 6px;">
                    &gt; USER ACCESS PROTOCOL
                </div>
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #6b7280; margin-bottom: 10px;">
                    ENTER VERIFIED CREDENTIALS TO INITIALIZE SCANNER
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("user_login_form"):
                email = st.text_input("USER_EMAIL // IDENTIFIER", placeholder="user or user@example.com")
                password = st.text_input("SECURITY_KEY // PASSWORD", type="password", placeholder="Enter key (e.g. 123)")
                login_button = st.form_submit_button("⚡ INITIALIZE SESSION", use_container_width=True)
                
                if login_button:
                    if check_user_credentials(email, password):
                        st.session_state.authenticated = True
                        st.session_state.is_admin = False
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error("❌ ACCESS DENIED // INVALID IDENTITY MATRIX")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Admin login toggle
            if st.button("🔑 SWITCH TO ELEVATED ROOT ACCESS", use_container_width=True):
                st.session_state.show_admin_login = True
                st.rerun()
                
        else:
            st.markdown("""
            <div style="background: #12121a; border: 1px solid #ff00ff; box-shadow: 0 0 15px rgba(255, 0, 255, 0.25); padding: 18px 24px 10px 24px; clip-path: polygon(0 12px, 12px 0, calc(100% - 12px) 0, 100% 12px, 100% calc(100% - 12px), calc(100% - 12px) 100%, 12px 100%, 0 calc(100% - 12px)); margin-bottom: 15px;">
                <div style="font-family: 'Orbitron', monospace; font-size: 15px; color: #ff00ff; font-weight: 700; letter-spacing: 2px; margin-bottom: 6px;">
                    &gt; ROOT / ADMIN OVERRIDE
                </div>
                <div style="font-family: 'Share Tech Mono', monospace; font-size: 11px; color: #6b7280; margin-bottom: 10px;">
                    PRIVILEGED TERMINAL CONTROLS & TELEMETRY ACCESS
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("admin_login_form"):
                username = st.text_input("ROOT_USER // USERNAME", placeholder="admin")
                password = st.text_input("CIPHER_KEY // ADMIN_PASSWORD", type="password", placeholder="Enter root cipher")
                admin_login_button = st.form_submit_button("⚡ AUTHENTICATE ROOT", use_container_width=True)
                
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
            if st.button("← RETURN TO STANDARD ACCESS", use_container_width=True):
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