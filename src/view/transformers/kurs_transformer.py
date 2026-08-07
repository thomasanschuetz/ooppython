from datetime import date
from src.entity.kurs import Kurs
from src.entity.enums import KursStatus
from src.view.models.kurs_view_model import KursViewModel
from src.view.transformers.formatierer import Formatierer


class KursTransformer():
    """
    Transformer für die Konvertierung von Kurs-Entitäten in KursViewModel.
    """

    def __init__(self, formatierer: Formatierer):
        self.formatierer = formatierer
    
    def transformiere(self, kurs: Kurs, datum: date) -> KursViewModel:
        """
        Konvertiert eine Kurs-Entität in ein KursViewModel.
        
        Args:
            kurs (Kurs): Die zu konvertierende Kurs-Entität.
            datum (date): Das aktuelle Datum.
            
        Returns:
            KursViewModel: Das konvertierte KursViewModel.
        """
        status = kurs.berechne_status(datum)
        
        return KursViewModel(
            id=kurs.id,
            name=kurs.name,
            schwere=str(kurs.schwere),
            ects=str(kurs.ects),
            anzahl_tage=str(kurs.anzahl_tage) if kurs.anzahl_tage else '0',
            hoehe_rel=str(kurs.anzahl_tage) if kurs.anzahl_tage else '0',
            beginn=self.formatierer.formatiere_datum(kurs.beginn),
            ende=self.formatierer.formatiere_datum(kurs.ende),
            ist_fertig=status == KursStatus.FERTIG,
            ist_faellig=status == KursStatus.FAELLIG,
            ist_aktiv=status == KursStatus.AKTIV,
            note=self.formatierer.formatiere_note(kurs.note),
            noten=kurs.noten,
            zeige_note2=self._zeige_note(2, kurs),
            zeige_note3=self._zeige_note(3, kurs)
        )
    

    def _zeige_note(self, x:int, kurs: Kurs) -> bool:
        """
        Prüft, ob eine bestimmte Note angezeigt werden soll.
        
        Args:
            x (int): Die Nummer der Note (2 oder 3).
            kurs (Kurs): Der Kurs, dessen Noten geprüft werden sollen.
            
        Returns:
            bool: True, wenn die Note angezeigt werden soll, False sonst.
        """
        return (len(kurs.noten) == x-1 and kurs.kann_note_hinzufuegen()) or (len(kurs.noten) >= x)
