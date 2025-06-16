import openai
from game.engine import GameEngine

def main():
    # Clave de API hardcodeada según lo solicitado
    openai.api_key = "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"

    # Inicializar y ejecutar el motor de juego
    engine = GameEngine(openai.api_key)
    engine.run()

if __name__ == "__main__":
    main()
