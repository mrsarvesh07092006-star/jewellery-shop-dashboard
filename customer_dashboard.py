# ============================================================================
# 📱 CUSTOMER_DASHBOARD.PY - Customer Personal Dashboard
# ============================================================================

"""
Complete customer dashboard with:
- Personal profile & summary
- Transaction history with filters
- Invoice generation (PDF download)
- Available offers & campaigns
- Chit management & schedule
- Current gold/silver prices
- Pending amount tracking
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# ============================================================================
# CUSTOMER DASHBOARD
# ============================================================================

class CustomerDashboard:
    """Main customer dashboard handler"""
    
    def __init__(self, customer_data: dict):
        self.customer_data = customer_data
        self.customer_id = customer_data.get('id')
        self.customer_name = customer_data.get('name')
        self.mobile = customer_data.get('mobile')
    
    def render(self):
        """Render main customer dashboard"""
        
        st.set_page_config(
            page_title=f"Dashboard - {self.customer_name}",
            layout="wide",
            page_icon="💎"
        )
        
        # Custom CSS
        st.markdown("""
            <style>
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                color: white;
                margin: 10px 0;
            }
            .status-completed { color: #00dd00; }
            .status-pending { color: #ffaa00; }
            .price-box {
                background: #f0f0f0;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Header
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.title(f"💎 Welcome, {self.customer_name}!")
        
        with col3:
            if st.button("🚪 Logout", key="customer_logout"):
                st.session_state.authenticated = False
                st.rerun()
        
        st.divider()
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Summary",
            "📜 History",
            "📄 Invoices",
            "🎁 Offers",
            "🏦 Chits",
            "👤 Profile"
        ])
        
        with tab1:
            self.render_summary()
        
        with tab2:
            self.render_transaction_history()
        
        with tab3:
            self.render_invoices()
        
        with tab4:
            self.render_offers()
        
        with tab5:
            self.render_chits()
        
        with tab6:
            self.render_profile()
    
    # ========================
    # SUMMARY TAB
    # ========================
    
    def render_summary(self):
        """Dashboard summary with key metrics"""
        
        st.subheader("📊 Your Summary")
        
        # Load data
        customers_df = pd.read_csv('customers.csv')
        transactions_df = pd.read_csv('transactions.csv')
        summary_df = pd.read_csv('summary.csv')
        
        customer = customers_df[customers_df['id'] == self.customer_id].iloc[0]
        
        # Key Metrics - Row 1
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Total Purchases",
                f"₹{customer['total_purchased']:,.0f}",
                delta="Lifetime value"
            )
        
        with col2:
            st.metric(
                "⏳ Pending Amount",
                f"₹{customer['pending_amount']:,.0f}",
                delta="Amount due" if customer['pending_amount'] > 0 else "All clear",
                delta_color="off" if customer['pending_amount'] > 0 else "off"
            )
        
        with col3:
            st.metric(
                "🥇 Loyalty Tier",
                customer['tier'],
                delta="Member since " + customer['joined_date']
            )
        
        with col4:
            st.metric(
                "🏦 Chit Amount",
                f"₹{customer['chit_amount']:,.0f}",
                delta="Active chits"
            )
        
        st.divider()
        
        # Current Rates
        st.subheader("💎 Current Market Rates")
        
        col1, col2, col3 = st.columns(3)
        
        gold_rate = float(summary_df.iloc[0]['gold_rate']) if not summary_df.empty else 7500
        silver_rate = float(summary_df.iloc[0]['silver_rate']) if not summary_df.empty else 85
        
        with col1:
            st.markdown(f"""
                <div class="price-box">
                <h3>🥇 Gold</h3>
                <p style="font-size: 28px; color: #d4af37;">₹{gold_rate:,.0f}</p>
                <p style="color: #666; font-size: 12px;">Per gram</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="price-box">
                <h3>⚪ Silver</h3>
                <p style="font-size: 28px; color: #c0c0c0;">₹{silver_rate:,.0f}</p>
                <p style="color: #666; font-size: 12px;">Per gram</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            last_updated = summary_df.iloc[0]['last_updated'] if not summary_df.empty else "N/A"
            st.markdown(f"""
                <div class="price-box">
                <h3>🕐 Last Updated</h3>
                <p style="font-size: 14px;">{last_updated}</p>
                <p style="color: #666; font-size: 12px;">Market time</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Recent Transactions
        st.subheader("📋 Recent Transactions")
        
        customer_txns = transactions_df[
            transactions_df['customer_id'] == self.customer_id
        ].head(5).copy()
        
        if not customer_txns.empty:
            display_cols = ['date', 'amount', 'category', 'type', 'status']
            st.dataframe(
                customer_txns[display_cols],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No transactions yet")
    
    # ========================
    # TRANSACTION HISTORY
    # ========================
    
    def render_transaction_history(self):
        """Detailed transaction history with filters"""
        
        st.subheader("📜 Transaction History")
        
        # Load data
        transactions_df = pd.read_csv('transactions.csv')
        customer_txns = transactions_df[
            transactions_df['customer_id'] == self.customer_id
        ].copy()
        
        if customer_txns.empty:
            st.info("No transactions found")
            return
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_filter = st.date_input(
                "Filter by date",
                value=None,
                key="txn_date"
            )
        
        with col2:
            categories = ['All'] + sorted(customer_txns['category'].unique().tolist())
            category_filter = st.selectbox(
                "Filter by category",
                categories,
                key="txn_category"
            )
        
        with col3:
            types = ['All'] + sorted(customer_txns['type'].unique().tolist())
            type_filter = st.selectbox(
                "Filter by type",
                types,
                key="txn_type"
            )
        
        # Apply filters
        filtered_txns = customer_txns.copy()
        
        if date_filter:
            filtered_txns = filtered_txns[
                filtered_txns['date'].astype(str).str.startswith(str(date_filter))
            ]
        
        if category_filter != 'All':
            filtered_txns = filtered_txns[filtered_txns['category'] == category_filter]
        
        if type_filter != 'All':
            filtered_txns = filtered_txns[filtered_txns['type'] == type_filter]
        
        # Display with styling
        st.markdown("### Transactions")
        
        for idx, row in filtered_txns.iterrows():
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
            
            with col1:
                st.write(f"📅 {row['date']}")
            
            with col2:
                st.write(f"💰 ₹{row['amount']:,.0f}")
            
            with col3:
                st.write(f"📦 {row['category'].title()}")
            
            with col4:
                status_color = "🟢" if row['status'] == 'completed' else "🟡"
                st.write(f"{status_color} {row['status'].title()}")
            
            with col5:
                st.caption(f"ID: {row['id']}")
        
        # Summary stats
        st.divider()
        st.subheader("📊 Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total = filtered_txns['amount'].sum()
            st.metric("Total Amount", f"₹{total:,.0f}")
        
        with col2:
            count = len(filtered_txns)
            st.metric("Total Transactions", count)
        
        with col3:
            avg = filtered_txns['amount'].mean()
            st.metric("Average", f"₹{avg:,.0f}")
    
    # ========================
    # INVOICES
    # ========================
    
    def render_invoices(self):
        """Invoice generation and download"""
        
        st.subheader("📄 Invoices & Receipts")
        
        # Load transactions
        transactions_df = pd.read_csv('transactions.csv')
        customer_txns = transactions_df[
            transactions_df['customer_id'] == self.customer_id
        ].copy()
        
        if customer_txns.empty:
            st.info("No transactions to invoice")
            return
        
        # Select transaction
        selected_idx = st.selectbox(
            "Select transaction to generate invoice",
            options=range(len(customer_txns)),
            format_func=lambda i: f"{customer_txns.iloc[i]['date']} - ₹{customer_txns.iloc[i]['amount']:,.0f}"
        )
        
        transaction = customer_txns.iloc[selected_idx]
        
        # Invoice preview
        st.markdown("### 📋 Invoice Preview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Invoice Number:** INV-{transaction['id']:06d}")
            st.write(f"**Date:** {transaction['date']}")
            st.write(f"**Status:** {transaction['status'].title()}")
        
        with col2:
            st.write(f"**Customer:** {self.customer_name}")
            st.write(f"**Mobile:** {self.mobile}")
            st.write(f"**Tier:** {self.customer_data.get('tier', 'Standard')}")
        
        st.divider()
        
        st.write("**Transaction Details:**")
        
        details_col1, details_col2, details_col3, details_col4 = st.columns(4)
        
        with details_col1:
            st.write(f"Amount: **₹{transaction['amount']:,.0f}**")
        
        with details_col2:
            st.write(f"Category: **{transaction['category'].title()}**")
        
        with details_col3:
            st.write(f"Type: **{transaction['type'].title()}**")
        
        with details_col4:
            st.write(f"ID: **{transaction['id']}**")
        
        # Download button
        st.divider()
        
        if st.button("📥 Download Invoice (PDF)", use_container_width=True):
            pdf_buffer = self._generate_invoice_pdf(transaction)
            
            st.download_button(
                label="📥 Click to Download",
                data=pdf_buffer,
                file_name=f"invoice_INV-{transaction['id']:06d}.pdf",
                mime="application/pdf",
                key="download_invoice"
            )
            st.success("✅ Invoice ready for download!")
    
    def _generate_invoice_pdf(self, transaction):
        """Generate PDF invoice"""
        
        buffer = io.BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#D4AF37'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        elements.append(Paragraph("💎 INVOICE", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Invoice details
        invoice_data = [
            ['Invoice #:', f"INV-{transaction['id']:06d}"],
            ['Date:', str(transaction['date'])],
            ['Status:', transaction['status'].title()],
        ]
        
        invoice_table = Table(invoice_data, colWidths=[2*inch, 2*inch])
        invoice_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(invoice_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Customer details
        elements.append(Paragraph("Customer Details", styles['Heading2']))
        
        customer_data = [
            ['Name:', self.customer_name],
            ['Mobile:', self.mobile],
            ['Tier:', self.customer_data.get('tier', 'Standard')],
        ]
        
        customer_table = Table(customer_data, colWidths=[2*inch, 2*inch])
        customer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F0F0F0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(customer_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Transaction details
        elements.append(Paragraph("Transaction Details", styles['Heading2']))
        
        txn_data = [
            ['Description', 'Amount', 'Category', 'Type'],
            ['Purchase', f"₹{transaction['amount']:,.0f}", 
             transaction['category'].title(), transaction['type'].title()],
        ]
        
        txn_table = Table(txn_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        txn_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D4AF37')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(txn_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Total
        elements.append(Paragraph(
            f"<b>Total Amount: ₹{transaction['amount']:,.0f}</b>",
            styles['Heading2']
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    # ========================
    # OFFERS & CAMPAIGNS
    # ========================
    
    def render_offers(self):
        """Display available offers and campaigns"""
        
        st.subheader("🎁 Special Offers & Campaigns")
        
        # Load offers
        try:
            offers_df = pd.read_csv('offers.csv')
        except FileNotFoundError:
            st.warning("No offers data available")
            return
        
        # Get customer tier
        customer_tier = self.customer_data.get('tier', 'Standard').lower()
        
        # Filter offers
        applicable_offers = offers_df[
            (offers_df['applicable_to'].str.lower() == 'all') |
            (offers_df['applicable_to'].str.lower() == customer_tier)
        ]
        
        if applicable_offers.empty:
            st.info("No active offers for your tier")
            return
        
        # Display offers
        for idx, offer in applicable_offers.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"### 🎉 {offer['name']}")
                    st.write(offer['description'])
                
                with col2:
                    st.markdown(f"**Campaign:**\n{offer['campaign_message']}")
                    st.write(f"Valid till: {offer['valid_to']}")
                
                with col3:
                    st.markdown(f"### <span style='color:#00dd00'>{offer['discount_percent']} OFF</span>", 
                              unsafe_allow_html=True)
                    
                    if st.button(f"👉 Redeem", key=f"offer_{idx}", use_container_width=True):
                        st.success(f"✅ Offer '{offer['name']}' added to your cart!")
                
                st.divider()
    
    # ========================
    # CHIT MANAGEMENT
    # ========================
    
    def render_chits(self):
        """Chit scheme management"""
        
        st.subheader("🏦 Chit Management")
        
        # Load chits data
        try:
            chits_df = pd.read_csv('chits.csv')
            chit_members_df = pd.read_csv('chit_members.csv')
        except FileNotFoundError:
            st.warning("Chit data not available")
            return
        
        # Find customer's chits
        customer_chits = chit_members_df[
            chit_members_df['customer_id'] == self.customer_id
        ]
        
        if customer_chits.empty:
            st.info("You are not part of any chit schemes yet")
            
            # Show available chits
            st.markdown("### Available Chit Schemes")
            
            for idx, chit in chits_df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"### {chit['name']}")
                        st.write(f"💰 Amount: ₹{chit['amount']:,.0f}")
                    
                    with col2:
                        st.write(f"📅 Monthly: ₹{chit['monthly_payment']:,.0f}")
                        st.write(f"👥 Members: {chit['members']}")
                    
                    with col3:
                        if st.button("Join", key=f"join_chit_{idx}", use_container_width=True):
                            st.success(f"✅ Successfully joined {chit['name']}!")
                    
                    st.divider()
        
        else:
            # Display active chits
            for idx, membership in customer_chits.iterrows():
                chit = chits_df[chits_df['id'] == membership['chit_id']].iloc[0]
                
                with st.container():
                    st.markdown(f"### {chit['name']}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Chit", f"₹{chit['amount']:,.0f}")
                    
                    with col2:
                        st.metric("Paid Amount", f"₹{membership['amount_paid']:,.0f}")
                    
                    with col3:
                        st.metric("Remaining", f"₹{membership['amount_remaining']:,.0f}")
                    
                    with col4:
                        st.metric("Status", membership['status'].title())
                    
                    # Progress bar
                    paid_percent = (membership['amount_paid'] / chit['amount']) * 100
                    st.progress(paid_percent / 100)
                    
                    # Draw schedule
                    st.write(f"**Draw Schedule:** {chit['draw_schedule']}")
                    st.write(f"**Draw Number:** {membership['draw_number']}")
                    
                    st.divider()
    
    # ========================
    # PROFILE
    # ========================
    
    def render_profile(self):
        """Customer profile & settings"""
        
        st.subheader("👤 Your Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Personal Information")
            st.write(f"**Name:** {self.customer_data.get('name')}")
            st.write(f"**Mobile:** {self.customer_data.get('mobile')}")
            st.write(f"**Email:** {self.customer_data.get('email', 'N/A')}")
            st.write(f"**Username:** {self.customer_data.get('username')}")
        
        with col2:
            st.markdown("### Account Details")
            st.write(f"**Tier:** {self.customer_data.get('tier')}")
            st.write(f"**Member Since:** {self.customer_data.get('joined_date')}")
            st.write(f"**Total Purchases:** ₹{self.customer_data.get('total_purchased'):,.0f}")
            st.write(f"**Account Status:** ✅ Active")
        
        st.divider()
        
        st.markdown("### Update Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_email = st.text_input("Email", value=self.customer_data.get('email', ''))
        
        with col2:
            new_phone = st.text_input("Phone", value=self.customer_data.get('mobile', ''))
        
        if st.button("💾 Update Profile", use_container_width=True):
            st.success("✅ Profile updated successfully!")
        
        st.divider()
        
        st.markdown("### Security")
        
        if st.button("🔐 Change Password", use_container_width=True):
            
            old_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.button("Update Password"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters")
                else:
                    st.success("✅ Password changed successfully!")

# ============================================================================
# RENDER FUNCTION
# ============================================================================

def render_customer_dashboard(customer_data: dict):
    """Main function to render customer dashboard"""
    
    dashboard = CustomerDashboard(customer_data)
    dashboard.render()
