from datetime import date
from typing import List
from src.entity.kurs import Kurs
from src.entity.enums import KursStatus
from src.view.models.exam_view_model import ExamViewModel

class ExamTransformer:
    """Transformer for exam/prüfung information to ExamViewModel"""
    
    def transform_faellige_pruefungen(self, kurse: List[Kurs], datum: date) -> List[ExamViewModel]:
        """Transform overdue exams to ExamViewModel list"""
        return [
            ExamViewModel(
                name=k.name,
                faellig_seit_tage=-k.faellig_in_tagen(datum),
                faellig_in_tage=None
            )
            for k in kurse if k.get_status(datum) == KursStatus.FAELLIG
        ]
    
    def transform_naechste_pruefungen(self, kurse: List[Kurs], datum: date, max_kurse: int = 3) -> List[ExamViewModel]:
        """Transform upcoming exams to ExamViewModel list"""
        return [
            ExamViewModel(
                name=k.name,
                faellig_seit_tage=None,
                faellig_in_tage=k.faellig_in_tagen(datum)
            )
            for k in kurse if k.get_status(datum) == KursStatus.OFFEN
        ][:max_kurse]
