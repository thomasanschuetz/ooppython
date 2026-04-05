from typing import List
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import math
import pickle

class Kurs:
    def __init__(self, 
            name:str,
            semester:int,
            schwere:int,
            ects:int,
            note:float|None=None,
            pruefung_datum:date|None = None,
            beginn:date|None = None,
            ende:date|None = None
        ):

        assert schwere >=1 and schwere <=5

        assert beginn is None or ende is None or beginn < ende

        self.name = name
        self.semester = semester
        self.schwere = schwere
        self.ects = ects
        self.note = note
        self.pruefung_datum = pruefung_datum
        self.beginn = beginn
        self.ende = ende
        
    
    def __str__(self):
        return f"{self.name}, {self.ects}, {self.schwere}, {self.beginn} - {self.ende}"
    
class Semester:
    def __init__(self, no:int, beginn:date, ende:date, kurse:List[Kurs]):
        self.no = no
        self.beginn = beginn
        self.ende = ende
        self.kurse = self._bestimme_zeitraeume(kurse)
    
    def _bestimme_zeitraeume(self, kurse: List[Kurs]) -> List[Kurs]:

        if not kurse:
            return kurse

        summe_schwere = sum([k.schwere for k in kurse])
        anzahl_tage = (self.ende - self.beginn).days + 1

        tage_pro_kurs = [round(k.schwere / summe_schwere * anzahl_tage) for k in kurse] # besser: summenerhaltendes runden
        tage_pro_kurs[-1] = anzahl_tage - sum(tage_pro_kurs[:-1])

        assert sum(tage_pro_kurs) == anzahl_tage
        
        referenzdatum = self.beginn
        for idx, k in enumerate(kurse):
            k.beginn = referenzdatum
            k.ende = k.beginn + timedelta(days=tage_pro_kurs[idx]-1)
            referenzdatum = k.ende + timedelta(days=1)

        return kurse

        

    def __str__(self):
        return f"Semester {self.no} {self.beginn} - {self.ende}" + "\n" + "\n".join([f"    {k}" for k in self.kurse])

class Studium:
    def __init__(self, name: str, beginn: date, kurse: List[Kurs]):
        self.name = name
        self.beginn = beginn
        sorted(kurse, key=lambda k: k.semester) # stabil https://docs.python.org/3.11/howto/sorting.html
        self.semester = self._create_semester(kurse)

    def _create_semester(self, kurse:List[Kurs])->List[Semester]:
        all_semester = []
        max_semester = max(kurse, key=lambda k: k.semester).semester

        for s in range(max_semester):
            beginn = self.beginn + relativedelta(months=6*s)
            ende = beginn + relativedelta(months=6) - relativedelta(days=1)
            all_semester.append(Semester(
                no=s+1,
                beginn=beginn,
                ende=ende,
                kurse=[k for k in filter(lambda k: k.semester == s+1, kurse)]
            ))
        
            
        return all_semester

    def anzahl_kurse_soll(self, datum:date) -> int:
        # brauche fälligkeit von kurse
        self.beginn

    

    def __str__(self):
        return self.name + "\n" + "\n".join([f"  {s}" for s in self.semester])


kurse = [Kurs(f"kurs {k+1}", k//6 + 1, 3, 5) for k in range(32)]
kurse[28].ects = 10
kurse[29].semester = 6
kurse[29].ects = 10
kurse[30].ects = 10
kurse[31].ects = 10
studium = Studium("KI", date.today(), kurse)

print(studium)

# über semester iterieren
 # über kurse iterieren
  # fertig, todo, überfällig

# für semester
 # start, end von kurs

# über alles
 # durchschnitt
 # im verzug
 # nächste prüfungen
