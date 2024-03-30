import sys
from typing import Any
from pygame import *
from random import randint
mixer.init()
FPS = 60
WIDTH, HEIGHT = 700, 525
window = display.set_mode((WIDTH, HEIGHT))
mixer.music.load('model\music\Forest.ogg')
mixer.music.play()
mixer.music.set_volume(1)
count = 0
attaks = []
mobs = []
sprites = sprite.Group()
reload = 1
attak_deffens = 1

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)
    
    def draw(self):
        window.blit(self.image, self.rect)
map_X='0'
map_Y='0'
class Player(GameSprite):
    def __init__(self, sprite_img, x, y, width, height,hp,xp,xp_for_nextLVL,LVL,damage):
        super().__init__(sprite_img, x, y, width, height)
        self.hp = hp
        self.xp = xp
        self.damage = damage
        self.xp_for_nextLVL = xp_for_nextLVL
        self.LVL = LVL
    def update(self):
        pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if pressed[K_w]:
            self.rect.y -= 3

        if pressed[K_s]:
            self.rect.y += 3

        if pressed[K_a]:
            self.rect.x -= 3

        if pressed[K_d]:
            self.rect.x += 3
        at = True
        global reload
        if reload == 1:
            if pressed[K_UP] and at:
                attak=Attak('model\wepon\effect\icicle_up.png',self.rect.x,self.rect.y,32,32,'up',self.damage)
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_DOWN] and at:
                attak=Attak('model\wepon\effect\icicle_down.png',self.rect.x,self.rect.y,32,32,'down',self.damage)
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_RIGHT] and at:
                attak=Attak('model\wepon\effect\icicle_right.png',self.rect.x,self.rect.y,32,32,'right',self.damage)
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_LEFT] and at:
                attak=Attak('model\wepon\effect\icicle_left.png',self.rect.x,self.rect.y,32,32,'left',self.damage)
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_x]:
                self.xp = int(self.xp)
                self.xp = self.xp + 1
                self.xp = str(self.xp)
        for a in attaks:
            for mob in mobs:    
                if a.rect.x < -5 or a.rect.x > WIDTH or a.rect.y > HEIGHT or a.rect.y < 0:
                    attaks.remove(a)
                    sprites.remove(a)
                if sprite.collide_rect(a,mob):
                    attaks.remove(a)
                    sprites.remove(a)
                    mob.hp -= self.damage
        for a in mobs:
            if a.hp <=0 :
                mobs.remove(a)
                sprites.remove(a)
                self.xp = int(self.xp)
                self.xp = self.xp + a.xp
                self.xp = str(self.xp)
        if self.xp >= self.xp_for_nextLVL:
            self.xp = int(self.xp)
            self.xp = 0
            self.xp = str(self.xp)
            self.xp_for_nextLVL = int(self.xp_for_nextLVL)
            self.xp_for_nextLVL += 2
            self.xp_for_nextLVL = str(self.xp_for_nextLVL)
            self.damage += 1
            print(self.damage)
            self.LVL = int(self.LVL)
            self.LVL += 1
            self.LVL = str(self.LVL)

        for w in walss:
            if sprite.collide_rect(player, w):
                self.rect.x, self.rect.y = old_pos

class Mob(GameSprite):
    def __init__(self, sprite_img, x, y, width, height,hp,damage,xp,status):
        super().__init__(sprite_img, x, y, width, height)
        self.hp = hp
        self.xp = xp
        self.damage = damage
        self.status = status
        mobs.append(self)
    def update(self):
        if player.rect.x >= self.rect.x:
            self.rect.x += 2
        if player.rect.x <= self.rect.x:
            self.rect.x -=2
        if player.rect.y >= self.rect.y:
            self.rect.y +=2
        if player.rect.y <= self.rect.y:
            self.rect.y -=2
        global attak_deffens
        if attak_deffens == 1:
            if sprite.collide_rect (player, self):
                player.hp -=1
                attak_deffens = 30
                print (player.hp)
                print(attak_deffens)
