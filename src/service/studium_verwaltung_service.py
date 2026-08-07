from datetime import date
from typing import List
from src.repo.studium_repository import StudiumRepository
from src.entity.studium import Studium
from src.entity.enums import KursSchwere


class StudiumVerwaltungService:
    """
    Service für die Verwaltung von Studium und Kursen.
    
    Diese Klasse kapselt die Lese- und Schreiboperationen für Studium und Kurse.
    """

    def __init__(self, repository: StudiumRepository):
        """
        Initialisiert den StudiumVerwaltungService.
        
        Args:
            repository (StudiumRepository): Repository für den Zugriff auf die Studiumsdaten.
        """
        self.repository = repository

    def erstelle_kurs(self, studium: Studium, name: str, ects: int, schwere: KursSchwere) -> None:
        """
        Erstellt einen neuen Kurs und fügt ihn dem Studium hinzu.
        
        Args:
            studium (Studium): Das Studium, dem der Kurs hinzugefügt werden soll.
            name (str): Der Name des Kurses.
            ects (int): Die ECTS-Punkte des Kurses.
            schwere (KursSchwere): Die Schwierigkeit des Kurses.
        """
        import uuid
        studium.fuege_kurs_hinzu(kurs_id=uuid.uuid4().hex, name=name, ects=ects, schwere=schwere)
        self.repository.speichere_studium(studium)

    def aktualisiere_kurs(self, studium: Studium, kurs_id: str, name: str, ects: int, schwere: int, noten: List[float]) -> None:
        """
        Aktualisiert einen bestehenden Kurs.
        
        Args:
            studium (Studium): Das Studium, das den Kurs enthält.
            kurs_id (str): Die ID des zu aktualisierenden Kurses.
            name (str): Der neue Name des Kurses.
            ects (int): Die neuen ECTS-Punkte des Kurses.
            schwere (int): Die neue Schwierigkeit des Kurses.
            noten (List[float]): Die neuen Noten des Kurses.
        """
        studium.aktualisiere_kurs(kurs_id=kurs_id, name=name, ects=ects, schwere=schwere, noten=noten)
        self.repository.speichere_studium(studium)

    def verschiebe_kurs(self, studium: Studium, kurs_id: str, hoch: bool) -> None:
        """
        Verschiebt einen Kurs in der Reihenfolge.
        
        Args:
            studium (Studium): Das Studium, das den Kurs enthält.
            kurs_id (str): Die ID des zu verschiebenden Kurses.
            hoch (bool): True, wenn der Kurs nach oben verschoben werden soll, False für nach unten.
        """
        studium.verschiebe_kurs(kurs_id, hoch)
        self.repository.speichere_studium(studium)

    def aktualisiere_studium(self, studium: Studium, name: str, beginn: date, ziel_note: float, ziel_monate: int) -> None:
        """
        Aktualisiert die Eigenschaften des Studiums.
        
        Args:
            studium (Studium): Das zu aktualisierende Studium.
            name (str): Der neue Name des Studiums.
            beginn (date): Der neue Beginn des Studiums.
            ziel_note (float): Die neue Zielnote des Studiums.
            ziel_monate (int): Die neue Zieldauer des Studiums in Monaten.
        """
        studium.name = name
        studium.beginn = beginn
        studium.ziel_note = ziel_note
        studium.ziel_monate = ziel_monate
        self.repository.speichere_studium(studium)
