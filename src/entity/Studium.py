from dataclasses import dataclass, field
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List, Iterator

from src.entity.kurs import Kurs

@dataclass
class Studium:
    name: str
    beginn: date
    ziel_note: float
    ziel_monate: int
    _kurse: List[Kurs] = field(default_factory=list)

    @property
    def ende(self) -> date:
        return self.beginn + relativedelta(months=self.ziel_monate) - relativedelta(days=1)

    @property
    def anzahl_tage(self) -> int:
        return (self.ende - self.beginn).days + 1

    @property
    def kurse(self) -> Iterator[Kurs]:
        for kurs in self._kurse:
            yield kurs
    
    @property
    def anzahl_kurse(self) -> int:
        return len(self._kurse)

    def vergangene_tage(self, datum:date) -> int:
        return (datum - self.beginn).days


    def verbleibende_tage(self, datum:date) -> int:
        return self.anzahl_tage - self.vergangene_tage(datum)


    def add_kurs(self, kurs: Kurs) -> None:
        self._kurse.append(kurs)

    
    def bewege_kurs(self, kurs_id: str, hoch: bool) -> None:
        kurs_ids = list(self._kurse.keys())
        
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
        
        self._kurse = {key: self._kurse[key] for key in kurs_ids}

    def __str__(self):
        return self.name + "\n" + "\n".join([f"  {k}" for k in self._kurse])
