import os
import openai
from game.engine import GameEngine

def main():
    # Leer la clave desde la variable de entorno
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise RuntimeError("No se encontró OPENAI_API_KEY en las variables de entorno")

    # Inicializar y ejecutar el motor de juego
    engine = GameEngine(openai.api_key)
    engine.run()

if __name__ == "__main__":
    main()
