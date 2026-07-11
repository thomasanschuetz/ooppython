from dataclasses import dataclass

@dataclass
class ExamViewModel:
    """View model for exam/prüfung information"""
    name: str
    faellig_seit_tage: int | None = None
    faellig_in_tage: int | None = None
