"""
Travel Planner Crew - LangGraph Implementation
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any, List
import random
from datetime import datetime
from agents.coordinator import CoordinatorAgent
from memory.vector_memory import travel_memory

class TravelState(TypedDict):
    request: str
    user_id: str
    destination: str
    budget: int
    duration: int
    travelers: int
    plan: Dict[str, Any]

class TravelPlannerCrew:
    """Agentic travel planner using LangGraph"""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.graph = self._build_graph()
        print("✅ Travel Planner Crew Ready (LangGraph mode)")
    
    def _build_graph(self):
        """Build the agent workflow graph"""
        workflow = StateGraph(TravelState)
        
        # Add nodes (each is like an agent)
        workflow.add_node("coordinator", self._coordinator_node)
        workflow.add_node("flight_agent", self._flight_agent_node)
        workflow.add_node("hotel_agent", self._hotel_agent_node)
        workflow.add_node("itinerary_agent", self._itinerary_agent_node)
        workflow.add_node("budget_agent", self._budget_agent_node)
        workflow.add_node("finalizer", self._finalizer_node)
        
        # Define workflow
        workflow.set_entry_point("coordinator")
        workflow.add_edge("coordinator", "flight_agent")
        workflow.add_edge("flight_agent", "hotel_agent")
        workflow.add_edge("hotel_agent", "itinerary_agent")
        workflow.add_edge("itinerary_agent", "budget_agent")
        workflow.add_edge("budget_agent", "finalizer")
        workflow.add_edge("finalizer", END)
        
        return workflow.compile()
    
    def _coordinator_node(self, state: TravelState) -> TravelState:
        """Coordinator agent - analyze request"""
        print("🤖 Coordinator: Analyzing request...")
        
        analysis = self.coordinator.analyze_request(state['request'])
        
        # Get context from memory for personalization
        context = travel_memory.get_context_for_agent(state['user_id'], state['request'])
        if context.get('preferences'):
            print(f"📚 Using {len(context['preferences'])} past preferences for personalization")
        
        return {
            **state,
            "destination": analysis['destination'],
            "budget": analysis['budget'],
            "duration": analysis['duration'],
            "travelers": analysis['travelers']
        }
    
    def _flight_agent_node(self, state: TravelState) -> TravelState:
        """Flight agent - find flight options"""
        print("✈️ Flight Agent: Searching for best flights...")
        
        budget = state['budget']
        destination = state['destination']
        travelers = state['travelers']
        
        # Ensure minimum budget for flights
        if budget < 500:
            base_flight_cost = max(100, int(budget * 0.25))
        else:
            base_flight_cost = int(budget * 0.15)
        
        if destination in ["Tokyo", "Singapore", "Sydney", "Denmark"]:  # Long haul
            base_flight_cost = max(150, int(budget * 0.30))
        elif destination in ["Paris", "London", "New York"]:  # Medium haul
            base_flight_cost = max(120, int(budget * 0.25))
        
        flights = [
            {
                "airline": "Delta Airlines",
                "departure": "08:00 AM",
                "arrival": "12:00 PM",
                "duration": "4h",
                "price": f"${base_flight_cost}",
                "price_value": base_flight_cost,
                "stops": "Direct",
                "recommended": True
            },
            {
                "airline": "United Airlines",
                "departure": "02:00 PM",
                "arrival": "06:00 PM",
                "duration": "4h 30m",
                "price": f"${max(80, int(base_flight_cost * 0.8))}",
                "price_value": max(80, int(base_flight_cost * 0.8)),
                "stops": "1 stop",
                "recommended": False
            },
            {
                "airline": "Emirates",
                "departure": "10:00 PM",
                "arrival": "08:00 AM+1",
                "duration": "10h",
                "price": f"${base_flight_cost + 50}",
                "price_value": base_flight_cost + 50,
                "stops": "Direct",
                "recommended": False
            }
        ]
        
        if 'plan' not in state:
            state['plan'] = {}
        state['plan']['flights'] = flights
        
        return state
    
    def _hotel_agent_node(self, state: TravelState) -> TravelState:
        """Hotel agent - find accommodation"""
        print("🏨 Hotel Agent: Finding best accommodations...")
        
        budget = state['budget']
        destination = state['destination']
        travelers = state['travelers']
        duration = state['duration']
        
        # Calculate nightly budget with minimum guarantee
        if duration > 0 and budget > 0:
            nightly_budget = max(30, int((budget * 0.30) / duration))
        else:
            nightly_budget = 50
        
        hotels = [
            {
                "name": f"{destination} Grand Hotel",
                "rating": 4.5,
                "price_per_night": nightly_budget,
                "total_price": nightly_budget * duration,
                "location": "City Center",
                "amenities": ["Free WiFi", "Breakfast", "Pool", "Spa"],
                "recommended": True
            },
            {
                "name": f"{destination} Boutique Inn",
                "rating": 4.2,
                "price_per_night": max(25, int(nightly_budget * 0.7)),
                "total_price": max(25, int(nightly_budget * 0.7 * duration)),
                "location": "Arts District",
                "amenities": ["Free WiFi", "Breakfast"],
                "recommended": False
            },
            {
                "name": f"{destination} Luxury Suites",
                "rating": 4.8,
                "price_per_night": nightly_budget * 2,
                "total_price": nightly_budget * 2 * duration,
                "location": "Downtown",
                "amenities": ["Free WiFi", "Breakfast", "Pool", "Spa", "Gym", "Restaurant"],
                "recommended": False
            }
        ]
        
        state['plan']['hotels'] = hotels
        
        return state
    
    def _itinerary_agent_node(self, state: TravelState) -> TravelState:
        """Itinerary agent - create daily schedule"""
        print("🗺️ Itinerary Agent: Creating daily schedule...")
        
        destination = state['destination']
        duration = state['duration']
        budget = state['budget']
        
        # Activity templates by destination
        activities_db = {
            "Paris": ["Eiffel Tower", "Louvre Museum", "Seine Cruise", "Montmartre", "Notre-Dame", "Versailles"],
            "Tokyo": ["Senso-ji Temple", "Shibuya Crossing", "Tokyo Tower", "Meiji Shrine", "Akihabara", "Disneyland"],
            "New York": ["Times Square", "Central Park", "Statue of Liberty", "Empire State", "Broadway", "Museum of Art"],
            "London": ["Big Ben", "London Eye", "British Museum", "Tower of London", "Buckingham Palace", "Hyde Park"],
            "Rome": ["Colosseum", "Vatican", "Trevi Fountain", "Pantheon", "Roman Forum", "Spanish Steps"],
            "Denmark": ["Tivoli Gardens", "Nyhavn", "Little Mermaid", "Christiansborg Palace", "Rosenborg Castle", "National Museum"]
        }
        
        activities = activities_db.get(destination, ["City Tour", "Museum Visit", "Local Cuisine", "Shopping", "Parks", "Cultural Show"])
        
        # Calculate daily activity budget with safety check for small budgets
        if duration > 0 and budget > 0:
            daily_activity_budget = max(15, int((budget * 0.20) / duration))
        else:
            daily_activity_budget = 30
        
        itinerary = {}
        for day in range(1, duration + 1):
            day_activities = []
            
            # Morning activity
            morning_activity = activities[(day - 1) % len(activities)]
            morning_cost = min(daily_activity_budget // 2, random.randint(10, max(15, daily_activity_budget // 2)))
            day_activities.append({
                "time": "09:00", 
                "title": morning_activity, 
                "description": f"Experience the best of {destination}'s {morning_activity.lower()}", 
                "cost": max(10, morning_cost)
            })
            
            # Afternoon activity
            afternoon_activity = activities[day % len(activities)]
            afternoon_cost = min(daily_activity_budget // 3, random.randint(8, max(12, daily_activity_budget // 3)))
            day_activities.append({
                "time": "14:00", 
                "title": afternoon_activity, 
                "description": f"Continue exploring {destination} with {afternoon_activity.lower()}", 
                "cost": max(8, afternoon_cost)
            })
            
            # Evening activity
            if day == 1:
                evening_title = f"Welcome Dinner at Traditional {destination} Restaurant"
                evening_desc = f"Authentic {destination} cuisine experience"
            elif day == duration:
                evening_title = "Farewell Dinner & Cultural Show"
                evening_desc = f"Celebrate your amazing journey in {destination}"
            else:
                evening_title = "Evening Exploration & Dinner"
                evening_desc = f"Discover {destination}'s vibrant nightlife and local dining"
            
            evening_cost = min(daily_activity_budget, random.randint(15, max(20, daily_activity_budget)))
            day_activities.append({
                "time": "19:00", 
                "title": evening_title, 
                "description": evening_desc, 
                "cost": max(15, evening_cost)
            })
            
            itinerary[f"Day {day}"] = day_activities
        
        state['plan']['itinerary'] = itinerary
        state['plan']['activities_count'] = sum(len(day) for day in itinerary.values())
        
        return state
    
    def _budget_agent_node(self, state: TravelState) -> TravelState:
        """Budget agent - optimize spending"""
        print("💰 Budget Agent: Optimizing budget allocation...")
        
        budget = state['budget']
        duration = state['duration']
        
        # Ensure budget is positive
        if budget <= 0:
            budget = 500  # Default fallback for small budgets
        
        # Smart budget allocation based on destination and duration
        if duration <= 3:
            # Short trips - spend more on experiences
            breakdown = {
                "Flights": max(100, int(budget * 0.35)),
                "Hotels": max(80, int(budget * 0.25)),
                "Activities": max(50, int(budget * 0.25)),
                "Food": max(30, int(budget * 0.10)),
                "Transport": max(20, int(budget * 0.05))
            }
        elif duration >= 7:
            # Long trips - more on accommodation and food
            breakdown = {
                "Flights": max(150, int(budget * 0.25)),
                "Hotels": max(100, int(budget * 0.35)),
                "Activities": max(60, int(budget * 0.20)),
                "Food": max(40, int(budget * 0.15)),
                "Transport": max(20, int(budget * 0.05))
            }
        else:
            # Standard allocation
            breakdown = {
                "Flights": max(120, int(budget * 0.30)),
                "Hotels": max(90, int(budget * 0.30)),
                "Activities": max(50, int(budget * 0.20)),
                "Food": max(35, int(budget * 0.15)),
                "Transport": max(20, int(budget * 0.05))
            }
        
        state['plan']['budget_breakdown'] = breakdown
        state['plan']['total_cost'] = sum(breakdown.values())
        state['plan']['savings'] = max(0, budget - state['plan']['total_cost'])
        state['plan']['budget'] = budget
        
        return state
    
    def _finalizer_node(self, state: TravelState) -> TravelState:
        """Finalize and store the plan"""
        print("✅ Finalizing plan...")
        
        state['plan']['destination'] = state['destination']
        state['plan']['duration'] = state['duration']
        state['plan']['travelers'] = state['travelers']
        state['plan']['generated_at'] = datetime.now().isoformat()
        state['plan']['destinations'] = 1  # For display
        
        # Store user preferences automatically
        interests = f"Visited {state['destination']} with ${state['budget']} budget for {state['duration']} days"
        travel_memory.store_user_preference(
            state['user_id'],
            interests,
            "travel_history"
        )
        
        # Store complete trip
        travel_memory.store_trip(state['user_id'], state['plan'])
        
        return state
    
    def plan_trip(self, user_request: str, user_id: str = "default_user") -> Dict[str, Any]:
        """Main method to plan a trip"""
        
        print(f"\n🚀 Starting Agentic Trip Planning for {user_id}...")
        print(f"📝 Request: {user_request[:100]}...")
        
        # Get user preferences from memory with context
        preferences = travel_memory.get_user_preferences(user_id, limit=5)
        if preferences:
            print(f"📚 Found {len(preferences)} past preferences")
        
        # Get similar past trips for better recommendations
        similar_trips = travel_memory.get_similar_trips(user_id, limit=2)
        if similar_trips:
            print(f"📖 Found {len(similar_trips)} similar past trips")
        
        # Run the agent graph
        result = self.graph.invoke({
            "request": user_request,
            "user_id": user_id,
            "destination": "",
            "budget": 0,
            "duration": 0,
            "travelers": 0,
            "plan": {}
        })
        
        print(f"\n✅ Trip plan ready for {result['destination']}!")
        print(f"💰 Total Cost: ${result['plan'].get('total_cost', 0)}")
        print(f"🎯 Activities: {result['plan'].get('activities_count', 0)}")
        
        return result['plan']


# Quick test
if __name__ == "__main__":
    planner = TravelPlannerCrew()
    plan = planner.plan_trip(
        "Plan a 5-day trip to Paris with $3000 budget for 2 people",
        "test_user"
    )
    print(f"\n📊 Final Plan: {list(plan.keys())}")
    print(f"💰 Total Cost: ${plan.get('total_cost', 0)}")
    print(f"📍 Destination: {plan.get('destination', 'Unknown')}")