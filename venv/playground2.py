import pygame

vec = pygame.math.Vector2

class Text_box:
    def __init__(self,x,y,w,h, bg_color=(255,200,200), active_color=(255,255,255)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pos = vec(x,y)
        self.size = vec(w,h)
        self.image = pygame.Surface((w,h))
        self.bg_color = bg_color
        self.active_color = active_color
        self.active = False

    def draw(self, window):
        print(self.active)
        if not self.active:
            self.image.fill(self.bg_color)
        else:
            self.image.fill(self.active_color)

        window.blit(self.image, (self.pos))

    def check_click(self, pos):
        if pos[0] > self.x and pos[0] < self.x+self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                print("works")
                self.active = True
