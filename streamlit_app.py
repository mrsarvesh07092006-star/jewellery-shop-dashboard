"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v8.1
Complete AI + BI System with Fixed Errors
Fixed: Command History Display Error
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
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# Light Theme Only
THEME = {
    "bg_color": "#f8f9fa",
    "card_bg": "#ffffff",
    "text_color": "#1a1a1a",
    "text_secondary": "#666666",
    "border_color": "#e0e0e0",
    "primary": "#FFD700",
    "success_bg": "#d4edda",
    "warning_bg": "#fff3cd",
    "error_bg": "#f8d7da",
    "info_bg": "#d1ecf1"
}

# Dynamic CSS Styling
st.markdown(f"""
<style>
    :root {{
        --bg-color: {THEME['bg_color']};
        --card-bg: {THEME['card_bg']};
        --text-color: {THEME['text_color']};
        --text-secondary: {THEME['text_secondary']};
        --border-color: {THEME['border_color']};
        --primary: {THEME['primary']};
    }}

    * {{
        color: var(--text-color);
    }}

    body {{
        background-color: var(--bg-color);
    }}

    .main {{
        background-color: var(--bg-color);
    }}

    .main-title {{ 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: {THEME['primary']}; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    .ai-response {{
        background-color: var(--card-bg);
        border: 2px solid {THEME['primary']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}

    .info-box {{ 
        background-color: {THEME['info_bg']}; 
        border-left: 4px solid #17a2b8; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state - FIXED VERSION
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.smart_command_messages = []  # Initialize as empty list
    st.session_state.customer_messages = []
    st.session_state.chatbot_messages = []
    st.session_state.ai_messages = []

# TODAY'S RATES
TODAY_RATES = {
    "gold": {"current": 7850, "previous": 7800, "change": 50, "currency": "₹"},
    "silver": {"current": 95, "previous": 92, "change": 3, "currency": "₹"}
}

# STAFF DATA
STAFF_MEMBERS = {
    "ram": {"name": "Ram Kumar", "position": "Sales Executive", "pending": "₹15,000"},
    "priya": {"name": "Priya Singh", "position": "Manager", "pending": "₹8,500"},
    "amit": {"name": "Amit Verma", "position": "Sales Associate", "pending": "₹12,000"},
    "neha": {"name": "Neha Sharma", "position": "Cashier", "pending": "₹5,500"}
}

# ============================================================================
# AUTHENTICATION
# ============================================================================

USERS = {
    "manager": {
        "password": hashlib.sha256("manager123".encode()).hexdigest(),
        "role": "Manager",
        "name": "Manager"
    },
    "staff": {
        "password": hashlib.sha256("staff123".encode()).hexdigest(),
        "role": "Sales Staff",
        "name": "Sales Staff"
    },
    "customer": {
        "password": hashlib.sha256("customer123".encode()).hexdigest(),
        "role": "Customer",
        "name": "Customer"
    },
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Admin",
        "name": "Admin"
    }
}

def get_accessible_pages(role):
    pages = {
        "Manager": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "👨‍💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Smart Commands",
            "💬 Chatbot"
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "💾 Sales Record",
            "🎁 Loyalty Program",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Chatbot"
        ],
        "Customer": [
            "🛍️ My Purchases",
            "💎 My Chits",
            "🎁 Offers & Rewards",
            "📊 My Summary",
            "💬 Support Chat"
        ],
        "Admin": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "👨‍💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Smart Commands",
            "💬 Chatbot",
            "⚙️ Settings"
        ]
    }
    return pages.get(role, [])

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

            if st.button("🔓 Login", use_container_width=True, key="mgr_btn"):
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif login_type == "Staff":
            st.subheader("👤 Staff Login")
            username = st.text_input("Username", key="staff_user_id")
            password = st.text_input("Password", type="password", key="staff_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="staff_btn"):
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif login_type == "Customer":
            st.subheader("🛍️ Customer Login")
            username = st.text_input("Username", key="cust_user_id")
            password = st.text_input("Password", type="password", key="cust_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="cust_btn"):
                if username == "customer" and hashlib.sha256(password.encode()).hexdigest() == USERS["customer"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        else:
            st.subheader("🔐 Admin Login")
            username = st.text_input("Username", key="admin_user_id")
            password = st.text_input("Password", type="password", key="admin_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="admin_btn"):
                if username == "admin" and hashlib.sha256(password.encode()).hexdigest() == USERS["admin"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Admin"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        st.divider()
        st.markdown("""
        ### 📝 Demo Credentials:
        **Manager:** username: `manager` | password: `manager123`
        **Staff:** username: `staff` | password: `staff123`
        **Customer:** username: `customer` | password: `customer123`
        **Admin:** username: `admin` | password: `admin123`
        """)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)

    dates = pd.date_range(start='2025-11-01', end='2025-12-11', freq='D')
    sales_data = np.random.randint(50000, 200000, len(dates))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Sales", f"₹{sum(sales_data):,}", "+₹5,000")
    with col2:
        st.metric("👥 Total Customers", "1,250", "+45")
    with col3:
        st.metric("📦 Stock Value", "₹45,00,000", "-₹2,00,000")
    with col4:
        st.metric("💎 Active Chits", "85", "+12")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Sales Trend")
        fig = px.line(x=dates, y=sales_data, title="Daily Sales (Nov-Dec 2025)")
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Sales (₹)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💍 Product Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories, title="Product Sales by Category")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 All Customers", "➕ Add Customer"])

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

        if st.button("✅ Add Customer", use_container_width=True):
            st.success("✅ Customer added successfully!")

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)

    inventory_df = pd.DataFrame({
        'Item Code': ['GLD001', 'SLV002', 'DMD003', 'PLT004', 'GLD005'],
        'Item Name': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
        'Category': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Gold'],
        'Quantity': [45, 120, 15, 8, 32],
        'Unit Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000'],
        'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low Stock', '🔴 Critical', '✅ In Stock']
    })

    st.subheader("Current Inventory")
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

# ============================================================================
# CAMPAIGNS PAGE
# ============================================================================

def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Active Campaigns", "➕ Create Campaign"])

    with tab1:
        st.subheader("📊 All Active Campaigns")
        campaigns_df = pd.DataFrame({
            'Campaign Name': ['🎄 Diwali Sale 2025', '💒 Wedding Season', '🎉 Clearance Sale', '✨ New Year Special'],
            'Start Date': ['2025-10-15', '2025-11-01', '2025-12-01', '2025-12-25'],
            'End Date': ['2025-12-31', '2025-03-31', '2025-12-31', '2026-01-15'],
            'Discount': ['20%', '15%', '30%', '25%'],
            'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟡 Scheduled'],
            'Revenue': ['₹45,00,000', '₹32,00,000', '₹25,00,000', '₹0'],
            'ROI': ['285%', '250%', '180%', 'TBD']
        })
        st.dataframe(campaigns_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("➕ Create New Campaign")
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Campaign Name", key="camp_name")
            st.selectbox("Campaign Type", ["Seasonal Sale", "Festival Offer", "Clearance"], key="camp_type")
            st.slider("Discount %", 5, 50, 15, key="camp_discount")

        with col2:
            st.number_input("Target Revenue (₹)", min_value=100000, step=100000, key="camp_target")
            st.number_input("Marketing Budget (₹)", min_value=10000, step=10000, key="camp_budget")
            st.date_input("End Date", key="camp_end")

        if st.button("🚀 Launch Campaign", use_container_width=True):
            st.success("✅ Campaign launched successfully!")
            st.balloons()

# ============================================================================
# SMART COMMANDS PAGE - FIXED VERSION
# ============================================================================

def smart_commands_page():
    st.markdown("<h2 class='main-title'>💬 Smart Commands - Staff Alerts</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>🎯 Smart Command System</strong><br>
    Send alerts and commands to staff members. Example: "Alert Ram about pending ₹15,000" or "Send notification to all staff about meeting"
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔔 Alert Ram - Pending ₹15,000", use_container_width=True, key="alert_ram"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Ram about pending ₹15,000"},
                {"role": "assistant", "content": "🔔 **Alert Sent Successfully**\n\n✅ Ram Kumar has been notified\n📛 Alert: Pending amount ₹15,000\n⏰ Time: " + datetime.now().strftime("%H:%M") + "\n📱 Status: Delivered via SMS & In-app notification"}
            ]
            st.rerun()

    with col2:
        if st.button("🔔 Alert Priya - Pending ₹8,500", use_container_width=True, key="alert_priya"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Priya about pending ₹8,500"},
                {"role": "assistant", "content": "🔔 **Alert Sent Successfully**\n\n✅ Priya Singh has been notified\n📛 Alert: Pending amount ₹8,500\n⏰ Time: " + datetime.now().strftime("%H:%M") + "\n📱 Status: Delivered via SMS & In-app notification"}
            ]
            st.rerun()

    with col3:
        if st.button("📢 Notify All Staff", use_container_width=True, key="alert_all"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Send notification to all staff"},
                {"role": "assistant", "content": "📢 **Broadcast Alert Sent Successfully**\n\n✅ All 5 staff members notified\n👥 Recipients: Ram, Priya, Amit, Neha, Vikram\n⏰ Time: " + datetime.now().strftime("%H:%M") + "\n📱 Status: All delivered"}
            ]
            st.rerun()

    st.divider()

    st.subheader("📤 Send Custom Alert/Command")

    col1, col2 = st.columns([3, 1])

    with col1:
        custom_command = st.text_input(
            "Enter command",
            placeholder="e.g., 'Alert Ram about his pending amount' or 'Send notification to all staff'",
            key="custom_cmd"
        )

    with col2:
        send_btn = st.button("📤 Send", use_container_width=True, key="send_cmd_btn")

    if send_btn and custom_command:
        command_lower = custom_command.lower()

        staff_alerts = {
            "ram": {"name": "Ram Kumar", "pending": "₹15,000"},
            "priya": {"name": "Priya Singh", "pending": "₹8,500"},
            "amit": {"name": "Amit Verma", "pending": "₹12,000"},
            "neha": {"name": "Neha Sharma", "pending": "₹5,500"}
        }

        response = "❌ Command not recognized. Please try: 'Alert [staff name] about [message]' or 'Send notification to all staff'"

        if "alert" in command_lower or "notify" in command_lower or "send" in command_lower:
            found = False
            for staff_key, staff_info in staff_alerts.items():
                if staff_key in command_lower:
                    response = f"""🔔 **Alert Sent Successfully**

✅ {staff_info['name']} has been notified
📛 Alert: {custom_command}
⏰ Time: {datetime.now().strftime("%H:%M")}
📱 Status: Delivered via SMS & In-app notification
💰 Pending: {staff_info['pending']}"""
                    found = True
                    break

            if not found and "all" in command_lower:
                response = f"""📢 **Broadcast Alert Sent Successfully**

✅ All 5 staff members notified
👥 Recipients: Ram, Priya, Amit, Neha, Vikram
📌 Message: {custom_command}
⏰ Time: {datetime.now().strftime("%H:%M")}
📱 Status: All delivered"""

        st.session_state.smart_command_messages.append({"role": "user", "content": custom_command})
        st.session_state.smart_command_messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.divider()

    st.subheader("📋 Command History")

    # FIXED: Only display if messages exist
    if st.session_state.smart_command_messages:
        for message in st.session_state.smart_command_messages:
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"**Command:** {message['content']}")
    else:
        st.info("✅ No commands sent yet. Send a command above to see history here.")

# ============================================================================
# CHATBOT PAGE
# ============================================================================

def chatbot_page():
    st.markdown("<h2 class='main-title'>💬 Smart Chatbot</h2>", unsafe_allow_html=True)

    st.subheader("🎯 Quick Help Topics")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📦 Purchase Help", use_container_width=True, key="cb_purchase"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "📦 **Your Purchases:** You have 4 purchase records. Most recent: Gold Ring (Dec 10, ₹15,000). All items delivered ✅. You earned 890 loyalty points!"}]
            st.rerun()

    with col2:
        if st.button("💎 Chit Support", use_container_width=True, key="cb_chit"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "💎 **Your Chits:** You have 2 active chits: Gold 12-Month (₹1,00,000) and Diamond Savings (₹2,00,000)"}]
            st.rerun()

    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True, key="cb_loyalty"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "🎁 **Loyalty Program:** You're in Gold Tier with 890 points. Redeem 100 points = ₹50 discount!"}]
            st.rerun()

    st.divider()

    # Display chat messages
    if st.session_state.chatbot_messages:
        for message in st.session_state.chatbot_messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything!"):
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Simple response logic
        response = "Thank you for contacting us! How can I help you today?"

        if any(word in prompt.lower() for word in ["purchase", "buy", "order"]):
            response = "📦 Your recent purchases are delivered. You earned 890 loyalty points!"
        elif any(word in prompt.lower() for word in ["chit", "payment", "installment"]):
            response = "💎 You have 2 active chits. Next payment due Dec 15."
        elif any(word in prompt.lower() for word in ["loyalty", "points", "discount"]):
            response = "🎁 You're in Gold tier! Enjoy 15% birthday discount and free maintenance."
        elif any(word in prompt.lower() for word in ["offer", "sale", "discount"]):
            response = "🎉 Active offers: 15% wedding discount, 30% clearance sale!"

        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>Welcome, {st.session_state.username}! ({st.session_state.user_role})</h3>", unsafe_allow_html=True)
            st.divider()

            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)

            st.divider()

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

        # Route to pages
        if selected_page == "📊 Dashboard":
            dashboard_page()
        elif selected_page == "👥 Customers":
            customers_page()
        elif selected_page == "📦 Inventory":
            inventory_page()
        elif selected_page == "📢 Campaigns":
            campaigns_page()
        elif selected_page == "💬 Smart Commands":
            smart_commands_page()
        elif selected_page == "💬 Chatbot":
            chatbot_page()

if __name__ == "__main__":
    main()
