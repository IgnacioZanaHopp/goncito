# game/events.py

import random
from game.emotion import EmotionEngine
from game.db import save_npc_memory

class EventManager:
    """
    Gestiona eventos globales. Cada cierto tiempo dispara un evento
    aleatorio, notifica al EmotionEngine, guarda en BD y avisa al GameEngine.
    """

    def __init__(
        self,
        event_list: list[tuple[str,str]],
        emotion_engine: EmotionEngine,
        save_memory_fn,
        on_event_callback,
        interval: float = 15.0,
        history_size: int = 5
    ):
        self.event_list = event_list
        self.emotion_engine = emotion_engine
        self.save_memory = save_memory_fn
        self.on_event = on_event_callback
        self.interval = interval
        self.history_size = history_size
        self.env_timer = 0.0
        self.recent_events: list[tuple[str,str]] = []

    def update(self, dt: float = 1.0):
        self.env_timer += dt
        if self.env_timer >= self.interval:
            self._trigger_event()

    def _trigger_event(self):
        evento, desc = random.choice(self.event_list)

        # Notificar motor emocional para cada NPC
        for npc_name in self.emotion_engine.emotions.keys():
            self.emotion_engine.handle_event(npc_name, evento)

        # Formatear mensaje y notificar al juego
        mensaje = f"[EVENTO] {evento} → {desc}"
        self.on_event(mensaje)

        # Guardar en memoria de cada NPC
        for npc_name in self.emotion_engine.emotions.keys():
            self.save_memory(npc_name, mensaje)

        # Mantener historial interno
        self.recent_events.append((evento, desc))
        if len(self.recent_events) > self.history_size:
            self.recent_events.pop(0)

        # Resetear timer
        self.env_timer = 0.0
