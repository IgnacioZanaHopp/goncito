import os
import pygame
import pygame_menu
from pygame.math import Vector2
from game.db import init_db, save_npc_memory, load_npc_memory
from game.emotion import EmotionEngine
from game.events import EventManager
from game.conversation import ConversationManager

class GameEngine:
    # Estados del juego
    MENU, WHOAMI, NAME_INPUT, CHAR_SELECT, LORE, PLAYING, CHAT = (
        "MENU", "WHOAMI", "NAME_INPUT", "CHAR_SELECT", "LORE", "PLAYING", "CHAT"
    )

    def __init__(self, openai_api_key: str):
        pygame.init()
        init_db()
        pygame.display.set_caption("Mini RPG Narrativo")
        self.W, self.H = 720, 480
        self.screen = pygame.display.set_mode((self.W, self.H))

        # Directorio base y assets
        base = os.path.dirname(os.path.dirname(__file__))
        assets = os.path.join(base, "assets")

        # Fondo de menú
        menu_bg_path = os.path.join(assets, "menu", "background.png")
        raw_menu_bg = pygame.image.load(menu_bg_path).convert()
        self.menu_bg = pygame.transform.scale(raw_menu_bg, (self.W, self.H))

        # Fondo de mapa para PLAYING
        map_bg_path = os.path.join(assets, "maps", "fondo_pueblo.png")
        raw_map_bg = pygame.image.load(map_bg_path).convert()
        self.map_bg = pygame.transform.scale(raw_map_bg, (self.W, self.H))

        # Fuentes
        fonts_dir = os.path.join(assets, "fonts")
        font_path = os.path.join(fonts_dir, "CinzelDecorative-Regular.ttf")
        self.font_text  = pygame.font.Font(font_path, 24)
        self.font_small = pygame.font.Font(font_path, 20)

        # Jugador y chat
        self.openai_api_key = openai_api_key
        self.player_name = ""
        self.player_class = ""
        self.player_pos = Vector2(self.W/2, self.H/2)
        self.chat_history = []
        self.chat_input = ""
        self.current_npc = None

        # NPCs
        self.npcs = [
            {"name": "Carlos", "pos": Vector2(200, 200)},
            {"name": "Lina",   "pos": Vector2(400, 300)},
            {"name": "Eldar",  "pos": Vector2(600, 250)},
        ]
        names = [n["name"] for n in self.npcs]

        # Motores
        self.emotion_manager = EmotionEngine(names)
        self.event_manager   = EventManager([], self.emotion_manager, save_npc_memory, self._on_event)
        self.conv_manager    = ConversationManager(names, self.openai_api_key)

        # Estado inicial
        self.state = self.MENU

        # Tema de pygame_menu
        theme = pygame_menu.themes.Theme(
            background_color=(0,0,0,0), title=False,
            widget_font=font_path, widget_font_size=32,
            widget_font_color=(255,255,255),
            widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(),
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            widget_margin=(10,10), widget_background_color=(0,0,0,160)
        )

        # Menú principal
        self.main_menu = pygame_menu.Menu(width=self.W, height=self.H, theme=theme, title='')
        self.main_menu.add.button('JUGAR',        self._set_state, self.NAME_INPUT)
        self.main_menu.add.button('¿QUIÉN SOY?',  self._set_state, self.WHOAMI)
        self.main_menu.add.button('SALIR',        pygame_menu.events.EXIT)

        # Ingreso de nombre
        self.name_menu = pygame_menu.Menu(width=self.W, height=self.H, theme=theme, title='')
        self.name_menu.add.text_input('Nombre: ', textinput_id='player_name', default='', input_underline='_')
        self.name_menu.add.button('Aceptar', self._accept_name)
        self.name_menu.add.button('Volver',  self._set_state, self.MENU)

        # Selección de clase
        self.char_menu = pygame_menu.Menu(width=self.W, height=self.H, theme=theme, title='')
        for cls in ('Guerrero','Mago','Pícaro'):
            self.char_menu.add.button(cls, self._accept_class, cls)
        self.char_menu.add.button('Volver', self._set_state, self.NAME_INPUT)

        # Prólogo
        self.lore_menu = pygame_menu.Menu(width=self.W, height=self.H, theme=theme, title='')
        story = [
            "Hace siglos, un gran imperio cayó en ruinas.",
            "Solo valientes aventureros exploran sus secretos."
        ]
        for line in story:
            self.lore_menu.add.label(line, align=pygame_menu.locals.ALIGN_CENTER, font_size=24)
        self.lore_menu.add.button('Continuar', self._start_adventure)

        # Quién soy
        self.whoami_menu = pygame_menu.Menu(width=self.W, height=self.H, theme=theme, title='')
        self.whoami_menu.add.label(lambda: f"Jugador: {self.player_name}", align=pygame_menu.locals.ALIGN_CENTER, font_size=24)
        self.whoami_menu.add.button('Volver', self._set_state, self.MENU)

    def _on_event(self, event):
        pass

    def _set_state(self, state):
        self.state = state

    def _accept_name(self):
        w = self.name_menu.get_widget('player_name')
        self.player_name = w.get_value().strip() or 'Anónimo'
        self.state = self.CHAR_SELECT

    def _accept_class(self, cls):
        self.player_class = cls
        self.state = self.LORE

    def _start_adventure(self):
        self.state = self.PLAYING

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60)/1000.0
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    running = False
                if self.state == self.PLAYING and e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:    self.player_pos.y -= 200*dt
                    if e.key == pygame.K_DOWN:  self.player_pos.y += 200*dt
                    if e.key == pygame.K_LEFT:  self.player_pos.x -= 200*dt
                    if e.key == pygame.K_RIGHT: self.player_pos.x += 200*dt
                    if e.key == pygame.K_SPACE:
                        for npc in self.npcs:
                            if self.player_pos.distance_to(npc['pos']) < 50:
                                self.current_npc = npc['name']
                                self.chat_history.clear()
                                self.chat_input = ''
                                self.state = self.CHAT
                if self.state == self.CHAT and e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.chat_input = self.chat_input[:-1]
                    elif e.key == pygame.K_RETURN:
                        msg = self.chat_input.strip()
                        if msg:
                            self.chat_history.append(('Tú', msg))
                            reply = self.conv_manager.get_dialogue(self.current_npc, self.player_name, msg)
                            self.chat_history.append((self.current_npc, reply))
                        self.chat_input = ''
                    elif e.unicode.isprintable():
                        self.chat_input += e.unicode
                    if e.key == pygame.K_ESCAPE:
                        self.state = self.PLAYING

            if self.state == self.MENU or self.state == self.NAME_INPUT or self.state == self.CHAR_SELECT or self.state == self.LORE or self.state == self.WHOAMI:
                self._draw_menu(events)
            elif self.state == self.PLAYING:
                self._show_playing()
            elif self.state == self.CHAT:
                self._show_chat()

            pygame.display.flip()
        pygame.quit()

    def _draw_menu(self, events):
        self.screen.blit(self.menu_bg, (0,0))
        if self.state == self.MENU:
            self.main_menu.update(events);    self.main_menu.draw(self.screen)
        elif self.state == self.NAME_INPUT:
            self.name_menu.update(events);    self.name_menu.draw(self.screen)
        elif self.state == self.CHAR_SELECT:
            self.char_menu.update(events);    self.char_menu.draw(self.screen)
        elif self.state == self.LORE:
            self.lore_menu.update(events);    self.lore_menu.draw(self.screen)
        elif self.state == self.WHOAMI:
            self.whoami_menu.update(events);  self.whoami_menu.draw(self.screen)

    def _show_playing(self):
        # Dibujar mapa de fondo
        self.screen.blit(self.map_bg, (0,0))
        # Dibujar NPCs
        for npc in self.npcs:
            pos = (int(npc['pos'].x), int(npc['pos'].y))
            pygame.draw.circle(self.screen, (200,50,50), pos, 20)
            label = self.font_small.render(npc['name'], True, (255,255,255))
            self.screen.blit(label, (pos[0]-label.get_width()//2, pos[1]-30))
        # Dibujar jugador
        ppos = (int(self.player_pos.x), int(self.player_pos.y))
        pygame.draw.circle(self.screen, (50,150,200), ppos, 15)

    def _show_chat(self):
        self.screen.fill((30,30,30))
        y = 20
        for speaker,msg in self.chat_history[-10:]:
            surf = self.font_text.render(f"{speaker}: {msg}", True, (255,255,255))
            self.screen.blit(surf, (20, y)); y += surf.get_height() + 5
        ibox = pygame.Rect(20, self.H-40, self.W-40, 30)
        pygame.draw.rect(self.screen, (70,70,70), ibox)
        inp = self.font_small.render(self.chat_input+"_", True, (255,255,255))
        self.screen.blit(inp, (ibox.x+5, ibox.y+5))
