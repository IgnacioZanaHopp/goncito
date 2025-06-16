import os
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def safe_load_image(subpath: str, colorkey=None):
    full_path = os.path.join(ASSETS_DIR, subpath)
    img = pygame.image.load(full_path).convert_alpha()
    if colorkey is not None:
        img.set_colorkey(colorkey)
    return img


def load_font(name: str, size: int):
    full_path = os.path.join(ASSETS_DIR, "fonts", name)
    return pygame.font.Font(full_path, size)