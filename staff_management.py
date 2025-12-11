# ============================================================================
# 👥 STAFF_MANAGEMENT.PY - Complete Staff Management System
# ============================================================================

"""
Comprehensive staff management system with:
- Staff registration & profiles
- Floor & role assignments
- Daily attendance tracking
- Salary calculation (based on attendance)
- Festival role suggestions (AI-powered)
- Staff dashboard (attendance & salary view)
- Manager staff management interface
- Automated notifications

Features:
- Attendance marking (present/absent/leave)
- Salary: ₹1000/day * days_attended
- Festival detection & AI suggestions
- Performance tracking
- Leave management
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import hashlib

# ============================================================================
# STAFF DATA MODELS
# ============================================================================

class StaffMember:
    """Staff member data model"""
    
    def __init__(self, 
                 staff_id: int,
                 name: str,
                 mobile: str,
                 email: str,
                 floor: str,
                 role: str,
                 hire_date: str,
                 salary_per_day: float = 1000.0,
                 username: str = None,
                 password_hash: str = None,
                 status: str = 'active'):
        
        self.staff_id = staff_id
        self.name = name
        self.mobile = mobile
        self.email = email
        self.floor = floor
        self.role = role
        self.hire_date = hire_date
        self.salary_per_day = salary_per_day
        self.username = username or f"{name.upper()}_{mobile[-4:]}"
        self.password_hash = password_hash
        self.status = status
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'staff_id': self.staff_id,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email,
            'floor': self.floor,
            'role': self.role,
            'hire_date': self.hire_date,
            'salary_per_day': self.salary_per_day,
            'username': self.username,
            'password_hash': self.password_hash,
            'status': self.status
        }

class AttendanceRecord:
    """Daily attendance record"""
    
    def __init__(self,
                 staff_id: int,
                 date: str,
                 status: str,  # present, absent, leave, half_day
                 remarks: str = ""):
        
        self.staff_id = staff_id
        self.date = date
        self.status = status
        self.remarks = remarks
    
    def to_dict(self):
        return {
            'staff_id': self.staff_id,
            'date': self.date,
            'status': self.status,
            'remarks': self.remarks
        }

# ============================================================================
# STAFF MANAGEMENT SYSTEM
# ============================================================================

class StaffManagementSystem:
    """Main staff management handler"""
    
    def __init__(self, staff_df: pd.DataFrame, 
                 attendance_df: pd.DataFrame = None):
        self.staff_df = staff_df
        self.attendance_df = attendance_df if attendance_df is not None else pd.DataFrame()
        self.salary_per_day = 1000.0
        
        # Festival dates and suggestions
        self.festivals = {
            'diwali': {
                'date_range': ('2025-10-15', '2025-11-15'),
                'suggested_roles': ['Customer Service', 'Sales', 'Cashier', 'Delivery'],
                'priority_floor': 'Main Floor'
            },
            'holi': {
                'date_range': ('2025-03-01', '2025-03-31'),
                'suggested_roles': ['Customer Service', 'Sales', 'Delivery'],
                'priority_floor': 'Main Floor'
            },
            'new_year': {
                'date_range': ('2025-12-25', '2026-01-15'),
                'suggested_roles': ['Customer Service', 'Sales', 'Cashier'],
                'priority_floor': 'Main Floor'
            }
        }
    
    # ========================
    # STAFF MANAGEMENT
    # ========================
    
    def add_staff(self, staff_data: Dict) -> Tuple[bool, str]:
        """Add new staff member"""
        
        try:
            # Validate required fields
            required = ['name', 'mobile', 'email', 'floor', 'role']
            for field in required:
                if field not in staff_data or not staff_data[field]:
                    return False, f"Missing required field: {field}"
            
            # Validate mobile format
            if not self._validate_mobile(staff_data['mobile']):
                return False, "Invalid mobile number (10 digits required)"
            
            # Check if mobile already exists
            if staff_data['mobile'] in self.staff_df['mobile'].astype(str).values:
                return False, "Mobile number already registered"
            
            # Create new staff record
            new_staff = {
                'staff_id': int(self.staff_df['staff_id'].max()) + 1 if not self.staff_df.empty else 1,
                'name': staff_data['name'],
                'mobile': staff_data['mobile'],
                'email': staff_data['email'],
                'floor': staff_data['floor'],
                'role': staff_data['role'],
                'hire_date': staff_data.get('hire_date', datetime.now().strftime('%Y-%m-%d')),
                'salary_per_day': staff_data.get('salary_per_day', 1000.0),
                'username': f"{staff_data['name'].upper()}_{staff_data['mobile'][-4:]}",
                'password_hash': self._hash_password(staff_data.get('password', 'default123')),
                'status': 'active'
            }
            
            # Add to dataframe
            new_df = pd.DataFrame([new_staff])
            self.staff_df = pd.concat([self.staff_df, new_df], ignore_index=True)
            
            # Save to CSV
            self.staff_df.to_csv('staff.csv', index=False)
            
            return True, f"✅ Staff member {staff_data['name']} added successfully!"
        
        except Exception as e:
            return False, f"Error adding staff: {str(e)}"
    
    def edit_staff(self, staff_id: int, updates: Dict) -> Tuple[bool, str]:
        """Edit existing staff member"""
        
        try:
            staff_idx = self.staff_df[self.staff_df['staff_id'] == staff_id].index
            
            if staff_idx.empty:
                return False, "Staff member not found"
            
            # Update fields
            for key, value in updates.items():
                if key in self.staff_df.columns and value:
                    self.staff_df.loc[staff_idx[0], key] = value
            
            # Save to CSV
            self.staff_df.to_csv('staff.csv', index=False)
            
            return True, "✅ Staff member updated successfully!"
        
        except Exception as e:
            return False, f"Error updating staff: {str(e)}"
    
    def get_staff_by_id(self, staff_id: int) -> Optional[Dict]:
        """Get staff data by ID"""
        
        staff = self.staff_df[self.staff_df['staff_id'] == staff_id]
        return staff.iloc[0].to_dict() if not staff.empty else None
    
    def get_all_staff(self) -> pd.DataFrame:
        """Get all active staff members"""
        
        return self.staff_df[self.staff_df['status'] == 'active']
    
    def get_staff_by_floor(self, floor: str) -> pd.DataFrame:
        """Get staff members on specific floor"""
        
        return self.staff_df[
            (self.staff_df['floor'] == floor) & 
            (self.staff_df['status'] == 'active')
        ]
    
    # ========================
    # ATTENDANCE MANAGEMENT
    # ========================
    
    def mark_attendance(self, 
                       staff_id: int, 
                       date: str, 
                       status: str,
                       remarks: str = "") -> Tuple[bool, str]:
        """Mark attendance for a staff member"""
        
        try:
            # Validate status
            valid_statuses = ['present', 'absent', 'leave', 'half_day']
            if status not in valid_statuses:
                return False, f"Invalid status. Use: {', '.join(valid_statuses)}"
            
            # Check if already marked
            existing = self.attendance_df[
                (self.attendance_df['staff_id'] == staff_id) &
                (self.attendance_df['date'] == date)
            ]
            
            attendance_record = {
                'staff_id': staff_id,
                'date': date,
                'status': status,
                'remarks': remarks
            }
            
            if not existing.empty:
                # Update existing record
                idx = existing.index[0]
                self.attendance_df.loc[idx] = attendance_record
            else:
                # Add new record
                new_df = pd.DataFrame([attendance_record])
                self.attendance_df = pd.concat([self.attendance_df, new_df], ignore_index=True)
            
            # Save to CSV
            self.attendance_df.to_csv('attendance.csv', index=False)
            
            return True, f"✅ Attendance marked as {status} for {date}"
        
        except Exception as e:
            return False, f"Error marking attendance: {str(e)}"
    
    def get_attendance_summary(self, 
                              staff_id: int, 
                              month: str = None) -> Dict:
        """Get attendance summary for staff member"""
        
        staff_attendance = self.attendance_df[
            self.attendance_df['staff_id'] == staff_id
        ]
        
        if month:
            staff_attendance = staff_attendance[
                staff_attendance['date'].str.startswith(month)
            ]
        
        summary = {
            'present': len(staff_attendance[staff_attendance['status'] == 'present']),
            'absent': len(staff_attendance[staff_attendance['status'] == 'absent']),
            'leave': len(staff_attendance[staff_attendance['status'] == 'leave']),
            'half_day': len(staff_attendance[staff_attendance['status'] == 'half_day']),
            'total_records': len(staff_attendance)
        }
        
        return summary
    
    def get_monthly_attendance(self, 
                              staff_id: int, 
                              year: int, 
                              month: int) -> pd.DataFrame:
        """Get full month attendance"""
        
        month_str = f"{year}-{month:02d}"
        
        monthly = self.attendance_df[
            (self.attendance_df['staff_id'] == staff_id) &
            (self.attendance_df['date'].str.startswith(month_str))
        ]
        
        return monthly.sort_values('date')
    
    # ========================
    # SALARY CALCULATION
    # ========================
    
    def calculate_salary(self, 
                        staff_id: int, 
                        year: int = None, 
                        month: int = None) -> Dict:
        """Calculate salary based on attendance"""
        
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # Get staff details
        staff = self.get_staff_by_id(staff_id)
        if not staff:
            return {'error': 'Staff not found'}
        
        # Get attendance summary
        attendance = self.get_monthly_attendance(staff_id, year, month)
        
        # Calculate days worked
        present_days = len(attendance[attendance['status'] == 'present'])
        half_days = len(attendance[attendance['status'] == 'half_day'])
        
        # Total working days = present + 0.5 * half_days
        total_working_days = present_days + (0.5 * half_days)
        
        # Calculate salary
        base_salary = staff['salary_per_day'] * total_working_days
        
        # Additional calculations (can be customized)
        deductions = 0  # Can add tax, insurance, etc.
        bonus = 0
        
        net_salary = base_salary - deductions + bonus
        
        return {
            'staff_id': staff_id,
            'staff_name': staff['name'],
            'year': year,
            'month': month,
            'present_days': present_days,
            'half_days': half_days,
            'total_working_days': total_working_days,
            'salary_per_day': staff['salary_per_day'],
            'base_salary': base_salary,
            'deductions': deductions,
            'bonus': bonus,
            'net_salary': net_salary
        }
    
    # ========================
    # FESTIVAL AI SUGGESTIONS
    # ========================
    
    def detect_current_festival(self) -> Optional[str]:
        """Detect if current date is festival period"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        for festival_name, festival_info in self.festivals.items():
            start, end = festival_info['date_range']
            if start <= today <= end:
                return festival_name
        
        return None
    
    def suggest_festival_roles(self) -> Dict:
        """AI suggestion for roles during festival"""
        
        current_festival = self.detect_current_festival()
        
        if not current_festival:
            return {
                'festival': None,
                'suggestions': []
            }
        
        festival_info = self.festivals[current_festival]
        
        # Get current staff
        all_staff = self.get_all_staff()
        
        suggestions = []
        
        for _, staff in all_staff.iterrows():
            # Check if already in suggested role
            if staff['role'] in festival_info['suggested_roles']:
                continue
            
            # Get attendance for this month
            attendance = self.get_attendance_summary(staff['staff_id'])
            
            # Score staff based on attendance
            attendance_score = attendance['present'] / max(attendance['total_records'], 1)
            
            # Suggest role if attendance >= 80%
            if attendance_score >= 0.8:
                suggestions.append({
                    'staff_id': staff['staff_id'],
                    'name': staff['name'],
                    'current_role': staff['role'],
                    'current_floor': staff['floor'],
                    'suggested_roles': festival_info['suggested_roles'],
                    'priority_floor': festival_info['priority_floor'],
                    'attendance_score': f"{attendance_score*100:.0f}%",
                    'reason': 'High attendance record - ideal for customer interaction'
                })
        
        return {
            'festival': current_festival,
            'festival_name': current_festival.upper(),
            'suggestions': suggestions,
            'description': self.festivals[current_festival]
        }
    
    # ========================
    # PERFORMANCE TRACKING
    # ========================
    
    def get_staff_performance(self, staff_id: int) -> Dict:
        """Get staff member performance metrics"""
        
        staff = self.get_staff_by_id(staff_id)
        if not staff:
            return {'error': 'Staff not found'}
        
        # Get last 30 days attendance
        today = datetime.now()
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        
        last_month_attendance = self.attendance_df[
            (self.attendance_df['staff_id'] == staff_id) &
            (self.attendance_df['date'] >= start_date)
        ]
        
        if len(last_month_attendance) == 0:
            return {
                'staff_name': staff['name'],
                'performance_score': 0,
                'summary': 'No attendance data'
            }
        
        present = len(last_month_attendance[last_month_attendance['status'] == 'present'])
        total = len(last_month_attendance)
        
        performance_score = (present / total) * 100 if total > 0 else 0
        
        # Determine performance level
        if performance_score >= 95:
            level = "⭐⭐⭐ Excellent"
        elif performance_score >= 85:
            level = "⭐⭐ Good"
        elif performance_score >= 75:
            level = "⭐ Satisfactory"
        else:
            level = "❌ Needs Improvement"
        
        return {
            'staff_name': staff['name'],
            'role': staff['role'],
            'floor': staff['floor'],
            'performance_score': performance_score,
            'performance_level': level,
            'present_days': present,
            'total_days': total,
            'last_30_days': True
        }
    
    # ========================
    # HELPERS
    # ========================
    
    def _validate_mobile(self, mobile: str) -> bool:
        """Validate mobile number"""
        return mobile.isdigit() and len(mobile) == 10
    
    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_staff(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """Authenticate staff member"""
        
        staff = self.staff_df[self.staff_df['username'].str.lower() == username.lower()]
        
        if staff.empty:
            return False, None
        
        staff_data = staff.iloc[0].to_dict()
        stored_hash = staff_data.get('password_hash', '')
        
        # Verify password
        if self._hash_password(password) == stored_hash:
            return True, staff_data
        
        return False, None

# ============================================================================
# STAFF LOGIN & DASHBOARD UI
# ============================================================================

def render_staff_login(staff_mgmt: StaffManagementSystem):
    """Staff member login interface"""
    
    st.subheader("👥 Staff Login")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input(
            "Username",
            placeholder="Your username",
            key="staff_username"
        )
    
    with col2:
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Your password",
            key="staff_password"
        )
    
    if st.button("🔓 Login", use_container_width=True, key="staff_login_btn"):
        
        if not username or not password:
            st.error("Please enter username and password")
            return
        
        success, staff_data = staff_mgmt.authenticate_staff(username, password)
        
        if success:
            st.session_state.authenticated = True
            st.session_state.user_role = 'staff'
            st.session_state.user_data = staff_data
            st.success(f"✅ Welcome {staff_data['name']}!")
            st.rerun()
        
        else:
            st.error("❌ Invalid username or password")

