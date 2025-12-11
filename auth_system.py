# ============================================================================
# 🔐 AUTH_SYSTEM.PY - Multi-role Authentication System
# ============================================================================

"""
Comprehensive authentication system for:
- Existing users (Manager, Staff) - Username/Password
- New customers - Mobile/OTP registration
- Existing customers - Mobile/OTP login

Features:
- Password hashing (SHA-256)
- OTP generation & verification
- Session management
- Role-based access
- Account creation
"""

import streamlit as st
import pandas as pd
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional

# ============================================================================
# PASSWORD HASHING
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

# ============================================================================
# OTP SYSTEM
# ============================================================================

def generate_otp(mobile: str) -> str:
    """Generate 4-digit OTP (last 4 digits of mobile for testing)"""
    # Production: Use random.randint(1000, 9999)
    # Testing: Use last 4 digits of mobile
    return mobile[-4:] if len(mobile) >= 4 else "0000"

def verify_otp(entered_otp: str, correct_otp: str) -> bool:
    """Verify OTP"""
    return entered_otp == correct_otp

def send_otp_sms(mobile: str, otp: str) -> bool:
    """
    Send OTP via SMS (simulated)
    Production: Use Twilio or other SMS service
    """
    # Simulated: In real app, send via Twilio
    st.session_state.otp_sent = True
    st.session_state.pending_otp = otp
    st.session_state.otp_mobile = mobile
    return True

# ============================================================================
# USER AUTHENTICATION
# ============================================================================

