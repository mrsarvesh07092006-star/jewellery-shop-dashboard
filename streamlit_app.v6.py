"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v10.3
✨ CAMPAIGN NOTIFICATIONS TAB ADDED TO CUSTOMER DASHBOARD
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG - LUXURY BLACK & SILVER THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# LUXURY BLACK & SILVER THEME - DARK & ELEGANT
st.markdown("""
<style>
    * {
        color: #e8e8e8 !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f0f0f !important;
    }

    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 2px solid #c0c0c0 !important;
    }

    [data-testid="stForm"] {
        background-color: #1a1a1a !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        padding: 25px !important;
    }

    [role="radiogroup"] {
        background-color: transparent !important;
    }

    .main {
        background-color: #0f0f0f !important;
        padding: 2rem !important;
    }

    .main-title { 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: #c0c0c0 !important;
        text-shadow: 2px 2px 8px rgba(192, 192, 192, 0.3);
        letter-spacing: 2px;
        margin-bottom: 2rem !important;
    }

    h2 {
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 1rem !important;
        border-bottom: 2px solid #404040 !important;
    }

    h3 {
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    .metric-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
        padding: 25px !important;
        text-align: center !important;
        color: #e8e8e8 !important;
        box-shadow: 0 8px 32px rgba(192, 192, 192, 0.1) !important;
        margin-bottom: 1.5rem !important;
    }

    .chart-box {
        background-color: #1a1a1a !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin-bottom: 1.5rem !important;
    }

    .info-box { 
        background: linear-gradient(135deg, #1a3a3a 0%, #1a2a3a 100%) !important;
        border-left: 4px solid #c0c0c0 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
        margin-bottom: 2rem !important;
        margin-top: 1rem !important;
    }

    .success-box {
        background: linear-gradient(135deg, #1a3a1a 0%, #1a2a1a 100%) !important;
        border-left: 4px solid #7cb342 !important;
        padding: 20px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
        margin-bottom: 2rem !important;
        margin-top: 1rem !important;
    }

    .warning-box {
        background: linear-gradient(135deg, #3a3a1a 0%, #2a2a1a 100%) !important;
        border-left: 4px solid #fbc02d !important;
        padding: 20px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
        margin-bottom: 2rem !important;
        margin-top: 1rem !important;
    }

    .ai-response {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f2a3a 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        color: #e8e8e8 !important;
        box-shadow: 0 4px 16px rgba(192, 192, 192, 0.08) !important;
    }

    .button-primary {
        background: linear-gradient(135deg, #c0c0c0 0%, #a8a8a8 100%) !important;
        color: #0f0f0f !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(192, 192, 192, 0.2) !important;
        margin: 10px 0 !important;
    }

    button {
        margin: 8px 0 !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        color: #e8e8e8 !important;
        margin-bottom: 1.5rem !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #c0c0c0 !important;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #c0c0c0 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }

    [data-testid="stMetricLabel"] {
        color: #a8a8a8 !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #1a1a1a !important;
    }

    [role="tablist"] {
        border-bottom: 2px solid #404040 !important;
        margin-bottom: 1.5rem !important;
    }

    [role="tab"] {
        color: #a8a8a8 !important;
        border-bottom: 2px solid transparent !important;
        padding: 12px 20px !important;
    }

    [role="tab"][aria-selected="true"] {
        color: #c0c0c0 !important;
        border-bottom: 2px solid #c0c0c0 !important;
    }

    input, textarea, select {
        background-color: #1a1a1a !important;
        border: 1px solid #404040 !important;
        color: #e8e8e8 !important;
        border-radius: 6px !important;
        padding: 10px 15px !important;
        margin: 8px 0 !important;
    }

    input:focus, textarea:focus, select:focus {
        border: 2px solid #c0c0c0 !important;
        box-shadow: 0 0 8px rgba(192, 192, 192, 0.2) !important;
    }

    .spacer {
        margin-bottom: 2rem !important;
    }

    .rate-card {
        background: linear-gradient(135deg, #1a3a1a 0%, #2a2a1a 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        text-align: center !important;
    }

    .notification-card {
        background: linear-gradient(135deg, #3a2a1a 0%, #2a2a1a 100%) !important;
        border-left: 4px solid #fbc02d !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 12px 0 !important;
    }

    .campaign-card {
        background: linear-gradient(135deg, #2a3a3a 0%, #1a2a3a 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        box-shadow: 0 4px 12px rgba(192, 192, 192, 0.1) !important;
    }

    .campaign-active {
        background: linear-gradient(135deg, #2a3a2a 0%, #1a2a1a 100%) !important;
        border-left: 4px solid #7cb342 !important;
    }

    .campaign-upcoming {
        background: linear-gradient(135deg, #3a3a2a 0%, #2a2a1a 100%) !important;
        border-left: 4px solid #fbc02d !important;
    }

    .campaign-expired {
        background: linear-gradient(135deg, #3a2a2a 0%, #2a1a1a 100%) !important;
        border-left: 4px solid #a8a8a8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.smart_command_messages = []
    st.session_state.customer_messages = []
    st.session_state.chatbot_messages = []

# TODAY'S RATES - REAL TIME
TODAY_RATES = {
    "gold": {"current": 7850, "previous": 7800, "change": 50, "currency": "₹", "unit": "/gram"},
    "silver": {"current": 95, "previous": 92, "change": 3, "currency": "₹", "unit": "/gram"}
}

# STAFF DATA
STAFF_MEMBERS = {
    "ram": {"name": "Ram Kumar", "position": "Sales Executive", "pending": "₹15,000"},
    "priya": {"name": "Priya Singh", "position": "Manager", "pending": "₹8,500"},
    "amit": {"name": "Amit Verma", "position": "Sales Associate", "pending": "₹12,000"},
    "neha": {"name": "Neha Sharma", "position": "Cashier", "pending": "₹5,500"}
}

# CAMPAIGN DATA - ENHANCED
CAMPAIGNS = [
    {
        "id": 1,
        "name": "🎄 Diwali Sale 2025",
        "discount": "20%",
        "status": "Active",
        "start_date": "2025-10-15",
        "end_date": "2025-11-15",
        "description": "Celebrate Diwali with amazing discounts on all gold and silver jewellery",
        "terms": "Valid on minimum purchase of ₹10,000. Cannot be combined with other offers.",
        "received": True,
        "received_date": "2025-10-15"
    },
    {
        "id": 2,
        "name": "💒 Wedding Season Special",
        "discount": "15%",
        "status": "Active",
        "start_date": "2025-11-01",
        "end_date": "2026-03-31",
        "description": "Make your wedding journey special with exclusive wedding collection discounts",
        "terms": "Apply discount code WEDDING15 at checkout. Valid on all bridal collections.",
        "received": True,
        "received_date": "2025-11-01"
    },
    {
        "id": 3,
        "name": "🎉 Clearance Sale",
        "discount": "30%",
        "status": "Active",
        "start_date": "2025-12-01",
        "end_date": "2025-12-31",
        "description": "Year-end clearance! Huge discounts on selected items. Limited stock available.",
        "terms": "First come first serve basis. Valid on selected items only as shown in store.",
        "received": True,
        "received_date": "2025-12-01"
    },
    {
        "id": 4,
        "name": "✨ New Year New Look",
        "discount": "25%",
        "status": "Upcoming",
        "start_date": "2025-12-25",
        "end_date": "2026-01-15",
        "description": "Start 2026 with a fresh look! Special collection launch with exclusive discounts",
        "terms": "Early bird offers available. Register now for exclusive previews.",
        "received": False,
        "received_date": None
    },
    {
        "id": 5,
        "name": "💎 Loyalty Rewards Program",
        "discount": "5X Points",
        "status": "Active",
        "start_date": "2025-01-01",
        "end_date": "2026-12-31",
        "description": "Earn 5X loyalty points on every purchase. Redeem points for free gifts!",
        "terms": "1 point = ₹1. Minimum ₹500 points required for redemption.",
        "received": True,
        "received_date": "2025-01-15"
    },
    {
        "id": 6,
        "name": "👑 VIP Member Exclusive",
        "discount": "Exclusive Access",
        "status": "Upcoming",
        "start_date": "2026-01-20",
        "end_date": "2026-03-20",
        "description": "Exclusive previews of new collections before public launch",
        "terms": "Available only for Gold tier and above members. Complimentary consultation included.",
        "received": False,
        "received_date": None
    }
]

# CUSTOMER DATA - ENHANCED
CUSTOMER_DATA = {
    "customer": {
        "name": "Rajesh Patel",
        "tier": "Premium",
        "total_spent": 500000,
        "purchases": [
            {"date": "2025-12-10", "item": "Gold Ring", "amount": 45000, "quantity": 10, "status": "Delivered"},
            {"date": "2025-12-05", "item": "Diamond Pendant", "amount": 55000, "quantity": 1, "status": "Delivered"},
            {"date": "2025-11-28", "item": "Silver Bracelet", "amount": 8000, "quantity": 2, "status": "Delivered"},
            {"date": "2025-11-20", "item": "Gold Necklace", "amount": 75000, "quantity": 1, "status": "Delivered"},
            {"date": "2025-11-10", "item": "Platinum Ring", "amount": 120000, "quantity": 1, "status": "Delivered"},
        ],
        "chits": [
            {"name": "Gold 12-Month", "amount": 100000, "paid": 50000, "pending": 50000, "status": "Active"},
            {"name": "Diamond Savings", "amount": 200000, "paid": 100000, "pending": 100000, "status": "Active"},
        ],
        "loyalty_points": 890,
        "loyalty_tier": "Gold",
        "campaigns_received": [
            {"name": "Diwali Sale 2025", "discount": "20%", "status": "Received", "date": "2025-10-15"},
            {"name": "Wedding Season", "discount": "15%", "status": "Received", "date": "2025-11-01"},
            {"name": "Clearance Sale", "discount": "30%", "status": "Received", "date": "2025-12-01"},
            {"name": "New Year Special", "discount": "25%", "status": "Upcoming", "date": "2025-12-25"},
        ]
    }
}

# Authentication
USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager", "name": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff", "name": "Sales Staff"},
    "customer": {"password": hashlib.sha256("customer123".encode()).hexdigest(), "role": "Customer", "name": "Customer"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin", "name": "Admin"}
}

def get_accessible_pages(role):
    pages = {
        "Manager": ["Dashboard", "Customers", "Inventory", "Tax & Compliance", "Campaigns", "Staff Management", "Quick Actions", "AI Assistant", "Smart Commands", "Chatbot"],
        "Sales Staff": ["Dashboard", "Customers", "Sales Record", "Loyalty Program", "Quick Actions", "AI Assistant", "Chatbot"],
        "Customer": ["Dashboard", "My Purchases", "My Chits", "Offers & Rewards", "My Summary", "Support Chat"],
        "Admin": ["Dashboard", "Customers", "Inventory", "Tax & Compliance", "Campaigns", "Staff Management", "Quick Actions", "AI Assistant", "Smart Commands", "Chatbot", "Settings"]
    }
    return pages.get(role, [])

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("### Premium Management System for Indian Jewellery Retail")
        st.divider()

        login_type = st.radio("Login As:", ["Manager", "Staff", "Customer", "Admin"], horizontal=True, key="login_type")

        if login_type == "Manager":
            st.subheader("👨‍💼 Manager Login")
            username = st.text_input("Username", key="mgr_user_id")
            password = st.text_input("Password", type="password", key="mgr_pass_id")

            if st.button("Login", use_container_width=True, key="mgr_btn"):
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        elif login_type == "Staff":
            st.subheader("👤 Staff Login")
            username = st.text_input("Username", key="staff_user_id")
            password = st.text_input("Password", type="password", key="staff_pass_id")

            if st.button("Login", use_container_width=True, key="staff_btn"):
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        elif login_type == "Customer":
            st.subheader("🛍️ Customer Login")
            username = st.text_input("Username", key="cust_user_id")
            password = st.text_input("Password", type="password", key="cust_pass_id")

            if st.button("Login", use_container_width=True, key="cust_btn"):
                if username == "customer" and hashlib.sha256(password.encode()).hexdigest() == USERS["customer"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        else:
            st.subheader("🔐 Admin Login")
            username = st.text_input("Username", key="admin_user_id")
            password = st.text_input("Password", type="password", key="admin_pass_id")

            if st.button("Login", use_container_width=True, key="admin_btn"):
                if username == "admin" and hashlib.sha256(password.encode()).hexdigest() == USERS["admin"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Admin"
                    st.session_state.username = username
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        st.divider()
        st.markdown("""
        ### Demo Credentials:
        **Manager:** manager / manager123  
        **Staff:** staff / staff123  
        **Customer:** customer / customer123  
        **Admin:** admin / admin123
        """)

# ============================================================================
# CUSTOMER DASHBOARD PAGE - WITH CAMPAIGN TAB
# ============================================================================

def customer_dashboard_page():
    st.markdown("<h2 class='main-title'>Dashboard</h2>", unsafe_allow_html=True)

    customer = CUSTOMER_DATA["customer"]

    # CREATE TABS FOR DIFFERENT SECTIONS
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "💰 My Purchases",
        "📦 My Chits",
        "🎯 Campaigns",
        "ℹ️ Account"
    ])

    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    with tab1:
        st.markdown("")

        # Gold & Silver Rates Section
        st.subheader("Gold & Silver Rates")
        st.markdown("")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class='rate-card'>
                <h4>Gold Price</h4>
                <h2>₹{TODAY_RATES['gold']['current']:,}</h2>
                <p>Per Gram</p>
                <p style='color: #7cb342;'>↑ ₹{TODAY_RATES['gold']['change']} from yesterday</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='rate-card'>
                <h4>Silver Price</h4>
                <h2>₹{TODAY_RATES['silver']['current']}</h2>
                <p>Per Gram</p>
                <p style='color: #7cb342;'>↑ ₹{TODAY_RATES['silver']['change']} from yesterday</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='rate-card'>
                <h4>Your Tier</h4>
                <h2>{customer['loyalty_tier']}</h2>
                <p>Status</p>
                <p style='color: #7cb342;'>{customer['loyalty_points']} Points</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
        st.divider()

        # Purchase Summary Section
        st.subheader("Your Purchase Summary")
        st.markdown("")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Spent", f"₹{customer['total_spent']:,}", "Premium Customer")
        with col2:
            st.metric("Total Purchases", len(customer['purchases']), f"{customer['tier']} Tier")
        with col3:
            st.metric("Active Chits", len(customer['chits']), "₹3,00,000 Total")
        with col4:
            st.metric("Loyalty Points", customer['loyalty_points'], "+150 this month")

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    # ========================================================================
    # TAB 2: MY PURCHASES
    # ========================================================================
    with tab2:
        st.markdown("")
        st.subheader("Your Recent Purchases")

        purchases_df = pd.DataFrame({
            'Date': [p['date'] for p in customer['purchases']],
            'Item': [p['item'] for p in customer['purchases']],
            'Quantity': [p['quantity'] for p in customer['purchases']],
            'Amount': [f"₹{p['amount']:,}" for p in customer['purchases']],
            'Status': [p['status'] for p in customer['purchases']]
        })

        st.dataframe(purchases_df, use_container_width=True, hide_index=True)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        st.success(f"✅ Total Purchases: {len(customer['purchases'])} items | Total Spent: ₹{customer['total_spent']:,}")

    # ========================================================================
    # TAB 3: MY CHITS
    # ========================================================================
    with tab3:
        st.markdown("")
        st.subheader("Your Pending Amounts (Chit Payments)")

        pending_data = []
        for chit in customer['chits']:
            pending_data.append({
                'Chit Name': chit['name'],
                'Total Amount': f"₹{chit['amount']:,}",
                'Paid': f"₹{chit['paid']:,}",
                'Pending': f"₹{chit['pending']:,}",
                'Status': chit['status']
            })

        pending_df = pd.DataFrame(pending_data)
        st.dataframe(pending_df, use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class='warning-box'>
        <strong>Total Pending Amount: ₹{sum([c['pending'] for c in customer['chits']]):,}</strong><br>
        Pay before due date to maintain your Premium status!
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💳 Pay Now", use_container_width=True):
                st.success("Payment gateway opening...")
        with col2:
            if st.button("📅 Schedule Payment", use_container_width=True):
                st.info("Payment scheduled for future date")
        with col3:
            if st.button("📧 Payment Reminder", use_container_width=True):
                st.success("Reminder email sent!")

    # ========================================================================
    # TAB 4: CAMPAIGNS (NEW COMPREHENSIVE TAB)
    # ========================================================================
    with tab4:
        st.markdown("")
        st.subheader("Campaign Notifications You Received")
        st.markdown("View all campaigns and exclusive offers available for you")

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        # Filter campaigns
        filter_type = st.radio(
            "Filter Campaigns:",
            ["All Campaigns", "Active Only", "Upcoming Only", "Received Only"],
            horizontal=True,
            key="campaign_filter"
        )

        st.markdown("")

        # Filter logic
        filtered_campaigns = CAMPAIGNS.copy()

        if filter_type == "Active Only":
            filtered_campaigns = [c for c in filtered_campaigns if c['status'] == 'Active']
        elif filter_type == "Upcoming Only":
            filtered_campaigns = [c for c in filtered_campaigns if c['status'] == 'Upcoming']
        elif filter_type == "Received Only":
            filtered_campaigns = [c for c in filtered_campaigns if c['received']]

        # Display campaigns
        if filtered_campaigns:
            for i, campaign in enumerate(filtered_campaigns, 1):
                # Determine card style based on status
                if campaign['status'] == 'Active' and campaign['received']:
                    card_class = "campaign-card campaign-active"
                    status_icon = "✅"
                elif campaign['status'] == 'Upcoming':
                    card_class = "campaign-card campaign-upcoming"
                    status_icon = "📅"
                else:
                    card_class = "campaign-card campaign-expired"
                    status_icon = "⏳"

                st.markdown(f"""
                <div class='{card_class}'>
                    <h4>{status_icon} {campaign['name']}</h4>
                    <p><strong>Discount:</strong> {campaign['discount']}</p>
                    <p><strong>Status:</strong> {campaign['status']}</p>
                    <p><strong>Valid:</strong> {campaign['start_date']} to {campaign['end_date']}</p>
                    <p style='color: #a8a8a8;'>{campaign['description']}</p>
                    <p style='color: #7cb342; margin-top: 10px;'><strong>Terms:</strong> {campaign['terms']}</p>
                </div>
                """, unsafe_allow_html=True)

                # Action buttons for each campaign
                col1, col2, col3 = st.columns([1, 1, 2])

                with col1:
                    if campaign['status'] == 'Active':
                        if st.button(f"🛍️ Shop Now", key=f"shop_{i}", use_container_width=True):
                            st.success(f"Opening {campaign['name']} collection!")

                with col2:
                    if st.button(f"📋 Details", key=f"details_{i}", use_container_width=True):
                        st.info(f"More information about {campaign['name']}")

                with col3:
                    if campaign['received'] and campaign['received_date']:
                        st.markdown(f"<p style='color: #7cb342; text-align: center;'>📨 Received on {campaign['received_date']}</p>", unsafe_allow_html=True)
                    elif not campaign['received']:
                        st.markdown("<p style='color: #fbc02d; text-align: center;'>⏰ Coming Soon</p>", unsafe_allow_html=True)

                st.markdown("")
        else:
            st.info("No campaigns match your filter criteria")

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
        st.divider()

        # Campaign Summary Section
        st.subheader("Your Campaign Benefits")

        active_campaigns = len([c for c in CAMPAIGNS if c['status'] == 'Active' and c['received']])
        upcoming_campaigns = len([c for c in CAMPAIGNS if c['status'] == 'Upcoming'])
        total_discount = "₹10,000+" if active_campaigns > 0 else "₹0"

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Active Campaigns", active_campaigns, "Available Now")
        with col2:
            st.metric("Upcoming Campaigns", upcoming_campaigns, "Coming Soon")
        with col3:
            st.metric("Loyalty Points Earned", customer['loyalty_points'], "Through campaigns")
        with col4:
            st.metric("Est. Savings", total_discount, "This year")

    # ========================================================================
    # TAB 5: ACCOUNT INFO
    # ========================================================================
    with tab5:
        st.markdown("")
        st.subheader("Your Account Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class='info-box'>
                <strong>👤 Profile Details</strong><br>
                <br>
                <strong>Name:</strong> {customer['name']}<br>
                <strong>Membership Tier:</strong> {customer['loyalty_tier']}<br>
                <strong>Account Status:</strong> Active<br>
                <strong>Member Since:</strong> March 2023
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='success-box'>
                <strong>🎁 Loyalty Status</strong><br>
                <br>
                <strong>Loyalty Points:</strong> {customer['loyalty_points']}<br>
                <strong>Tier Benefits:</strong> {customer['loyalty_tier']} Member<br>
                <strong>Point Value:</strong> ₹{customer['loyalty_points']}<br>
                <strong>Next Tier Unlocks At:</strong> 1,000 Points
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
        st.divider()

        st.subheader("Account Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✏️ Edit Profile", use_container_width=True):
                st.success("Profile edit mode enabled")

        with col2:
            if st.button("🔒 Change Password", use_container_width=True):
                st.success("Password change initiated")

        with col3:
            if st.button("📞 Contact Support", use_container_width=True):
                st.info("Contacting our support team...")

# ============================================================================
# MANAGER DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>Dashboard</h2>", unsafe_allow_html=True)

    dates = pd.date_range(start='2025-11-01', end='2025-12-11', freq='D')
    sales_data = np.random.randint(50000, 200000, len(dates))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Sales", f"₹{sum(sales_data):,}", "+₹5,000")
    with col2:
        st.metric("Total Customers", "1,250", "+45")
    with col3:
        st.metric("Stock Value", "₹45,00,000", "-₹2,00,000")
    with col4:
        st.metric("Active Chits", "85", "+12")

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sales Trend")
        fig = px.line(x=dates, y=sales_data, title="Daily Sales Trend")
        fig.update_layout(paper_bgcolor='#0f0f0f', plot_bgcolor='#1a1a1a', font=dict(color='#e8e8e8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories)
        fig.update_layout(paper_bgcolor='#0f0f0f', font=dict(color='#e8e8e8'))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>Customers</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["All Customers", "Add Customer"])

    with tab1:
        st.subheader("Customer List")
        customers_df = pd.DataFrame({
            'ID': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
            'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard'],
            'Total Purchases': ['₹5,00,000', '₹3,50,000', '₹1,80,000', '₹2,20,000', '₹80,000'],
            'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25']
        })
        st.dataframe(customers_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Add New Customer")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", key="cust_name")
            st.text_input("Email", key="cust_email")
        with col2:
            st.selectbox("Customer Tier", ["Standard", "Silver", "Gold", "Premium"], key="cust_tier")
            st.date_input("Date of Birth", key="cust_dob")

        if st.button("Add Customer", use_container_width=True):
            st.success("Customer added successfully!")

# ============================================================================
# SMART COMMANDS PAGE - FIXED SPACING
# ============================================================================

def smart_commands_page():
    st.markdown("<h2 class='main-title'>Smart Commands - Staff Alerts</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>Smart Command System</strong><br>
    Send alerts to staff members instantly!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

    st.subheader("Quick Alerts")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("Alert Ram - 15000", use_container_width=True, key="alert_ram", help="Send alert to Ram Kumar"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Ram about pending rupees 15000"},
                {"role": "assistant", "content": "Alert Sent\n\nRam Kumar notified\nAmount: ₹15,000\nTime: " + datetime.now().strftime("%H:%M")}
            ]
            st.rerun()

    with col2:
        if st.button("Alert Priya - 8500", use_container_width=True, key="alert_priya", help="Send alert to Priya Singh"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Priya about pending rupees 8500"},
                {"role": "assistant", "content": "Alert Sent\n\nPriya Singh notified\nAmount: ₹8,500\nTime: " + datetime.now().strftime("%H:%M")}
            ]
            st.rerun()

    with col3:
        if st.button("Notify All Staff", use_container_width=True, key="alert_all", help="Send alert to all staff"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Send notification to all staff"},
                {"role": "assistant", "content": "Broadcast Sent\n\nAll 5 staff notified\nTime: " + datetime.now().strftime("%H:%M")}
            ]
            st.rerun()

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    st.divider()

    st.subheader("Send Custom Alert")
    st.markdown("")

    col1, col2 = st.columns([4, 1])

    with col1:
        custom_command = st.text_input("Enter your message", placeholder="e.g., Alert Ram about pending", key="custom_cmd", label_visibility="collapsed")

    with col2:
        send_btn = st.button("Send", use_container_width=True, key="send_cmd_btn")

    if send_btn and custom_command:
        command_lower = custom_command.lower()
        staff_alerts = {
            "ram": {"name": "Ram Kumar", "pending": "₹15,000"},
            "priya": {"name": "Priya Singh", "pending": "₹8,500"},
            "amit": {"name": "Amit Verma", "pending": "₹12,000"},
            "neha": {"name": "Neha Sharma", "pending": "₹5,500"}
        }

        response = "Command not recognized"

        if "alert" in command_lower or "notify" in command_lower:
            found = False
            for staff_key, staff_info in staff_alerts.items():
                if staff_key in command_lower:
                    response = f"Alert Sent\n\n{staff_info['name']} notified\nMessage: {custom_command}\nTime: {datetime.now().strftime('%H:%M')}"
                    found = True
                    break

            if not found and "all" in command_lower:
                response = f"Broadcast Sent\n\nAll staff notified\nMessage: {custom_command}\nTime: {datetime.now().strftime('%H:%M')}"

        st.session_state.smart_command_messages.append({"role": "user", "content": custom_command})
        st.session_state.smart_command_messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    st.divider()

    st.subheader("Command History")
    st.markdown("")

    if st.session_state.smart_command_messages:
        for message in st.session_state.smart_command_messages:
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"**You:** {message['content']}")
    else:
        st.info("No commands sent yet. Send your first alert above!")

# ============================================================================
# OTHER PAGES (SIMPLIFIED)
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>Inventory</h2>", unsafe_allow_html=True)
    inventory_df = pd.DataFrame({
        'Item': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
        'Quantity': [45, 120, 15, 8, 32],
        'Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000'],
        'Status': ['In Stock', 'In Stock', 'Low Stock', 'Critical', 'In Stock']
    })
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

def campaigns_page():
    st.markdown("<h2 class='main-title'>Campaigns</h2>", unsafe_allow_html=True)
    campaigns_df = pd.DataFrame({
        'Campaign': ['Diwali Sale', 'Wedding Season', 'Clearance Sale', 'New Year'],
        'Discount': ['20%', '15%', '30%', '25%'],
        'Status': ['Active', 'Active', 'Active', 'Scheduled'],
        'Revenue': ['₹45L', '₹32L', '₹25L', '₹0']
    })
    st.dataframe(campaigns_df, use_container_width=True, hide_index=True)

def quick_actions_page():
    st.markdown("<h2 class='main-title'>Quick Actions</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Daily Report", use_container_width=True):
            st.success("Report generated!")
    with col2:
        if st.button("Process Payments", use_container_width=True):
            st.success("5 payments processed")
    with col3:
        if st.button("Stock Check", use_container_width=True):
            st.success("Stock verified")

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>AI Assistant</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='success-box'>
    <strong>AI-Powered Insights</strong><br>
    Get smart recommendations for your jewellery business!
    </div>
    """, unsafe_allow_html=True)
    st.info("Sales trending upward 15% this month")
    st.info("87% customers are repeat buyers")
    st.warning("Platinum inventory critical - Reorder immediately")

