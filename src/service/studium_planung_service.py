from datetime import date
from dateutil.relativedelta import relativedelta
import math
from typing import List

from src.entity.studium import Studium
from src.entity.studium import Kurs
from src.entity.semester import Semester
from src.entity.enums import KursStatus
from src.entity.studium_statistik import StudiumStatistik


class StudiumPlanungService:
    """
    Service für die Planung und Statistik eines Studiums.
    
    Diese Klasse bietet Methoden zur Berechnung von Kurszeiträumen, Semestern und Statistiken.
    """
    
    def setze_kurs_zeitraeume(self, studium: Studium) -> None:
        """
        Setzt die Zeiträume für die Kurse eines Studiums.
        
        Args:
            studium (Studium): Das Studium, dessen Kurszeiträume gesetzt werden sollen.
        """
        kurse = studium.kurse

        if not kurse:
            return

        summe_schwere = sum([k.schwere for k in kurse])
        
        tage_pro_kurs = [round(k.schwere / summe_schwere * studium.anzahl_tage) for k in kurse]
        tage_pro_kurs[-1] = studium.anzahl_tage - sum(tage_pro_kurs[:-1])

        assert sum(tage_pro_kurs) == studium.anzahl_tage
        
        referenzdatum = studium.beginn
        for idx, k in enumerate(kurse):
            k.beginn = referenzdatum
            k.ende = k.beginn + relativedelta(days=tage_pro_kurs[idx]-1)
            referenzdatum = k.ende + relativedelta(days=1)
            
    
    def get_semester(self, studium: Studium) -> List[Semester]:
        """
        Berechnet die Semester eines Studiums.
        
        Args:
            studium (Studium): Das Studium, dessen Semester berechnet werden sollen.
            
        Returns:
            List[Semester]: Die Liste der Semester.
        """
        all_semester = []
        max_semester = math.ceil(studium.ziel_monate / 6)

        referenzdatum = studium.beginn
        for s in range(max_semester):
            beginn = referenzdatum
            ende = min(referenzdatum + relativedelta(months=6), studium.ende)
            referenzdatum = ende + relativedelta(days=1)
            
            all_semester.append(Semester(
                no=s+1,
                beginn=beginn,
                ende=ende
            ))
                    
        return all_semester


    def get_studium_statistik(self, studium: Studium, datum: date) -> StudiumStatistik:
        """
        Berechnet die Statistiken eines Studiums.
        
        Args:
            studium (Studium): Das Studium, dessen Statistiken berechnet werden sollen.
            datum (date): Das aktuelle Datum.
            
        Returns:
            StudiumStatistik: Die Statistiken des Studiums.
        """
        return StudiumStatistik(
            anzahl_kurse = studium.anzahl_kurse,
            anzahl_kurse_soll = len(self.kurse_soll(studium, datum)),
            anzahl_kurse_ist = len(self.kurse_fertig(studium)),
            anzahl_ects = self.anzahl_ects(studium),
            anzahl_ects_soll = self.anzahl_ects_soll(studium, datum),
            anzahl_ects_ist = self.anzahl_ects_fertig(studium),
            durchnitt_note = self.durchschnittsnote(studium),
            benoetigt_note = self.benoetigte_durchschnittsnote(studium)
        )


    def kurse_fertig(self, studium: Studium) -> List[Kurs]:
        """
        Gibt eine Liste der abgeschlossenen Kurse zurück.
        
        Args:
            studium (Studium): Das Studium, dessen abgeschlossene Kurse zurückgegeben werden sollen.
            
        Returns:
            List[Kurs]: Die Liste der abgeschlossenen Kurse.
        """
        return [k for k in filter(lambda k: k.ist_fertig, studium.kurse)]


    def kurse_offen(self, studium: Studium, datum: date) -> List[Kurs]:
        """
        Gibt eine Liste der offenen Kurse zurück.
        
        Args:
            studium (Studium): Das Studium, dessen offene Kurse zurückgegeben werden sollen.
            datum (date): Das aktuelle Datum.
            
        Returns:
            List[Kurs]: Die Liste der offenen Kurse.
        """
        return [k for k in filter(lambda k: k.berechne_status(datum) == KursStatus.OFFEN, studium.kurse)]


    def kurse_soll(self, studium: Studium, datum: date) -> List[Kurs]:
        """
        Gibt eine Liste der Kurse zurück, die bis zum aktuellen Datum abgeschlossen sein sollten.
        
        Args:
            studium (Studium): Das Studium, dessen Kurse zurückgegeben werden sollen.
            datum (date): Das aktuelle Datum.
            
        Returns:
            List[Kurs]: Die Liste der Kurse, die bis zum aktuellen Datum abgeschlossen sein sollten.
        """
        return [k for k in filter(lambda k: k.berechne_status(datum) in [KursStatus.FERTIG, KursStatus.FAELLIG], studium.kurse)]


    def naechste_pruefungen(self, studium: Studium, datum: date, max_kurse:int=3) -> List[Kurs]:    
        """
        Gibt eine Liste der nächsten Prüfungen zurück.
        
        Args:
            studium (Studium): Das Studium, dessen nächste Prüfungen zurückgegeben werden sollen.
            datum (date): Das aktuelle Datum.
            max_kurse (int): Die maximale Anzahl der zurückzugebenden Kurse.
            
        Returns:
            List[Kurs]: Die Liste der nächsten Prüfungen.
        """
        return [k for k in filter(lambda k: k.berechne_status(datum) == KursStatus.AKTIV, studium.kurse)][:max_kurse]


    def anzahl_ects(self, studium: Studium) -> int:
        """
        Berechnet die Gesamtanzahl der ECTS-Punkte eines Studiums.
        
        Args:
            studium (Studium): Das Studium, dessen ECTS-Punkte berechnet werden sollen.
            
        Returns:
            int: Die Gesamtanzahl der ECTS-Punkte.
        """
        return sum([k.ects for k in studium.kurse])


    def anzahl_ects_soll(self, studium: Studium, datum: date) -> int:
        """
        Berechnet die Anzahl der ECTS-Punkte, die bis zum aktuellen Datum erreicht sein sollten.
        
        Args:
            studium (Studium): Das Studium, dessen ECTS-Punkte berechnet werden sollen.
            datum (date): Das aktuelle Datum.
            
        Returns:
            int: Die Anzahl der ECTS-Punkte, die bis zum aktuellen Datum erreicht sein sollten.
        """
        return sum([k.ects for k in self.kurse_soll(studium, datum)])


    def anzahl_ects_fertig(self, studium: Studium) -> int:
        """
        Berechnet die Anzahl der ECTS-Punkte der abgeschlossenen Kurse.
        
        Args:
            studium (Studium): Das Studium, dessen ECTS-Punkte berechnet werden sollen.
            
        Returns:
            int: Die Anzahl der ECTS-Punkte der abgeschlossenen Kurse.
        """
        return sum([k.ects for k in studium.kurse if k.ist_fertig])


    def durchschnittsnote(self, studium: Studium) -> float|None: # todo ects beachten
        """
        Berechnet die durchschnittliche Note der abgeschlossenen Kurse.
        
        Args:
            studium (Studium): Das Studium, dessen Durchschnittsnote berechnet werden soll.
            
        Returns:
            float | None: Die durchschnittliche Note oder None, falls keine abgeschlossenen Kurse vorhanden sind.
        """
        kurse_fertig = [k for k in self.kurse_fertig(studium)]
        if not kurse_fertig:
            return None
        
        return sum([k.note for k in kurse_fertig]) / len(kurse_fertig)
    

    def benoetigte_durchschnittsnote(self, studium: Studium) -> float|None:
        """
        Berechnet die benötigte Durchschnittsnote für die offenen Kurse, um das Ziel zu erreichen.
        
        Args:
            studium (Studium): Das Studium, dessen benötigte Durchschnittsnote berechnet werden soll.
            
        Returns:
            float | None: Die benötigte Durchschnittsnote oder None, falls keine offenen Kurse vorhanden sind.
        """
        anzahl_kurse = studium.anzahl_kurse
        anzahl_kurse_fertig = len([k for k in self.kurse_fertig(studium)])
        anzahl_kurse_offen = anzahl_kurse - anzahl_kurse_fertig
        if anzahl_kurse == 0 or anzahl_kurse_offen == 0:
            return None

        return (studium.ziel_note * anzahl_kurse - sum([k.note for k in self.kurse_fertig(studium)])) / anzahl_kurse_offen