class AuthenticationSystem:
    """Main authentication handler"""
    
    def __init__(self, users_df: pd.DataFrame, customers_df: pd.DataFrame):
        self.users_df = users_df
        self.customers_df = customers_df
    
    # ========================
    # MANAGER/STAFF LOGIN
    # ========================
    
    def authenticate_staff(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate manager/staff by username & password
        Returns: (success, user_data or error_message)
        """
        
        # Check if user exists
        user = self.users_df[self.users_df['username'].str.lower() == username.lower()]
        
        if user.empty:
            return False, "❌ Username not found"
        
        # Verify password
        stored_hash = user.iloc[0]['password_hash']
        if not verify_password(password, stored_hash):
            return False, "❌ Incorrect password"
        
        # Authentication successful
        user_data = user.iloc[0].to_dict()
        return True, user_data
    
    # ========================
    # CUSTOMER OTP LOGIN
    # ========================
    
    def initiate_customer_login(self, mobile: str) -> Tuple[bool, str]:
        """
        Start customer login by mobile number
        Sends OTP and prepares verification
        """
        
        # Validate mobile format
        if not self._validate_mobile(mobile):
            return False, "❌ Invalid mobile number"
        
        # Check if customer exists
        customer = self.customers_df[
            self.customers_df['mobile'].astype(str) == mobile
        ]
        
        if customer.empty:
            # Check if registration is being initiated
            st.session_state.new_customer_mobile = mobile
            st.session_state.is_new_customer = True
            return True, "New customer detected - Please register"
        
        # Generate and send OTP
        otp = generate_otp(mobile)
        send_otp_sms(mobile, otp)
        
        st.session_state.otp_for_mobile = mobile
        st.session_state.pending_otp = otp
        
        return True, f"OTP sent to {mobile[-4:]} (****)"
    
    def verify_customer_otp(self, mobile: str, entered_otp: str) -> Tuple[bool, str]:
        """Verify OTP and authenticate customer"""
        
        # Check if OTP is correct
        correct_otp = st.session_state.get('pending_otp', '')
        if not verify_otp(entered_otp, correct_otp):
            return False, "❌ Invalid OTP"
        
        # Get customer data
        customer = self.customers_df[
            self.customers_df['mobile'].astype(str) == mobile
        ]
        
        if customer.empty:
            return False, "❌ Customer not found"
        
        # Authentication successful
        customer_data = customer.iloc[0].to_dict()
        st.session_state.pending_otp = ''  # Clear OTP
        
        return True, customer_data
    
    # ========================
    # CUSTOMER REGISTRATION
    # ========================
    
    def register_new_customer(self, 
                             mobile: str,
                             name: str,
                             email: str,
                             password: str) -> Tuple[bool, str]:
        """
        Register a new customer
        """
        
        # Validations
        if not self._validate_mobile(mobile):
            return False, "Invalid mobile number"
        
        if not self._validate_email(email):
            return False, "Invalid email address"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Check if mobile already exists
        if mobile in self.customers_df['mobile'].astype(str).values:
            return False, "Mobile number already registered"
        
        # Create customer record
        try:
            new_customer = {
                'id': int(self.customers_df['id'].max()) + 1,
                'name': name,
                'mobile': mobile,
                'email': email,
                'username': f"{name.upper()}_{mobile[-4:]}",
                'password_hash': hash_password(password),
                'tier': 'Standard',
                'joined_date': datetime.now().strftime('%Y-%m-%d'),
                'pending_amount': 0.0,
                'total_purchased': 0.0,
                'chit_amount': 0.0
            }
            
            # Add to dataframe
            new_df = pd.DataFrame([new_customer])
            updated_df = pd.concat([self.customers_df, new_df], ignore_index=True)
            
            # Save to CSV
            updated_df.to_csv('customers.csv', index=False)
            self.customers_df = updated_df
            
            return True, "✅ Registration successful! You can now log in."
        
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    # ========================
    # HELPERS
    # ========================
    
    def _validate_mobile(self, mobile: str) -> bool:
        """Validate mobile number (10 digits)"""
        return mobile.isdigit() and len(mobile) == 10
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        return '@' in email and '.' in email
    
    def get_customer_by_mobile(self, mobile: str) -> Optional[Dict]:
        """Get customer data by mobile"""
        customer = self.customers_df[
            self.customers_df['mobile'].astype(str) == mobile
        ]
        return customer.iloc[0].to_dict() if not customer.empty else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user data by username"""
        user = self.users_df[self.users_df['username'].str.lower() == username.lower()]
        return user.iloc[0].to_dict() if not user.empty else None

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    if 'pending_otp' not in st.session_state:
        st.session_state.pending_otp = None
    
    if 'otp_for_mobile' not in st.session_state:
        st.session_state.otp_for_mobile = None
    
    if 'is_new_customer' not in st.session_state:
        st.session_state.is_new_customer = False
    
    if 'login_method' not in st.session_state:
        st.session_state.login_method = None

def set_authenticated(user_data: Dict, role: str):
    """Set user as authenticated"""
    
    st.session_state.authenticated = True
    st.session_state.user_data = user_data
    st.session_state.user_role = role
    
    if role == 'customer':
        st.session_state.user_id = user_data.get('id')
        st.session_state.username = user_data.get('name')
        st.session_state.mobile = user_data.get('mobile')
    else:
        st.session_state.user_id = user_data.get('user_id')
        st.session_state.username = user_data.get('username')

def logout():
    """Clear authentication"""
    
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.user_data = None
    st.session_state.pending_otp = None
    st.session_state.is_new_customer = False
    st.session_state.login_method = None

# ============================================================================
# LOGIN UI COMPONENTS
# ============================================================================

def render_login_page():
    """Main login page with multiple authentication methods"""
    
    st.set_page_config(
        page_title="Login",
        layout="centered",
        page_icon="🔐"
    )
    
    init_session_state()
    
    # Custom CSS
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 10px;
        }
        .tab-content {
            padding: 1.5rem;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 💎 Jewelry Retail")
        st.markdown("### Login Portal")
    
    st.divider()
    
    # Load data
    try:
        users_df = pd.read_csv('users.csv')
        customers_df = pd.read_csv('customers.csv')
    except FileNotFoundError:
        st.error("Data files not found. Please ensure users.csv and customers.csv exist.")
        return
    
    auth = AuthenticationSystem(users_df, customers_df)
    
    # Login method selection
    login_type = st.radio(
        "Select Login Type:",
        ["👨‍💼 Staff/Manager Login", "📱 Customer Login"],
        horizontal=True
    )
    
    if login_type == "👨‍💼 Staff/Manager Login":
        render_staff_login(auth)
    else:
        render_customer_login(auth)

def render_staff_login(auth: AuthenticationSystem):
    """Staff/Manager login form"""
    
    st.subheader("👨‍💼 Staff & Manager Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="staff_username"
        )
    
    with col2:
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password",
            key="staff_password"
        )
    
    if st.button("🔓 Login", use_container_width=True, key="staff_login_btn"):
        
        if not username or not password:
            st.error("Please enter username and password")
            return
        
        success, result = auth.authenticate_staff(username, password)
        
        if success:
            # Get user role
            user_data = result
            role = user_data.get('role', 'Staff')
            
            set_authenticated(user_data, role)
            st.success(f"✅ Welcome {username}! Logging in...")
            st.session_state.page = "Dashboard"
            st.rerun()
        
        else:
            st.error(result)

