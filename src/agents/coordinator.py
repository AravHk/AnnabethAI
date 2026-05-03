"""
Coordinator Agent - Using LangGraph (No CrewAI)
"""

from typing import Dict, Any, List
import re

class CoordinatorAgent:
    """Main coordinator agent - LangGraph version"""
    
    def __init__(self):
        self.role = "Chief Travel Coordinator"
        
    def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """Extract key information from user request"""
        
        # Extract destination
        destinations = ["Paris", "Tokyo", "New York", "London", "Dubai", "Bali", "Rome", 
                       "Singapore", "Bangkok", "Istanbul", "Barcelona", "Amsterdam"]
        destination = "Paris"  # default
        for dest in destinations:
            if dest.lower() in user_request.lower():
                destination = dest
                break
        
        # Extract budget
        budget_match = re.search(r'\$\s*(\d+)', user_request)
        budget = int(budget_match.group(1)) if budget_match else 2000
        
        # Extract duration (days)
        duration_match = re.search(r'(\d+)\s*(?:day|night)', user_request.lower())
        duration = int(duration_match.group(1)) if duration_match else 5
        
        # Extract travelers
        travelers_match = re.search(r'(\d+)\s*(?:people|person|travelers|pax)', user_request.lower())
        travelers = int(travelers_match.group(1)) if travelers_match else 2
        
        return {
            "destination": destination,
            "budget": budget,
            "duration": duration,
            "travelers": travelers,
            "original_request": user_request
        }