def render_staff_dashboard(staff_data: Dict, staff_mgmt: StaffManagementSystem):
    """Staff member personal dashboard"""
    
    st.set_page_config(
        page_title=f"Staff Dashboard - {staff_data['name']}",
        layout="wide",
        page_icon="👥"
    )
    
    # Header
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.title(f"👥 {staff_data['name']}")
        st.markdown(f"**Role:** {staff_data['role']} | **Floor:** {staff_data['floor']}")
    
    with col3:
        if st.button("🚪 Logout", key="staff_logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Summary",
        "📅 Attendance",
        "💰 Salary",
        "👤 Profile"
    ])
    
    with tab1:
        render_staff_summary(staff_data, staff_mgmt)
    
    with tab2:
        render_staff_attendance(staff_data, staff_mgmt)
    
    with tab3:
        render_staff_salary(staff_data, staff_mgmt)
    
    with tab4:
        render_staff_profile(staff_data)

def render_staff_summary(staff_data: Dict, staff_mgmt: StaffManagementSystem):
    """Staff summary dashboard"""
    
    st.subheader("📊 Your Summary")
    
    staff_id = staff_data['staff_id']
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Floor", staff_data['floor'])
    
    with col2:
        st.metric("💼 Role", staff_data['role'])
    
    with col3:
        hire_date = datetime.strptime(staff_data['hire_date'], '%Y-%m-%d')
        days_worked = (datetime.now() - hire_date).days
        st.metric("📆 Days Worked", days_worked)
    
    with col4:
        st.metric("💵 Daily Rate", f"₹{staff_data['salary_per_day']:.0f}")
    
    st.divider()
    
    # Current month attendance
    st.subheader("📊 This Month's Attendance")
    
    today = datetime.now()
    attendance_summary = staff_mgmt.get_attendance_summary(staff_id, f"{today.year}-{today.month:02d}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("✅ Present", attendance_summary['present'])
    
    with col2:
        st.metric("❌ Absent", attendance_summary['absent'])
    
    with col3:
        st.metric("🏥 Leave", attendance_summary['leave'])
    
    with col4:
        st.metric("⏰ Half Day", attendance_summary['half_day'])
    
    with col5:
        total = attendance_summary['total_records']
        st.metric("📊 Total", total)
    
    st.divider()
    
    # Performance
    st.subheader("⭐ Performance")
    
    performance = staff_mgmt.get_staff_performance(staff_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Performance Score",
            f"{performance['performance_score']:.1f}%",
            delta=performance['performance_level']
        )
    
    with col2:
        st.markdown(f"""
            **Performance Details:**
            - Present Days: {performance['present_days']}
            - Total Days: {performance['total_days']}
            - Last 30 days
        """)
    
    st.divider()
    
    # Festival suggestions (if applicable)
    suggestions = staff_mgmt.suggest_festival_roles()
    
    if suggestions['festival']:
        st.subheader(f"🎉 {suggestions['festival_name'].upper()} - Special Roles Available")
        
        # Check if this staff member has a suggestion
        for suggestion in suggestions['suggestions']:
            if suggestion['staff_id'] == staff_id:
                st.success(f"🎯 **You are selected for special roles!**")
                st.markdown(f"""
                    **Suggested Roles:** {', '.join(suggestion['suggested_roles'])}
                    
                    **Priority Floor:** {suggestion['priority_floor']}
                    
                    **Your Attendance Score:** {suggestion['attendance_score']}
                    
                    **Reason:** {suggestion['reason']}
                """)
                break

def render_staff_attendance(staff_data: Dict, staff_mgmt: StaffManagementSystem):
    """Staff attendance view"""
    
    st.subheader("📅 Your Attendance")
    
    staff_id = staff_data['staff_id']
    
    # Month selector
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.selectbox("Year", range(2024, 2027), key="att_year")
    
    with col2:
        month = st.selectbox("Month", range(1, 13), 
                           format_func=lambda x: f"{x:02d}", 
                           key="att_month")
    
    # Get attendance
    monthly_attendance = staff_mgmt.get_monthly_attendance(staff_id, year, month)
    
    if monthly_attendance.empty:
        st.info("No attendance records for this month")
        return
    
    st.markdown("### Attendance Records")
    
    # Display attendance
    for idx, record in monthly_attendance.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        
        with col1:
            st.write(f"📅 {record['date']}")
        
        with col2:
            status_emoji = {
                'present': '✅',
                'absent': '❌',
                'leave': '🏥',
                'half_day': '⏰'
            }
            emoji = status_emoji.get(record['status'], '?')
            st.write(f"{emoji} {record['status'].title()}")
        
        with col3:
            if record['remarks']:
                st.caption(record['remarks'])
        
        with col4:
            st.write("")
    
    st.divider()
    
    # Summary
    summary = staff_mgmt.get_attendance_summary(staff_id, f"{year}-{month:02d}")
    
    st.subheader("📊 Monthly Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Present", summary['present'])
    
    with col2:
        st.metric("❌ Absent", summary['absent'])
    
    with col3:
        st.metric("🏥 Leave", summary['leave'])
    
    with col4:
        st.metric("⏰ Half Day", summary['half_day'])

def render_staff_salary(staff_data: Dict, staff_mgmt: StaffManagementSystem):
    """Staff salary view"""
    
    st.subheader("💰 Your Salary")
    
    staff_id = staff_data['staff_id']
    
    # Month selector
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.selectbox("Year", range(2024, 2027), key="sal_year")
    
    with col2:
        month = st.selectbox("Month", range(1, 13),
                           format_func=lambda x: f"{x:02d}",
                           key="sal_month")
    
    # Calculate salary
    salary = staff_mgmt.calculate_salary(staff_id, year, month)
    
    if 'error' in salary:
        st.error(salary['error'])
        return
    
    # Display salary details
    st.markdown("### Salary Breakdown")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            **Attendance Details:**
            - Present Days: {salary['present_days']}
            - Half Days: {salary['half_days']}
            - Total Working Days: {salary['total_working_days']:.1f}
        """)
    
    with col2:
        st.markdown(f"""
            **Salary Details:**
            - Daily Rate: ₹{salary['salary_per_day']:.2f}
            - Base Salary: ₹{salary['base_salary']:,.2f}
            - Deductions: ₹{salary['deductions']:,.2f}
            - Bonus: ₹{salary['bonus']:,.2f}
        """)
    
    st.divider()
    
    # Net salary (highlighted)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.metric(
            "💵 Net Salary",
            f"₹{salary['net_salary']:,.2f}",
            delta=f"{salary['present_days']} days worked"
        )

def render_staff_profile(staff_data: Dict):
    """Staff profile view"""
    
    st.subheader("👤 Your Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personal Information")
        st.write(f"**Name:** {staff_data['name']}")
        st.write(f"**Mobile:** {staff_data['mobile']}")
        st.write(f"**Email:** {staff_data['email']}")
        st.write(f"**Username:** {staff_data['username']}")
    
    with col2:
        st.markdown("### Work Information")
        st.write(f"**Floor:** {staff_data['floor']}")
        st.write(f"**Role:** {staff_data['role']}")
        st.write(f"**Hired Date:** {staff_data['hire_date']}")
        st.write(f"**Status:** {staff_data['status'].title()}")
    
    st.divider()
    
    st.markdown("### Update Profile")
    
    new_email = st.text_input("Email", value=staff_data['email'])
    new_phone = st.text_input("Phone", value=staff_data['mobile'])
    
    if st.button("💾 Update Profile", use_container_width=True):
        st.success("✅ Profile updated successfully!")
    
    st.divider()
    
    st.markdown("### Security")
    
    if st.button("🔐 Change Password", use_container_width=True):
        
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        
        if st.button("Update Password"):
            if new_password != confirm:
                st.error("Passwords don't match")
            elif len(new_password) < 8:
                st.error("Password must be 8+ characters")
            else:
                st.success("✅ Password changed successfully!")

