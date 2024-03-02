from pygame import *
mixer.init()
FPS = 60
WIDTH, HEIGHT = 700, 525
window = display.set_mode((WIDTH, HEIGHT))
mixer.music.load('model\music\Forest.ogg')
mixer.music.play()
mixer.music.set_volume(1)
count = 0
display.set_caption('Лабіринт')

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height):
        self.image = transform.scale(image.load(sprite_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_w]:
            self.rect.y -= 3
        if pressed[K_s]:
            self.rect.y += 3
        if pressed[K_a]:
            self.rect.x -= 3
        if pressed[K_d]:
            self.rect.x += 3
class grass(GameSprite):
    def __init__(self, x , y, ):
        super().__init__('model\map\grass_1_new.png', x, y, 35, 35)


bg = transform.scale(image.load("model\map\grass_1_new.png"), (WIDTH, HEIGHT))
player = Player('model\player\centaur_brown_female.png', 0 , 0, 30, 30)

Grass = []


with open('map\map_x0_y0.txt', 'r') as file:
    x, y = 0, 0
    map = file.readlines()
    for line in map:
        for symbol in line:
            if symbol == 'G':
                Grass.append(grass(x, y))
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
    for g in Grass:
        g.draw()
    player.update()
    player.draw()
    display.update()
    clock.tick(FPS)