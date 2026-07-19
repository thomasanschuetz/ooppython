from datetime import date
from typing import List
from src.entity.kurs import Kurs
from src.entity.enums import KursStatus
from src.view.models.pruefung_view_model import PruefungViewModel

class PruefungTransformer:
    
    def transformiere_faellige_pruefungen(self, kurse: List[Kurs], datum: date) -> List[PruefungViewModel]:
        return [
            PruefungViewModel(
                name=k.name,
                faellig_seit_tage=-k.faellig_in_tagen(datum),
                faellig_in_tage=None
            )
            for k in kurse if k.get_status(datum) == KursStatus.FAELLIG
        ]
    
    def transformiere_naechste_pruefungen(self, kurse: List[Kurs], datum: date, max_kurse: int = 3) -> List[PruefungViewModel]:
        return [
            PruefungViewModel(
                name=k.name,
                faellig_seit_tage=None,
                faellig_in_tage=k.faellig_in_tagen(datum)
            )
            for k in kurse if k.get_status(datum) == KursStatus.OFFEN
        ][:max_kurse]
