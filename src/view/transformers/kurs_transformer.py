from datetime import date
from src.entity.kurs import Kurs
from src.entity.enums import KursStatus
from src.view.models.kurs_view_model import KursViewModel
from src.view.transformers.base_transformer import BaseTransformer

class KursTransformer(BaseTransformer):
    """Transformer for Kurs entities to KursViewModel"""
    
    def transform(self, kurs: Kurs, datum: date) -> KursViewModel:
        """Transform a Kurs entity to KursViewModel"""
        status = kurs.get_status(datum)
        
        return KursViewModel(
            id=kurs.id,
            name=kurs.name,
            schwere=str(kurs.schwere),
            ects=str(kurs.ects),
            anzahl_tage=str(kurs.anzahl_tage) if kurs.anzahl_tage else '0',
            hoehe_rel=str(kurs.anzahl_tage) if kurs.anzahl_tage else '0',
            beginn=self.format_date(kurs.beginn),
            ende=self.format_date(kurs.ende),
            ist_fertig=status == KursStatus.FERTIG,
            ist_faellig=status == KursStatus.FAELLIG,
            ist_aktiv=status == KursStatus.AKTIV,
            note=self.formatiere_note(kurs.note),
            noten=[self.formatiere_note(note) for note in kurs.noten],
            zeige_note2=len(kurs.noten) >= 1,
            zeige_note3=len(kurs.noten) >= 2
        )
