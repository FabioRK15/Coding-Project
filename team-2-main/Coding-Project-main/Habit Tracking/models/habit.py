from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List, Dict

@dataclass
class Habit:
    name: str
    type: str  # "good" or "bad"
    streak: int = 0
    last_logged: Optional[date] = None
    history: List[Dict] = field(default_factory=list)
    mushroom_id: Optional[int] = None  # NEW: ID 1-5 for bad habits
    mushroom_active: bool = True       # NEW: Whether mushroom shows (True by default for bad habits)
    
    def __post_init__(self):
        """Initialize mushroom_active based on habit type"""
        if self.type == "bad":
            self.mushroom_active = True  # Bad habits start with active mushrooms
        else:
            self.mushroom_active = False  # Good habits don't have mushrooms

    def log_day(self, log_date: date, completed: bool):
        """
        completed = True:
            - good habits: done
            - bad habits: avoided
        completed = False:
            - bad habits: relapse
        """
        self.history.append({
            "date": log_date.isoformat(),
            "completed": completed
        })
        self.last_logged = log_date
        
        # NEW: Update mushroom status for bad habits
        if self.type == "bad":
            if completed:
                # Bad habit avoided → remove mushroom
                self.mushroom_active = False
            else:
                # Relapse → mushroom stays active
                self.mushroom_active = True
    
    def get_mushroom_status(self) -> str:
        """Helper method to get mushroom status text"""
        if self.type != "bad":
            return "N/A"
        return "Active" if self.mushroom_active else "Removed"