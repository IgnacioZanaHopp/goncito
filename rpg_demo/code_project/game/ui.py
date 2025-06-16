import pygame
from game.data import WIDTH, HEIGHT, CLASSES


def character_selection(screen):
    """
    Muestra un menú para seleccionar la clase del jugador.
    Retorna el diccionario con los datos de la clase seleccionada.
    """
    pygame.font.init()
    title_font = pygame.font.SysFont("Arial", 32)
    option_font = pygame.font.SysFont("Arial", 24)
    options = list(CLASSES.keys())
    selected = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        # Título
        title_surf = title_font.render("Selecciona tu clase", True, (255, 255, 255))
        screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, 80))

        # Opciones
        for idx, key in enumerate(options):
            cls = CLASSES[key]
            text = f"{cls['name']}: {cls['description']}"
            surf = option_font.render(text, True, (255, 255, 255))
            x = 100
            y = 180 + idx * 60
            if idx == selected:
                rect = pygame.Rect(x - 10, y - 5, surf.get_width() + 20, surf.get_height() + 10)
                pygame.draw.rect(screen, (70, 70, 160), rect)
            screen.blit(surf, (x, y))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_t):
                    return CLASSES[options[selected]]


class UI:
    @staticmethod
    def draw_text(screen, text, pos, font_size=18, color=(255, 255, 255)):
        font = pygame.font.SysFont("Arial", font_size)
        surf = font.render(text, True, color)
        screen.blit(surf, pos)

    @staticmethod
    def draw_menu(screen, greeting, options, selected_index):
        """
        Dibuja un cuadro de diálogo con saludo y opciones seleccionables.
        """
        line_h = 30
        box_w = WIDTH - 40
        box_h = line_h * (len(options) + 1) + 20
        y0 = HEIGHT - box_h - 20

        # Fondo semitransparente
        box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box.fill((0, 0, 0, 200))
        screen.blit(box, (20, y0))

        # Saludo
        font = pygame.font.SysFont("Arial", 20)
        surf = font.render(greeting, True, (255, 255, 255))
        screen.blit(surf, (30, y0 + 10))

        # Opciones
        opt_font = pygame.font.SysFont("Arial", 18)
        for i, opt in enumerate(options):
            prefix = '→ ' if i == selected_index else '   '
            surf = opt_font.render(prefix + opt, True, (255, 255, 255))
            screen.blit(surf, (30, y0 + 10 + line_h * (i + 1)))
