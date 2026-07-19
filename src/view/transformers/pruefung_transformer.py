# Import der benötigten Module und Klassen
from datetime import date
from typing import List
from src.entity.kurs import Kurs
from src.entity.enums import KursStatus
from src.view.models.pruefung_view_model import PruefungViewModel

class PruefungTransformer:
    """
    Transformer für die Konvertierung von Prüfungsdaten in PruefungViewModel.
    """
    
    def transformiere_faellige_pruefungen(self, kurse: List[Kurs], datum: date) -> List[PruefungViewModel]:
        """
        Konvertiert fällige Prüfungen in eine Liste von PruefungViewModel.
        
        Args:
            kurse (List[Kurs]): Die Liste der Kurse.
            datum (date): Das aktuelle Datum.
            
        Returns:
            List[PruefungViewModel]: Die Liste der fälligen Prüfungen.
        """
        return [
            PruefungViewModel(
                name=k.name,
                faellig_seit_tage=-k.faellig_in_tagen(datum),
                faellig_in_tage=None
            )
            for k in kurse if k.get_status(datum) == KursStatus.FAELLIG
        ]
    
    def transformiere_naechste_pruefungen(self, kurse: List[Kurs], datum: date, max_kurse: int = 3) -> List[PruefungViewModel]:
        """
        Konvertiert die nächsten Prüfungen in eine Liste von PruefungViewModel.
        
        Args:
            kurse (List[Kurs]): Die Liste der Kurse.
            datum (date): Das aktuelle Datum.
            max_kurse (int): Die maximale Anzahl der zurückzugebenden Prüfungen.
            
        Returns:
            List[PruefungViewModel]: Die Liste der nächsten Prüfungen.
        """
        return [
            PruefungViewModel(
                name=k.name,
                faellig_seit_tage=None,
                faellig_in_tage=k.faellig_in_tagen(datum)
            )
            for k in kurse if k.get_status(datum) == KursStatus.OFFEN
        ][:max_kurse]
