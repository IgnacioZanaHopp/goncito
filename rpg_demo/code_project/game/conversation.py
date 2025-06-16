# game/conversation.py

import openai
from game.db import load_npc_memory, save_npc_memory

class ConversationManager:
    def __init__(self, api_key: str, memory_limit: int = 100):
        openai.api_key = api_key
        self.memory_limit = memory_limit

    def get_dialogue(
        self,
        npc_name: str,
        player_name: str,
        player_message: str = None
    ) -> str:
        """
        Devuelve la respuesta del NPC usando GPT-3.5-turbo,
        basándose en la memoria histórica (por jugador y NPC).
        """
        # 1) Cargo toda la historia
        history = load_npc_memory(npc_name, player_name)
        # tomo solo las últimas memory_limit entradas
        recent = history[-self.memory_limit:]

        # 2) Preparo prompt
        system_prompt = (
            f"Tú eres **{npc_name}**. Recuerda estas líneas de tu memoria:\n"
            + "\n".join(f"- {m}" for m in recent)
        )
        messages = [{"role": "system", "content": system_prompt}]
        if player_message:
            messages.append({"role": "user", "content": player_message})

        # 3) Llamo a la API
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = resp.choices[0].message.content.strip()
        except Exception:
            reply = "Lo siento, no puedo responder ahora mismo."

        # 4) Guardo en memoria (jugador y NPC)
        if player_message:
            save_npc_memory(npc_name, player_name, f"Jugador: {player_message}")
        save_npc_memory(npc_name, player_name, f"{npc_name}: {reply}")

        return reply

# alias para compatibilidad
ConversationManager.send_message = ConversationManager.get_dialogue
