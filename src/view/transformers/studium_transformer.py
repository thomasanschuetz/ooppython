from datetime import date
from typing import List
from src.entity.studium import Studium
from src.entity.semester import Semester
from src.entity.studium_statistik import StudiumStatistik
from src.view.models.studium_view_model import StudiumViewModel
from src.view.models.semester_view_model import SemesterViewModel
from src.view.transformers.kurs_transformer import KursTransformer
from src.view.transformers.stats_transformer import StatsTransformer
from src.view.transformers.grade_transformer import GradeTransformer
from src.view.transformers.exam_transformer import ExamTransformer

class StudiumTransformer:
    """Main transformer for Studium entities to StudiumViewModel"""
    
    def __init__(self):
        self.kurs_transformer = KursTransformer()
        self.stats_transformer = StatsTransformer()
        self.grade_transformer = GradeTransformer()
        self.exam_transformer = ExamTransformer()
    
    def transform(self, studium: Studium, statistik: StudiumStatistik,
                 semester_list: List[Semester], datum: date) -> StudiumViewModel:
        """Transform Studium and related entities to StudiumViewModel"""
        
        # Transform semester
        semester_view_models = [
            SemesterViewModel(
                name=str(s.no),
                hoehe_rel=s.anzahl_tage()
            )
            for s in semester_list
        ]
        
        # Transform courses
        kurs_view_models = [
            self.kurs_transformer.transform(k, datum)
            for k in studium.kurse
        ]
        
        # Transform exams
        faellige_pruefungen = self.exam_transformer.transform_faellige_pruefungen(
            list(studium.kurse), datum
        )
        naechste_pruefungen = self.exam_transformer.transform_naechste_pruefungen(
            list(studium.kurse), datum
        )
        
        # Transform grades
        noten_view_model = self.grade_transformer.transform(
            ziel_note=studium.ziel_note,
            durchnitt_note=statistik.durchnitt_note,
            benoetigt_note=statistik.benoetigt_note
        )
        
        # Transform stats
        stats_view_model = self.stats_transformer.transform(
            statistik=statistik,
            ziel_note=studium.ziel_note
        )
        
        return StudiumViewModel(
            name=studium.name,
            datum=datum.isoformat(),
            anzahl_tage_gesamt=studium.anzahl_tage,
            vergangene_tage=studium.vergangene_tage(datum),
            verbleibende_tage=studium.verbleibende_tage(datum),
            kurse=kurs_view_models,
            semester=semester_view_models,
            faellige_pruefungen=faellige_pruefungen,
            naechste_pruefungen=naechste_pruefungen,
            noten=noten_view_model,
            stats=stats_view_model
        )
