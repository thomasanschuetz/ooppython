# Import der benötigten Module und Klassen
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
    """
    Transformer für die Konvertierung von Studiumsdaten in StudiumViewModel.
    """
    def __init__(self):
        """
        Initialisiert den StudiumTransformer.
        """
        self.kurs_transformer: KursTransformer = KursTransformer()
        self.stats_transformer: StatsTransformer = StatsTransformer()
        self.grade_transformer:NotenTransformer = NotenTransformer()
        self.exam_transformer:PruefungTransformer = PruefungTransformer()
    
    def transformiere(self, studium: Studium, statistik: StudiumStatistik,
                 semester_list: List[Semester], datum: date) -> StudiumViewModel:
        """
        Konvertiert Studiumsdaten in ein StudiumViewModel.
        
        Args:
            studium (Studium): Das zu konvertierende Studium.
            statistik (StudiumStatistik): Die Statistikdaten des Studiums.
            semester_list (List[Semester]): Die Liste der Semester.
            datum (date): Das aktuelle Datum.
            
        Returns:
            StudiumViewModel: Das konvertierte StudiumViewModel.
        """
        """Transform a Kurs entity to KursViewModel"""
        semester_view_models = [
            SemesterViewModel(
                name=str(s.no),
                hoehe_rel=s.anzahl_tage()
            )
            for s in semester_list
        ]
        
        kurs_view_models = [
            self.kurs_transformer.transformiere(k, datum)
            for k in studium.kurse
        ]
        
        faellige_pruefungen = self.exam_transformer.transformiere_faellige_pruefungen(
            list(studium.kurse), datum
        )
        naechste_pruefungen = self.exam_transformer.transformiere_naechste_pruefungen(
            list(studium.kurse), datum
        )
        
        # Transform grades
        noten_view_model = self.grade_transformer.transformiere(
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