def chatbot_page():
    st.markdown("<h2 class='main-title'>Chatbot</h2>", unsafe_allow_html=True)
    if prompt := st.chat_input("Ask me anything!"):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("How can I help you with your jewellery business?")

def staff_management_page():
    st.markdown("<h2 class='main-title'>Staff Management</h2>", unsafe_allow_html=True)
    staff_df = pd.DataFrame({
        'Name': ['Ram Kumar', 'Priya Singh', 'Amit Verma', 'Neha Sharma'],
        'Position': ['Sales Executive', 'Manager', 'Sales Associate', 'Cashier'],
        'Pending': ['₹15,000', '₹8,500', '₹12,000', '₹5,500'],
        'Status': ['Pending', 'Pending', 'Pending', 'Pending']
    })
    st.dataframe(staff_df, use_container_width=True, hide_index=True)

def tax_compliance_page():
    st.markdown("<h2 class='main-title'>Tax & Compliance</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Period", "Q4 2025")
    with col2:
        st.metric("Income", "₹25L")
    with col3:
        st.metric("Liability", "₹3.75L")
    with col4:
        st.metric("Paid", "₹2.5L")

def my_purchases_page():
    st.markdown("<h2 class='main-title'>My Purchases</h2>", unsafe_allow_html=True)
    customer = CUSTOMER_DATA["customer"]
    purchases_df = pd.DataFrame({
        'Date': [p['date'] for p in customer['purchases']],
        'Item': [p['item'] for p in customer['purchases']],
        'Amount': [f"₹{p['amount']:,}" for p in customer['purchases']],
        'Status': [p['status'] for p in customer['purchases']]
    })
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