class Grass(GameSprite):
    def __init__(self, x , y,view):
        super().__init__('model\map\grass_1_new.png', x, y, 35, 35)
        self.view = view
        if view == "Winter":
            self.image=transform.scale(image.load("model\map\cobble_blood_2_old.png"), (35,35))

class Attak(GameSprite):
    def __init__(self, sprite_img, x, y, width, height,move,damage):
        super().__init__(sprite_img, x, y, width, height)
        self.move= move
        self.damage = damage
    def update(self):
        if self.move == 'up':
            self.rect.y -=10
        if self.move == 'down':
            self.rect.y+=10
        if self.move == 'left':
            self.rect.x -=10
        if self.move == 'right':
            self.rect.x +=10


bg = transform.scale(image.load("model\map\grass_1_new.png"), (WIDTH, HEIGHT))
player = Player('model\player\centaur_brown_female.png', 350 , 300, 30, 30,5,"0","5","1",1)

grass = []
objects = []
walss = []

map_txt='map\map_x'+ map_X +'_y' + map_Y +'.txt'
with open(map_txt, 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for line in map:
        for symbol in line:
            grass.append(Grass(x, y,""),)
            if symbol == '1':
                objects.append(GameSprite("model\map\sarcophagus_open.png",x,y,35,35))
            if symbol =="w":
                walss.append(GameSprite("model\map\shallow_water_disturbance.png",x,y,35,35))
            x += 35
        y += 35
        x = 0

run = True
clock = time.Clock()

mob = 1

font.init()
font1 = font.SysFont('Impact', 35)
font2 = font.SysFont('Impact', 15)
font3 = font.SysFont('Impact', 50)

lose = font3.render("YOU DIE" , True, (200,10, 0))
restart = 0
while run:
    for e in event.get():
            if e.type == QUIT:
                run = False
                sys.exit()
    if player.hp <=0 :
        window.blit(lose, (240, 250))
        if restart == 0 :
            restart = 200
        elif restart:
            restart -=1
            if restart == 0:
                player.hp = 5
                player.LVL = "1"
                player.xp_for_nextLVL= "5"
                player.xp = "0"
                player.damage = 1
                sprites.empty()
                walss.clear()
                player.rect.x = 350
                player.rect.y = 300
                map_X='0'
                map_Y='0'
                map_txt='map\map_x'+ map_X +'_y' + map_Y +'.txt'
                with open(map_txt, 'r') as file:
                    x, y = 0, 0
                    map = file.readlines()
                    for line in map:
                        for symbol in line:
                            grass.append(Grass(x, y,""),)
                            if symbol == '1':
                                objects.append(GameSprite("model\map\sarcophagus_open.png",x,y,35,35))
                            if symbol =="w":
                                walss.append(GameSprite("model\map\shallow_water_disturbance.png",x,y,35,35))
                            x += 35
                        y += 35
                        x = 0
        for a in mobs:
            mobs.remove(a)
            sprites.remove(a)

    else:    
        window.blit(bg, (0, 0))
        sprites.draw(window)
        player.update()
        player.draw()
        if player.rect.x <= -5:
            map_X = int(map_X)
            map_X += 1
            map_X = str(map_X)
            player.rect.x = 700 - 35
            sprites.empty()
            walss.clear()
            map_txt='map\map_x'+ map_X +'_y' + map_Y +'.txt'
            for a in mobs:
                mobs.remove(a)
                sprites.remove(a)
            with open(map_txt, 'r') as file:
                x, y = 0, 0
                map = file.readlines()
                for line in map:
                    for symbol in line:
                        grass.append(Grass(x, y,""),)
                        if symbol == '1':
                            objects.append(GameSprite("model\map\sarcophagus_open.png",x,y,35,35))
                        if symbol =="w":
                            walss.append(GameSprite("model\map\shallow_water_disturbance.png",x,y,35,35))
                        x += 35
                    y += 35
                    x = 0
            if map_X != "0" or map_Y !="0":
                mob = Mob("model\mob\mob.png",randint(0,WIDTH-35),randint(0,HEIGHT-35),35,35,3,1,1,'angry')
        if player.rect.x >= 700 -25:
            map_X = int(map_X)
            map_X -= 1
            map_X = str(map_X)
            player.rect.x = -3
            sprites.empty()
            walss.clear()
            map_txt='map\map_x'+ map_X +'_y' + map_Y +'.txt'
            for a in mobs:
                mobs.remove(a)
                sprites.remove(a)
            with open(map_txt, 'r') as file:
                x, y = 0, 0
                map = file.readlines()
                for line in map:
                    for symbol in line:
                        grass.append(Grass(x, y,""),)
                        if symbol == '1':
                            objects.append(GameSprite("model\map\sarcophagus_open.png",x,y,35,35))
                        if symbol =="w":
                            walss.append(GameSprite("model\map\shallow_water_disturbance.png",x,y,35,35))
                        x += 35
                    y += 35
                    x = 0
            if map_X != "0" or map_Y !="0":
                mob = Mob("model\mob\mob.png",randint(0,WIDTH-35),randint(0,HEIGHT-35),35,35,3,1,1,'angry')
        if player.rect.y <= -5:
            player.rect.y = 500
            map_Y = int(map_Y)
            map_Y += 1
            map_Y = str(map_Y)
            sprites.empty()
            walss.clear()
            map_txt='map\map_x'+ map_X +'_y' + map_Y +'.txt'
            for a in mobs:
                mobs.remove(a)
                sprites.remove(a)
            with open(map_txt, 'r') as file:
                x, y = 0, 0
                map = file.readlines()
                for line in map:
                    for symbol in line:
                        grass.append(Grass(x, y,""),)
                        if symbol == '1':
                            objects.append(GameSprite("model\map\sarcophagus_open.png",x,y,35,35))
                        if symbol =="w":
                            walss.append(GameSprite("model\map\shallow_water_disturbance.png",x,y,35,35))
                        x += 35
                    y += 35
                    x = 0
            if map_X != "0" or map_Y !="0":
                mob = Mob("model\mob\mob.png",randint(0,WIDTH-35),randint(0,HEIGHT-35),35,35,3,1,1,'angry')
        if player.rect.y >= 505:
            player.rect.y = 0
            map_Y = int(map_Y)
            map_Y -= 1
            map_Y = str(map_Y)
            sprites.empty()
            walss.clear()
            map_txt='map\map_x'+ map_X +'_y' + map_Y +'.txt'
            for a in mobs:
                mobs.remove(a)
                sprites.remove(a)
            with open(map_txt, 'r') as file:
                x, y = 0, 0
                map = file.readlines()
                for line in map:
                    for symbol in line:
                        grass.append(Grass(x, y,""),)
                        if symbol == '1':
                            objects.append(GameSprite("model\map\sarcophagus_open.png",x,y,35,35))
                        if symbol =="w":
                            walss.append(GameSprite("model\map\shallow_water_disturbance.png",x,y,35,35))
                        x += 35
                    y += 35
                    x = 0
            if map_X != "0" or map_Y !="0":
                mob = Mob("model\mob\mob.png",randint(0,WIDTH-35),randint(0,HEIGHT-35),35,35,3,1,1,'angry')
        for i in attaks:
            i.update()
        if reload != 1 :
            reload -= 1 
        HP = str(player.hp)
        hp = font3.render(HP , True, (140, 100, 30))
        result = font1.render(player.xp + "/" + player.xp_for_nextLVL , True, (140, 100, 30))
        lvl = font2.render(player.LVL , True, (140, 100, 30))
        window.blit(lvl, (player.rect.x, player.rect.y-20))
        window.blit(result, (0, HEIGHT-35))
        window.blit(hp, (15,20))
        for i in mobs:
            i.update()
        if attak_deffens !=1:
            attak_deffens -=1
    
    display.update()
    clock.tick(FPS)