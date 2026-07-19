from src.view.models.noten_view_model import NotenViewModel
from src.view.transformers.base_transformer import BaseTransformer

class NotenTransformer(BaseTransformer):
    def transform(self, ziel_note: float, durchnitt_note: float | None, 
                 benoetigt_note: float | None) -> NotenViewModel:
        if durchnitt_note is None:
            return NotenViewModel(
                ziel=self.formatiere_note(ziel_note),
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
            ziel=self.formatiere_note(ziel_note),
            aktuell={
                'note': self.formatiere_note(durchnitt_note),
                'ok': durchnitt_note <= ziel_note
            },
            benoetigt={
                'note': self.formatiere_note(benoetigt_note) if benoetigt_note else 'n.a.',
                'ok': benoetigt_note >= ziel_note if benoetigt_note else True
            }
        )
