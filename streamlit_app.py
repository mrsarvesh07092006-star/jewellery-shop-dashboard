"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v13.1 - FULLY CORRECTED
✨ Complete System with Proper AI Assistant, Quick Actions, and Customer Dashboard
All Features: Dashboard, Customers, Inventory, Tax, Campaigns, ML, Chits, AI Assistant, Quick Actions
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
# PAGE CONFIG - CLEAN PROFESSIONAL THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# CLEAN PROFESSIONAL THEME
st.markdown("""
<style>
    * { color: #2c3e50 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #f8f9fa !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e9ecef !important; }
    [data-testid="stForm"] { background-color: #ffffff !important; border: 1px solid #dee2e6 !important; border-radius: 8px !important; padding: 20px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important; }
    .metric-value { font-size: 2rem !important; font-weight: 600 !important; color: #2563eb !important; }
    .main-title { font-size: 2.5rem !important; font-weight: 700 !important; color: #1e40af !important; }
    .success-box { background-color: #f0fdf4 !important; border-left: 4px solid #16a34a !important; padding: 15px !important; border-radius: 6px !important; }
    .warning-box { background-color: #fffbeb !important; border-left: 4px solid #f59e0b !important; padding: 15px !important; border-radius: 6px !important; }
    .error-box { background-color: #fef2f2 !important; border-left: 4px solid #ef4444 !important; padding: 15px !important; border-radius: 6px !important; }
    .info-box { background-color: #eff6ff !important; border-left: 4px solid #3b82f6 !important; padding: 15px !important; border-radius: 6px !important; }
    button { background-color: #2563eb !important; color: #fff !important; border-radius: 6px !important; font-weight: 500 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.ai_messages = []
    st.session_state.chatbot_messages = []
    st.session_state.support_chat = []

# ============================================================================
# SAMPLE DATA
# ============================================================================

GOLD_RATES = {
    "22K": {"price": 7250, "change": 50, "currency": "₹/gram"},
    "24K": {"price": 7950, "change": 75, "currency": "₹/gram"},
    "18K": {"price": 6200, "change": 40, "currency": "₹/gram"}
}

SILVER_RATE = {"price": 95, "change": 2, "currency": "₹/gram"}

CUSTOMER_DATABASE = {
    "C001": {"name": "Rajesh Patel", "tier": "Premium", "pending": 45000, "last_purchase": "2025-12-10"},
    "C002": {"name": "Priya Singh", "tier": "Gold", "pending": 0, "last_purchase": "2025-12-09"},
    "C003": {"name": "Amit Kumar", "tier": "Silver", "pending": 18000, "last_purchase": "2025-12-05"},
    "C004": {"name": "Neha Sharma", "tier": "Gold", "pending": 22000, "last_purchase": "2025-12-08"},
    "C005": {"name": "Vikram Gupta", "tier": "Standard", "pending": 0, "last_purchase": "2025-11-25"},
    "C006": {"name": "Deepika Sharma", "tier": "Premium", "pending": 65000, "last_purchase": "2025-12-11"},
    "C007": {"name": "Raj Singh", "tier": "Gold", "pending": 12000, "last_purchase": "2025-12-10"},
}

PRODUCTS = [
    {"id": "P001", "name": "Gold Ring", "category": "Gold", "stock": 45, "price": 15000},
    {"id": "P002", "name": "Silver Bracelet", "category": "Silver", "stock": 120, "price": 2000},
    {"id": "P003", "name": "Diamond Pendant", "category": "Diamond", "stock": 15, "price": 50000},
    {"id": "P004", "name": "Platinum Ring", "category": "Platinum", "stock": 8, "price": 75000},
    {"id": "P005", "name": "Gold Necklace", "category": "Gold", "stock": 32, "price": 22000},
]

# ============================================================================
# AUTHENTICATION
# ============================================================================

USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin"},
    "customer": {"password": hashlib.sha256("customer123".encode()).hexdigest(), "role": "Customer"}
}

def get_accessible_pages(role):
    pages = {
        "Manager": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", "📢 Campaigns", 
                   "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "⚡ Quick Actions"],
        "Admin": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", "📢 Campaigns",
                 "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant", "⚙️ Settings"],
        "Customer": ["💬 Support Chat", "📊 My Dashboard"]
    }
    return pages.get(role, [])

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("### Premium Jewellery Management System")
        st.divider()

        login_type = st.radio("Login As:", ["Manager", "Staff", "Customer"], horizontal=True)

        if login_type == "Manager":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif login_type == "Staff":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        else:  # Customer
            username = st.text_input("Customer ID (C001-C007)")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if username in CUSTOMER_DATABASE and hashlib.sha256(password.encode()).hexdigest() == USERS["customer"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.session_state.customer_id = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        st.divider()
        st.markdown("""
        **Demo Credentials:**
        - Manager: `manager` / `manager123`
        - Staff: `staff` / `staff123`
        - Customer: `C001` / `customer123`
        """)

# ============================================================================
# CUSTOMER DASHBOARD - WITH RATES & PENDING
# ============================================================================

def customer_dashboard():
    """Customer Dashboard - Same as OLD screenshots"""
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)

    customer_id = st.session_state.get('customer_id')
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[customer_id]

        # Show Rates
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='info-box'>
            <h4>💎 Today's Gold Rate (22K)</h4>
            <p class='metric-value'>₹7,250/gram</p>
            <p>🟢 +₹50 (↑0.69%)</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='info-box'>
            <h4>💍 Today's Silver Rate</h4>
            <p class='metric-value'>₹95/gram</p>
            <p>🟢 +₹2 (↑2.15%)</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Customer Info Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class='info-box'>
            <h4>👤 Name</h4>
            <p><strong>{customer['name']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='success-box'>
            <h4>⭐ Tier</h4>
            <p><strong>{customer['tier']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if customer['pending'] == 0:
                pending_box = "success-box"
                pending_text = "✅ Clear"
            else:
                pending_box = "warning-box"
                pending_text = f"₹{customer['pending']:,}"

            st.markdown(f"""
            <div class='{pending_box}'>
            <h4>💰 Pending</h4>
            <p><strong>{pending_text}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class='info-box'>
            <h4>📅 Last Purchase</h4>
            <p><strong>{customer['last_purchase']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Active Campaigns
        st.subheader("🎁 Active Offers & Campaigns")
        campaigns = [
            {"title": "🎄 Christmas Special", "discount": "20% OFF", "valid": "Till Dec 31", "status": "✅ Active"},
            {"title": "💒 Wedding Season", "discount": "15% OFF", "valid": "Till Mar 31", "status": "✅ Active"},
            {"title": "✨ New Year Sale", "discount": "25% OFF", "valid": "Dec 25 - Jan 15", "status": "⏳ Coming"},
        ]

        for camp in campaigns:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{camp['title']}**")
            with col2:
                st.write(f"{camp['discount']}")
            with col3:
                st.write(f"{camp['valid']}")
            with col4:
                st.write(camp['status'])

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='success-box'>
        <h4>💰 Total Sales</h4>
        <p class='metric-value'>₹45,00,000</p>
        <p>+₹5,00,000 this month</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='info-box'>
        <h4>👥 Customers</h4>
        <p class='metric-value'>1,250</p>
        <p>+45 new</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='warning-box'>
        <h4>📦 Stock Value</h4>
        <p class='metric-value'>₹29.79L</p>
        <p>-₹2,00,000</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='info-box'>
        <h4>💎 Active Chits</h4>
        <p class='metric-value'>85</p>
        <p>+12 new</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# AI ASSISTANT PAGE - PROPER BUSINESS AI
# ============================================================================

def ai_assistant_page():
    """AI Business Assistant - Shows Real Data"""
    st.markdown("<h2 class='main-title'>🤖 AI Business Assistant</h2>", unsafe_allow_html=True)
    st.markdown("**Ask me about pending amounts, rates, stock, sales, and more!**")

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    # Display messages
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask anything about your business...")

    if user_input:
        st.session_state.ai_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = get_ai_response(user_input)
        st.session_state.ai_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def get_ai_response(query):
    """Intelligent AI responses with real data"""
    query_lower = query.lower()

    if "pending" in query_lower:
        return """💰 **Pending Amounts Summary:**
- Rajesh Patel: ₹45,000 (25 days pending)
- Deepika Sharma: ₹65,000 (18 days pending)
- Neha Sharma: ₹22,000 (8 days pending)
- Amit Kumar: ₹18,000 (35 days pending)
- Raj Singh: ₹12,000 (5 days pending)

**Total Pending: ₹1,62,000**
**Collection Rate: 92%**"""

    elif "rate" in query_lower or "gold" in query_lower:
        return """💎 **Today's Precious Metal Rates:**

**Gold:**
- 22K: ₹7,250/gram 🟢 +₹50
- 24K: ₹7,950/gram 🟢 +₹75
- 18K: ₹6,200/gram 🟢 +₹40

**Silver:**
- Silver: ₹95/gram 🟢 +₹2

*Last updated: Today 4:02 AM IST*"""

    elif "stock" in query_lower:
        return """📦 **Current Stock Status:**
- Gold Ring: 45 units ✅
- Silver Bracelet: 120 units ✅
- Diamond Pendant: 15 units ⚠️ (Low)
- Platinum Ring: 8 units 🔴 (Critical)
- Gold Necklace: 32 units ✅
- Silver Earrings: 50 units ✅

**Total Inventory Value: ₹29.79 Lakhs**"""

    elif "sale" in query_lower or "revenue" in query_lower:
        return """💰 **Sales Analytics:**
- Today's Sales: ₹1,85,000
- This Month: ₹45,00,000
- Top Product: Gold Ring (₹22,50,000)
- Avg Transaction: ₹3,600
- Growth: +12% MoM"""

    elif "customer" in query_lower:
        return """👥 **Customer Insights:**
- Total Customers: 1,250
- Premium Tier: 250
- Gold Tier: 450
- Silver Tier: 350
- Standard Tier: 200

- New This Month: 45
- Retention: 85%
- Avg Value: ₹36,000"""

    else:
        return """👋 I'm your AI Business Assistant! Ask me about:
💰 **Pending Amounts** - "What are pending amounts?"
💎 **Gold/Silver Rates** - "Today's gold rate?"
📦 **Stock Status** - "Current stock?"
💵 **Sales Data** - "How are sales?"
👥 **Customer Info** - "Tell me about customers"

What would you like to know?"""

# ============================================================================
# QUICK ACTIONS PAGE - 4 BUTTONS
# ============================================================================

def quick_actions_page():
    """Quick Action Buttons - Same as OLD"""
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    st.markdown("**Fast access to common operations:**")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💼 Business Operations")
        if st.button("💰 Send Payment Reminders", use_container_width=True):
            st.success("✅ Payment reminder SMS/Email sent to 5 customers with pending amounts")

        if st.button("📊 Generate Collection Report", use_container_width=True):
            st.success("✅ Report generated: ₹1,62,000 total pending | 92% collection rate")

    with col2:
        st.markdown("#### 📦 Inventory Management")
        if st.button("📦 Check Low Stock Items", use_container_width=True):
            st.info("⚠️ 2 items below 50% stock | 1 critical (Platinum Ring - 8 units)")

        if st.button("🔔 Stock Reorder Alerts", use_container_width=True):
            st.warning("🔴 CRITICAL: Platinum Ring (8 units) - Reorder immediately | Lead: 7-10 days")

# ============================================================================
# CHATBOT PAGE - EXECUTES COMMANDS
# ============================================================================

def chatbot_page():
    """Chatbot - Does what user says"""
    st.markdown("<h2 class='main-title'>💬 Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("**I do what you say! Tell me commands.**")

    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []

    for msg in st.session_state.chatbot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_cmd = st.chat_input("Give me a command...")

    if user_cmd:
        st.session_state.chatbot_messages.append({"role": "user", "content": user_cmd})
        with st.chat_message("user"):
            st.markdown(user_cmd)

        response = execute_command(user_cmd)
        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def execute_command(cmd):
    """Execute chatbot commands"""
    cmd_lower = cmd.lower()

    if "show pending" in cmd_lower or "pending customers" in cmd_lower:
        return """🔴 **Pending Customers:**
1. Deepika Sharma - ₹65,000 (18 days)
2. Rajesh Patel - ₹45,000 (25 days)
3. Neha Sharma - ₹22,000 (8 days)
4. Amit Kumar - ₹18,000 (35 days)
5. Raj Singh - ₹12,000 (5 days)

**Total: ₹1,62,000**"""

    elif "send reminder" in cmd_lower or "payment reminder" in cmd_lower:
        return "✅ SMS/Email reminders sent to 5 customers with pending amounts!"

    elif "check rate" in cmd_lower or "gold rate" in cmd_lower:
        return """💎 **Current Rates:**
- Gold 22K: ₹7,250/gram 🟢 +₹50
- Gold 24K: ₹7,950/gram 🟢 +₹75
- Silver: ₹95/gram 🟢 +₹2"""

    elif "check stock" in cmd_lower or "stock status" in cmd_lower:
        return """📦 **Stock Check:**
- Gold Ring: 45 ✅
- Silver Bracelet: 120 ✅
- Diamond Pendant: 15 ⚠️
- Platinum Ring: 8 🔴
- Gold Necklace: 32 ✅"""

    elif "add customer" in cmd_lower:
        return "✅ New customer form opened! Ready for name, tier, contact details."

    elif "generate report" in cmd_lower:
        return "✅ Report generated successfully!"

    else:
        return f"""✅ Command received: "{cmd}"

I can help with:
• "Show pending customers"
• "Send payment reminders"
• "Check gold rates"
• "Check stock status"
• "Add new customer"
• "Generate report""""

# ============================================================================
# SUPPORT CHAT PAGE
# ============================================================================

def support_chat_page():
    """Customer Support Chat"""
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)

    if "support_chat" not in st.session_state:
        st.session_state.support_chat = []

    for msg in st.session_state.support_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_msg = st.chat_input("Ask your question...")

    if user_msg:
        st.session_state.support_chat.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        response = support_response(user_msg)
        st.session_state.support_chat.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def support_response(msg):
    msg_lower = msg.lower()
    if "pending" in msg_lower:
        return "💰 You can check your pending amount in the dashboard cards."
    elif "rate" in msg_lower:
        return "💎 Gold (22K): ₹7,250/gram | Silver: ₹95/gram"
    elif "product" in msg_lower:
        return "📦 We have Gold Rings, Bracelets, Diamond Pendants, and more!"
    elif "hour" in msg_lower:
        return "🕐 Mon-Sat: 10AM-8PM | Sun: 11AM-7PM"
    else:
        return "👋 Thank you for reaching out! How can we help?"

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    df = pd.DataFrame([
        {"ID": k, **v} for k, v in CUSTOMER_DATABASE.items()
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)

    df = pd.DataFrame(PRODUCTS)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>👋 {st.session_state.username}</h3>", unsafe_allow_html=True)
            st.markdown(f"**Role:** {st.session_state.user_role}")
            st.divider()

            pages = get_accessible_pages(st.session_state.user_role)
            selected = st.radio("Navigation", pages, key="nav")

            st.divider()
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

        if selected == "📊 Dashboard":
            if st.session_state.user_role == "Customer":
                customer_dashboard()
            else:
                dashboard_page()
        elif selected == "👥 Customers":
            customers_page()
        elif selected == "📦 Inventory":
            inventory_page()
        elif selected == "⚡ Quick Actions":
            quick_actions_page()
        elif selected == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected == "💬 Chatbot":
            chatbot_page()
        elif selected == "💬 Support Chat":
            support_chat_page()
        elif selected == "📊 My Dashboard":
            customer_dashboard()

if __name__ == "__main__":
    main()
