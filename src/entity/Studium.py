from dataclasses import dataclass, field
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List, Iterator
from src.entity.kurs import Kurs
from src.entity.enums import KursSchwere


@dataclass
class Studium:
    """
    Klasse zur Darstellung eines Studiums.
    
    Attribute:
        name (str): Der Name des Studiums.
        beginn (date): Der Beginn des Studiums.
        ziel_note (float): Die angestrebte Durchschnittsnote.
        ziel_monate (int): Die angestrebte Dauer des Studiums in Monaten.
        _kurse (List[Kurs]): Die Liste der Kurse des Studiums.
    """
    name: str
    beginn: date
    ziel_note: float
    ziel_monate: int
    _kurse: List[Kurs] = field(default_factory=list)


    @property
    def ende(self) -> date:
        """
        Berechnet das Ende des Studiums.
        
        Returns:
            date: Das Ende des Studiums.
        """
        return self.beginn + relativedelta(months=self.ziel_monate) - relativedelta(days=1)


    @property
    def anzahl_tage(self) -> int:
        """
        Berechnet die Anzahl der Tage des Studiums.
        
        Returns:
            int: Die Anzahl der Tage.
        """
        return (self.ende - self.beginn).days + 1

    @property
    def kurse(self) -> Iterator[Kurs]:
        """
        Gibt einen Iterator über die Kurse des Studiums zurück.
        
        Returns:
            Iterator[Kurs]: Ein Iterator über die Kurse.
        """
        return self._kurse


    @property
    def anzahl_kurse(self) -> int:
        """
        Gibt die Anzahl der Kurse des Studiums zurück.
        
        Returns:
            int: Die Anzahl der Kurse.
        """
        return len(self._kurse)

    def vergangene_tage(self, datum:date) -> int:
        """
        Berechnet die Anzahl der vergangenen Tage seit Beginn des Studiums.
        
        Args:
            datum (date): Das aktuelle Datum.
            
        Returns:
            int: Die Anzahl der vergangenen Tage.
        """
        return (datum - self.beginn).days


    def verbleibende_tage(self, datum:date) -> int:
        """
        Berechnet die Anzahl der verbleibenden Tage bis zum Ende des Studiums.
        
        Args:
            datum (date): Das aktuelle Datum.
            
        Returns:
            int: Die Anzahl der verbleibenden Tage.
        """
        return self.anzahl_tage - self.vergangene_tage(datum)


    def fuege_kurs_hinzu(self, kurs_id: str, name: str, ects: int, schwere: KursSchwere, noten: list = None, beginn: date | None = None, ende: date | None = None) -> None:
        """
        Fügt einen Kurs zum Studium hinzu.
        
        Args:
            kurs_id (str): Die ID des Kurses.
            name (str): Der Name des Kurses.
            ects (int): Die ECTS-Punkte des Kurses.
            schwere (KursSchwere): Die Schwierigkeit des Kurses.
            noten (list): Die Noten des Kurses.
            beginn (date | None): Der Beginn des Kurses.
            ende (date | None): Das Ende des Kurses.
        """
        neuer_kurs = Kurs(id=kurs_id, name=name, ects=ects, schwere=schwere, noten=noten or [], beginn=beginn, ende=ende)
        self._kurse.append(neuer_kurs)


    def aktualisiere_kurs(self, kurs_id: str, name: str, ects: int, schwere: KursSchwere, noten: list = None, beginn: date | None = None, ende: date | None = None) -> None:
        """
        Aktualisiert einen bestehenden Kurs.
        
        Args:
            kurs_id (str): Die ID des zu aktualisierenden Kurses.
            name (str): Der neue Name des Kurses.
            ects (int): Die neuen ECTS-Punkte des Kurses.
            schwere (KursSchwere): Die neue Schwierigkeit des Kurses.
            noten (list): Die neuen Noten des Kurses.
            beginn (date | None): Der neue Beginn des Kurses.
            ende (date | None): Das neue Ende des Kurses.
            
        Raises:
            ValueError: Wenn der Kurs nicht gefunden wird.
        """
        idx = self._kurs_idx(kurs_id)
        if idx is None:
            raise ValueError(f"Kurs mit id {kurs_id} nicht gefunden.")
        
        aktualisierter_kurs = Kurs(id=kurs_id, name=name, ects=ects, schwere=schwere, noten=noten or [], beginn=beginn, ende=ende)
        self._kurse[idx] = aktualisierter_kurs

    
    def verschiebe_kurs(self, kurs_id: str, hoch: bool) -> None:
        """
        Verschiebt einen Kurs in der Reihenfolge.
        
        Args:
            kurs_id (str): Die ID des zu verschiebenden Kurses.
            hoch (bool): True, wenn der Kurs nach oben verschoben werden soll, False für nach unten.
        """
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
        """
        Findet den Index eines Kurses anhand seiner ID.
        
        Args:
            kurs_id (str): Die ID des Kurses.
            
        Returns:
            int | None: Der Index des Kurses oder None, falls der Kurs nicht gefunden wurde.
        """
        return next((i for i, kurs in enumerate(self._kurse) if kurs.id == kurs_id), None)


    def __str__(self):
        """
        Gibt eine String-Darstellung des Studiums zurück.
        
        Returns:
            str: Die String-Darstellung des Studiums.
        """
        return self.name + "\n" + "\n".join([f"  {k}" for k in self._kurse])
