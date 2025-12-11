import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

class StaffManagementSystem:
    def __init__(self, staff_df, attendance_df):
        self.staff_df = staff_df
        self.attendance_df = attendance_df
    
    def add_staff(self, staff_data):
        """Add a new staff member"""
        return True, "Staff member added successfully"
    
    def mark_attendance(self, staff_id, date, status, remarks):
        """Mark attendance for staff"""
        return True, f"Attendance marked as {status}"
    
    def get_monthly_attendance(self, staff_id, year, month):
        """Get monthly attendance for a staff member"""
        filtered = self.attendance_df[
            (self.attendance_df['staff_id'] == staff_id)
        ].copy()
        return filtered.head(30)
    
    def get_attendance_summary(self, staff_id, month):
        """Get attendance summary for the month"""
        filtered = self.attendance_df[self.attendance_df['staff_id'] == staff_id]
        
        summary = {
            'present': len(filtered[filtered['status'] == 'present']),
            'absent': len(filtered[filtered['status'] == 'absent']),
            'leave': len(filtered[filtered['status'] == 'leave']),
            'half_day': len(filtered[filtered['status'] == 'half_day'])
        }
        return summary
    
    def calculate_salary(self, staff_id, year, month):
        """Calculate salary for staff member"""
        staff = self.staff_df[self.staff_df['staff_id'] == staff_id]
        
        if staff.empty:
            return {'error': 'Staff not found'}
        
        salary_per_day = staff.iloc[0]['salary_per_day']
        
        # Get attendance for the month
        summary = self.get_attendance_summary(staff_id, f"{year}-{month:02d}")
        
        present_days = summary['present']
        half_days = summary['half_day']
        total_working_days = present_days + (half_days * 0.5)
        
        base_salary = total_working_days * salary_per_day
        deductions = base_salary * 0.08  # 8% deductions
        bonus = base_salary * 0.05  # 5% bonus
        net_salary = base_salary - deductions + bonus
        
        return {
            'present_days': present_days,
            'half_days': half_days,
            'total_working_days': total_working_days,
            'salary_per_day': salary_per_day,
            'base_salary': base_salary,
            'deductions': deductions,
            'bonus': bonus,
            'net_salary': net_salary
        }
    
    def suggest_festival_roles(self):
        """Suggest festival roles based on attendance"""
        # Check if it's festival season
        month = datetime.now().month
        
        festival_map = {
            10: {'festival': 'diwali', 'roles': ['Sales Lead', 'VIP Manager', 'Premium Counter']},
            1: {'festival': 'new_year', 'roles': ['Event Manager', 'Counter Manager', 'Sales Lead']},
            3: {'festival': 'holi', 'roles': ['Promotion Manager', 'Sales Associate', 'Customer Care']}
        }
        
        current_festival = festival_map.get(month, {'festival': None, 'roles': []})
        
        suggestions = []
        for idx, staff in self.staff_df.head(5).iterrows():
            suggestions.append({
                'name': staff['name'],
                'current_role': staff['role'],
                'suggested_roles': current_festival.get('roles', []),
                'attendance_score': 85,
                'priority_floor': staff['floor']
            })
        
        return {
            'festival': current_festival.get('festival'),
            'suggestions': suggestions
        }

def render_staff_login():
    """Render staff login page"""
    st.title("🔐 Staff Login")
    st.info("Staff login page placeholder")

def render_staff_dashboard(user_data, staff_mgmt):
    """Render staff dashboard"""
    st.set_page_config(page_title="Staff Dashboard", layout="wide", page_icon="👨‍💼")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.title("👨‍💼 Staff Dashboard")
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    # Staff info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Name", user_data.get('name', 'Staff'))
    
    with col2:
        st.metric("Role", "Sales")
    
    with col3:
        st.metric("Floor", "Main Floor")
    
    with col4:
        st.metric("Attendance", "95%")
    
    st.divider()
    
    # Main navigation
    staff_tabs = st.tabs([
        "📊 Dashboard",
        "📝 Attendance",
        "💰 Salary",
        "🎁 Bonuses",
        "📈 Performance"
    ])
    
    with staff_tabs[0]:
        st.subheader("📊 Your Dashboard")
        st.info("Staff dashboard summary")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Status:** Active ✅")
            st.write("**Daily Rate:** ₹1,000")
        
        with col2:
            st.write("**Hire Date:** 2025-01-01")
            st.write("**Performance:** Excellent 🌟")
    
    with staff_tabs[1]:
        st.subheader("📝 My Attendance")
        
        # Mock attendance data
        attendance_data = {
            'Date': pd.date_range(start='2025-12-01', periods=10),
            'Status': ['present', 'present', 'absent', 'present', 'present', 
                      'half_day', 'present', 'present', 'leave', 'present'],
            'Remarks': ['', '', 'Sick', '', '', 'Late', '', '', 'Festival', '']
        }
        st.dataframe(pd.DataFrame(attendance_data), use_container_width=True)
    
    with staff_tabs[2]:
        st.subheader("💰 Salary Details")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Base Salary:** ₹25,000")
            st.write("**Deductions:** ₹2,000")
        
        with col2:
            st.write("**Bonus:** ₹1,000")
            st.write("**Net Salary:** ₹24,000")
    
    with staff_tabs[3]:
        st.subheader("🎁 My Bonuses")
        
        bonus_data = {
            'Month': ['October', 'November', 'December'],
            'Sales Target': ['₹100,000', '₹120,000', '₹150,000'],
            'Bonus': ['₹2,000', '₹3,000', '₹3,500']
        }
        st.dataframe(bonus_data, use_container_width=True)
    
    with staff_tabs[4]:
        st.subheader("📈 Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sales This Month", "₹450,000", "+15%")
        with col2:
            st.metric("Customers Served", "125", "+10%")
        with col3:
            st.metric("Rating", "4.8/5", "+0.2")
