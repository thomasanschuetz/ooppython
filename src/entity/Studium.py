from datetime import date
from dateutil.relativedelta import relativedelta
import math
from typing import List, Dict
from src.entity.Kurs import Kurs
from src.entity.Semester import Semester

class Studium:

    def __init__(self, name: str, beginn: date, ziel_monate:int, ziel_note:float, kurse: List[Kurs]):

        assert ziel_monate > 1
        assert ziel_note >= 1.0 and ziel_note <= 6.0

        self.name = name
        self.beginn = beginn
        self.ziel_monate = ziel_monate
        self.ziel_note = ziel_note
        # todo clone kurse: sollten nicht nach aussen geändert werden
        self.kurse : Dict[str, Kurs] = {k.id: k for k in kurse}
        self._setze_kurs_zeitraeume()
        self.semester = self._init_semester()

    def _setze_kurs_zeitraeume(self) -> None:

        kurse = self.kurse.values()

        if not kurse:
            return

        summe_schwere = sum([k.schwere for k in kurse]) # todo ects mitbeachten
        anzahl_tage = (self.ende() - self.beginn).days + 1

        tage_pro_kurs = [round(k.schwere / summe_schwere * anzahl_tage) for k in kurse] # besser: summenerhaltendes runden
        tage_pro_kurs[-1] = anzahl_tage - sum(tage_pro_kurs[:-1])

        assert sum(tage_pro_kurs) == anzahl_tage
        
        referenzdatum = self.beginn
        for idx, k in enumerate(kurse):
            k.beginn = referenzdatum
            k.ende = k.beginn + relativedelta(days=tage_pro_kurs[idx]-1)
            referenzdatum = k.ende + relativedelta(days=1)

    def _init_semester(self) -> List[Semester]:
        all_semester = []
        max_semester = math.ceil(self.ziel_monate / 6)

        referenzdatum = self.beginn
        for s in range(max_semester):
            beginn = referenzdatum
            ende = min(referenzdatum + relativedelta(months=6), self.ende())
            referenzdatum = ende + relativedelta(days=1)
            
            all_semester.append(Semester(
                no=s+1,
                beginn=beginn,
                ende=ende
            ))
                    
        return all_semester

    def ende(self) -> date:
        return self.beginn + relativedelta(months=self.ziel_monate) - relativedelta(days=1)

    def vergangene_tage(self, datum:date) -> int:
        return (datum - self.beginn).days

    def verbleibende_tage(self, datum:date) -> int:
        return self.anzahl_tage() - self.vergangene_tage(datum)

    def anzahl_tage(self) -> int:
        return (self.ende() - self.beginn).days + 1
    
    def anzahl_kurse(self) -> int:
        return len(self.kurse.values())

    def kurse_fertig(self) -> List[Kurs]:
        return [k for k in filter(lambda k: k.note is not None, self.kurse.values())]
    
    def kurse_offen(self) -> List[Kurs]:
        return [k for k in filter(lambda k: k.note is None, self.kurse.values())]
        
    def kurse_soll(self, datum: date) -> List[Kurs]:
        return [k for k in filter(lambda k: k.ende is not None and k.ende < datum, self.kurse_offen())]

    def naechste_pruefungen(self, datum: date, max_kurse:int=3) -> List[Kurs]:    
        return [k for k in filter(lambda k: k.note is None and datum <= k.ende, self.kurse.values())][:max_kurse]
    
    def anzahl_ects(self) -> int:
        return sum([k.ects for k in self.kurse.values()])

    def anzahl_ects_soll(self, datum: date) -> int:
        return sum([k.ects for k in self.kurse_soll(datum)])
    
    def anzahl_ects_fertig(self) -> int:
        return sum([k.ects for k in self.kurse_fertig()])


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
    
    def get_kurse(self) -> List[Kurs]:
        return [k for k in self.kurse.values()]
    
    def set_kurs_data(self, kurs_id:str, schwere:int, note:float|None, pruefung_datum: date|None) -> None:
        kurs = self.kurs(kurs_id)
        if kurs is None:
            return
        
        self.kurs(kurs_id).set_data(schwere, note, pruefung_datum)
        self._init_semester()
    
    def add_kurs(self, kurs_id: str, name: str, ects: int, schwere: int) -> None:
        pass

    def entferne_kurs(self, kurs_id: str) -> None:
        pass

    def __str__(self):
        return self.name + "\n" + "\n".join([f"  {k}" for k in self.kurse])
