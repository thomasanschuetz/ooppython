from datetime import date
from typing import List
from src.entity.studium import Studium
from src.entity.semester import Semester
from src.entity.studium_statistik import StudiumStatistik
from src.view.models.studium_view_model import StudiumViewModel
from src.view.models.semester_view_model import SemesterViewModel
from src.view.transformers.kurs_transformer import KursTransformer
from src.view.transformers.stats_transformer import StatsTransformer
from src.view.transformers.noten_transformer import NotenTransformer
from src.view.transformers.pruefung_transformer import PruefungTransformer

class StudiumTransformer:
    def __init__(self):
        self.kurs_transformer = KursTransformer()
        self.stats_transformer = StatsTransformer()
        self.grade_transformer = NotenTransformer()
        self.exam_transformer = PruefungTransformer()
    
    def transformiere(self, studium: Studium, statistik: StudiumStatistik,
                 semester_list: List[Semester], datum: date) -> StudiumViewModel:
        semester_view_models = [
            SemesterViewModel(
                name=str(s.no),
                hoehe_rel=s.anzahl_tage()
            )
            for s in semester_list
        ]
        
        kurs_view_models = [
            self.kurs_transformer.transform(k, datum)
            for k in studium.kurse
        ]
        
        faellige_pruefungen = self.exam_transformer.transformiere_faellige_pruefungen(
            list(studium.kurse), datum
        )
        naechste_pruefungen = self.exam_transformer.transformiere_naechste_pruefungen(
            list(studium.kurse), datum
        )
        
        # Transform grades
        noten_view_model = self.grade_transformer.transform(
            ziel_note=studium.ziel_note,
            durchnitt_note=statistik.durchnitt_note,
            benoetigt_note=statistik.benoetigt_note
        )
        
        # Transform stats
        stats_view_model = self.stats_transformer.transformiere(
            statistik=statistik
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
