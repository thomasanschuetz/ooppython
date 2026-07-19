from dataclasses import dataclass
from typing import List
from src.view.models.kurs_view_model import KursViewModel
from src.view.models.semester_view_model import SemesterViewModel
from src.view.models.pruefung_view_model import PruefungViewModel
from src.view.models.noten_view_model import NotenViewModel
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
    faellige_pruefungen: List[PruefungViewModel]
    naechste_pruefungen: List[PruefungViewModel]
    noten: NotenViewModel
    stats: StatsViewModel
