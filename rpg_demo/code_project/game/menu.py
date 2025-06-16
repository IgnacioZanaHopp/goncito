import pygame
import os
import sys

# ─── Rutas base ──────────────────────────────────────────────────────────────
# BASE_DIR = carpeta "code_project"
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FONTS_DIR  = os.path.join(ASSETS_DIR, 'fonts')
MENU_DIR   = os.path.join(ASSETS_DIR, 'menu')

class Menu:
    def __init__(self):
        # Inicializa Pygame (por si aún no se hizo)
        if not pygame.get_init():
            pygame.init()

        # Ventana principal (toma la existente si ya está creada)
        if pygame.display.get_surface() is None:
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Mi RPG Demo")
        else:
            self.screen = pygame.display.get_surface()

        self.screen_width, self.screen_height = self.screen.get_size()

        # ─── Fuentes ──────────────────────────────────────────────────────────
        self.title_font  = pygame.font.Font(
            os.path.join(FONTS_DIR, 'The Amazing Spider-Man.ttf'), 72
        )
        self.option_font = pygame.font.Font(
            os.path.join(FONTS_DIR, 'CinzelDecorative-Regular.ttf'), 48
        )

        # ─── Imagen del botón ────────────────────────────────────────────────
        self.button_img = pygame.image.load(
            os.path.join(MENU_DIR, 'button.png')
        ).convert_alpha()

        # Opciones
        self.options = ["INICIAR", "QUIÉN SOY"]
        self.buttons = []  # (Rect, texto)

        # Colores
        self.bg_color    = (0,   0,   0)
        self.title_color = (255, 215, 0)
        self.text_color  = (255, 255, 255)

        self.clock = pygame.time.Clock()

    # ──────────────────────────────────────────────────────────────────────────
    # Métodos de dibujo y loop
    # ──────────────────────────────────────────────────────────────────────────
    def _draw(self):
        self.screen.fill(self.bg_color)
        self.buttons.clear()

        # Título
        title_surf = self.title_font.render("MI RPG DEMO", True, self.title_color)
        title_rect = title_surf.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_surf, title_rect)

        # Botones
        for idx, text in enumerate(self.options):
            btn_x = (self.screen_width - self.button_img.get_width()) // 2
            btn_y = 250 + idx * (self.button_img.get_height() + 20)
            btn_rect = pygame.Rect(btn_x, btn_y,
                                   self.button_img.get_width(),
                                   self.button_img.get_height())

            # Fondo
            self.screen.blit(self.button_img, btn_rect)

            # Texto
            txt_surf = self.option_font.render(text, True, self.text_color)
            txt_rect = txt_surf.get_rect(center=btn_rect.center)
            self.screen.blit(txt_surf, txt_rect)

            self.buttons.append((btn_rect, text))

        pygame.display.flip()

    def run(self):
        """
        Muestra el menú hasta que el usuario haga click en una opción.
        Devuelve el texto de la opción seleccionada.
        """
        running = True
        selected = None

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    pos = pygame.mouse.get_pos()
                    for rect, text in self.buttons:
                        if rect.collidepoint(pos):
                            selected = text
                            running = False
                            break

            self._draw()
            self.clock.tick(60)

        return selected
