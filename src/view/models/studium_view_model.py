from dataclasses import dataclass
from typing import List

@dataclass
class StudiumViewModel:
    """View model for study program information"""
    name: str
    datum: str
    anzahl_tage_gesamt: int
    vergangene_tage: int
    verbleibende_tage: int
    kurse: List['KursViewModel']
    semester: List['SemesterViewModel']
    faellige_pruefungen: List['ExamViewModel']
    naechste_pruefungen: List['ExamViewModel']
    noten: 'GradeViewModel'
    stats: 'StatsViewModel'
