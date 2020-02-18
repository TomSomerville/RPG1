import pygame
from senddata import *
from _thread import *
import time

import loginscreen
uid = loginscreen.uid
username = loginscreen.username
token = loginscreen.token
authdata = uid,username,token
auth = pickle.dumps(authdata)
map_change = True


connect_server()
#init pygame - required
pygame.init()
#init and set window size
screen = pygame.display.set_mode((800, 608))

#Title and Icon
pygame.display.set_caption("Shitty Runescape")
icon = pygame.image.load('images//fav.jfif')
pygame.display.set_icon(icon)

#init Pygame clock for framrate in loop
clock = pygame.time.Clock()
time1 = time.time()
time2 = time.time()
def update_vel():
    global time1
    global time2
    time1 = time2
    time2 = time.time()
    td = time2 - time1
    p.vel = p.speed * td
    #print(p.vel)

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
        self.hitrect = pygame.Rect(self.x,self.y,self.w,self.h)

    def draw(self):
        screen.blit(self.playerImg, (self.x, self.y))

        self.hitbox()
    def move(self):
        update_vel()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.check_col(self.hitrect)
            self.y -= self.vel

            send_cords = "update_coordinates", p.x, p.y
            send_data(auth, pickle.dumps(send_cords))
        if keys[pygame.K_s]:
            self.y += self.vel
            send_cords = "update_coordinates", p.x, p.y
            send_data(auth, pickle.dumps(send_cords))
        if keys[pygame.K_a]:
            self.x -= self.vel
            send_cords = "update_coordinates", p.x, p.y
            send_data(auth, pickle.dumps(send_cords))
        if keys[pygame.K_d]:
            self.x += self.vel
            send_cords = "update_coordinates", p.x, p.y
            send_data(auth, pickle.dumps(send_cords))
        self.hitrect = (self.x, self.y, self.w, self.h)

    def hitbox(self):
        pygame.draw.rect(screen,(255,0,0),self.hitrect,1)

class Map_Objects():
    def __init__(self, x, y, img,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.image.load(img)
        self.pos = x * 16,y * 16

    def draw(self):
        screen.blit(self.img, self.pos)
        self.hitbox()
    def hitbox(self):
        pygame.draw.rect(screen,(255,0,0),(self.x*16,self.y*16,self.w,self.h),1)

#Game loop
running = True
p = Player(loginscreen.x_cord, loginscreen.y_cord,loginscreen.vel,loginscreen.playerImg, loginscreen.map_id)

def other_players():
    get_players = "get_players", p.map_id
    other_players = send_data(auth, pickle.dumps(get_players))
    o_players = pickle.loads(other_players)
    for op in o_players:
        Player(op[1], op[2], op[3], op[4], op[5]).draw()

def draw_grid():
    for x in range(0,800,16):
        pygame.draw.line(screen, (0,0,0), (x,0),(x,608))
    for y in range(0,608,16):
        pygame.draw.line(screen, (0,0,0),(0,y), (800,y))

map_data = []
map_objects = []

def get_map_data(map_id):
    global map_data
    global map_change
    map_data = []
    senddata = "get_map_data", p.map_id
    response = send_data(auth, pickle.dumps(senddata))
    unpickled_data = (pickle.loads(response))
    map_data = unpickled_data[:]
    map_change = False
    for o in map_data:
        map_objects.append(Map_Objects(o[2],o[3],o[1],o[4],o[5]))

def draw_map():
    for o in map_objects:
        o.draw()

def redrawScreen():
    global map_change
    screen.fill((200,200,200))
    draw_grid()
    if map_change == True:
        get_map_data(p.map_id)
    draw_map()
    p.draw()
    p.move()
    other_players()

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
