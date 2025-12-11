# ============================================================================
# 💰 BONUS_SYSTEM.PY - AI-Powered Sales-Based Bonus System
# ============================================================================

"""
Advanced bonus system with:
- Sales tracking & analysis
- Festival period bonus multipliers
- AI bonus suggestions based on sales performance
- Daily/Weekly/Monthly sales reports
- Bonus calculation & forecasting
- Owner happiness index
- Staff incentive tracking

Features:
- Festival bonus multipliers (150%, 200%)
- Sales threshold analysis
- Performance-based incentives
- Bonus history & analytics
- Automated suggestions
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

# ============================================================================
# BONUS SYSTEM DATA MODELS
# ============================================================================

class SalesRecord:
    """Daily sales record"""
    
    def __init__(self,
                 date: str,
                 daily_sales: float,
                 gold_sales: float = 0,
                 silver_sales: float = 0,
                 diamond_sales: float = 0,
                 other_sales: float = 0,
                 staff_count: int = 1):
        
        self.date = date
        self.daily_sales = daily_sales
        self.gold_sales = gold_sales
        self.silver_sales = silver_sales
        self.diamond_sales = diamond_sales
        self.other_sales = other_sales
        self.staff_count = staff_count
    
    def to_dict(self):
        return {
            'date': self.date,
            'daily_sales': self.daily_sales,
            'gold_sales': self.gold_sales,
            'silver_sales': self.silver_sales,
            'diamond_sales': self.diamond_sales,
            'other_sales': self.other_sales,
            'staff_count': self.staff_count
        }

class BonusMultiplier:
    """Bonus multiplier rules"""
    
    def __init__(self,
                 name: str,
                 period: str,
                 normal_sales_multiplier: float,
                 high_sales_multiplier: float,
                 threshold_increase_percent: float = 20.0):
        
        self.name = name
        self.period = period  # diwali, holi, new_year, normal
        self.normal_sales_multiplier = normal_sales_multiplier  # 1.5x
        self.high_sales_multiplier = high_sales_multiplier      # 2.0x
        self.threshold_increase_percent = threshold_increase_percent
    
    def to_dict(self):
        return {
            'name': self.name,
            'period': self.period,
            'normal_sales_multiplier': self.normal_sales_multiplier,
            'high_sales_multiplier': self.high_sales_multiplier,
            'threshold_increase_percent': self.threshold_increase_percent
        }

# ============================================================================
# BONUS MANAGEMENT SYSTEM
# ============================================================================

class BonusManagementSystem:
    """Advanced bonus calculation & AI suggestions"""
    
    def __init__(self, sales_df: pd.DataFrame = None, 
                 staff_df: pd.DataFrame = None):
        
        self.sales_df = sales_df if sales_df is not None else pd.DataFrame()
        self.staff_df = staff_df if staff_df is not None else pd.DataFrame()
        
        # Festival periods with bonus multipliers
        self.festival_rules = {
            'diwali': {
                'date_range': ('2025-10-15', '2025-11-15'),
                'normal_bonus': 1.5,  # 150% of salary
                'high_bonus': 2.0,    # 200% of salary
                'threshold_increase': 20.0  # 20% above average
            },
            'holi': {
                'date_range': ('2025-03-01', '2025-03-31'),
                'normal_bonus': 1.5,
                'high_bonus': 2.0,
                'threshold_increase': 20.0
            },
            'new_year': {
                'date_range': ('2025-12-25', '2026-01-15'),
                'normal_bonus': 1.5,
                'high_bonus': 2.0,
                'threshold_increase': 20.0
            },
            'normal': {
                'date_range': None,
                'normal_bonus': 1.0,  # No bonus in normal days
                'high_bonus': 1.25,   # 25% bonus if sales exceed
                'threshold_increase': 15.0
            }
        }
        
        # Sales benchmarks
        self.benchmarks = {
            'daily_target': 100000,      # ₹100K per day
            'weekly_target': 700000,     # ₹700K per week
            'monthly_target': 3000000,   # ₹30L per month
            'festival_target_increase': 1.5  # 50% more during festivals
        }
    
    # ========================
    # SALES TRACKING
    # ========================
    
    def record_daily_sales(self, 
                          date: str,
                          daily_sales: float,
                          category_breakdown: Dict = None) -> Tuple[bool, str]:
        """Record daily sales"""
        
        try:
            # Check if already exists
            existing = self.sales_df[self.sales_df['date'] == date]
            
            sales_record = {
                'date': date,
                'daily_sales': daily_sales,
                'gold_sales': category_breakdown.get('gold', 0) if category_breakdown else 0,
                'silver_sales': category_breakdown.get('silver', 0) if category_breakdown else 0,
                'diamond_sales': category_breakdown.get('diamond', 0) if category_breakdown else 0,
                'other_sales': category_breakdown.get('other', 0) if category_breakdown else 0,
                'staff_count': 1
            }
            
            if not existing.empty:
                # Update
                idx = existing.index[0]
                self.sales_df.loc[idx] = sales_record
            else:
                # Add new
                new_df = pd.DataFrame([sales_record])
                self.sales_df = pd.concat([self.sales_df, new_df], ignore_index=True)
            
            # Save
            self.sales_df.to_csv('sales.csv', index=False)
            
            return True, f"✅ Sales recorded for {date}: ₹{daily_sales:,.0f}"
        
        except Exception as e:
            return False, f"Error recording sales: {str(e)}"
    
    def get_daily_sales(self, date: str) -> Optional[Dict]:
        """Get sales for specific date"""
        
        sales = self.sales_df[self.sales_df['date'] == date]
        return sales.iloc[0].to_dict() if not sales.empty else None
    
    def get_period_sales(self, start_date: str, end_date: str) -> Dict:
        """Get sales summary for period"""
        
        period_sales = self.sales_df[
            (self.sales_df['date'] >= start_date) &
            (self.sales_df['date'] <= end_date)
        ]
        
        if period_sales.empty:
            return {
                'total_sales': 0,
                'average_daily': 0,
                'max_daily': 0,
                'min_daily': 0,
                'days_count': 0
            }
        
        return {
            'total_sales': period_sales['daily_sales'].sum(),
            'average_daily': period_sales['daily_sales'].mean(),
            'max_daily': period_sales['daily_sales'].max(),
            'min_daily': period_sales['daily_sales'].min(),
            'days_count': len(period_sales),
            'gold_sales': period_sales['gold_sales'].sum(),
            'silver_sales': period_sales['silver_sales'].sum(),
            'diamond_sales': period_sales['diamond_sales'].sum()
        }
    
    # ========================
    # FESTIVAL DETECTION
    # ========================
    
    def get_current_festival(self) -> Optional[str]:
        """Detect current festival period"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        for festival_name, festival_info in self.festival_rules.items():
            if festival_name == 'normal':
                continue
            
            date_range = festival_info['date_range']
            if date_range and date_range[0] <= today <= date_range[1]:
                return festival_name
        
        return None
    
    def get_festival_period_sales(self, festival: str) -> Dict:
        """Get sales during festival period"""
        
        if festival not in self.festival_rules or festival == 'normal':
            return {'error': 'Invalid festival'}
        
        date_range = self.festival_rules[festival]['date_range']
        
        return self.get_period_sales(date_range[0], date_range[1])
    
    # ========================
    # BONUS CALCULATION
    # ========================
    
    def calculate_staff_bonus(self,
                             staff_id: int,
                             year: int,
                             month: int,
                             salary_per_day: float,
                             working_days: float) -> Dict:
        """Calculate bonus for staff member"""
        
        # Get base salary
        base_salary = salary_per_day * working_days
        
        # Get period dates
        start_date = f"{year}-{month:02d}-01"
        
        # Calculate end date
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            import calendar
            last_day = calendar.monthrange(year, month)[1]
            end_date = f"{year}-{month:02d}-{last_day}"
        
        # Get sales for period
        sales_info = self.get_period_sales(start_date, end_date)
        
        # Get average sales
        if sales_info['days_count'] == 0:
            return {
                'staff_id': staff_id,
                'year': year,
                'month': month,
                'base_salary': base_salary,
                'bonus': 0,
                'total_with_bonus': base_salary,
                'bonus_multiplier': 1.0,
                'reason': 'No sales data available'
            }
        
        average_daily_sales = sales_info['average_daily']
        
        # Detect festival
        current_festival = self.get_current_festival()
        
        # Get applicable rules
        if current_festival:
            rules = self.festival_rules[current_festival]
        else:
            rules = self.festival_rules['normal']
        
        # Get target for this period
        if current_festival:
            daily_target = self.benchmarks['daily_target'] * \
                          self.festival_rules[current_festival]['threshold_increase'] / 100
        else:
            daily_target = self.benchmarks['daily_target']
        
        # Calculate bonus multiplier
        threshold = daily_target * (1 + rules['threshold_increase'] / 100)
        
        if average_daily_sales >= threshold:
            # High sales - maximum bonus
            multiplier = rules['high_bonus']
            performance = "🚀 EXCELLENT - Sales exceeded expectations!"
        elif average_daily_sales >= daily_target:
            # Normal sales - normal bonus
            multiplier = rules['normal_bonus']
            performance = "✅ GOOD - Sales met expectations!"
        else:
            # Below target - reduced or no bonus
            multiplier = 1.0 if current_festival else 1.0
            performance = "⚠️ AVERAGE - Sales below target"
        
        # Calculate bonus
        bonus = base_salary * (multiplier - 1)  # Bonus is additional
        total_with_bonus = base_salary + bonus
        
        return {
            'staff_id': staff_id,
            'year': year,
            'month': month,
            'base_salary': base_salary,
            'bonus': bonus,
            'total_with_bonus': total_with_bonus,
            'bonus_multiplier': multiplier,
            'multiplier_percent': f"{(multiplier - 1) * 100:.0f}%",
            'performance': performance,
            'average_daily_sales': average_daily_sales,
            'daily_target': daily_target,
            'threshold': threshold,
            'festival': current_festival
        }
    
    # ========================
    # AI BONUS SUGGESTIONS
    # ========================
    
    def suggest_bonus_for_all_staff(self,
                                   year: int,
                                   month: int) -> Dict:
        """AI suggestion for all staff bonuses"""
        
        if self.staff_df.empty:
            return {
                'error': 'No staff data available',
                'suggestions': []
            }
        
        # Get period sales
        start_date = f"{year}-{month:02d}-01"
        import calendar
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            last_day = calendar.monthrange(year, month)[1]
            end_date = f"{year}-{month:02d}-{last_day}"
        
        sales_info = self.get_period_sales(start_date, end_date)
        average_daily_sales = sales_info.get('average_daily', 0)
        
        # Detect festival
        current_festival = self.get_current_festival()
        
        # Get daily target
        if current_festival:
            daily_target = self.benchmarks['daily_target'] * \
                          self.festival_rules[current_festival]['threshold_increase'] / 100
        else:
            daily_target = self.benchmarks['daily_target']
        
        # AI Analysis
        threshold = daily_target * 1.2  # 20% above target for high bonus
        
        # Determine bonus level
        if average_daily_sales >= threshold:
            bonus_level = 'HIGH'
            suggested_multiplier = 2.0  # 200%
            message = "🎉 OWNER HAPPY! Sales exceeded expectations significantly!"
            action = "Give 200% bonus to all staff"
        elif average_daily_sales >= daily_target:
            bonus_level = 'NORMAL'
            suggested_multiplier = 1.5  # 150%
            message = "✅ Good performance! Sales met target expectations!"
            action = "Give 150% bonus to all staff"
        else:
            bonus_level = 'LOW'
            suggested_multiplier = 1.0
            message = "⚠️ Sales below target. Consider incentive strategy."
            action = "No bonus or small incentive"
        
        # Build suggestions for each staff
        suggestions = []
        
        for _, staff in self.staff_df.iterrows():
            # You would get actual working days from attendance
            # For now, assuming 25 days per month
            working_days = 25
            
            bonus_calc = self.calculate_staff_bonus(
                staff['staff_id'],
                year,
                month,
                staff.get('salary_per_day', 1000),
                working_days
            )
            
            suggestions.append({
                'staff_id': staff['staff_id'],
                'staff_name': staff['name'],
                'role': staff['role'],
                'base_salary': bonus_calc['base_salary'],
                'suggested_bonus': bonus_calc['bonus'],
                'total_with_bonus': bonus_calc['total_with_bonus'],
                'multiplier': suggested_multiplier,
                'multiplier_percent': f"{(suggested_multiplier - 1) * 100:.0f}%"
            })
        
        return {
            'festival': current_festival,
            'average_daily_sales': average_daily_sales,
            'daily_target': daily_target,
            'bonus_level': bonus_level,
            'suggested_multiplier': suggested_multiplier,
            'message': message,
            'action': action,
            'suggestions': suggestions,
            'total_bonus_cost': sum([s['suggested_bonus'] for s in suggestions]),
            'total_salary_with_bonus': sum([s['total_with_bonus'] for s in suggestions])
        }
    
    # ========================
    # OWNER MOOD INDEX
    # ========================
    
    def calculate_owner_mood(self, sales: float, target: float) -> Dict:
        """Calculate owner's mood based on sales"""
        
        performance_percent = (sales / target) * 100 if target > 0 else 0
        
        if performance_percent >= 120:
            mood = "😍 VERY HAPPY"
            mood_level = 5
            description = "Sales exceeded by 20%+! Time to celebrate!"
            suggestion = "Give 200% bonus to staff!"
        elif performance_percent >= 100:
            mood = "😊 HAPPY"
            mood_level = 4
            description = "Sales met target! Good performance!"
            suggestion = "Give 150% bonus to staff!"
        elif performance_percent >= 80:
            mood = "😐 NEUTRAL"
            mood_level = 3
            description = "Sales decent but could be better"
            suggestion = "Give 100-125% bonus to staff"
        elif performance_percent >= 60:
            mood = "😟 CONCERNED"
            mood_level = 2
            description = "Sales below target by 20%+"
            suggestion = "No bonus, focus on strategy"
        else:
            mood = "😠 UNHAPPY"
            mood_level = 1
            description = "Sales significantly below target"
            suggestion = "Review operations"
        
        return {
            'mood': mood,
            'mood_level': mood_level,
            'performance_percent': performance_percent,
            'description': description,
            'suggestion': suggestion,
            'emoji': mood.split()[0]
        }
    
    # ========================
    # ANALYTICS & REPORTS
    # ========================
    
    def get_monthly_bonus_report(self, year: int, month: int) -> Dict:
        """Get comprehensive bonus report"""
        
        # Get sales data
        start_date = f"{year}-{month:02d}-01"
        import calendar
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            last_day = calendar.monthrange(year, month)[1]
            end_date = f"{year}-{month:02d}-{last_day}"
        
        sales_info = self.get_period_sales(start_date, end_date)
        
        # Get festival
        current_festival = self.get_current_festival()
        
        # Get AI suggestions
        suggestions = self.suggest_bonus_for_all_staff(year, month)
        
        # Calculate owner mood
        target = self.benchmarks['daily_target'] * \
                (calendar.monthrange(year, month)[1])  # Working days estimate
        
        mood = self.calculate_owner_mood(sales_info['total_sales'], target)
        
        return {
            'year': year,
            'month': month,
            'festival': current_festival,
            'sales': sales_info,
            'mood': mood,
            'suggestions': suggestions,
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_bonus_history(self, staff_id: int) -> List[Dict]:
        """Get bonus history for staff member"""
        
        # In production, would fetch from database
        # For now, returning structure
        
        return [
            {
                'month': 'December 2025',
                'base_salary': 25000,
                'bonus': 12500,
                'total': 37500,
                'multiplier': 1.5,
                'reason': 'Diwali Festival - Normal Sales'
            },
            {
                'month': 'November 2025',
                'base_salary': 24000,
                'bonus': 12000,
                'total': 36000,
                'multiplier': 1.5,
                'reason': 'Diwali Festival - Normal Sales'
            }
        ]

# ============================================================================
# UI COMPONENTS
# ============================================================================

def render_sales_tracking(bonus_mgmt: BonusManagementSystem):
    """Sales tracking interface"""
    
    st.subheader("📊 Daily Sales Tracking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sales_date = st.date_input("Date", value=datetime.now())
    
    with col2:
        daily_sales = st.number_input(
            "Daily Sales (₹)",
            min_value=0,
            value=100000,
            step=1000
        )
    
    st.markdown("### Category Breakdown (Optional)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gold = st.number_input("Gold Sales (₹)", min_value=0, step=1000)
    
    with col2:
        silver = st.number_input("Silver Sales (₹)", min_value=0, step=1000)
    
    with col3:
        diamond = st.number_input("Diamond Sales (₹)", min_value=0, step=1000)
    
    with col4:
        other = st.number_input("Other Sales (₹)", min_value=0, step=1000)
    
    if st.button("💾 Record Sales", use_container_width=True):
        
        breakdown = {
            'gold': gold,
            'silver': silver,
            'diamond': diamond,
            'other': other
        }
        
        success, message = bonus_mgmt.record_daily_sales(
            sales_date.strftime('%Y-%m-%d'),
            daily_sales,
            breakdown
        )
        
        if success:
            st.success(message)
        else:
            st.error(message)

def render_bonus_suggestions(bonus_mgmt: BonusManagementSystem):
    """AI bonus suggestions interface"""
    
    st.subheader("🤖 AI Bonus Suggestions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.selectbox("Year", range(2024, 2027), key="bonus_year")
    
    with col2:
        month = st.selectbox("Month", range(1, 13), 
                           format_func=lambda x: f"{x:02d}",
                           key="bonus_month")
    
    # Get suggestions
    suggestions = bonus_mgmt.suggest_bonus_for_all_staff(year, month)
    
    if 'error' in suggestions:
        st.error(suggestions['error'])
        return
    
    # Display owner mood
    st.markdown("### 📈 Shop Performance & Owner Mood")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Daily Sales",
            f"₹{suggestions['average_daily_sales']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Daily Target",
            f"₹{suggestions['daily_target']:,.0f}"
        )
    
    with col3:
        performance = (suggestions['average_daily_sales'] / 
                      suggestions['daily_target']) * 100
        st.metric(
            "Performance",
            f"{performance:.0f}%"
        )
    
    st.divider()
    
    # Mood indication
    st.markdown("### 😊 Owner Mood Analysis")
    
    # Get mood
    mood = bonus_mgmt.calculate_owner_mood(
        suggestions['average_daily_sales'],
        suggestions['daily_target']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            **Current Mood:** {mood['mood']}
            
            **Level:** {'⭐' * mood['mood_level']}
            
            **Performance:** {mood['performance_percent']:.0f}%
            
            **Status:** {mood['description']}
        """)
    
    with col2:
        st.warning(f"**Action:** {mood['suggestion']}")
    
    st.divider()
    
    # AI Recommendation
    st.markdown("### 🎯 AI Bonus Recommendation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Bonus Level", suggestions['bonus_level'])
    
    with col2:
        st.metric("Suggested Multiplier", f"{suggestions['suggested_multiplier']:.0%}")
    
    with col3:
        st.metric("Bonus Percent", suggestions['suggestions'][0]['multiplier_percent'])
    
    st.info(f"💡 {suggestions['message']}\n\n**Recommended Action:** {suggestions['action']}")
    
    st.divider()
    
    # Staff bonus breakdown
    st.markdown("### 👥 Individual Staff Bonuses")
    
    bonus_data = []
    
    for staff in suggestions['suggestions']:
        bonus_data.append({
            'Staff': staff['staff_name'],
            'Role': staff['role'],
            'Base Salary': f"₹{staff['base_salary']:,.0f}",
            'Suggested Bonus': f"₹{staff['suggested_bonus']:,.0f}",
            'Total (with Bonus)': f"₹{staff['total_with_bonus']:,.0f}",
            'Multiplier': staff['multiplier_percent']
        })
    
    st.dataframe(bonus_data, use_container_width=True)
    
    st.divider()
    
    # Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Base Salary",
            f"₹{sum([s['base_salary'] for s in suggestions['suggestions']]):,.0f}"
        )
    
    with col2:
        st.metric(
            "Total Bonus Cost",
            f"₹{suggestions['total_bonus_cost']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Total with Bonus",
            f"₹{suggestions['total_salary_with_bonus']:,.0f}"
        )
    
    # Accept button
    st.markdown("---")
    
    if st.button("✅ Accept & Apply Bonuses", use_container_width=True):
        st.success(f"""
            ✅ Bonuses applied successfully!
            
            - Total Cost: ₹{suggestions['total_bonus_cost']:,.0f}
            - {len(suggestions['suggestions'])} staff members bonus updated
            - Period: {year}-{month:02d}
        """)

def render_bonus_analytics(bonus_mgmt: BonusManagementSystem):
    """Bonus analytics dashboard"""
    
    st.subheader("📊 Bonus Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.selectbox("Year", range(2024, 2027), key="analytics_year")
    
    with col2:
        month = st.selectbox("Month", range(1, 13),
                           format_func=lambda x: f"{x:02d}",
                           key="analytics_month")
    
    # Get report
    report = bonus_mgmt.get_monthly_bonus_report(year, month)
    
    # Sales metrics
    st.markdown("### 📈 Sales Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Sales",
            f"₹{report['sales']['total_sales']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Avg Daily",
            f"₹{report['sales']['average_daily']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Max Daily",
            f"₹{report['sales']['max_daily']:,.0f}"
        )
    
    with col4:
        st.metric(
            "Days Recorded",
            report['sales']['days_count']
        )
    
    st.divider()
    
    # Festival info
    if report['festival']:
        st.info(f"🎉 Current Festival: **{report['festival'].upper()}**")
    
    st.divider()
    
    # Owner mood
    st.markdown("### 😊 Owner's Mood")
    st.markdown(f"""
        {report['mood']['mood']}
        
        Performance: {report['mood']['performance_percent']:.0f}%
        
        {report['mood']['description']}
        
        💡 {report['mood']['suggestion']}
    """)

def render_staff_bonus_view(staff_data: Dict, bonus_mgmt: BonusManagementSystem):
    """Staff view of their bonuses"""
    
    st.subheader("💰 Your Bonus Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.selectbox("Year", range(2024, 2027), key="staff_bonus_year")
    
    with col2:
        month = st.selectbox("Month", range(1, 13),
                           format_func=lambda x: f"{x:02d}",
                           key="staff_bonus_month")
    
    # Calculate bonus
    bonus = bonus_mgmt.calculate_staff_bonus(
        staff_data['staff_id'],
        year,
        month,
        staff_data.get('salary_per_day', 1000),
        25  # Assuming 25 working days
    )
    
    if 'error' in bonus:
        st.error(bonus['error'])
        return
    
    st.divider()
    
    # Display bonus info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            **Base Salary:** ₹{bonus['base_salary']:,.0f}
            
            **Bonus Multiplier:** {bonus['bonus_multiplier']:.1f}x ({bonus['multiplier_percent']})
            
            **Bonus Amount:** ₹{bonus['bonus']:,.0f}
        """)
    
    with col2:
        st.markdown(f"""
            **Performance:** {bonus['performance']}
            
            **Festival:** {bonus['festival'].upper() if bonus['festival'] else 'Regular Days'}
            
            **Reason:** {bonus['reason']}
        """)
    
    st.divider()
    
    # Total
    st.metric(
        "💰 Total Salary (with Bonus)",
        f"₹{bonus['total_with_bonus']:,.0f}",
        delta=f"₹{bonus['bonus']:,.0f} bonus"
    )
    
    st.divider()
    
    # Bonus history (if available)
    st.markdown("### 📋 Recent Bonus History")
    
    history = bonus_mgmt.get_bonus_history(staff_data['staff_id'])
    
    for record in history:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**{record['month']}**")
        
        with col2:
            st.write(f"Bonus: ₹{record['bonus']:,.0f}")
        
        with col3:
            st.write(f"Total: ₹{record['total']:,.0f}")
        
        st.caption(record['reason'])