def my_chits_page():
    st.markdown("<h2 class='main-title'>My Chits</h2>", unsafe_allow_html=True)
    customer = CUSTOMER_DATA["customer"]
    chits_df = pd.DataFrame({
        'Name': [c['name'] for c in customer['chits']],
        'Amount': [f"₹{c['amount']:,}" for c in customer['chits']],
        'Paid': [f"₹{c['paid']:,}" for c in customer['chits']],
        'Pending': [f"₹{c['pending']:,}" for c in customer['chits']],
        'Status': [c['status'] for c in customer['chits']]
    })
    st.dataframe(chits_df, use_container_width=True, hide_index=True)

def offers_page():
    st.markdown("<h2 class='main-title'>Offers & Rewards</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='success-box'>
    Active Offers:<br>
    - 15% Wedding Season Discount<br>
    - 30% Clearance Sale<br>
    - Free Maintenance for 1 Year
    </div>
    """, unsafe_allow_html=True)

def my_summary_page():
    st.markdown("<h2 class='main-title'>My Summary</h2>", unsafe_allow_html=True)
    customer = CUSTOMER_DATA["customer"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", f"₹{customer['total_spent']:,}")
    with col2:
        st.metric("Purchases", len(customer['purchases']))
    with col3:
        st.metric("Active Chits", len(customer['chits']))
    with col4:
        st.metric("Loyalty Tier", customer['loyalty_tier'])

def support_chat_page():
    st.markdown("<h2 class='main-title'>Support Chat</h2>", unsafe_allow_html=True)
    if prompt := st.chat_input("Message our support team"):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("Thank you! Our team will respond soon.")

def settings_page():
    st.markdown("<h2 class='main-title'>Settings</h2>", unsafe_allow_html=True)
    st.text_input("Full Name", value="Admin")
    st.text_input("Email", value="admin@jewellery.com")
    if st.button("Save"):
        st.success("Saved!")

def sales_record_page():
    st.markdown("<h2 class='main-title'>Sales Record</h2>", unsafe_allow_html=True)
    st.info("Your sales records appear here")

def loyalty_program_page():
    st.markdown("<h2 class='main-title'>Loyalty Program</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tier", "Gold")
    with col2:
        st.metric("Points", "890")
    with col3:
        st.metric("Redemptions", "5")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>Welcome, {st.session_state.username}!</h3>", unsafe_allow_html=True)
            st.markdown(f"**Role:** {st.session_state.user_role}")
            st.markdown("")
            st.divider()

            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)

            st.markdown("")
            st.divider()

            if st.button("Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

        # PAGE ROUTING
        if selected_page == "Dashboard":
            if st.session_state.user_role == "Customer":
                customer_dashboard_page()
            else:
                dashboard_page()
        elif selected_page == "Customers":
            customers_page()
        elif selected_page == "Inventory":
            inventory_page()
        elif selected_page == "Tax & Compliance":
            tax_compliance_page()
        elif selected_page == "Campaigns":
            campaigns_page()
        elif selected_page == "Staff Management":
            staff_management_page()
        elif selected_page == "Quick Actions":
            quick_actions_page()
        elif selected_page == "AI Assistant":
            ai_assistant_page()
        elif selected_page == "Smart Commands":
            smart_commands_page()
        elif selected_page == "Chatbot":
            chatbot_page()
        elif selected_page == "My Purchases":
            my_purchases_page()
        elif selected_page == "My Chits":
            my_chits_page()
        elif selected_page == "Offers & Rewards":
            offers_page()
        elif selected_page == "My Summary":
            my_summary_page()
        elif selected_page == "Support Chat":
            support_chat_page()
        elif selected_page == "Sales Record":
            sales_record_page()
        elif selected_page == "Loyalty Program":
            loyalty_program_page()
        elif selected_page == "Settings":
            settings_page()

if __name__ == "__main__":
    main()
