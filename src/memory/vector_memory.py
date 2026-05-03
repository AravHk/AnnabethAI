"""
Vector Memory System for Travel Planner
Stores and retrieves user preferences and past trips using ChromaDB
"""

import chromadb
from chromadb.utils import embedding_functions
import json
from datetime import datetime
import hashlib
from typing import Dict, Any  # Add this with other imports

class TravelMemory:
    def __init__(self, persist_directory="./data/chroma_db"):
        """Initialize vector database with persistence"""
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Create collections for different memory types
        self.user_preferences = self.client.get_or_create_collection(
            name="user_preferences",
            embedding_function=self.embedding_fn
        )
        
        self.past_trips = self.client.get_or_create_collection(
            name="past_trips",
            embedding_function=self.embedding_fn
        )
        
        self.real_time = self.client.get_or_create_collection(
            name="real_time_updates",
            embedding_function=self.embedding_fn
        )
        
        print("✅ Vector Memory System Initialized")
    
    def store_user_preference(self, user_id: str, preference: str, category: str):
        """Store user preference with metadata"""
        doc_id = f"{user_id}_{category}_{hashlib.md5(preference.encode()).hexdigest()[:10]}"
        
        self.user_preferences.upsert(
            documents=[preference],
            metadatas=[{
                "user_id": user_id,
                "category": category,
                "timestamp": datetime.now().isoformat()
            }],
            ids=[doc_id]
        )
        print(f"📝 Stored preference for {user_id}: {preference[:50]}...")
    
    def get_user_preferences(self, user_id: str, category: str = None, limit: int = 5):
        """Retrieve user preferences with optional category filter"""
        where_filter = {"user_id": user_id}
        if category:
            where_filter["category"] = category
        
        results = self.user_preferences.query(
            query_texts=[""],
            n_results=limit,
            where=where_filter
        )
        
        return results['documents'][0] if results['documents'] else []
    
    def find_similar_preferences(self, user_id: str, query: str, limit: int = 3):
        """Find preferences similar to query using semantic search"""
        results = self.user_preferences.query(
            query_texts=[query],
            n_results=limit,
            where={"user_id": user_id}
        )
        
        return results['documents'][0] if results['documents'] else []
    def get_context_for_agent(self, user_id: str, current_request: str, limit: int = 5) -> Dict[str, Any]:
    
            context = {
                "preferences": [],
                "past_similar_trips": [],
                "relevant_history": []
            }
            
            # Get similar preferences
            similar_prefs = self.find_similar_preferences(user_id, current_request, limit=3)
            context["preferences"] = similar_prefs
            
            # Extract destination if present in request
            import re
            destination_match = re.search(r'(?:to|in|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', current_request)
            if destination_match:
                destination = destination_match.group(1)
                past_trips = self.get_similar_trips(user_id, destination, limit=2)
                context["past_similar_trips"] = past_trips
            
            return context
    def store_trip(self, user_id: str, trip_data: dict):
        """Store complete trip information"""
        trip_summary = json.dumps(trip_data, default=str)
        trip_id = f"{user_id}_{trip_data.get('destination', 'unknown')}_{datetime.now().timestamp()}"
        
        self.past_trips.upsert(
            documents=[trip_summary],
            metadatas=[{
                "user_id": user_id,
                "destination": trip_data.get('destination', ''),
                "budget": trip_data.get('budget', 0),
                "duration": trip_data.get('duration', 0),
                "timestamp": datetime.now().isoformat()
            }],
            ids=[trip_id]
        )
        print(f"💾 Stored trip for {user_id}: {trip_data.get('destination', 'Unknown')}")
    
    def get_similar_trips(self, user_id: str, destination: str = None, limit: int = 3):
        """Find similar past trips"""
        if destination:
            results = self.past_trips.query(
                query_texts=[destination],
                n_results=limit,
                where={"user_id": user_id}
            )
        else:
            results = self.past_trips.query(
                query_texts=[""],
                n_results=limit,
                where={"user_id": user_id}
            )
        
        trips = []
        if results['documents'][0]:
            for doc in results['documents'][0]:
                try:
                    trips.append(json.loads(doc))
                except:
                    trips.append({"raw": doc})
        
        return trips
    
    def update_prices(self, trip_id: str, price_updates: dict):
        """Store real-time price updates"""
        update_id = f"price_{trip_id}_{datetime.now().timestamp()}"
        
        self.real_time.upsert(
            documents=[json.dumps(price_updates)],
            metadatas=[{
                "trip_id": trip_id,
                "type": "price_update",
                "timestamp": datetime.now().isoformat()
            }],
            ids=[update_id]
        )
    
    def clear_user_data(self, user_id: str):
        """Clear all data for a specific user"""
        # ChromaDB doesn't support easy deletion, so we'll recreate collections
        print(f"⚠️ Clearing data for {user_id} - feature in development")
    
    def get_memory_stats(self):
        """Get statistics about stored memories"""
        return {
            "user_preferences": len(self.user_preferences.get()['ids']),
            "past_trips": len(self.past_trips.get()['ids']),
            "real_time_updates": len(self.real_time.get()['ids'])
        }


# Global instance for easy import
travel_memory = TravelMemory()


# Quick test function
def test_memory():
    """Test the memory system"""
    print("\n🧪 Testing Vector Memory System...")
    
    # Store test preference
    travel_memory.store_user_preference(
        "test_user",
        "I love beach destinations and seafood",
        "interests"
    )
    
    # Find similar preferences
    similar = travel_memory.find_similar_preferences(
        "test_user",
        "I want a coastal vacation"
    )
    print(f"🔍 Similar preferences found: {len(similar)}")
    
    # Store test trip
    travel_memory.store_trip("test_user", {
        "destination": "Bali",
        "budget": 2000,
        "duration": 7,
        "activities": ["surfing", "yoga"]
    })
    
    # Get past trips
    trips = travel_memory.get_similar_trips("test_user", "Bali")
    print(f"📚 Past trips found: {len(trips)}")
    
    stats = travel_memory.get_memory_stats()
    print(f"📊 Memory stats: {stats}")
    
    print("✅ Memory test complete!\n")

if __name__ == "__main__":
    test_memory()