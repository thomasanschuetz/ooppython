from dataclasses import dataclass

@dataclass
class SemesterViewModel:
    """View model for semester information"""
    name: str
    hoehe_rel: int
