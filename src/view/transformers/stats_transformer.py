from src.entity.studium_statistik import StudiumStatistik
from src.view.models.stats_view_model import StatsViewModel

class StatsTransformer:
    """
    Transformer für die Konvertierung von Statistikdaten in StatsViewModel.
    """
    def transformiere(self, statistik: StudiumStatistik) -> StatsViewModel:
        """
        Konvertiert Statistikdaten in ein StatsViewModel.
        
        Args:
            statistik (StudiumStatistik): Die zu konvertierenden Statistikdaten.
            
        Returns:
            StatsViewModel: Das konvertierte StatsViewModel.
        """
        anzahl_kurse_soll = statistik.anzahl_kurse_soll
        anzahl_kurse_ist = statistik.anzahl_kurse_ist
        anzahl_ects_soll = statistik.anzahl_ects_soll
        anzahl_ects_ist = statistik.anzahl_ects_ist
        
        return StatsViewModel(
            anzahl_kurse=statistik.anzahl_kurse,
            anzahl_ects=statistik.anzahl_ects,
            anzahl_kurse_soll=anzahl_kurse_soll,
            anzahl_ects_soll=anzahl_ects_soll,
            kurse_ist={
                'anzahl': anzahl_kurse_ist,
                'ok': anzahl_kurse_ist >= anzahl_kurse_soll
            },
            ects_ist={
                'anzahl': anzahl_ects_ist,
                'ok': anzahl_ects_ist >= anzahl_ects_soll
            }
        )
