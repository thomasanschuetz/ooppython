from datetime import date
from dateutil.relativedelta import relativedelta
import math
import copy
import uuid
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
        self.kurse : Dict[str, Kurs] = {k.id: copy.deepcopy(k) for k in kurse}
        self._setze_kurs_zeitraeume()
        self.semester = self._init_semester()



    def set_name(self, name: str) -> None:
        #todo validation
        self.name = name

    def set_beginn(self, beginn: date) -> None:
        #todo validation
        self.beginn = beginn

    def set_ziel_note(self, note: float) -> None:
        #todo validation
        self.ziel_note = note

    def set_ziel_monate(self, monate: int) -> None:
        #todo validation
        self.monate = monate

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
        return [k for k in filter(lambda k: k.ist_fertig(), self.kurse.values())]
    
    def kurse_offen(self) -> List[Kurs]:
        return [k for k in filter(lambda k: not k.ist_fertig(), self.kurse.values())]
        
    def kurse_soll(self, datum: date) -> List[Kurs]:
        return [k for k in filter(lambda k: k.ende is not None and k.ende < datum, self.kurse_offen())]

    def naechste_pruefungen(self, datum: date, max_kurse:int=3) -> List[Kurs]:    
        return [k for k in filter(lambda k: not k.ist_fertig() and datum <= k.ende, self.kurse.values())][:max_kurse]
    
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
        
        return sum([k.get_note() for k in kurse_fertig]) / len(kurse_fertig)
    
    def benoetigte_durchschnittsnote(self) -> float|None: # todo ects beachten

        anzahl_kurse = self.anzahl_kurse()
        anzahl_kurse_offen = len(self.kurse_offen())
        if self.anzahl_kurse() == 0 or anzahl_kurse_offen == 0:
            return None

        return (self.ziel_note * anzahl_kurse - sum([k.get_note() for k in self.kurse_fertig()])) / len(self.kurse_offen())

    def kurs(self, kurs_id:str) -> Kurs|None:
        return self.kurse.get(kurs_id)
    
    def get_kurse(self) -> List[Kurs]:
        return [k for k in self.kurse.values()]
    
    def bewege_kurs(self, kurs_id: str, hoch: bool) -> None:
        kurs_ids = list(self.kurse.keys())
        
        if not kurs_id in kurs_ids:
            return
        
        idx = kurs_ids.index(kurs_id)

        if hoch:
            if idx == 0:
                return
            kurs_ids[idx-1], kurs_ids[idx] = kurs_ids[idx], kurs_ids[idx-1]
        else:
            if idx == (len(kurs_ids) - 1):
                return
            kurs_ids[idx+1], kurs_ids[idx] = kurs_ids[idx], kurs_ids[idx+1]
        
        self.kurse = {key: self.kurse[key] for key in kurs_ids}

    def set_kurs_data(self, kurs_id:str, name: str, ects: int, schwere:int, noten:List[float]) -> None:
        kurs = self.kurs(kurs_id)
        if kurs is None:
            raise ValueError(f"wrong kurs_id: {kurs_id}")
        
        self.kurs(kurs_id).set_data(name, ects, schwere, noten)
        self._init_semester()
    
    def add_kurs(self, name: str, ects: int, schwere: int) -> None:
        id = uuid.uuid4().hex
        self.kurse[id] = Kurs(id, name, schwere, ects)
        self._setze_kurs_zeitraeume()

    def entferne_kurs(self, kurs_id: str) -> None:
        pass

    def __str__(self):
        return self.name + "\n" + "\n".join([f"  {k}" for k in self.kurse])
