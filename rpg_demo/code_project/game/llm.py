# game/llm.py
from game.data import DIALOGUE_TREES

class LLMClient:
    """
    Fallback offline: usa los árboles de diálogo definidos en data.DIALOGUE_TREES.
    """
    def __init__(self):
        pass

    def start_conversation(self, npc_name):
        """
        Devuelve (saludo, opciones:list[str]) para el árbol del NPC.
        """
        tree = DIALOGUE_TREES.get(npc_name)
        if not tree:
            return "…", ["Adiós."]
        greeting = tree.get("greeting", "Hola.")
        options  = [opt["text"] for opt in tree.get("options", [])]
        return greeting, options

    def reply(self, npc_name, option_index):
        """
        Devuelve la respuesta asociada al índice seleccionado.
        """
        tree = DIALOGUE_TREES.get(npc_name)
        if not tree:
            return "…"
        opts = tree.get("options", [])
        if option_index < 0 or option_index >= len(opts):
            return "…"
        return opts[option_index].get("response", "…")
