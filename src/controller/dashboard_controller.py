from datetime import date

from src.repo.studium_repository import StudiumRepository
from src.service.studium_planung_service import StudiumPlanungService
from src.entity.studium import Studium
from src.entity.kurs import Kurs
from src.view.studium_view import StudiumView

class DashboardController:

    def __init__(self, planung_service: StudiumPlanungService, repository: StudiumRepository, datum: date):
        self.planung_service = planung_service
        self.repository = repository
        self.datum = datum

    def lade_studium(self) -> Studium:

        #todo remove test code:
        kurse = [Kurs(str(k+1), f"kurs {k+1}", 3, 5) for k in range(15)]
        kurse[0].schwere = 5
        kurse[1].noten = [3.0]
        kurse[12].ects = 10
        kurse[13].ects = 10
        kurse[14].ects = 10
        kurse[12].schwere = 4
        kurse[13].schwere = 4
        kurse[14].schwere = 5

        studium = Studium("KI", date.today(), 39, 2.0, kurse)

        #test code
        #studium = self.repository.lade_studium()

        if studium is None:
            studium = Studium(date.today(), 'Mein Studium', 1.0, 36, [])
        
        self.planung_service.setze_kurs_zeitraeume(studium)

        return studium
    
    def lade_dashboard_view(self):
        studium = self.lade_studium()
        studium_view = StudiumView(
            studium,
            self.planung_service.get_studium_statistik(studium, self.datum),
            self.planung_service.get_semester(studium),
            self.datum
        )

        return studium_view

    def fuege_kurs_hinzu(self, kurs_id: str, name: str, ects: int, schwere: int) -> None:
        """
        Nimmt die Formulardaten aus Flask entgegen, erstellt das Objekt
        und stößt die Kette (Struktur ändern -> Berechnen -> Speichern) an.
        """
        studium = self.repository.lade_studium()
        
        # Neues Domain-Objekt erstellen
        neuer_kurs = Kurs(id=kurs_id, name=name, ects=ects, schwere=schwere)
        
        # A) Struktur-Logik: Entity fügt sich selbst den Kurs hinzu
        studium.kurs_hinzufuegen(neuer_kurs)
        
        # B) Prozess-Logik: Service berechnet die Termine für die neue Liste neu
        self.planung_service.setze_kurs_zeitraeume(studium)
        
        # C) Datenpersistenz: Repository speichert den neuen Zustand
        self.repository.speichere_studium(studium)

    def verschiebe_kurs_nach_oben(self, kurs_id: str) -> None:
        """
        Sorgt dafür, dass ein Kurs in der Reihenfolge eins nach oben rutscht.
        """
        studium = self.repository.lade_studium()
        
        # A) Struktur-Logik: Entity tauscht die Plätze in ihrer verborgenen Liste
        studium.kurs_nach_oben_verschieben(kurs_id)
        
        # B) Prozess-Logik: Service berechnet die Termine für die neue Reihenfolge neu
        self.planung_service.initialisiere_kurs_zeitraeume(studium)
        
        # C) Speichern
        self.repository.speichere_studium(studium)

    def verschiebe_kurs_nach_unten(self, kurs_id: str) -> None:
        """
        Das Gegenstück zum Verschieben nach oben.
        """
        studium = self.repository.lade_studium()
        studium.kurs_nach_unten_verschieben(kurs_id)
        self.planung_service.initialisiere_kurs_zeitraeume(studium)
        self.repository.speichere_studium(studium)

    def fuege_pruefungsleistung_hinzu(self, kurs_id: str, note: float) -> None:
        """
        Fügt einem bestimmten Kurs eine Note hinzu und fängt Business-Rule-Fehler ab.
        """
        studium = self.repository.lade_studium()
        
        # Hilfsmethode der Entity nutzen, um den richtigen Kurs zu greifen
        kurs = studium.finde_kurs_per_id(kurs_id)
        
        if kurs:
            # Die Entity Kurs prüft selbst intern: "Habe ich schon 3 Prüfungen?"
            # Falls ja, wirft sie eine Exception, die bis zu Flask hochfliegt
            kurs.pruefung_hinzufuegen(Pruefungsleistung(note=note))
            
            # Da sich an den Kurs-Zeiträumen nichts ändert, müssen wir hier 
            # den zeitlichen Planungsservice nicht zwingend aufrufen.
            self.repository.speichere_studium(studium)