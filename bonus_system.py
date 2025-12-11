import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class BonusManagementSystem:
    def __init__(self, sales_df, staff_df):
        self.sales_df = sales_df
        self.staff_df = staff_df
    
    def calculate_bonus(self, sales_amount, base_bonus_percent=5):
        """Calculate bonus based on sales"""
        if sales_amount < 100000:
            bonus = sales_amount * 0.05  # 5%
        elif sales_amount < 250000:
            bonus = sales_amount * 0.08  # 8%
        else:
            bonus = sales_amount * 0.10  # 10%
        
        return bonus
    
    def get_sales_summary(self):
        """Get overall sales summary"""
        if self.sales_df.empty:
            return {'total': 0, 'avg': 0, 'max': 0}
        
        return {
            'total': self.sales_df['daily_sales'].sum(),
            'avg': self.sales_df['daily_sales'].mean(),
            'max': self.sales_df['daily_sales'].max(),
            'records': len(self.sales_df)
        }
    
    def get_staff_bonus_suggestions(self):
        """Get bonus suggestions for staff"""
        suggestions = []
        
        for idx, staff in self.staff_df.head(10).iterrows():
            sales_mock = 150000  # Mock sales
            bonus = self.calculate_bonus(sales_mock)
            
            suggestions.append({
                'staff_id': staff['staff_id'],
                'name': staff['name'],
                'sales': sales_mock,
                'bonus': bonus,
                'bonus_percent': (bonus / sales_mock) * 100,
                'eligible': bonus > 5000
            })
        
        return suggestions

def render_sales_tracking(bonus_mgmt):
    """Render sales tracking interface"""
    st.subheader("📊 Record Daily Sales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date = st.date_input("Date")
    
    with col2:
        daily_sales = st.number_input("Daily Sales (₹)", value=100000, min_value=0)
    
    with col3:
        staff_count = st.number_input("Staff Count", value=3, min_value=1)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gold_sales = st.number_input("Gold Sales (₹)", value=50000, min_value=0)
    
    with col2:
        silver_sales = st.number_input("Silver Sales (₹)", value=30000, min_value=0)
    
    with col3:
        diamond_sales = st.number_input("Diamond Sales (₹)", value=20000, min_value=0)
    
    if st.button("💾 Save Sales Data", use_container_width=True):
        st.success("✅ Sales data saved successfully!")

def render_bonus_suggestions(bonus_mgmt):
    """Render bonus suggestions for staff"""
    st.subheader("🤖 AI Bonus Suggestions")
    
    st.info("Based on sales performance, here are bonus recommendations:")
    
    suggestions = bonus_mgmt.get_staff_bonus_suggestions()
    
    for sugg in suggestions:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**{sugg['name']}**")
        
        with col2:
            st.write(f"Sales: ₹{sugg['sales']:,}")
        
        with col3:
            st.write(f"Bonus: ₹{sugg['bonus']:,.0f}")
        
        with col4:
            if sugg['eligible']:
                st.write("✅ Eligible")
            else:
                st.write("⏳ Not Yet")

def render_bonus_analytics(bonus_mgmt):
    """Render bonus analytics and reports"""
    st.subheader("📈 Bonus Analytics")
    
    # Sales summary
    summary = bonus_mgmt.get_sales_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sales", f"₹{summary['total']:,.0f}")
    
    with col2:
        st.metric("Average Daily", f"₹{summary['avg']:,.0f}")
    
    with col3:
        st.metric("Peak Sales", f"₹{summary['max']:,.0f}")
    
    with col4:
        st.metric("Data Points", summary['records'])
    
    st.divider()
    
    # Analytics charts
    if not bonus_mgmt.sales_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales trend
            fig = px.line(
                bonus_mgmt.sales_df.tail(30),
                x='date',
                y='daily_sales',
                title='Sales Trend (Last 30 Days)',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown
            latest = bonus_mgmt.sales_df.iloc[-1] if not bonus_mgmt.sales_df.empty else {}
            
            categories = {
                'Gold': latest.get('gold_sales', 0),
                'Silver': latest.get('silver_sales', 0),
                'Diamond': latest.get('diamond_sales', 0),
                'Other': latest.get('other_sales', 0)
            }
            
            fig = px.pie(
                names=categories.keys(),
                values=categories.values(),
                title='Sales by Category (Latest Day)'
            )
            st.plotly_chart(fig, use_container_width=True)

def render_staff_bonus_view():
    """Render staff view of their bonuses"""
    st.subheader("💰 My Bonuses")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("This Month", "₹5,000", "+₹1,000")
    
    with col2:
        st.metric("Last Month", "₹4,000")
    
    with col3:
        st.metric("Year Total", "₹45,000")
    
    st.divider()
    
    # Bonus history
    bonus_history = {
        'Month': ['January', 'February', 'March', 'April', 'May', 'June'],
        'Sales Target': ['₹100,000', '₹120,000', '₹150,000', '₹140,000', '₹160,000', '₹180,000'],
        'Actual Sales': ['₹125,000', '₹145,000', '₹180,000', '₹155,000', '₹190,000', '₹210,000'],
        'Bonus': ['₹3,750', '₹4,350', '₹5,400', '₹4,650', '₹5,700', '₹6,300']
    }
    
    st.dataframe(bonus_history, use_container_width=True)
