from datetime import date
from typing import List

class Kurs:

    def __init__(self,
            id:str,     
            name:str,
            schwere:int,
            ects:int,
            beginn:date|None = None,
            ende:date|None = None
        ):

        assert id != ""
        assert schwere >=1 and schwere <=5

        assert beginn is None or ende is None or beginn < ende

        self.id = id
        self.name = name
        self.schwere = schwere
        self.ects = ects
        self.beginn = beginn
        self.ende = ende
        self.noten = []
        
    def anzahl_tage(self) -> int|None:
        if self.beginn is None or self.ende is None:
            return None
        return (self.ende - self.beginn).days + 1
    
    def faellig_in_tagen(self, datum: date) -> int:
        return (self.ende - datum).days
    
    def ist_fertig(self) -> bool:
        for note in self.noten:
            if note <= 4.0:
                return True
            
        return False
    
    def get_note(self) -> float|None:
        if not self.noten:
            return None
        else:
            return self.noten[-1]
    
    def kann_note_hinzufuegen(self) -> bool:
        return len(self.noten) < 3 and not self.ist_fertig()
    
    def ist_aktiv(self, datum) -> bool:
        return (not self.ist_faellig(datum)) and (not self.ist_fertig()) and self.beginn <= datum and datum <= self.ende

    def ist_faellig(self, datum: date) -> bool:
        return (not self.ist_fertig()) and self.ende < datum

    def set_data(self, name: str, ects: int, schwere:int, noten: List[float]) -> None:
        self.name = name
        self.ects = ects
        self.schwere = schwere
        self.noten = noten

    def __str__(self):
        return f"{self.id}, {self.name}, {self.ects}, {self.schwere}, {self.beginn} - {self.ende}"
