import pygame
from senddata import *
from _thread import *
import time

import loginscreen
uid = loginscreen.uid
username = loginscreen.username
token = loginscreen.token


#uid = "1"
#username = "Beached"
#token = '3293853d4a0356f573ce3e870bf055e4707569857f9981f7f78e44ba95688e6e'



connect_server()
#init pygame - required
pygame.init()
#init and set window size
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Shitty Runescape")
icon = pygame.image.load('images//fav.jfif')
pygame.display.set_icon(icon)

#init Pygame clock for framrate in loop
clock = pygame.time.Clock()

class Player():
    def __init__(self,x,y,vel,img,map_id):
        self.x = x
        self.y = y
        self.speed = 50
        self.vel = vel
        self.playerImg = pygame.image.load(img)
        self.map_id = map_id

    def draw(self):
        screen.blit(self.playerImg, (self.x, self.y))
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

#Game loop
running = True
p = Player(loginscreen.x_cord, loginscreen.y_cord,loginscreen.vel,loginscreen.playerImg, loginscreen.map_id)

time1 = time.time()
time2 = time.time()
def update_vel():
    global time1
    global time2
    time1 = time2
    time2 = time.time()
    td = time2 - time1
    p.vel = p.speed * td
    print(p.vel)

def redrawScreen():

    ops=[]
    screen.fill((200,200,200))
    p.draw()
    update_vel()
    p.move()


    response = send_data(uid, username, token, p.x, p.y)
    players = pickle.loads(response)
    for op in players:
        ops.append(Player(op[1], op[2], op[3], op[4], op[5]))
    for i in ops:
        i.draw()

    pygame.display.update()

while running:
    #set framerate
    clock.tick(1000)

    #watch for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_server()
            running = False

    #update surface with everything
    redrawScreen()
