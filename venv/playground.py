import pygame

pygame.init()
screen = pygame.display.set_mode((800, 608))
pygame.display.set_caption("Shitty Runescape")
icon = pygame.image.load('images//fav.jfif')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()


class Player():
    def __init__(self,x,y,vel,img,map_id):
        self.x = x
        self.y = y
        self.speed = 50
        self.vel = vel
        self.playerImg = pygame.image.load(img)
        self.map_id = map_id
        self.pos = x,y
        self.w = self.playerImg.get_rect().size[0]
        self.h = self.playerImg.get_rect().size[1]
        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

    def draw(self):
        screen.blit(self.playerImg, (self.x, self.y))
        self.hitbox()


    def move2(self):
        keys = pygame.key.get_pressed()

        #if keys[pygame.K_w]:
        #    self.y -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel
        if keys[pygame.K_w] and not (self.rect.colliderect(mo) == True and self.rect.top <= mo.rect.bottom and self.rect.midtop >= mo.rect.left):
            self.y -= self.vel


        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)

        #if p.rect.top <= mo.rect.bottom and mo.rect.left <= p.rect.left <= mo.rect.right:
        #    print("top > Bottom and in between")
        #    print(p.rect.top)


    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel
        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel

        self.rect = pygame.Rect(self.x,self.y,self.w,self.h)
        # send_cords = "update_coordinates", p.x, p.y
        # send_data(auth, pickle.dumps(send_cords))

    def hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.rect,1)

class Map_Objects():
    def __init__(self, x, y, img,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.image.load(img)
        self.pos = x * 16,y * 16
        self.rect = pygame.Rect(self.x*16, self.y*16, self.w, self.h)

    def draw(self):
        screen.blit(self.img, self.pos)
        self.hitbox()
    def hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.rect,1)


running = True
p = Player(100, 100,.2,"images//hero.png", 1)
mo = Map_Objects(5,5,"images//square.png", 16,16)

def draw_grid():
    for x in range(0,800,16):
        pygame.draw.line(screen, (0,0,0), (x,0),(x,608))
    for y in range(0,608,16):
        pygame.draw.line(screen, (0,0,0),(0,y), (800,y))

def redrawScreen():
    screen.fill((200,200,200))
    draw_grid()
    p.draw()
    p.move2()
    mo.draw()
    pygame.display.update()

while running:
    #set framerate
    clock.tick(1000)
    #watch for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update surface with everything
    redrawScreen()