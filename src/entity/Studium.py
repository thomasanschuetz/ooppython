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


    def fuege_kurs_hinzu(self, kurs: Kurs) -> None:
        self._kurse.append(kurs)

    def aktualisiere_kurs(self, kurs: Kurs) -> None:
        idx = self._kurs_idx(kurs.id)
        if idx is None:
            raise ValueError(f"Kurs mit id {kurs.id} nicht gefunden.")
        
        self._kurse[idx] = Kurs

    
    def verschiebe_kurs(self, kurs_id: str, hoch: bool) -> None:

        idx = self._kurs_idx(kurs_id)

        if idx == None:
            return None
        
        if hoch:
            if idx == 0:
                return
            self._kurse[idx-1], self._kurse[idx] = self._kurse[idx], self._kurse[idx-1]
        else:
            if idx == (len(self._kurse) - 1):
                return
            self._kurse[idx+1], self._kurse[idx] = self._kurse[idx], self._kurse[idx+1]

    def _kurs_idx(self, kurs_id: str) -> int|None:
        return next((i for i, kurs in enumerate(self._kurse) if kurs.id == kurs_id), None)

    def __str__(self):
        return self.name + "\n" + "\n".join([f"  {k}" for k in self._kurse])
