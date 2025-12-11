import streamlit as st
import pandas as pd

def render_customer_dashboard(user_data):
    """Render the customer dashboard"""
    st.set_page_config(page_title="Customer Dashboard", layout="wide", page_icon="👤")
    
    # Header
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.title("👤 Customer Dashboard")
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    # Customer info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mobile", user_data.get('mobile', 'N/A'))
    
    with col2:
        st.metric("Tier", "Gold")
    
    with col3:
        st.metric("Total Purchased", "₹5,00,000")
    
    with col4:
        st.metric("Pending Amount", "₹50,000")
    
    st.divider()
    
    # Main navigation
    customer_tabs = st.tabs([
        "📊 Dashboard",
        "🛍️ Purchases",
        "💎 Chits",
        "💰 Offers",
        "📋 Transactions"
    ])
    
    with customer_tabs[0]:
        st.subheader("📊 Overview")
        st.info("Your account summary appears here")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Account Status:** Active ✅")
            st.write("**Membership Tier:** Gold 🏆")
        
        with col2:
            st.write("**Join Date:** 2025-01-15")
            st.write("**Loyalty Points:** 5,000")
    
    with customer_tabs[1]:
        st.subheader("🛍️ Your Purchases")
        st.info("Recent purchase history appears here")
        
        purchase_data = {
            'Date': ['2025-12-10', '2025-12-08', '2025-12-05'],
            'Item': ['Gold Ring', 'Silver Necklace', 'Diamond Earrings'],
            'Amount': ['₹50,000', '₹25,000', '₹75,000'],
            'Status': ['Completed', 'Completed', 'Completed']
        }
        st.dataframe(purchase_data, use_container_width=True)
    
    with customer_tabs[2]:
        st.subheader("💎 Chit Membership")
        st.info("Your chit participation details")
        
        chit_data = {
            'Chit Name': ['Gold Chit 100K', 'Premium Chit 150K'],
            'Status': ['Active', 'Active'],
            'Amount Paid': ['₹500,000', '₹750,000'],
            'Remaining': ['₹500,000', '₹750,000']
        }
        st.dataframe(chit_data, use_container_width=True)
    
    with customer_tabs[3]:
        st.subheader("💰 Available Offers")
        st.info("Special offers available for you")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🎉 Gold Member Bonus
            **12% Discount** on all gold items
            - Valid till: 2025-12-31
            - Click to apply coupon
            """)
            if st.button("Apply", key="offer1"):
                st.success("Coupon applied! 🎉")
        
        with col2:
            st.markdown("""
            #### ✨ New Year Bonanza
            **20% Discount** on rings & bracelets
            - Valid till: 2026-01-31
            - Limited time offer!
            """)
            if st.button("Apply", key="offer2"):
                st.success("Coupon applied! 🎉")
    
    with customer_tabs[4]:
        st.subheader("📋 Transaction History")
        st.info("All your transactions")
        
        transaction_data = {
            'Date': ['2025-12-10', '2025-12-08', '2025-12-05', '2025-12-01'],
            'Type': ['Sale', 'Payment', 'Sale', 'Adjustment'],
            'Amount': ['₹50,000', '₹25,000', '₹75,000', '₹10,000'],
            'Status': ['Completed', 'Completed', 'Completed', 'Completed'],
            'Invoice': ['INV20251210001', 'INV20251208002', 'INV20251205003', 'INV20251201004']
        }
        st.dataframe(transaction_data, use_container_width=True)
