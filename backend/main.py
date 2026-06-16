import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Dict, Any

class ProjectStats(BaseModel):
    total_records: int
    active_users: int
    conversion_rate: float
    growth_percentage: float

class BackendService:
    """
    A service class representing the backend/business logic of our application.
    This simulates interactions with a database, third-party APIs, or heavy data processing.
    """
    
    @staticmethod
    def get_dashboard_stats() -> ProjectStats:
        # Simulate fetching statistics from database
        return ProjectStats(
            total_records=12540,
            active_users=1420,
            conversion_rate=3.45,
            growth_percentage=12.4
        )
        
    @staticmethod
    def get_time_series_data(days: int = 30) -> pd.DataFrame:
        # Generate dummy time-series data for the frontend charts
        np.random.seed(42)
        dates = [datetime.today() - timedelta(days=i) for i in range(days)]
        dates.reverse()
        
        data = {
            "Date": dates,
            "Revenue": np.random.randint(1000, 5000, size=days).cumsum(),
            "Signups": np.random.randint(10, 100, size=days),
            "Churn": np.random.randint(1, 10, size=days)
        }
        return pd.DataFrame(data)

    @staticmethod
    def process_user_input(text_input: str) -> Dict[str, Any]:
        # Simple NLP mock processing
        if not text_input.strip():
            return {"status": "empty", "message": "Please enter some text."}
        
        words = text_input.split()
        word_count = len(words)
        char_count = len(text_input)
        
        return {
            "status": "success",
            "word_count": word_count,
            "char_count": char_count,
            "sentiment": "Positive" if "good" in text_input.lower() or "awesome" in text_input.lower() else "Neutral"
        }
