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

    
    def setze_kurs_zeitraeume(self, studium: Studium) -> None:

        kurse = studium.kurse

        if not kurse:
            return

        summe_schwere = sum([k.schwere for k in kurse]) # todo ects mitbeachten
        
        tage_pro_kurs = [round(k.schwere / summe_schwere * studium.anzahl_tage) for k in kurse] # besser: summenerhaltendes runden
        tage_pro_kurs[-1] = studium.anzahl_tage - sum(tage_pro_kurs[:-1])

        assert sum(tage_pro_kurs) == studium.anzahl_tage
        
        referenzdatum = studium.beginn
        for idx, k in enumerate(kurse):
            k.beginn = referenzdatum
            k.ende = k.beginn + relativedelta(days=tage_pro_kurs[idx]-1)
            referenzdatum = k.ende + relativedelta(days=1)
            
    
    def get_semester(self, studium: Studium) -> List[Semester]:
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
        return [k for k in filter(lambda k: k.ist_fertig(), studium.kurse)]


    def kurse_offen(self, studium: Studium, datum: date) -> List[Kurs]:
        return [k for k in filter(lambda k: k.get_status(datum) == KursStatus.OFFEN, studium.kurse)]


    def kurse_soll(self, studium: Studium, datum: date) -> List[Kurs]:
        return [k for k in filter(lambda k: k.get_status(datum) in [KursStatus.FERTIG, KursStatus.FAELLIG], studium.kurse)]


    def naechste_pruefungen(self, studium: Studium, datum: date, max_kurse:int=3) -> List[Kurs]:    
        return [k for k in filter(lambda k: k.get_status(datum) == KursStatus.AKTIV, studium.kurse)][:max_kurse]


    def anzahl_ects(self, studium: Studium) -> int:
        return sum([k.ects for k in studium.kurse])


    def anzahl_ects_soll(self, studium: Studium, datum: date) -> int:
        return sum([k.ects for k in self.kurse_soll(studium, datum)])


    def anzahl_ects_fertig(self, studium: Studium) -> int:
        return sum([k.ects for k in studium.kurse if k.ist_fertig()])


    def durchschnittsnote(self, studium: Studium) -> float|None: # todo ects beachten
        kurse_fertig = [k for k in self.kurse_fertig(studium)]
        if not kurse_fertig:
            return None
        
        return sum([k.note for k in kurse_fertig]) / len(kurse_fertig)
    

    def benoetigte_durchschnittsnote(self, studium: Studium) -> float|None: # todo ects beachten

        anzahl_kurse = studium.anzahl_kurse
        anzahl_kurse_fertig = len([k for k in self.kurse_fertig(studium)])
        anzahl_kurse_offen = anzahl_kurse - anzahl_kurse_fertig
        if anzahl_kurse == 0 or anzahl_kurse_offen == 0:
            return None

        return (studium.ziel_note * anzahl_kurse - sum([k.note for k in self.kurse_fertig(studium)])) / anzahl_kurse_offen