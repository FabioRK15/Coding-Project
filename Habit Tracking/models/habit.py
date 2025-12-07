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