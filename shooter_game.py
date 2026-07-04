# import libs
from pygame import *
from time import time as timer
from random import randint

background_music = 'space.ogg'
background_file = 'galaxy.jpg'
player_file = 'rocket.png'
enemy_file = 'ufo.png'
bullet_file = 'bullet.png'
missile_file = 'missile2.png'
color = (255, 255, 255)

win_height = 700
win_width = 500
print("Ukuran window", win_width, win_height)

font.init()
font1 = font.Font(None, 25)
font2 = font.Font(None, 72)

text_win = font2.render("YOU WIN!", True, (100,255, 100))

class GameSprite(sprite.Sprite):
    def __init__(self, filename, player_x, player_y, size_x, size_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(filename), (size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_height:
            self.rect.x += self.speed
        
        if keys[K_t]:
            self.teleport()

    def fire(self):
        bullet = Bullet(bullet_file, self.rect.centerx, self.rect.top, 15,20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

# buat object window
window = display.set_mode((win_height,win_width))
display.set_caption("Game Shooter by Faisal")
background = transform.scale(image.load(background_file), (win_height,win_width))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load(background_music)
# mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

ship = Player(player_file, 300, 400, 80, 100, 5)
monster1 = Enemy('ufo.png',10, 0, 50,50, 1 )
monsters = sprite.Group()
monsters.add(monster1)

game = True
finish = False
while game:
    window.blit(background, (0,0))

    for e in event.get():
        if e.type == QUIT:
            game = False
    
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()

    if not finish:

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('ufo.png',10, 0, 50,50, 1 )
            monsters.add(monster1)
            
        ship.reset()
        ship.update()

        bullets.update()
        bullets.draw(window)

        monster1.reset()
        monster1.update()

   
        display.update()




    clock.tick(FPS)