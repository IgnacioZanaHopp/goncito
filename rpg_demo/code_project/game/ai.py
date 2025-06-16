from pygame.math import Vector2
import random

class NPCBehavior:
    """
    Patrullaje y reacción básica de NPC.
    """
    def __init__(self, start_pos, path_mask):
        self.pos = Vector2(start_pos)
        self.mask = path_mask
        self.speed = 2

    def step(self):
        # Movimiento aleatorio sencillo sobre la máscara
        dirs = [Vector2(1,0), Vector2(-1,0), Vector2(0,1), Vector2(0,-1)]
        move = random.choice(dirs) * self.speed
        new = self.pos + move
        x, y = int(new.x), int(new.y)
        if 0 <= x < self.mask.get_width() and 0 <= y < self.mask.get_height():
            if self.mask.get_at((x,y))[0] > 0:
                self.pos = new
        return self.pos