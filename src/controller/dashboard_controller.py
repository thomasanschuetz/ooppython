from datetime import date
import uuid
from typing import List

from src.repo.studium_repository import StudiumRepository
from src.service.studium_planung_service import StudiumPlanungService
from src.entity.studium import Studium
from src.entity.kurs import Kurs
from src.view.transformers.studium_transformer import StudiumTransformer
from src.view.models.studium_view_model import StudiumViewModel
from src.view.models.kurs_view_model import KursViewModel


class DashboardController:
    """
    Controller für das Dashboard der Anwendung.
    
    Diese Klasse verwaltet die Interaktion zwischen der Benutzeroberfläche und den Services.
    """

    def __init__(self, planung_service: StudiumPlanungService, repository: StudiumRepository, datum: date):
        """
        Initialisiert den DashboardController.
        
        Args:
            planung_service (StudiumPlanungService): Service für die Planung des Studiums.
            repository (StudiumRepository): Repository für den Zugriff auf die Studiumsdaten.
            datum (date): Das aktuelle Datum.
        """
        self.planung_service = planung_service
        self.repository = repository
        self.datum = datum
        self.studium_transformer = StudiumTransformer()

    def lade_studium(self) -> Studium:
        """
        Lädt das Studium aus dem Repository oder erstellt ein neues, falls keins vorhanden ist.
        
        Returns:
            Studium: Das geladene oder neu erstellte Studium.
        """
        studium = self.repository.lade_studium()

        if studium is None:
            studium = Studium('Mein Studium', date.today(), 1.0, 36, [])
        
        self.planung_service.setze_kurs_zeitraeume(studium)

        return studium
    
    def lade_kurs_view(self, kurs_id: str) -> KursViewModel|None:
        """
        Lädt die Ansicht eines bestimmten Kurses.
        
        Args:
            kurs_id (str): Die ID des Kurses.
            
        Returns:
            KursViewModel | None: Die Ansicht des Kurses oder None, falls der Kurs nicht gefunden wurde.
        """
        studium_view_model = self.lade_studium_view()
        return next((kurs for kurs in studium_view_model.kurse if kurs.id == kurs_id), None)


    def lade_studium_view(self) -> StudiumViewModel:
        """
        Lädt die Ansicht des Studiums inklusive Statistiken und Semestern.
        
        Returns:
            StudiumViewModel: Die Ansicht des Studiums.
        """
        studium = self.lade_studium()
        statistik = self.planung_service.get_studium_statistik(studium, self.datum)
        semester = self.planung_service.get_semester(studium)
        
        studium_view_model = self.studium_transformer.transformiere(
            studium=studium,
            statistik=statistik,
            semester_list=semester,
            datum=self.datum
        )

        return studium_view_model

    def erstelle_kurs(self, name: str, ects: int, schwere: int) -> None:
        """
        Erstellt einen neuen Kurs und fügt ihn dem Studium hinzu.
        
        Args:
            name (str): Der Name des Kurses.
            ects (int): Die ECTS-Punkte des Kurses.
            schwere (int): Die Schwierigkeit des Kurses.
        """
        studium = self.lade_studium()
        neuer_kurs = Kurs(id=uuid.uuid4().hex, name=name, ects=ects, schwere=schwere)
        studium.fuege_kurs_hinzu(neuer_kurs)
        self.planung_service.setze_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)

    def aktualisiere_kurs(self, kurs_id: str, name: str, ects: int, schwere: int, noten: List[float]) -> None:
        """
        Aktualisiert einen bestehenden Kurs.
        
        Args:
            kurs_id (str): Die ID des zu aktualisierenden Kurses.
            name (str): Der neue Name des Kurses.
            ects (int): Die neuen ECTS-Punkte des Kurses.
            schwere (int): Die neue Schwierigkeit des Kurses.
            noten (List[float]): Die neuen Noten des Kurses.
        """
        studium = self.lade_studium()
        neuer_kurs = Kurs(id=kurs_id, name=name, ects=ects, schwere=schwere, noten=noten)
        studium.aktualisiere_kurs(neuer_kurs)
        self.planung_service.setze_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)

    def verschiebe_kurs(self, kurs_id: str, hoch: bool) -> None:
        """
        Verschiebt einen Kurs in der Reihenfolge.
        
        Args:
            kurs_id (str): Die ID des zu verschiebenden Kurses.
            hoch (bool): True, wenn der Kurs nach oben verschoben werden soll, False für nach unten.
        """
        studium = self.lade_studium()
        studium.verschiebe_kurs(kurs_id, hoch)
        self.planung_service.setze_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)
