from dataclasses import dataclass, field
from datetime import date
from src.entity.enums import KursSchwere, KursStatus

@dataclass
class Kurs:
    id: str
    name: str = ''
    ects: int = 5
    schwere: KursSchwere = KursSchwere.DREI
    noten: list = field(default_factory=list)
    beginn: date|None = None
    ende: date|None = None


    def get_status(self, datum: date) -> KursStatus:
        if self.beginn is None or self.ende is None:
            return KursStatus.UNGEPLANT
        
        elif self.ist_fertig():
            return KursStatus.FERTIG
        
        elif self.ist_faellig(datum):
            return KursStatus.FAELLIG

        elif self.ist_aktiv(datum): # muss nach ist_faellig bleiben, da faellig -> aktiv impliziert
            return KursStatus.AKTIV
        
        else:
            return KursStatus.OFFEN
     

    @property
    def anzahl_tage(self) -> int|None:
        if not self._hat_start_und_ende():
            return None
        
        return (self.ende - self.beginn).days + 1
    

    def faellig_in_tagen(self, datum: date) -> int:
        if not self._hat_start_und_ende(): 
            return 0
        
        return (self.ende - datum).days
    
    def kann_note_hinzufuegen(self) -> bool:
        return len(self.noten) < 3 and not self.ist_fertig()
    

    def ist_fertig(self) -> bool:
        """concept: Auch über den Status bestimmbar, aber dafür benötige ich das Datum, das ist manchmal nicht nötig"""
        for note in self.noten:
            if note <= 4.0:
                return True

    @property        
    def note(self) -> None|float:
        if not self.noten:
            return None
        
        return self.noten[-1]
        

    def _hat_start_und_ende(self) -> bool:
        return not(self.beginn is None or self.ende is None)


    def ist_aktiv(self, datum: date) -> bool:
        if not self._hat_start_und_ende():
            return False
        return (not self.ist_faellig(datum)) and (not self.ist_fertig()) and self.beginn <= datum and datum <= self.ende


    def ist_faellig(self, datum: date) -> bool:
        if not self._hat_start_und_ende():
            return False
        return (not self.ist_fertig()) and self.ende < datum