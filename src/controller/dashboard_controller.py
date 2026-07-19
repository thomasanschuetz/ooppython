from datetime import date
import uuid
from typing import List

from src.repo.studium_repository import StudiumRepository
from src.service.studium_planung_service import StudiumPlanungService
from src.entity.studium import Studium
from src.entity.kurs import Kurs
from src.view.transformers.studium_transformer import StudiumTransformer
from src.view.models.studium_view_model import StudiumViewModel
from src.view.models.kurs_view_model import KursViewModel


class DashboardController:

    def __init__(self, planung_service: StudiumPlanungService, repository: StudiumRepository, datum: date):
        self.planung_service = planung_service
        self.repository = repository
        self.datum = datum
        self.studium_transformer = StudiumTransformer()

    def lade_studium(self) -> Studium:
        
        studium = self.repository.lade_studium()

        #todo remove test code:
        # from src.entity.enums import KursSchwere
        # kurse = [Kurs(str(k+1), f"kurs {k+1}", 3, KursSchwere.DREI) for k in range(15)]
        # kurse[0].schwere = KursSchwere.FUENF
        # kurse[1].noten = [3.0]
        # kurse[12].ects = 10
        # kurse[13].ects = 10
        # kurse[14].ects = 10
        # kurse[12].schwere = KursSchwere.VIER
        # kurse[13].schwere = KursSchwere.VIER
        # kurse[14].schwere = KursSchwere.FUENF

        # studium = Studium("KI", date.today(), 39, 2.0, kurse)
        #test code


        if studium is None:
            studium = Studium('Mein Studium', date.today(), 1.0, 36, [])
        
        self.planung_service.setze_kurs_zeitraeume(studium)

        return studium
    
    def lade_kurs_view(self, kurs_id: str) -> KursViewModel|None:
        studium_view_model = self.lade_studium_view()
        return next((kurs for kurs in studium_view_model.kurse if kurs.id == kurs_id), None)


    def lade_studium_view(self) -> StudiumViewModel:
        studium = self.lade_studium()
        statistik = self.planung_service.get_studium_statistik(studium, self.datum)
        semester = self.planung_service.get_semester(studium)
        
        studium_view_model = self.studium_transformer.transform(
            studium=studium,
            statistik=statistik,
            semester_list=semester,
            datum=self.datum
        )

        return studium_view_model

    def erstelle_kurs(self, name: str, ects: int, schwere: int) -> None:
        studium = self.lade_studium()
        neuer_kurs = Kurs(id=uuid.uuid4().hex, name=name, ects=ects, schwere=schwere)
        studium.fuege_kurs_hinzu(neuer_kurs)
        self.planung_service.setze_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)

    def aktualisiere_kurs(self, kurs_id: str, name: str, ects: int, schwere: int, noten: List[float]) -> None:
        studium = self.lade_studium()
        neuer_kurs = Kurs(id=kurs_id, name=name, ects=ects, schwere=schwere, noten=noten)
        studium.aktualisiere_kurs(neuer_kurs)
        self.planung_service.setze_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)

    def verschiebe_kurs(self, kurs_id: str, hoch: bool) -> None:
        
        studium = self.lade_studium()
        studium.verschiebe_kurs(kurs_id, hoch)
        self.planung_service.setze_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)
