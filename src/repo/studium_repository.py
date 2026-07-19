from src.entity.studium import Studium
from src.entity.kurs import Kurs
from src.entity.enums import KursSchwere
import json
from pathlib import Path
from datetime import date
from typing import Dict, Any


class StudiumRepository:
    """
    Repository für den Zugriff auf die Studiumsdaten.
    
    Diese Klasse verwaltet das Speichern und Laden von Studiumsdaten aus einer JSON-Datei.
    """
    def __init__(self, file_name: str):
        """
        Initialisiert das StudiumRepository.
        
        Args:
            file_name (str): Der Name der Datei, in der die Studiumsdaten gespeichert werden.
        """
        self.path: Path = Path(file_name)


    def speichere_studium(self, studium: Studium) -> None:
        """
        Speichert ein Studium in einer JSON-Datei.
        
        Args:
            studium (Studium): Das zu speichernde Studium.
        """
        data = self._studium_to_dict(studium)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def lade_studium(self) -> Studium | None:
        """
        Lädt ein Studium aus einer JSON-Datei.
        
        Returns:
            Studium | None: Das geladene Studium oder None, falls die Datei nicht existiert.
        """
        if not self.path.exists():
            return None
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self._dict_to_studium(data)


    def _studium_to_dict(self, studium: Studium) -> Dict[str, Any]:
        """
        Konvertiert ein Studium in ein Dictionary.
        
        Args:
            studium (Studium): Das zu konvertierende Studium.
            
        Returns:
            Dict[str, Any]: Das konvertierte Studium als Dictionary.
        """
        return {
            "name": studium.name,
            "beginn": studium.beginn.isoformat(),
            "ziel_note": studium.ziel_note,
            "ziel_monate": studium.ziel_monate,
            "kurse": [self._kurs_to_dict(kurs) for kurs in studium.kurse]
        }

    def _kurs_to_dict(self, kurs: Kurs) -> Dict[str, Any]:
        """
        Konvertiert einen Kurs in ein Dictionary.
        
        Args:
            kurs (Kurs): Der zu konvertierende Kurs.
            
        Returns:
            Dict[str, Any]: Der konvertierte Kurs als Dictionary.
        """
        return {
            "id": kurs.id,
            "name": kurs.name,
            "ects": kurs.ects,
            "schwere": kurs.schwere,
            "noten": kurs.noten,
            "beginn": kurs.beginn.isoformat() if kurs.beginn else None,
            "ende": kurs.ende.isoformat() if kurs.ende else None
        }

    def _dict_to_studium(self, data: Dict[str, Any]) -> Studium:
        """
        Konvertiert ein Dictionary in ein Studium.
        
        Args:
            data (Dict[str, Any]): Das zu konvertierende Dictionary.
            
        Returns:
            Studium: Das konvertierte Studium.
        """
        studium = Studium(
            name=data["name"],
            beginn=date.fromisoformat(data["beginn"]),
            ziel_note=data["ziel_note"],
            ziel_monate=data["ziel_monate"]
        )
        studium._kurse = [self._dict_to_kurs(kurs_data) for kurs_data in data["kurse"]]
        return studium


    def _dict_to_kurs(self, data: Dict[str, Any]) -> Kurs:
        """
        Konvertiert ein Dictionary in einen Kurs.
        
        Args:
            data (Dict[str, Any]): Das zu konvertierende Dictionary.
            
        Returns:
            Kurs: Der konvertierte Kurs.
        """
        return Kurs(
            id=data["id"],
            name=data["name"],
            ects=data["ects"],
            schwere=KursSchwere(data["schwere"]),
            noten=data["noten"],
            beginn=date.fromisoformat(data["beginn"]) if data["beginn"] else None,
            ende=date.fromisoformat(data["ende"]) if data["ende"] else None
        )
