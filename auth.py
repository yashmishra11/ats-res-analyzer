"""
Authentication System
Handles user and admin authentication
"""

import streamlit as st
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Admin credentials from environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = hashlib.sha256(
    os.getenv("ADMIN_PASSWORD", "admin123").encode()
).hexdigest()

# For demo - in production, use proper user database
DEMO_USERS = {
    "user@example.com": hashlib.sha256("password123".encode()).hexdigest(),
    "john@example.com": hashlib.sha256("john123".encode()).hexdigest(),
}


def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_admin_credentials(username, password):
    """Check if admin credentials are valid"""
    password_hash = hash_password(password)
    return username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH


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
    """Render the login page"""
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">🎯 ATS Resume Analyzer</h1>
        <p style="color: #8B8B8B; font-size: 1.1rem;">AI-powered resume optimization tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Toggle between user and admin login
        if not st.session_state.show_admin_login:
            st.markdown("### 🔐 User Login")
            
            with st.form("user_login_form"):
                email = st.text_input("Email", placeholder="user@example.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                login_button = st.form_submit_button("Login", use_container_width=True)
                
                if login_button:
                    if check_user_credentials(email, password):
                        st.session_state.authenticated = True
                        st.session_state.is_admin = False
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Demo credentials info
            with st.expander("📝 Demo Credentials"):
                st.info(
                    "**Demo User:**\n"
                    "- Email: user@example.com\n"
                    "- Password: password123"
                )
            
            # Admin login toggle
            if st.button("🔑 Admin Login", use_container_width=True):
                st.session_state.show_admin_login = True
                st.rerun()
                
        else:
            st.markdown("### 👨‍💼 Admin Login")
            
            with st.form("admin_login_form"):
                username = st.text_input("Username", placeholder="admin")
                password = st.text_input("Password", type="password", placeholder="Enter admin password")
                admin_login_button = st.form_submit_button("Login as Admin", use_container_width=True)
                
                if admin_login_button:
                    if check_admin_credentials(username, password):
                        st.session_state.authenticated = True
                        st.session_state.is_admin = True
                        st.session_state.user_email = "admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid admin credentials")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Demo admin credentials
            with st.expander("📝 Demo Admin Credentials"):
                st.info(
                    "**Demo Admin:**\n"
                    "- Username: admin\n"
                    "- Password: admin123"
                )
            
            # Back to user login
            if st.button("← Back to User Login", use_container_width=True):
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