def render_customer_login(auth: AuthenticationSystem):
    """Customer login/registration via OTP"""
    
    st.subheader("📱 Customer Login")
    
    # Step 1: Enter mobile
    mobile = st.text_input(
        "Mobile Number",
        placeholder="Enter 10-digit mobile number",
        max_chars=10,
        key="customer_mobile"
    )
    
    # Validate mobile format
    if mobile and not mobile.isdigit():
        st.error("❌ Please enter only digits")
        return
    
    if mobile and len(mobile) != 10:
        st.warning(f"Mobile number should be 10 digits (You entered {len(mobile)})")
    
    # Step 1 Button
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Send OTP", use_container_width=True, key="send_otp_btn"):
            if not mobile or len(mobile) != 10:
                st.error("Please enter a valid 10-digit mobile number")
                return
            
            success, message = auth.initiate_customer_login(mobile)
            
            if success:
                st.success(message)
                st.info(f"💡 Test OTP: {mobile[-4:]}")
                st.session_state.otp_sent = True
                st.rerun()
    
    with col2:
        if st.button("✏️ New Customer", use_container_width=True, key="new_customer_btn"):
            st.session_state.page = "Register"
            st.rerun()
    
    # Step 2: Enter OTP (after sending)
    if st.session_state.get('otp_sent', False):
        
        st.divider()
        
        otp = st.text_input(
            "Enter OTP",
            placeholder="Enter 4-digit OTP",
            max_chars=4,
            key="customer_otp"
        )
        
        if st.button("🔓 Verify OTP", use_container_width=True, key="verify_otp_btn"):
            
            if not otp or len(otp) != 4:
                st.error("Please enter a valid 4-digit OTP")
                return
            
            success, result = auth.verify_customer_otp(mobile, otp)
            
            if success:
                customer_data = result
                set_authenticated(customer_data, 'customer')
                st.success("✅ Login successful!")
                st.session_state.page = "Customer Dashboard"
                st.rerun()
            
            else:
                st.error(result)

def render_registration_page(auth: AuthenticationSystem):
    """Customer registration page"""
    
    st.set_page_config(page_title="Register", layout="centered", page_icon="📝")
    
    st.title("📝 Create Customer Account")
    
    mobile = st.text_input(
        "Mobile Number",
        placeholder="10-digit mobile number",
        max_chars=10,
        key="reg_mobile"
    )
    
    name = st.text_input(
        "Full Name",
        placeholder="Enter your full name",
        key="reg_name"
    )
    
    email = st.text_input(
        "Email Address",
        placeholder="Enter your email",
        key="reg_email"
    )
    
    password = st.text_input(
        "Password",
        type="password",
        placeholder="At least 8 characters",
        key="reg_password"
    )
    
    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter password",
        key="reg_confirm"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Register", use_container_width=True):
            
            # Validate inputs
            if not all([mobile, name, email, password]):
                st.error("Please fill all fields")
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            success, message = auth.register_new_customer(
                mobile, name, email, password
            )
            
            if success:
                st.success(message)
                st.info("You can now log in with your mobile number and password")
                if st.button("Go to Login"):
                    st.session_state.page = "Login"
                    st.rerun()
            
            else:
                st.error(message)
    
    with col2:
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

