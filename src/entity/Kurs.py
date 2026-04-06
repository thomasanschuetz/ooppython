from datetime import date

class Kurs:

    def __init__(self,
            id:str,     
            name:str,
            semester:int,
            schwere:int,
            ects:int,
            note:float|None=None,
            pruefung_datum:date|None = None,
            beginn:date|None = None,
            ende:date|None = None
        ):

        assert id != ""
        assert schwere >=1 and schwere <=5

        assert beginn is None or ende is None or beginn < ende

        self.id = id
        self.name = name
        self.semester = semester
        self.schwere = schwere
        self.ects = ects
        self.note = note
        self.pruefung_datum = pruefung_datum
        self.beginn = beginn
        self.ende = ende
        
    def anzahl_tage(self) -> int|None:
        if self.beginn is None or self.ende is None:
            return None
        return (self.ende - self.beginn).days + 1
    
    def faellig_in_tagen(self, datum: date) -> int:
        return (self.ende - datum).days

    def set_data(self, schwere:int, note:float|None, pruefung_datum: date|None) -> None:
        self.schwere = schwere
        self.note = note
        self.pruefung_datum = pruefung_datum

    def __str__(self):
        return f"{self.id}, {self.name}, {self.ects}, {self.schwere}, {self.beginn} - {self.ende}"
