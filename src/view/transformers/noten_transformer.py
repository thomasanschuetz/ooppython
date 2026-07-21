from src.view.models.noten_view_model import NotenViewModel
from src.view.transformers.formatierer import Formatierer

class NotenTransformer():
    """
    Transformer für die Konvertierung von Notendaten in NotenViewModel.
    """

    def __init__(self, formatierer: Formatierer):
        self.formatierer = formatierer


    def transformiere(self, ziel_note: float, durchnitt_note: float | None, 
                 benoetigt_note: float | None) -> NotenViewModel:
        """
        Konvertiert Notendaten in ein NotenViewModel.
        
        Args:
            ziel_note (float): Die angestrebte Durchschnittsnote.
            durchnitt_note (float | None): Die aktuelle Durchschnittsnote.
            benoetigt_note (float | None): Die benötigte Durchschnittsnote.
            
        Returns:
            NotenViewModel: Das konvertierte NotenViewModel.
        """
        if durchnitt_note is None:
            return NotenViewModel(
                ziel=self.formatierer.formatiere_note(ziel_note),
                aktuell={
                    'note': 'n.a.',
                    'ok': True
                },
                benoetigt={
                    'note': 'n.a.',
                    'ok': True
                }
            )
        
        return NotenViewModel(
            ziel=self.formatierer.formatiere_note(ziel_note),
            aktuell={
                'note': self.formatierer.formatiere_note(durchnitt_note),
                'ok': durchnitt_note <= ziel_note
            },
            benoetigt={
                'note': self.formatierer.formatiere_note(benoetigt_note) if benoetigt_note else 'n.a.',
                'ok': benoetigt_note >= ziel_note if benoetigt_note else True
            }
        )
