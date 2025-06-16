# game/emotion.py

import random
from typing import Dict, List

class EmotionEngine:
    """
    Motor emocional simplificado al estilo GAMYGDALA:
    Mantiene niveles de emociones primarias y aplica efectos según
    eventos de entorno y movimientos sociales.
    Emociones: alegría, ira, miedo.
    """
    def __init__(self, actors: List[str]):
        # Inicializa emociones en cero para cada actor
        self.emotions: Dict[str, Dict[str, float]] = {
            actor: {'alegria': 0.0, 'ira': 0.0, 'miedo': 0.0}
            for actor in actors
        }

    def adjust(self, actor: str, emotion: str, amount: float):
        """Ajusta la emoción de un actor en la cantidad dada, con límites [0,1]."""
        if actor not in self.emotions or emotion not in self.emotions[actor]:
            return
        val = self.emotions[actor][emotion] + amount
        # Clamp entre 0.0 y 1.0
        self.emotions[actor][emotion] = max(0.0, min(1.0, val))

    def handle_event(self, actor: str, event: str) -> None:
        """
        Mapea eventos de entorno a cambios emocionales de cada actor.
        Se llama desde EventManager cuando ocurre un evento global.
        """
        e = event.lower()
        if 'tormenta' in e or 'lluvia' in e:
            # Aumenta el miedo ante mal tiempo
            self.adjust(actor, 'miedo', 0.3)
        elif 'niebla' in e:
            # Niebla reduce visibilidad: un poco de miedo
            self.adjust(actor, 'miedo', 0.2)
        elif 'festival' in e:
            # Festival genera alegría
            self.adjust(actor, 'alegria', 0.4)
        # Otros eventos pueden añadirse aquí

    def handle_social_move(self, actor: str, move_name: str) -> None:
        """
        Ajusta emociones según acciones sociales (interacciones NPC-NPC o NPC-jugador).
        """
        m = move_name.lower()
        if m == 'ayudar':
            self.adjust(actor, 'alegria', 0.3)
        elif m == 'insultar':
            self.adjust(actor, 'ira', 0.4)
            self.adjust(actor, 'miedo', 0.1)
        elif m == 'chismear':
            self.adjust(actor, 'ira', 0.2)
        elif m == 'elogiar':
            self.adjust(actor, 'alegria', 0.2)
        # Puedes extender con más movimientos sociales

    def get(self, actor: str, emotion: str) -> float:
        """Devuelve el nivel actual de la emoción para un actor."""
        return self.emotions.get(actor, {}).get(emotion, 0.0)

    def get_emotions(self, actor: str) -> Dict[str, float]:
        """Devuelve todas las emociones actuales de un actor."""
        return dict(self.emotions.get(actor, {}))
