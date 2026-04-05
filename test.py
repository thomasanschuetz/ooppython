from typing import List, Dict
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import math
import pickle



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
        
    def set_data(self, schwere:int, note:float|None, pruefung_datum: date|None) -> None:
        self.schwere = schwere
        self.note = note
        self.pruefung_datum = pruefung_datum

    def __str__(self):
        return f"{self.id}, {self.name}, {self.ects}, {self.schwere}, {self.beginn} - {self.ende}"
    
class Semester:
    def __init__(self, no:int, beginn:date, ende:date, kurse:Dict[str, Kurs]):
        self.no = no
        self.beginn = beginn
        self.ende = ende
        self._setze_zeitraeume(kurse)
        self.kurse = kurse
    
    def _setze_zeitraeume(self, kurse: Dict[str, Kurs]) -> None:

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
        
    def kurs(self, kurs_id:str) -> Kurs|None:
        return self.kurse.get(kurs_id)

    def __str__(self):
        return f"Semester {self.no} {self.beginn} - {self.ende}" + "\n" + "\n".join([f"    {k}" for k in self.kurse])

class Studium:
    def __init__(self, name: str, beginn: date, ziel_semester:int, ziel_note:float, kurse: List[Kurs]):

        assert ziel_semester > 1
        assert ziel_note >= 1.0 and ziel_note <= 6.0

        self.name = name
        self.beginn = beginn
        self.ziel_semester = ziel_semester
        self.ziel_note = ziel_note
        # todo clone kurse: sollten nicht nach aussen geändert werden
        self.kurse = {k.id: k for k in sorted(kurse, key=lambda k: k.semester)} # stabil https://docs.python.org/3.11/howto/sorting.html
        self.semester = self._init_semester() # aktualisiert auch beginn und ende in self.kurse

    def _init_semester(self)->List[Semester]:
        kurse = self.kurse.values()
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

    def anzahl_kurse(self) -> int:
        return len(self.kurse.values())

    def kurse_fertig(self) -> List[Kurs]:
        return [k for k in filter(lambda k: k.note is not None, self.kurse.values())]
    
    def kurse_offen(self) -> List[Kurs]:
        return [k for k in filter(lambda k: k.note is None, self.kurse.values())]
    

    def durchschnittsnote(self) -> float|None: # todo ects beachten
        kurse_fertig = self.kurse_fertig()
        if not kurse_fertig:
            return None
        
        return sum([k.note for k in kurse_fertig]) / len(kurse_fertig)
    
    def benoetigte_durchschnittsnote(self) -> float|None: # todo ects beachten

        anzahl_kurse = self.anzahl_kurse()
        anzahl_kurse_offen = len(self.kurse_offen())
        if self.anzahl_kurse() == 0 or anzahl_kurse_offen == 0:
            return None

        return (self.ziel_note * anzahl_kurse - sum([k.note for k in self.kurse_fertig()])) / len(self.kurse_offen())

    def kurs(self, kurs_id:str) -> Kurs|None:
        return self.kurse.get(kurs_id)

    def faellige_pruefungen(self, datum:date, max_anzahl:int=3) -> List[Kurs]:
        return [k for k in self.kurse_offen() if k.ende is not None and k.ende < datum][:max_anzahl]
    
    def naechste_regulaere_pruefungen(self, datum:date, max_anzahl:int=3) -> List[Kurs]:
        return [k for k in self.kurse_offen() if k.ende is not None and k.ende >= datum][:max_anzahl]

    def set_kurs_data(self, kurs_id:str, schwere:int, note:float|None, pruefung_datum: date|None) -> None:
        kurs = self.kurs(kurs_id)
        if kurs is None:
            return
        
        self.kurs(kurs_id).set_data(schwere, note, pruefung_datum)
        self._init_semester()

    def __str__(self):
        return self.name + "\n" + "\n".join([f"  {s}" for s in self.semester])


kurse = [Kurs(str(k+1), f"kurs {k+1}", k//6 + 1, 3, 5) for k in range(32)]
kurse[28].ects = 10
kurse[29].semester = 6
kurse[29].ects = 10
kurse[30].ects = 10
kurse[31].ects = 10
studium = Studium("KI", date.today(), 6, 2.0, kurse)

print(studium)
print(f"Durchschnittsnote:{studium.durchschnittsnote()}")


print(f"Zielnote: {studium.ziel_note}, Durchschnittsnote:{studium.durchschnittsnote()}, benötigt:{studium.benoetigte_durchschnittsnote()}")
studium.set_kurs_data('1', 3, 2.0, None)
studium.set_kurs_data('7', 3, 3.0, None)
print(f"Zielnote: {studium.ziel_note}, Durchschnittsnote:{studium.durchschnittsnote()}, benötigt:{studium.benoetigte_durchschnittsnote()}")

datum = date(2026, 7, 4)

print(f"fällige Prüfungen zum {datum}:\n{"\n".join(map(str, studium.faellige_pruefungen(datum, 3)))}")
print(f"nächste reguläre Prüfungen zum {datum}:\n{"\n".join(map(str, studium.naechste_regulaere_pruefungen(datum, 3)))}")


# über semester iterieren
 # über kurse iterieren
  # fertig, todo, überfällig

# für semester
 # start, end von kurs

# über alles
 # durchschnitt
 # im verzug
 # nächste prüfungen


