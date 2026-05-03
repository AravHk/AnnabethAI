"""
Reusable UI Components for Travel Planner
"""

import streamlit as st
from typing import Callable, Dict, List
import time

class LoadingAnimation:
    """Custom loading animations"""
    
    @staticmethod
    def agent_thinking(agent_name: str, duration: float = 1.0):
        """Show agent thinking animation"""
        with st.spinner(f"🧠 {agent_name} is thinking..."):
            time.sleep(duration)
    
    @staticmethod
    def agent_searching(agent_name: str, query: str):
        """Show agent searching animation"""
        placeholder = st.empty()
        for i in range(3):
            placeholder.info(f"🔍 {agent_name} searching: {query} {'.' * (i+1)}")
            time.sleep(0.5)
        placeholder.empty()

class InteractiveElements:
    """Interactive UI elements"""
    
    @staticmethod
    def price_slider(label: str, min_val: int, max_val: int, default: int):
        """Custom price slider with formatting"""
        return st.slider(
            label,
            min_val, max_val, default,
            format="💰 $%d"
        )
    
    @staticmethod
    def rating_stars(rating: float, max_stars: int = 5):
        """Display rating as stars"""
        full_stars = int(rating)
        half_star = rating - full_stars >= 0.5
        empty_stars = max_stars - full_stars - (1 if half_star else 0)
        
        stars = "⭐" * full_stars
        if half_star:
            stars += "½"
        stars += "☆" * empty_stars
        
        return stars

class NotificationSystem:
    """Toast notifications for user feedback"""
    
    @staticmethod
    def success(message: str, duration: int = 3):
        """Show success notification"""
        st.toast(f"✅ {message}", icon="🎉")
    
    @staticmethod
    def warning(message: str, duration: int = 3):
        """Show warning notification"""
        st.toast(f"⚠️ {message}", icon="⚠️")
    
    @staticmethod
    def info(message: str, duration: int = 3):
        """Show info notification"""
        st.toast(f"ℹ️ {message}", icon="💡")