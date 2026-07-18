from dataclasses import dataclass
from typing import List
from src.view.models.kurs_view_model import KursViewModel
from src.view.models.semester_view_model import SemesterViewModel
from src.view.models.exam_view_model import ExamViewModel
from src.view.models.grade_view_model import GradeViewModel
from src.view.models.stats_view_model import StatsViewModel

@dataclass
class StudiumViewModel:
    """View model for study program information"""
    name: str
    datum: str
    anzahl_tage_gesamt: int
    vergangene_tage: int
    verbleibende_tage: int
    kurse: List[KursViewModel]
    semester: List[SemesterViewModel]
    faellige_pruefungen: List[ExamViewModel]
    naechste_pruefungen: List[ExamViewModel]
    noten: GradeViewModel
    stats: StatsViewModel
