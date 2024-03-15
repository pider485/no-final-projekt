from pygame import *
mixer.init()
FPS = 60
WIDTH, HEIGHT = 700, 525
window = display.set_mode((WIDTH, HEIGHT))
mixer.music.load('model\music\Forest.ogg')
mixer.music.play()
mixer.music.set_volume(1)
count = 0
attaks = []
sprites = sprite.Group()
reload = 1

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
                attak=Attak('model\wepon\effect\icicle_up.png',self.rect.x,self.rect.y,32,32,'up')
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_DOWN] and at:
                attak=Attak('model\wepon\effect\icicle_down.png',self.rect.x,self.rect.y,32,32,'down')
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_RIGHT] and at:
                attak=Attak('model\wepon\effect\icicle_right.png',self.rect.x,self.rect.y,32,32,'right')
                attaks.append(attak)
                at = False
                reload= 30
            if pressed[K_LEFT] and at:
                attak=Attak('model\wepon\effect\icicle_left.png',self.rect.x,self.rect.y,32,32,'left')
                attaks.append(attak)
                at = False
                reload= 30
        for a in attaks:
            if a.rect.x < -5 or a.rect.x > WIDTH or a.rect.y > HEIGHT or a.rect.y < 0:
                attaks.remove(a)
                sprites.remove(a)
        for w in walss:
            if sprite.collide_rect(player, w):
                self.rect.x, self.rect.y = old_pos



class Grass(GameSprite):
    def __init__(self, x , y,view):
        super().__init__('model\map\grass_1_new.png', x, y, 35, 35)
        self.view = view
        if view == "Winter":
            self.image=transform.scale(image.load("model\map\cobble_blood_2_old.png"), (35,35))

class Attak(GameSprite):
    def __init__(self, sprite_img, x, y, width, height,move):
        super().__init__(sprite_img, x, y, width, height)
        self.move= move
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
player = Player('model\player\centaur_brown_female.png', 350 , 300, 30, 30)

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


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
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
        print(map_X)
    if player.rect.x >= 700 -25:
        map_X = int(map_X)
        map_X -= 1
        map_X = str(map_X)
        player.rect.x = -3
        sprites.empty()
        walss.clear()
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
    if player.rect.y <= -5:
        player.rect.y = 500
        map_Y = int(map_Y)
        map_Y += 1
        map_Y = str(map_Y)
        sprites.empty()
        walss.clear()
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
    if player.rect.y >= 505:
        player.rect.y = 0
        map_Y = int(map_Y)
        map_Y -= 1
        map_Y = str(map_Y)
        sprites.empty()
        walss.clear()
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
    for i in attaks:
        i.update()
    if reload != 1 :
        reload -= 1 
    display.update()
    clock.tick(FPS)