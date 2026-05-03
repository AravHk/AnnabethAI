"""
Analytics Dashboard for Travel Plans - With AI Agent Integration
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any

class TravelDashboard:
    """Analytics dashboard component with AI-powered insights"""
    
    @staticmethod
    def create_cost_timeline(costs: Dict[str, List[float]], dates: List[str]):
        """Create interactive cost timeline"""
        if not costs or not dates:
            return None
            
        fig = go.Figure()
        
        for category, values in costs.items():
            if values:
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=values,
                    name=category,
                    mode='lines+markers',
                    line=dict(width=2),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title="Daily Cost Breakdown",
            xaxis_title="Date",
            yaxis_title="Cost (USD)",
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_activity_heatmap(activities: Dict[str, List[Any]], days: List[str]):
        """Create activity heatmap with AI insights"""
        if not activities or not days:
            return None
            
        # Calculate activity intensity and cost per day
        intensity = []
        total_cost = []
        
        for day in days:
            day_activities = activities.get(day, [])
            intensity.append(len(day_activities))
            total_cost.append(sum(act.get('cost', 0) for act in day_activities))
        
        # Create subplot with two metrics
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Activity Intensity', 'Daily Cost'),
            vertical_spacing=0.15
        )
        
        # Activity intensity heatmap
        fig.add_trace(
            go.Heatmap(
                z=[intensity],
                x=days,
                y=['Activities'],
                colorscale='Viridis',
                showscale=False
            ),
            row=1, col=1
        )
        
        # Cost bar chart
        fig.add_trace(
            go.Bar(
                x=days,
                y=total_cost,
                marker_color='lightblue',
                name='Cost'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title="Activity & Cost Analysis",
            height=500,
            showlegend=False
        )
        
        fig.update_yaxes(title_text="Number of Activities", row=1, col=1)
        fig.update_yaxes(title_text="Cost (USD)", row=2, col=1)
        
        return fig
    
    @staticmethod
    def show_ai_insights(plan_data: Dict, user_preferences: List = None):
        """Display AI-generated dynamic insights based on actual plan data"""
        st.markdown("### 🧠 AI-Powered Insights")
        
        insights = []
        
        # Dynamic insight 1: Budget analysis
        if plan_data:
            budget = plan_data.get('budget', 0)
            total_cost = plan_data.get('total_cost', 0)
            savings = plan_data.get('savings', 0)
            
            if budget > 0:
                savings_percent = int((savings / budget) * 100)
                insights.append(f"💰 **Budget Analysis:** You're saving ${savings} ({savings_percent}%) compared to your ${budget} budget. Great planning!")
            
            # Dynamic insight 2: Activity analysis
            activities_count = plan_data.get('activities_count', 0)
            duration = plan_data.get('duration', 5)
            if duration > 0:
                avg_activities_per_day = activities_count / duration
                if avg_activities_per_day > 4:
                    insights.append(f"🎯 **Pacing Alert:** You have {avg_activities_per_day:.1f} activities per day. Consider removing 1-2 for better relaxation.")
                elif avg_activities_per_day < 2:
                    insights.append(f"✨ **More Activities Available:** With only {avg_activities_per_day:.1f} activities per day, you could add more experiences!")
                else:
                    insights.append(f"✅ **Perfect Pacing:** {avg_activities_per_day:.1f} activities per day is ideal for an enjoyable trip!")
            
            # Dynamic insight 3: Destination-specific
            destination = plan_data.get('destination', '')
            if destination:
                insights.append(f"📍 **{destination} Tip:** The best time to visit {destination} is during shoulder season (spring/fall) for better weather and fewer crowds.")
            
            # Dynamic insight 4: Flight savings
            flights = plan_data.get('flights', [])
            if flights and budget > 0:
                flight_cost = 0
                for flight in flights:
                    if isinstance(flight, dict):
                        price_str = flight.get('price', '$0')
                        try:
                            flight_cost = int(price_str.replace('$', ''))
                        except:
                            flight_cost = budget * 0.3
                
                flight_percent = int((flight_cost / budget) * 100) if budget > 0 else 30
                if flight_percent > 35:
                    insights.append(f"✈️ **Flight Cost Alert:** Flights are {flight_percent}% of your budget. Try flying on Tuesdays/Wednesdays to save 20-30%.")
                else:
                    insights.append(f"✈️ **Good Deal:** Flights are only {flight_percent}% of your budget - great value!")
        
        # Dynamic insight 5: Personalization based on user preferences
        if user_preferences:
            interests = user_preferences
            if interests:
                insights.append(f"🎨 **Personalized For You:** Based on your interest in {', '.join(interests[:2])}, we've curated unique local experiences you'll love!")
        
        # Display insights with icons
        for insight in insights:
            st.info(insight)
        
        # Add an AI recommendation section
        if plan_data:
            with st.expander("🤖 AI Agent Recommendations", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✨ Upgrade Suggestions:**")
                    st.markdown("- Consider booking flights 6-8 weeks in advance")
                    st.markdown("- Travel insurance recommended for international trips")
                    st.markdown("- Download offline maps before departure")
                with col2:
                    st.markdown("**🎯 Local Tips:**")
                    st.markdown("- Learn 5 basic phrases in local language")
                    st.markdown("- Check local holidays before booking")
                    st.markdown("- Use public transportation for authentic experience")
    
    @staticmethod
    def create_budget_forecast(plan_data: Dict):
        """Create budget forecast chart"""
        if not plan_data:
            return None
        
        budget_breakdown = plan_data.get('budget_breakdown', {})
        if not budget_breakdown:
            return None
        
        # Create forecast for 7 days
        categories = list(budget_breakdown.keys())
        daily_rates = {cat: (val / 7) for cat, val in budget_breakdown.items() if val > 0}
        
        days = [f"Day {i}" for i in range(1, 8)]
        forecast_data = []
        
        for cat, daily_rate in daily_rates.items():
            cumulative = []
            running_total = 0
            for i in range(7):
                running_total += daily_rate
                cumulative.append(running_total)
            forecast_data.append({
                'category': cat,
                'cumulative': cumulative,
                'daily_rate': daily_rate
            })
        
        fig = go.Figure()
        
        for data in forecast_data:
            fig.add_trace(go.Scatter(
                x=days,
                y=data['cumulative'],
                name=data['category'],
                mode='lines+markers',
                stackgroup='one'
            ))
        
        fig.update_layout(
            title="7-Day Budget Forecast",
            xaxis_title="Day",
            yaxis_title="Cumulative Cost (USD)",
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    @staticmethod
    def show_agent_performance(agent_status: Dict):
        """Show AI agent performance metrics"""
        st.markdown("### 📊 Agent Performance")
        
        # Calculate performance
        total_agents = len(agent_status)
        completed = sum(1 for status in agent_status.values() if status in ['complete', 'idle'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Agents", total_agents)
        with col2:
            st.metric("Tasks Completed", completed)
        with col3:
            st.metric("Efficiency", f"{int((completed/total_agents)*100)}%")
        
        # Agent role breakdown
        agent_roles = {
            'coordinator': '🧠 Strategy',
            'flight_expert': '✈️ Flights',
            'hotel_expert': '🏨 Hotels',
            'itinerary_planner': '🗺️ Itinerary',
            'budget_manager': '💰 Budget'
        }
        
        cols = st.columns(5)
        for idx, (agent, role) in enumerate(agent_roles.items()):
            with cols[idx]:
                status = agent_status.get(agent, 'idle')
                emoji = '✅' if status == 'complete' else '⏳'
                st.markdown(f"{emoji} **{role}**")
                st.caption(status.upper())

# Quick test
if __name__ == "__main__":
    st.title("Dashboard Test")
    
    # Test data
    test_plan = {
        'budget': 3000,
        'total_cost': 2700,
        'savings': 300,
        'activities_count': 15,
        'duration': 5,
        'destination': 'Paris',
        'budget_breakdown': {
            'Flights': 900,
            'Hotels': 900,
            'Activities': 600,
            'Food': 450,
            'Transport': 150
        },
        'flights': [{'price': '$900'}]
    }
    
    TravelDashboard.show_ai_insights(test_plan, ['Culture', 'Food'])
    
    # Test agent status
    test_status = {
        'coordinator': 'complete',
        'flight_expert': 'searching',
        'hotel_expert': 'complete',
        'itinerary_planner': 'thinking',
        'budget_manager': 'complete'
    }
    
    TravelDashboard.show_agent_performance(test_status)