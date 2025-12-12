"""
💎 PREMIUM JEWELLERY DASHBOARD v6.0 ENHANCED
Complete AI + BI System with EXACT v4 Customers UI
Enhanced with ML Models, Pending Customers, At-Risk Analysis, & Slow Stock
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
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "📊 Dashboard"

# ============================================================================
# AUTHENTICATION
# ============================================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "manager": {
        "password": hash_password("manager123"),
        "role": "Manager",
        "name": "Manager"
    },
    "staff": {
        "password": hash_password("staff123"),
        "role": "Sales Staff",
        "name": "Sales Staff"
    },
    "admin": {
        "password": hash_password("admin123"),
        "role": "Admin",
        "name": "Admin"
    }
}

def get_accessible_pages(role):
    """Return pages based on user role"""
    pages = {
        "Manager": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "⚡ Quick Actions",
            "🤖 ML Models",
            "🤖 AI Assistant",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "💎 Chit Management"
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "⚡ Quick Actions"
        ],
        "Admin": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "⚡ Quick Actions",
            "🤖 ML Models",
            "🤖 AI Assistant",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "💎 Chit Management",
            "⚙️ Settings"
        ]
    }
    return pages.get(role, [])

def login_page():
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <h1>💎 Jewellery Shop AI Dashboard</h1>
        <p style="font-size: 18px; color: gray;">Premium Management System for Indian Jewellery Retail</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username", placeholder="manager")
        password = st.text_input("Password", type="password", placeholder="manager123")

        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username]["password"] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.username = username
                st.session_state.current_page = "📊 Dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

        st.markdown("---")
        st.markdown("""
        **📋 Demo Credentials:**
        - **Manager:** manager / manager123
        - **Staff:** staff / staff123
        - **Admin:** admin / admin123
        """)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_mock_customers():
    """Load mock customer data - EXACTLY LIKE v4"""
    np.random.seed(42)

    customers = []
    names = [
        "Rajesh Kumar", "Priya Singh", "Amit Patel", "Deepika Sharma", "Vikram Gupta",
        "Neha Verma", "Sanjay Pillai", "Anjali Nair", "Rohit Singh", "Pooja Reddy",
        "Arjun Rao", "Divya Joshi", "Anil Bhat", "Shreya Desai", "Manish Gupta",
        "Kavya Reddy", "Sanjiv Kumar", "Meera Sharma", "Ravi Patel", "Sneha Gupta",
        "Nikhil Singh", "Anjana Kumar", "Akshay Rao", "Divya Patel", "Rohan Joshi"
    ] * 2  # 50 customers

    tiers = ["VIP", "Regular", "Dormant"]

    for i, name in enumerate(names[:50]):
        tier_idx = np.random.randint(0, 3)
        customers.append({
            'id': i + 1,
            'name': f"{name}",
            'phone': f"98{np.random.randint(1000000, 9999999)}",
            'email': f"customer{i+1}@example.com",
            'total_spent': np.random.uniform(50000, 500000),
            'last_visit': (datetime.now() - timedelta(days=int(np.random.randint(1, 200)))).date(),
            'pending_amount': np.random.uniform(0, 100000),
            'tier': tiers[tier_idx]
        })

    return pd.DataFrame(customers)

def load_mock_transactions():
    """Load mock transaction data"""
    np.random.seed(42)
    transactions = []
    descriptions = ["Gold Ring", "Diamond", "Bracelet", "Necklace", "Earrings"]

    for i in range(200):
        desc_idx = np.random.randint(0, len(descriptions))
        transactions.append({
            'id': i + 1,
            'customer_id': np.random.randint(1, 61),
            'date': (datetime.now() - timedelta(days=int(np.random.randint(1, 90)))).date(),
            'amount': np.random.uniform(10000, 100000),
            'payment_received': np.random.uniform(5000, 100000),
            'gst': np.random.uniform(500, 5000),
            'description': descriptions[desc_idx]
        })

    return pd.DataFrame(transactions)

def load_mock_inventory():
    """Load mock inventory data"""
    np.random.seed(42)
    products = [
        ("Gold Ring - Traditional", "Rings", 22000, 35000),
        ("Diamond Ring - Solitaire", "Rings", 50000, 85000),
        ("Gold Bracelet - 22K", "Bracelets", 15000, 25000),
        ("Diamond Necklace - 18K", "Necklaces", 30000, 55000),
        ("Gold Earrings - Pair", "Earrings", 8000, 15000),
        ("Silver Ring - Oxidized", "Rings", 2000, 5000),
    ]

    inventory = []
    today = datetime.now().date()

    for _ in range(30):
        prod_idx = np.random.randint(0, len(products))
        prod_name, category, cost, price = products[prod_idx]
        stock_date = (datetime.now() - timedelta(days=int(np.random.randint(1, 180)))).date()
        days_in_stock = (today - stock_date).days

        inventory.append({
            'id': len(inventory) + 1,
            'product_name': prod_name,
            'category': category,
            'quantity': int(np.random.randint(1, 20)),
            'cost_price': cost,
            'selling_price': price,
            'margin_percent': ((price - cost) / price) * 100,
            'stock_date': stock_date,
            'days_in_stock': days_in_stock
        })

    return pd.DataFrame(inventory)

def load_mock_chit_schedule():
    """Load mock chit schedule"""
    np.random.seed(42)
    chits = []
    chit_groups = ["Group A", "Group B", "Group C"]
    payout_amounts = [100000, 150000, 200000]

    for i in range(10):
        group_idx = np.random.randint(0, len(chit_groups))
        payout_idx = np.random.randint(0, len(payout_amounts))
        chits.append({
            'id': i + 1,
            'customer_id': np.random.randint(1, 61),
            'chit_group': chit_groups[group_idx],
            'payout_date': (datetime.now() + timedelta(days=int(np.random.randint(5, 60)))).date(),
            'payout_amount': payout_amounts[payout_idx],
            'expected_spending': np.random.uniform(50000, 150000)
        })

    return pd.DataFrame(chits)

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def dashboard_page():
    """Dashboard with all metrics"""
    st.title("📊 Dashboard")

    try:
        customers_df = load_mock_customers()
        transactions_df = load_mock_transactions()
        inventory_df = load_mock_inventory()

        today = datetime.now().date()
        todays_sales = transactions_df[transactions_df['date'] == today]['amount'].sum()
        total_pending = customers_df['pending_amount'].sum()
        vip_count = len(customers_df[customers_df['tier'] == "VIP"])
        stale_items = len(inventory_df[inventory_df['days_in_stock'] > 90])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Today's Sales", f"₹{todays_sales:,.0f}", delta="12%")
        with col2:
            st.metric("Total Pending", f"₹{total_pending:,.0f}", delta="-5%")
        with col3:
            st.metric("VIP Customers", vip_count, delta="2")
        with col4:
            st.metric("Stale Items", stale_items, delta="-3")

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 Sales Trend (Last 30 Days)")
            sales_trend = transactions_df.groupby('date')['amount'].sum().reset_index()
            sales_trend = sales_trend.sort_values('date')
            if len(sales_trend) > 0:
                fig = px.line(sales_trend, x='date', y='amount', title='Daily Sales', markers=True)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("🎯 Customer Tier Distribution")
            tier_dist = customers_df['tier'].value_counts()
            if len(tier_dist) > 0:
                fig = px.pie(values=tier_dist.values, names=tier_dist.index, 
                           title='Customer Distribution',
                           color_discrete_map={"VIP": "FFD700", "Regular": "87CEEB", "Dormant": "D3D3D3"})
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("💰 Top 10 Customers with Pending Amounts")
        top_pending = customers_df.nlargest(10, 'pending_amount')[["name", "phone", "pending_amount", "last_visit"]]
        top_pending_display = top_pending.copy()
        top_pending_display['pending_amount'] = top_pending_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(top_pending_display, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

def customers_page():
    """EXACT REPLICA OF v4 CUSTOMERS UI"""
    st.title("👥 Customers")

    customers_df = load_mock_customers()

    # Create tabs - EXACTLY like v4
    tab1, tab2, tab3, tab4 = st.tabs([
        "All Customers",
        "At Risk",
        "VIP Management", 
        "Pending Customers"
    ])

    # TAB 1: All Customers
    with tab1:
        st.subheader("📋 Customer Database")

        # Search and filter
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("🔍 Search by name or phone")
        with col2:
            filter_tier = st.selectbox("Filter by Tier", ["All", "VIP", "Regular", "Dormant"])

        # Filter logic
        filtered = customers_df.copy()
        if search_term:
            filtered = filtered[
                filtered['name'].str.contains(search_term, case=False) |
                filtered['phone'].str.contains(search_term)
            ]

        if filter_tier != "All":
            filtered = filtered[filtered['tier'] == filter_tier]

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Found", len(filtered))
        with col2:
            st.metric("💰 Total Pending", f"₹{filtered['pending_amount'].sum():,.0f}")
        with col3:
            st.metric("💳 Total Spent", f"₹{filtered['total_spent'].sum():,.0f}")

        # Display table
        display_df = filtered[["name", "phone", "email", "total_spent", "pending_amount", "tier"]].copy()
        display_df['total_spent'] = display_df['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        display_df['pending_amount'] = display_df['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(display_df, use_container_width=True)

    # TAB 2: At-Risk Customers
    with tab2:
        st.subheader("⚠️ At-Risk Customers")
        st.write("**No visit for 90+ days**")

        today = datetime.now().date()
        at_risk = customers_df[
            (customers_df['last_visit'] < today - timedelta(days=90)) &
            (customers_df['pending_amount'] > 50000)
        ].copy()

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⚠️ At-Risk Count", len(at_risk))
        with col2:
            st.metric("💰 Total Pending", f"₹{at_risk['pending_amount'].sum():,.0f}")
        with col3:
            st.metric("📞 Urgent Calls Needed", len(at_risk[at_risk['pending_amount'] > 75000]))

        # Display
        at_risk_display = at_risk[["name", "phone", "pending_amount", "last_visit", "total_spent"]].copy()
        at_risk_display['pending_amount'] = at_risk_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        at_risk_display['total_spent'] = at_risk_display['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(at_risk_display, use_container_width=True)

        if st.button("📢 Send Reminder Campaign to At-Risk Customers"):
            st.success(f"✅ Campaign prepared for {len(at_risk)} customers with pending amounts!")

    # TAB 3: VIP Management
    with tab3:
        st.subheader("💎 VIP Customer Management")

        vips = customers_df[customers_df['tier'] == "VIP"].copy()

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💎 Total VIPs", len(vips))
        with col2:
            st.metric("💳 Total Spent", f"₹{vips['total_spent'].sum():,.0f}")
        with col3:
            st.metric("📊 Avg Customer Value", f"₹{vips['total_spent'].mean():,.0f}")

        # Display
        vip_display = vips[["name", "phone", "total_spent", "pending_amount", "last_visit"]].copy()
        vip_display['total_spent'] = vip_display['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        vip_display['pending_amount'] = vip_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(vip_display, use_container_width=True)

    # TAB 4: Pending Customers
    with tab4:
        st.subheader("💵 Customers with Pending Amounts")

        # Filter slider
        min_pending = st.slider("Filter by minimum pending amount", 0, 100000, 5000, 5000)

        pending_customers = customers_df[customers_df['pending_amount'] >= min_pending].copy()
        pending_customers = pending_customers.sort_values('pending_amount', ascending=False)

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"Customers with ₹{min_pending:,}+", len(pending_customers))
        with col2:
            st.metric("💰 Total Pending", f"₹{pending_customers['pending_amount'].sum():,.0f}")
        with col3:
            st.metric("📊 Avg Per Customer", f"₹{pending_customers['pending_amount'].mean():,.0f}")

        # Display
        pending_display = pending_customers[["name", "phone", "pending_amount", "tier", "total_spent"]].copy()
        pending_display['pending_amount'] = pending_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        pending_display['total_spent'] = pending_display['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(pending_display, use_container_width=True)

        if len(pending_customers) > 0 and st.button("📞 Send Payment Collection Campaign"):
            st.success(f"✅ Payment collection campaign sent to {len(pending_customers)} customers with pending amounts!")

def inventory_page():
    """Inventory management with slow stock analysis"""
    st.title("📦 Inventory Management")

    inventory_df = load_mock_inventory()

    tab1, tab2, tab3 = st.tabs(["Current Stock", "Slow Movers", "Markdown Recommendations"])

    with tab1:
        st.subheader("📋 Current Inventory Status")
        display_df = inventory_df[["product_name", "category", "quantity", "cost_price", "selling_price", "margin_percent", "days_in_stock"]].copy()
        display_df['cost_price'] = display_df['cost_price'].apply(lambda x: f"₹{x:,.0f}")
        display_df['selling_price'] = display_df['selling_price'].apply(lambda x: f"₹{x:,.0f}")
        display_df['margin_percent'] = display_df['margin_percent'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_df, use_container_width=True)

        total_value = (inventory_df['selling_price'] * inventory_df['quantity']).sum()
        st.metric("Total Inventory Value", f"₹{total_value:,.0f}")

    with tab2:
        st.subheader("🐢 Slow Moving Stock (90+ days)")
        slow_movers = inventory_df[inventory_df['days_in_stock'] > 90].copy()

        if len(slow_movers) > 0:
            st.warning(f"⚠️ {len(slow_movers)} slow-moving items detected")
            slow_display = slow_movers[["product_name", "quantity", "selling_price", "days_in_stock"]].copy()
            slow_display['selling_price'] = slow_display['selling_price'].apply(lambda x: f"₹{x:,.0f}")
            slow_display['value'] = slow_movers['quantity'] * slow_movers['selling_price']
            slow_display['value'] = slow_display['value'].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(slow_display, use_container_width=True)

            if st.button("Create Discount Campaign for Slow Items"):
                st.success("✅ Discount campaign created")
        else:
            st.success("✅ No slow-moving inventory!")

    with tab3:
        st.subheader("💰 Markdown Recommendations")
        slow_movers = inventory_df[inventory_df['days_in_stock'] > 90].copy()

        if len(slow_movers) > 0:
            st.write("**Recommended Discounts based on inventory age:**")
            recommendations = []

            for _, item in slow_movers.iterrows():
                days = item['days_in_stock']
                suggested_discount = min(30, int(days / 30) * 5)
                new_price = item['selling_price'] * (1 - suggested_discount / 100)

                recommendations.append({
                    'Product': item['product_name'],
                    'Current Price': f"₹{item['selling_price']:,.0f}",
                    'Suggested Discount': f"{suggested_discount}%",
                    'New Price': f"₹{new_price:,.0f}",
                    'Expected Conversion': f"{max(40, 100 - days // 20)}%"
                })

            rec_df = pd.DataFrame(recommendations)
            st.dataframe(rec_df, use_container_width=True)
        else:
            st.info("No slow-moving items to recommend discounts for")

def quick_actions_page():
    """Quick actions with recommendations"""
    st.title("⚡ Quick Actions")

    customers_df = load_mock_customers()
    inventory_df = load_mock_inventory()

    st.subheader("🎯 Recommended Actions")

    col1, col2 = st.columns(2)

    # Critical actions - Dead stock
    with col1:
        st.markdown("### 🔴 CRITICAL: Dead Stock (25% Markdown)")
        dead_stock = inventory_df[inventory_df['days_in_stock'] > 180]
        if len(dead_stock) > 0:
            for _, item in dead_stock.head(3).iterrows():
                recovery = item['quantity'] * item['selling_price'] * 0.25
                st.write(f"**{item['product_name']}**")
                st.write(f"- Apply 25% markdown → ₹{recovery:,.0f} recovery")
            if st.button("Execute Dead Stock Clearance"):
                st.success("✅ Dead stock clearance initiated")
        else:
            st.info("No dead stock items")

    # High priority - Slow stock
    with col2:
        st.markdown("### 🟡 HIGH: Slow Stock (15% Markdown)")
        slow_stock = inventory_df[(inventory_df['days_in_stock'] > 90) & (inventory_df['days_in_stock'] <= 180)]
        if len(slow_stock) > 0:
            for _, item in slow_stock.head(3).iterrows():
                boost = item['quantity'] * item['selling_price'] * 0.15
                st.write(f"**{item['product_name']}**")
                st.write(f"- Apply 15% markdown → ₹{boost:,.0f} boost")
            if st.button("Execute Slow Stock Markdown"):
                st.success("✅ Slow stock markdown initiated")
        else:
            st.info("No slow stock items")

def ml_models_page():
    """ML Models page with 3 advanced models"""
    st.title("🤖 ML Models")

    customers_df = load_mock_customers()
    transactions_df = load_mock_transactions()
    inventory_df = load_mock_inventory()

    tab1, tab2, tab3 = st.tabs(["Customer Risk", "Demand Forecast", "Pricing Optimization"])

    with tab1:
        st.subheader("⚠️ Customer Risk Prediction")

        customers_copy = customers_df.copy()
        today = datetime.now().date()
        customers_copy['recency_days'] = customers_copy['last_visit'].apply(lambda x: (today - x).days)
        customers_copy['churn_risk'] = (customers_copy['recency_days'] / 180 * 50 + 
                                       customers_copy['pending_amount'] / customers_copy['pending_amount'].max() * 30 +
                                       np.random.normal(10, 5, len(customers_copy))).clip(0, 100)

        high_risk = customers_copy[customers_copy['churn_risk'] > 60].copy()

        st.warning(f"⚠️ {len(high_risk)} customers at HIGH risk of churn")

        # Scatter plot
        fig = px.scatter(customers_copy, x='recency_days', y='churn_risk', 
                        hover_data=['name', 'phone'],
                        title='Customer Risk: Days Since Visit vs Churn Risk',
                        labels={'recency_days': 'Days Since Last Visit', 'churn_risk': 'Churn Risk Score'})
        st.plotly_chart(fig, use_container_width=True)

        if len(high_risk) > 0:
            st.dataframe(high_risk[["name", "phone", "pending_amount", "churn_risk"]].head(10), use_container_width=True)

    with tab2:
        st.subheader("📈 30-Day Demand Forecast")

        dates = pd.date_range(start=datetime.now().date(), periods=30)
        forecast_values = np.random.normal(25, 8, 30) * 100000
        forecast_values = np.maximum(forecast_values, 500000)

        forecast_df = pd.DataFrame({
            'date': dates,
            'forecast': forecast_values,
            'upper_bound': forecast_values * 1.2,
            'lower_bound': forecast_values * 0.8
        })

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['forecast'], 
                                mode='lines', name='Forecast', line=dict(color='blue', width=2)))
        fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['upper_bound'], 
                                fill=None, mode='lines', name='Upper Bound', 
                                line=dict(color='blue', width=0)))
        fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['lower_bound'], 
                                fill='tonexty', mode='lines', name='Lower Bound',
                                line=dict(color='blue', width=0)))

        st.plotly_chart(fig, use_container_width=True)

        total_forecast = forecast_df['forecast'].sum()
        st.metric("30-Day Total Forecast", f"₹{total_forecast:,.0f}")

    with tab3:
        st.subheader("💰 Pricing Optimization")

        selected_customer = st.selectbox("Select Customer", customers_df['name'].values)
        customer = customers_df[customers_df['name'] == selected_customer].iloc[0]

        base_price = 45000

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Cost", f"₹{base_price * 0.4:,.0f}")
        with col2:
            st.metric("Standard Price", f"₹{base_price:,.0f}")
        with col3:
            if customer['tier'] == "VIP":
                recommended = base_price * 1.08
                margin = 15
            elif customer['tier'] == "Regular":
                recommended = base_price * 0.95
                margin = 12
            else:
                recommended = base_price * 0.85
                margin = 10

            st.metric("Recommended Price", f"₹{recommended:,.0f}", delta=f"{margin}% margin")

def ai_assistant_page():
    """AI Business Assistant"""
    st.title("🤖 AI Business Assistant")

    customers_df = load_mock_customers()
    inventory_df = load_mock_inventory()
    transactions_df = load_mock_transactions()

    st.write("**Ask me anything about optimizing your jewellery business!**")

    problem_type = st.radio("What's your business challenge?", [
        "Slow Moving Inventory",
        "Customer Retention",
        "Pricing Strategy",
        "Sales Improvement",
        "Custom Question"
    ])

    if problem_type == "Slow Moving Inventory":
        slow_items = inventory_df[inventory_df['days_in_stock'] > 90]
        if len(slow_items) > 0:
            item = slow_items.iloc[0]
            st.write(f"""
            **Your Situation:**
            - Product: {item['product_name']}
            - In stock for: {item['days_in_stock']} days
            - Current price: ₹{item['selling_price']:,.0f}
            - Cost: ₹{item['cost_price']:,.0f}
            - Monthly sales: 0 units
            """)

            if st.button("Get AI Recommendations"):
                discount_price = item['selling_price'] * 0.85
                st.success("""
                **✅ Recommended Actions (Priority Order):**

                **1. Apply Strategic Discount (15-20%)**
                - New price: ₹{:,.0f}
                - Expected conversion: 60%
                - Estimated ROI: 25%

                **2. Bundle with Complementary Items**
                - Pair with lighter designs
                - Bundle discount: 10%
                - Expected conversion: 45%
                - Estimated ROI: 18%

                **3. Target Specific Segment via WhatsApp**
                - Send to high-value customers
                - Personalized offer
                - Expected conversion: 35%
                - Estimated ROI: 22%
                """.format(discount_price))
        else:
            st.info("No slow-moving inventory detected")

    elif problem_type == "Customer Retention":
        today = datetime.now().date()
        at_risk = customers_df[
            (customers_df['last_visit'] < today - timedelta(days=90)) &
            (customers_df['pending_amount'] > 50000)
        ]

        st.write(f"""
        **Your Situation:**
        - At-risk customers: {len(at_risk)}
        - Total pending from them: ₹{at_risk['pending_amount'].sum():,.0f}
        - Average customer value: ₹{customers_df['total_spent'].mean():,.0f}
        """)

        if st.button("Get Retention Strategy"):
            st.success(f"""
            **✅ 3-Step Retention Strategy:**

            **1. Immediate Payment Collection (Week 1)**
            - Send personalized reminders
            - Offer 2% discount for immediate payment
            - Expected collection rate: 60%
            - Estimated recovery: ₹{at_risk['pending_amount'].sum() * 0.6:,.0f}

            **2. Short-term Re-engagement (Weeks 2-4)**
            - Festival-specific offers
            - Exclusive "We miss you" discount: 10-15%
            - Expected conversion: 40%
            - Estimated repeat purchase: ₹{at_risk['pending_amount'].sum() * 0.4 * 0.5:,.0f}

            **3. Long-term VIP Program (Months 2-3)**
            - Classify by potential CLV
            - Special loyalty rewards
            - Quarterly exclusive previews
            - Expected retention: 80%
            """)

    elif problem_type == "Pricing Strategy":
        st.write("**AI Pricing Recommendations:**")
        if st.button("Analyze Pricing"):
            st.success("""
            **✅ Dynamic Pricing Strategy:**

            **1. VIP Customers (20% of base)**
            - Premium pricing: +8-10%
            - Exclusive designs
            - Expected margin: 15%

            **2. Regular Customers (50% of base)**
            - Standard pricing: -5%
            - Bundled offers
            - Expected margin: 12%

            **3. Dormant Customers (30% of base)**
            - Win-back pricing: -15%
            - Limited-time offers
            - Expected margin: 10%
            """)

    elif problem_type == "Sales Improvement":
        st.write("**Sales Growth Strategy:**")
        if st.button("Get Growth Roadmap"):
            st.success("""
            **✅ 30-60-90 Day Sales Plan:**

            **Month 1 - Foundation**
            - Fix 15 slow-moving items
            - Activate 50 dormant customers
            - Collect ₹10L pending amounts
            - Expected impact: ₹20L revenue

            **Month 2 - Growth**
            - Launch festival campaigns
            - Implement dynamic pricing
            - Launch VIP loyalty program
            - Expected impact: ₹35L revenue

            **Month 3 - Scale**
            - Expand product range
            - Open new channels
            - Double customer base
            - Expected impact: ₹50L revenue

            **Total 90-Day Target: ₹1.05 Crore**
            """)

    else:
        custom_q = st.text_area("What's your business question?")
        if st.button("Get AI Insights"):
            st.success("""
            **✅ AI Analysis:**

            Based on your jewellery retail data and industry benchmarks:

            - **Current Performance vs Competitors:** Good
            - **Main Opportunities:** Inventory optimization, customer segmentation
            - **Recommended Focus:** AI-driven pricing and retention campaigns
            - **Expected Impact:** 40-50% profit margin improvement

            **Next Steps:**
            1. Implement chit-aware demand forecasting
            2. Deploy festival-based churn prediction
            3. Launch WhatsApp campaigns
            4. Test dynamic pricing for top 10 products
            """)

def tax_compliance_page():
    """Tax & Compliance"""
    st.title("💰 Tax & Compliance")
    st.info("Tax Compliance & GST Calculator (Coming Soon)")

def campaigns_page():
    """Campaigns"""
    st.title("📢 Campaigns")
    st.info("Campaign Management (Coming Soon)")

def chit_management_page():
    """Chit Management"""
    st.title("💎 Chit Management")
    st.info("Chit Fund Management (Coming Soon)")

def settings_page():
    """Settings"""
    st.title("⚙️ Settings")

    if st.session_state.user_role != "Admin":
        st.error("Only Admin can access settings")
        return

    st.success("Settings (Coming Soon)")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    with st.sidebar:
        st.markdown("💎 **Jewellery Shop AI**")

        if st.session_state.authenticated:
            st.write(f"**User:** {st.session_state.username}")
            st.write(f"**Role:** {st.session_state.user_role}")

            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages, key="nav_radio")
            st.session_state.current_page = selected_page

            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.current_page = "📊 Dashboard"
                st.rerun()

        st.markdown("---")
        st.markdown("**v6.0 Enhanced** - AI Powered Jewellery Retail")

    if not st.session_state.authenticated:
        login_page()
    else:
        page = st.session_state.current_page

        if page == "📊 Dashboard":
            dashboard_page()
        elif page == "👥 Customers":
            customers_page()
        elif page == "📦 Inventory":
            inventory_page()
        elif page == "⚡ Quick Actions":
            quick_actions_page()
        elif page == "🤖 ML Models":
            ml_models_page()
        elif page == "🤖 AI Assistant":
            ai_assistant_page()
        elif page == "💰 Tax & Compliance":
            tax_compliance_page()
        elif page == "📢 Campaigns":
            campaigns_page()
        elif page == "💎 Chit Management":
            chit_management_page()
        elif page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
