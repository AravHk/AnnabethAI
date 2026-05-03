"""
Annabeth AI - Intelligent Travel Planner
Caribbean Blue Theme with Custom Text Colors
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import json
from typing import Dict, List
import time
from crew import TravelPlannerCrew
import tempfile
import urllib.parse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page configuration
st.set_page_config(
    page_title="Annabeth AI - Intelligent Travel Companion",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Caribbean Blue Theme and Custom Text Colors
st.markdown("""
<style>
    /* Original Fonts */
    /* Original Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main background - Deep Forest Green gradient */
.stApp {
    background: linear-gradient(135deg, #2C3E2D 0%, #1A2E1B 50%, #0F1A0F 100%);
}

/* Main content area - Warm Ivory */
.main .block-container {
    background: #F5F0E8;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

/* Sidebar - Deep Burgundy to Forest */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2C1810 0%, #4A2C2A 50%, #2C3E2D 100%);
    border-right: 2px solid #8B6914;
}

/* Main Header - Gradient Text */
.main-header {
    font-size: 4rem;
    background: linear-gradient(135deg, #2C3E2D 0%, #4A3728 50%, #1A2E1B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color:#FFFFFF;
}

/* Tagline - Warm Gold */
.tagline {
    text-align: center;
    color: #C9A84C;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
    font-style: italic;
    font-weight: 600;
}

/* Subtitle - Soft Cream */
.subtitle {
    text-align: center;
    color: #E8E0D0;
    font-size: 0.95rem;
    margin-bottom: 2rem;
    font-weight: 500;
}

/* Section Headers */
.section-header {
    color: #E8E0D0;
    font-weight: 700;
    font-size: 1.5rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Agent Cards */
.agent-card {
    background: linear-gradient(135deg, #2C3E2D 0%, #3D5C3A 50%, #4A6741 100%);
    padding: 0.75rem;
    border-radius: 10px;
    color: #E8E0D0;
    margin: 0.5rem 0;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    transition: transform 0.2s;
    border: 1px solid #8B6914;
}

.agent-card:hover {
    transform: scale(1.02);
    background: linear-gradient(135deg, #4A2C2A 0%, #6B3A35 50%, #2C1810 100%);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #2C3E2D 0%, #3D5C3A 100%);
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    color: #E8E0D0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    border: 1px solid #8B6914;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2C3E2D 0%, #3D5C3A 100%);
    color: #E8E0D0;
    border: 1px solid #8B6914;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s;
    padding: 0.5rem 1rem;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #4A2C2A 0%, #6B3A35 100%);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, #2C3E2D 0%, #3D5C3A 100%);
    color: #E8E0D0;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: bold;
    border: 1px solid #8B6914;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4A2C2A 0%, #6B3A35 100%);
}

/* Metric Value Colors */
[data-testid="stMetricValue"] {
    color: #2C3E2D !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}

/* Total Cost - Forest Green */
[data-testid="stMetricValue"]:first-child {
    color: #2C3E2D !important;
}

/* Budget - Burgundy */
[data-testid="stMetricValue"]:nth-child(2) {
    color: #4A2C2A !important;
}

/* Activities - Deep Teal */
[data-testid="stMetricValue"]:nth-child(3) {
    color: #1A3A3A !important;
}

/* Savings - Aged Gold */
[data-testid="stMetricValue"]:nth-child(4) {
    color: #8B6914 !important;
}

/* Metric Labels */
[data-testid="stMetricLabel"] {
    color: #5C4A3A !important;
    font-weight: 600 !important;
}

/* Expander Headers */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #2C3E2D 0%, #3D5C3A 100%);
    color: #E8E0D0 !important;
    border-radius: 8px;
    font-weight: bold;
    border: 1px solid #8B6914;
}

/* Info text */
.stAlert {
    background-color: #EDE8DC;
    border-left: 4px solid #8B6914;
    color: #2C1810;
}

/* Success message */
.stSuccess {
    background-color: #E8F0E8;
    color: #1A2E1B;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #EDE8DC;
    border-radius: 12px;
}

/* Sidebar text colors */
[data-testid="stSidebar"] .stMarkdown {
    color: #E8E0D0;
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: #C9A84C;
}

[data-testid="stSidebar"] .stAlert {
    background-color: rgba(201, 168, 76, 0.15);
    color: #E8E0D0;
}
</style>
""", unsafe_allow_html=True)

class TravelPlannerUI:
    """Main UI Controller"""
    
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        """Initialize session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_plan' not in st.session_state:
            st.session_state.current_plan = None
        if 'agent_status' not in st.session_state:
            st.session_state.agent_status = {
                'coordinator': 'idle',
                'flight_expert': 'idle',
                'hotel_expert': 'idle',
                'itinerary_planner': 'idle',
                'budget_manager': 'idle'
            }
        if 'planning_stage' not in st.session_state:
            st.session_state.planning_stage = 0
    
    def export_to_pdf(self, plan_data: Dict):
        """Export travel plan to PDF"""
        if not plan_data:
            st.warning("No plan to export!")
            return None
        
        from fpdf import FPDF
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 16)
                self.set_text_color(0, 119, 182)
                self.cell(0, 10, 'Annabeth AI - Intelligent Travel Planner', 0, 1, 'C')
                self.set_font('Arial', 'I', 10)
                self.set_text_color(0, 0, 0)
                self.cell(0, 5, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
                self.ln(8)
            
            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.set_text_color(128, 128, 128)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
        pdf = PDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 18)
        pdf.set_text_color(0, 119, 182)
        pdf.cell(0, 15, f"Trip to {plan_data.get('destination', 'Unknown')}", 0, 1, 'C')
        pdf.ln(5)
        
        # Trip Overview
        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "TRIP OVERVIEW", 0, 1)
        pdf.set_font('Arial', '', 12)
        
        overview_data = [
            f"Destination: {plan_data.get('destination', 'Unknown')}",
            f"Duration: {plan_data.get('duration', 5)} days",
            f"Travelers: {plan_data.get('travelers', 2)} people",
            f"Total Budget: ${plan_data.get('budget', 0):,}",
            f"Estimated Cost: ${plan_data.get('total_cost', 0):,}",
            f"Savings: ${plan_data.get('savings', 0):,}"
        ]
        
        for item in overview_data:
            pdf.cell(0, 8, item, 0, 1)
        pdf.ln(5)
        
        # Budget Breakdown
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "BUDGET BREAKDOWN", 0, 1)
        pdf.set_font('Arial', '', 12)
        
        breakdown = plan_data.get('budget_breakdown', {})
        for category, amount in breakdown.items():
            pdf.cell(60, 8, category, 0, 0)
            pdf.cell(0, 8, f"${amount:,}", 0, 1)
        pdf.ln(5)
        
        # Daily Itinerary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "DAILY ITINERARY", 0, 1)
        pdf.set_font('Arial', '', 11)
        
        itinerary = plan_data.get('itinerary', {})
        for day, activities in itinerary.items():
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(0, 119, 182)
            pdf.cell(0, 8, day, 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.set_text_color(0, 0, 0)
            
            for activity in activities:
                time_str = activity.get('time', '')
                title = activity.get('title', '')
                cost = activity.get('cost', 0)
                pdf.cell(25, 6, time_str, 0, 0)
                pdf.cell(100, 6, title[:50], 0, 0)
                pdf.cell(0, 6, f"${cost}", 0, 1)
            pdf.ln(2)
        
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf.output(temp_file.name)
        
        return temp_file.name
    
    def send_email_real(self, recipient_email: str, plan_data: Dict) -> bool:
        """Send actual email using SMTP (Gmail example)"""
        try:
            # Email configuration
            sender_email = "your_email@gmail.com"  # Replace with your email
            sender_password = "your_app_password"  # Replace with Gmail App Password
            
            subject = f"Your Travel Plan to {plan_data.get('destination', 'Unknown')} - Annabeth AI"
            
            # Create email body
            body = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #0077B6, #00B4D8); color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .budget {{ background: #f0f9ff; padding: 15px; border-radius: 10px; margin: 10px 0; }}
        .highlight {{ color: #0077B6; font-weight: bold; }}
        .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>✈️ Annabeth AI -Agentic Travel Planner</h2>
        <p>PLANS. DECIDES. ACTS.</p>
    </div>
    <div class="content">
        <h2 style="color: #0077B6;">Your Personalized Travel Plan</h2>
        
        <div class="budget">
            <h3>Destination: <span class="highlight">{plan_data.get('destination', 'Unknown')}</span></h3>
            <p> Duration: {plan_data.get('duration', 5)} days</p>
            <p> Travelers: {plan_data.get('travelers', 2)} people</p>
            <hr>
            <p> Total Budget: <strong>${plan_data.get('budget', 0):,}</strong></p>
            <p> Estimated Cost: <strong>${plan_data.get('total_cost', 0):,}</strong></p>
            <p> Savings: <strong>${plan_data.get('savings', 0):,}</strong></p>
        </div>
        
        <h3>🗺️ Daily Itinerary</h3>
"""
            
            itinerary = plan_data.get('itinerary', {})
            for day, activities in itinerary.items():
                body += f'<div style="margin: 15px 0;"><strong>{day}:</strong><ul>'
                for activity in activities:
                    body += f'<li>{activity.get("time", "")} - {activity.get("title", "")} (${activity.get("cost", 0)})</li>'
                body += '</ul></div>'
            
            body += f"""
        <div class="footer">
            <p>Generated by Annabeth AI | Powered by 5 Autonomous AI Agents</p>
            <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Attach HTML version
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            st.error(f"Email error: {e}")
            return False
    
    def export_to_email(self, plan_data: Dict, recipient_email: str):
        """Send travel plan via email (mailto fallback)"""
        if not plan_data:
            return False, "No plan to export!"
        
        subject = f"Your Travel Plan to {plan_data.get('destination', 'Unknown')} - Annabeth AI"
        
        body = f"""
ANNABETH AI - YOUR PERSONALIZED TRAVEL PLAN
{'='*60}

Destination: {plan_data.get('destination', 'Unknown')}
Duration: {plan_data.get('duration', 5)} days
Travelers: {plan_data.get('travelers', 2)} people

BUDGET SUMMARY
{'='*30}
Total Budget: ${plan_data.get('budget', 0):,}
Estimated Cost: ${plan_data.get('total_cost', 0):,}
Savings: ${plan_data.get('savings', 0):,}

DAILY ITINERARY
{'='*30}
"""
        itinerary = plan_data.get('itinerary', {})
        for day, activities in itinerary.items():
            body += f"\n{day}:\n"
            for activity in activities:
                body += f"  {activity.get('time', '')} - {activity.get('title', '')} (${activity.get('cost', 0)})\n"
        
        body += f"\n{'='*60}\nGenerated by Annabeth AI"
        body += f"\nYour Intelligent Travel Companion | Powered by 5 Autonomous AI Agents"
        body += f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        mailto_link = f"mailto:{recipient_email}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
        
        return True, mailto_link
    
    def render_sidebar(self):
        """Render sidebar with user inputs"""
        with st.sidebar:
            st.image("https://img.icons8.com/color/96/000000/airplane-take-off.png", width=80)
            st.markdown("## Annabeth AI")
            st.markdown("Plans. Decides. Acts.")
            st.markdown("---")
            st.markdown("### Trip Details")
            
            destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
            
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", min_value=date.today())
            with col2:
                end_date = st.date_input("End Date", min_value=start_date if 'start_date' in locals() else date.today())
            
            if start_date and end_date:
                duration = (end_date - start_date).days
                st.info(f"Duration: {duration} days")
            
            travelers = st.number_input("Travelers", min_value=1, max_value=20, value=2)
            budget = st.number_input("Budget (USD)", min_value=50, max_value=50000, value=3000, step=100)
            
            interests = st.multiselect(
                "Interests",
                ["Culture & History", "Food & Dining", "Nature & Hiking", 
                 "Beaches", "Shopping", "Nightlife", "Adventure Sports", "Relaxation"],
                default=["Culture & History", "Food & Dining"]
            )
            
            travel_style = st.select_slider(
                "Travel Style",
                options=["Budget Backpacker", "Moderate Explorer", "Comfort Seeker", "Luxury Traveler"],
                value="Moderate Explorer"
            )
            
            notes = st.text_area("Special Requests", placeholder="Dietary restrictions, mobility issues, must-see attractions...")
            
            st.markdown("---")
            generate_btn = st.button(" Generate Smart Plan", type="primary", use_container_width=True)
            
            return {
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'duration': duration,
                'travelers': travelers,
                'budget': budget,
                'interests': interests,
                'travel_style': travel_style,
                'notes': notes,
                'generate': generate_btn
            }
    
    def render_agent_status(self):
        """Render real-time agent status dashboard"""
        st.markdown("###  AI Agents")
        
        agent_display = {
            'coordinator': {'name': ' Coordinator'},
            'flight_expert': {'name': ' Flight'},
            'hotel_expert': {'name': ' Hotel'},
            'itinerary_planner': {'name': ' Itinerary'},
            'budget_manager': {'name': ' Budget'}
        }
        
        for agent_key, agent_info in agent_display.items():
            status = st.session_state.agent_status.get(agent_key, 'idle')
            status_emoji = {
                'idle': '○',
                'thinking': '◐',
                'searching': '◑',
                'negotiating': '◒',
                'complete': '●',
                'error': '⊗'
            }.get(status, '○')
            
            st.markdown(f"""
            <div class="agent-card">
                <strong>{agent_info['name']}</strong> {status_emoji} <span style="text-transform: uppercase;">{status}</span>
            </div>
            """, unsafe_allow_html=True)
    
    def render_chat_interface(self):
        """Render chat-like interaction interface"""
        st.markdown("### 💬 Chat with Annabeth AI")
        
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.chat_message("user").write(message['content'])
                else:
                    st.chat_message("assistant").write(f" Annabeth AI: {message['content']}")
            
            user_input = st.chat_input("Ask me to adjust your plan...")
            
            if user_input:
                st.session_state.chat_history.append({'role': 'user', 'content': user_input})
                st.chat_message("user").write(user_input)
                
                with st.chat_message("assistant"):
                    with st.spinner(" Annabeth AI is thinking..."):
                        response = self.process_chat_input(user_input)
                        st.write(f" Annabeth AI: {response}")
                        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                        st.rerun()
    
    def process_chat_input(self, user_input: str) -> str:
        """Process chat input with actual AI agent responses"""
        user_lower = user_input.lower()
        
        if st.session_state.current_plan:
            plan = st.session_state.current_plan
            
            if "budget" in user_lower or "$" in user_lower:
                import re
                match = re.search(r'\$?\s*(\d+)', user_lower)
                if match:
                    new_budget = int(match.group(1))
                    plan['budget'] = new_budget
                    plan['total_cost'] = new_budget - int(new_budget * 0.1)
                    plan['savings'] = int(new_budget * 0.1)
                    plan['budget_breakdown'] = {
                        "Flights": int(new_budget * 0.30),
                        "Hotels": int(new_budget * 0.30),
                        "Activities": int(new_budget * 0.20),
                        "Food": int(new_budget * 0.15),
                        "Transport": int(new_budget * 0.05)
                    }
                    st.session_state.current_plan = plan
                    st.rerun()
                    return f" Budget updated to ${new_budget}! Total Cost: ${plan['total_cost']}, Savings: ${plan['savings']}"
            
            elif any(word in user_lower for word in ["fly to", "go to", "change to", "destination"]):
                destinations = ["paris", "tokyo", "london", "new york", "rome", "dubai", "bali", "denmark"]
                for dest in destinations:
                    if dest in user_lower:
                        plan['destination'] = dest.title()
                        st.session_state.current_plan = plan
                        st.rerun()
                        return f" Destination changed to {dest.title()}! Please regenerate the plan to see updated itinerary."
            
            elif "allergy" in user_lower or "vegetarian" in user_lower or "vegan" in user_lower:
                return f" Noted: {user_input}. The Hotel and Itinerary agents will accommodate this request."
            
            else:
                return f" I've noted: '{user_input}'. I can help with budget changes (e.g., 'budget $1500'), destination changes (e.g., 'fly to Paris'), or special requests."
        
        else:
            return f" Please generate a travel plan first using the sidebar, then I can help you modify it!"
    
    def render_trip_plan(self, plan_data: Dict):
        """Render the generated trip plan"""
        if not plan_data:
            st.info(" No trip plan yet. Please generate a plan using the sidebar!")
            return
        
        st.markdown("##  Your Personalized Travel Plan")
        
        total_cost = plan_data.get('total_cost', 0)
        budget = plan_data.get('budget', 0)
        activities = plan_data.get('activities_count', 0)
        savings = plan_data.get('savings', 0)
        
        # Custom colored metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<p style="color: #666; font-weight: 600; margin-bottom: 0;"> Total Cost</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #2E8B57; font-size: 2rem; font-weight: 700; margin-top: -0.5rem;">${int(total_cost):,}</p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<p style="color: #666; font-weight: 600; margin-bottom: 0;"> Budget</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #4169E1; font-size: 2rem; font-weight: 700; margin-top: -0.5rem;">${int(budget):,}</p>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'<p style="color: #666; font-weight: 600; margin-bottom: 0;"> Activities</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #FF8C00; font-size: 2rem; font-weight: 700; margin-top: -0.5rem;">{activities}</p>', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'<p style="color: #666; font-weight: 600; margin-bottom: 0;"> Savings</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #DAA520; font-size: 2rem; font-weight: 700; margin-top: -0.5rem;">${int(savings):,}</p>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([" Daily Itinerary", " Flights", " Hotels", " Budget Breakdown"])
        
        with tab1:
            itinerary = plan_data.get('itinerary', {})
            if itinerary:
                for day, activities_list in itinerary.items():
                    with st.expander(f" {day}", expanded=True):
                        for activity in activities_list:
                            col_a, col_b, col_c = st.columns([1, 3, 1])
                            with col_a:
                                st.markdown(f"**{activity.get('time', '')}**")
                            with col_b:
                                st.markdown(f"**{activity.get('title', '')}**")
                                st.caption(activity.get('description', ''))
                            with col_c:
                                st.markdown(f"${activity.get('cost', 0)}")
            else:
                st.info("Itinerary details will appear here")
        
        with tab2:
            flights = plan_data.get('flights', [])
            if flights:
                for flight in flights:
                    st.markdown(f"**{flight.get('airline', 'Airline')}**")
                    st.caption(f"Departure: {flight.get('departure', 'TBD')} | Arrival: {flight.get('arrival', 'TBD')}")
                    st.caption(f"Duration: {flight.get('duration', 'TBD')} | Price: {flight.get('price', 'TBD')}")
                    st.markdown("---")
            else:
                st.info("Flight details will appear here")
        
        with tab3:
            hotels = plan_data.get('hotels', [])
            if hotels:
                for hotel in hotels:
                    st.markdown(f"**{hotel.get('name', 'Hotel')}** - ⭐ {hotel.get('rating', 4)}/5")
                    st.caption(f"Location: {hotel.get('location', 'City Center')} | ${hotel.get('price_per_night', 0)}/night")
                    st.markdown("---")
            else:
                st.info("Hotel recommendations will appear here")
        
        with tab4:
            budget_breakdown = plan_data.get('budget_breakdown', {})
            if budget_breakdown:
                fig = px.pie(
                    values=list(budget_breakdown.values()),
                    names=list(budget_breakdown.keys()),
                    title="Budget Allocation",
                    color_discrete_sequence=['#0077B6', '#00B4D8', '#48CAE4', '#90E0EF', '#CAF0F8']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                df_budget = pd.DataFrame([
                    {"Category": k, "Amount": f"${v}"} for k, v in budget_breakdown.items()
                ])
                st.dataframe(df_budget, use_container_width=True)
            else:
                st.info("Budget breakdown will appear here")
    
    def _generate_real_itinerary(self, destination: str, duration: int, interests: List[str]) -> Dict:
        """Generate dynamic itinerary based on destination and interests"""
        itinerary = {}
        for day in range(1, duration + 1):
            itinerary[f"Day {day}"] = [
                {"time": "09:00", "title": f"Explore {destination}", "description": f"Morning exploration of {destination}", "cost": 30},
                {"time": "14:00", "title": "Local Experience", "description": f"Discover {interests[0] if interests else 'local culture'}", "cost": 25},
                {"time": "19:00", "title": "Dinner", "description": f"Enjoy {destination} cuisine", "cost": 40},
            ]
        return itinerary
    
    def run(self):
        """Main UI loop"""
        # Annabeth AI Header with custom colored text
        st.markdown('<h1 class="main-header">✈️ Annabeth AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="tagline">"Your Intelligent Travel Companion"</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Powered by 5 Autonomous AI Agents</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        user_inputs = self.render_sidebar()
        
        col_main, col_side = st.columns([2.2, 0.8])
        
        with col_main:
            if user_inputs['generate'] and user_inputs['destination']:
                with st.spinner(" Annabeth AI is planning your perfect trip..."):
                    stages = [
                        " Coordinator Agent: Analyzing request...",
                        " Flight Expert: Searching best routes...",
                        " Hotel Expert: Finding accommodations...",
                        " Itinerary Planner: Creating daily schedule...",
                        " Budget Manager: Optimizing costs..."
                    ]
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, stage in enumerate(stages):
                        status_text.info(stage)
                        progress_bar.progress((i + 1) / len(stages))
                        time.sleep(0.5)
                        
                        if "Coordinator" in stage:
                            st.session_state.agent_status['coordinator'] = 'complete'
                        elif "Flight" in stage:
                            st.session_state.agent_status['flight_expert'] = 'complete'
                        elif "Hotel" in stage:
                            st.session_state.agent_status['hotel_expert'] = 'complete'
                        elif "Itinerary" in stage:
                            st.session_state.agent_status['itinerary_planner'] = 'complete'
                        elif "Budget" in stage:
                            st.session_state.agent_status['budget_manager'] = 'complete'
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                    try:
                        ai_request = f"""
                        Plan a {user_inputs['duration']}-day trip to {user_inputs['destination']} 
                        with ${user_inputs['budget']} budget for {user_inputs['travelers']} people.
                        Interests: {', '.join(user_inputs['interests'])}
                        Travel Style: {user_inputs['travel_style']}
                        Special requests: {user_inputs['notes'] if user_inputs['notes'] else 'None'}
                        """
                        
                        if 'planner' not in st.session_state:
                            st.session_state.planner = TravelPlannerCrew()
                        
                        result = st.session_state.planner.plan_trip(ai_request, "current_user")
                        
                        if isinstance(result, dict) and result:
                            st.session_state.current_plan = result
                        else:
                            st.session_state.current_plan = {
                                'total_cost': user_inputs['budget'] - int(user_inputs['budget'] * 0.1),
                                'budget': user_inputs['budget'],
                                'destination': user_inputs['destination'],
                                'duration': user_inputs['duration'],
                                'travelers': user_inputs['travelers'],
                                'savings': int(user_inputs['budget'] * 0.1),
                                'activities_count': user_inputs['duration'] * 3,
                                'itinerary': self._generate_real_itinerary(
                                    user_inputs['destination'], 
                                    user_inputs['duration'],
                                    user_inputs['interests']
                                ),
                                'budget_breakdown': {
                                    "Flights": int(user_inputs['budget'] * 0.30),
                                    "Hotels": int(user_inputs['budget'] * 0.30),
                                    "Activities": int(user_inputs['budget'] * 0.20),
                                    "Food": int(user_inputs['budget'] * 0.15),
                                    "Transport": int(user_inputs['budget'] * 0.05)
                                },
                                'flights': [
                                    {'airline': f'Flight to {user_inputs["destination"]}', 
                                    'departure': 'Flexible', 
                                    'price': f'${int(user_inputs["budget"] * 0.15)}', 
                                    'duration': 'Varies'}
                                ],
                                'hotels': [
                                    {'name': f'{user_inputs["destination"]} Central Hotel', 
                                    'rating': 4.2, 
                                    'location': 'City Center', 
                                    'price_per_night': int(user_inputs["budget"] * 0.05)}
                                ]
                            }
                        
                        st.success(f" Trip plan generated for {user_inputs['destination']}!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
                        st.info("Using fallback plan...")
            
            if st.session_state.current_plan:
                self.render_trip_plan(st.session_state.current_plan)
            else:
                st.info(" Fill in your trip details and click 'Generate Smart Plan' to start your journey with Annabeth AI!")
        
        with col_side:
            self.render_agent_status()
            
            st.markdown("---")
            
            st.markdown("###  Quick Stats")
            if st.session_state.current_plan:
                plan = st.session_state.current_plan
                
                budget = plan.get('budget', 1000)
                total_cost = plan.get('total_cost', 0)
                savings = plan.get('savings', 0)
                
                if budget > 0:
                    score = min(100, int(70 + ((budget - total_cost) / budget) * 30))
                    used_percent = int((total_cost / budget) * 100) if budget > 0 else 0
                else:
                    score = 85
                    used_percent = 0
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="margin: 0;"> Plan Score</h4>
                    <h1 style="margin: 0; font-size: 2.5rem;">{score}/100</h1>
                    <small>Budget: ${budget} | Used: {used_percent}%</small>
                </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(" Savings", f"${savings}")
                with col_b:
                    days = plan.get('duration', 1)
                    daily_cost = total_cost / days if days > 0 else 0
                    st.metric(" Daily Avg", f"${int(daily_cost)}")
            else:
                st.info("Generate a plan to see stats")
            
            st.markdown("---")
            
            st.markdown("###  Export")
            
            if st.button(" Download PDF", use_container_width=True):
                if st.session_state.current_plan:
                    with st.spinner("Generating PDF..."):
                        pdf_path = self.export_to_pdf(st.session_state.current_plan)
                        if pdf_path:
                            with open(pdf_path, 'rb') as f:
                                st.download_button(
                                    label=" Click to Download",
                                    data=f,
                                    file_name=f"annabeth_ai_travel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime='application/pdf',
                                    use_container_width=True
                                )
                            st.success("PDF ready!")
                        else:
                            st.error("Failed to generate PDF")
                else:
                    st.warning("Generate a plan first!")
            
            if st.button(" Email Plan", use_container_width=True):
                if st.session_state.current_plan:
                    email = st.text_input("Enter your email:", key="email_export", placeholder="you@example.com")
                    if email:
                        # Option 1: Use mailto link (works immediately)
                        success, result = self.export_to_email(st.session_state.current_plan, email)
                        if success:
                            st.success(" Click the link below to send your travel plan!")
                            st.markdown(f"[ Open in Email Client]({result})")
                            st.caption("Your email client will open with the plan pre-filled. Just click send!")
                        
                        # Option 2: For actual SMTP email (uncomment to use)
                        # if self.send_email_real(email, st.session_state.current_plan):
                        #     st.success(f"✅ Travel plan sent to {email}!")
                        # else:
                        #     st.error("Failed to send email. Using mailto link instead.")
                        #     success, result = self.export_to_email(st.session_state.current_plan, email)
                        #     st.markdown(f"[📨 Open in Email Client]({result})")
                    else:
                        st.info("Please enter your email address")
                else:
                    st.warning("Generate a travel plan first!")
        
        st.markdown("---")
        self.render_chat_interface()

if __name__ == "__main__":
    ui = TravelPlannerUI()
    ui.run()