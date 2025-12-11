import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

class AuthenticationSystem:
    def __init__(self, users_df, customers_df):
        self.users_df = users_df
        self.customers_df = customers_df
    
    def register_customer(self, name, mobile, email, password):
        """Register a new customer"""
        # Check if mobile already exists
        if mobile in self.customers_df['mobile'].values:
            return False, "Mobile number already registered"
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        return True, "Registration successful"
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = self.users_df[self.users_df['username'] == username]
        
        if user.empty:
            return False, None
        
        if user.iloc[0]['password_hash'] == password_hash:
            return True, user.iloc[0].to_dict()
        
        return False, None

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'page' not in st.session_state:
        st.session_state.page = 'Login'

def logout():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_data = None
    st.rerun()

def render_login_page():
    """Render the login page"""
    st.set_page_config(page_title="Jewelry Management System", layout="centered")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("💎 Login")
        st.markdown("---")
        
        login_type = st.radio("Login As", ["Manager", "Staff", "Customer"])
        
        if login_type == "Manager":
            st.info("👨‍💼 Manager Login")
            username = st.text_input("Username", value="manager_user")
            password = st.text_input("Password", type="password", value="manager123")
            
            if st.button("🔓 Login Manager", use_container_width=True):
                if username == "manager_user" and password == "manager123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.user_data = {"name": "Manager User", "role": "Manager"}
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        elif login_type == "Staff":
            st.info("👨‍💼 Staff Login")
            username = st.text_input("Username", placeholder="e.g., RAJESH_2001")
            password = st.text_input("Password", type="password", placeholder="staff123")
            
            if st.button("🔓 Login Staff", use_container_width=True):
                if password == "staff123":  # Demo password
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Staff"
                    st.session_state.user_data = {"name": username, "role": "Staff"}
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        else:  # Customer
            st.info("👤 Customer Login")
            mobile = st.text_input("Mobile Number", placeholder="9876543200")
            
            if st.button("📱 Send OTP", use_container_width=True):
                st.session_state.otp_sent = True
                st.success(f"OTP sent to {mobile}")
            
            if st.session_state.get('otp_sent'):
                otp = st.text_input("Enter OTP", placeholder="Last 4 digits of mobile")
                
                if st.button("✅ Verify & Login", use_container_width=True):
                    if otp == mobile[-4:]:
                        st.session_state.authenticated = True
                        st.session_state.user_role = "customer"
                        st.session_state.user_data = {"mobile": mobile, "role": "customer"}
                        st.rerun()
                    else:
                        st.error("Invalid OTP")
        
        st.markdown("---")
        st.markdown("**Don't have an account?**")
        if st.button("📝 Register", use_container_width=True):
            st.session_state.page = 'Register'
            st.rerun()

def render_registration_page(auth):
    """Render the registration page"""
    st.set_page_config(page_title="Register - Jewelry System", layout="centered")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("📝 Register")
        st.markdown("---")
        
        name = st.text_input("Full Name", placeholder="Enter your name")
        mobile = st.text_input("Mobile Number", placeholder="9876543200")
        email = st.text_input("Email Address", placeholder="example@email.com")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("✅ Register", use_container_width=True):
            if not all([name, mobile, email, password]):
                st.error("Please fill all fields")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                success, message = auth.register_customer(name, mobile, email, password)
                if success:
                    st.success(message)
                    st.info("Now you can login with your mobile number and OTP")
                else:
                    st.error(message)
        
        st.markdown("---")
        if st.button("🔙 Back to Login", use_container_width=True):
            st.session_state.page = 'Login'
            st.rerun()
