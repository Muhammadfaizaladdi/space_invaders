from pygame import *
from random import randint

win_width = 700
win_height = 500
display.set_caption("Shooter by Faisal")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

run = True
clock = time.Clock()
lost = 0

class Gamesprite(sprite.Sprite):
    def __init__(self, image_obj, cor_x, cor_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = transform.scale(image.load(image_obj), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = cor_x
        self.rect.y = cor_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    

class Bullet(Gamesprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(70, win_width-70)
            lost += 1


monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(70, win_width-70), -40, 80,60, randint(1,7))
    monsters.add(monster)


ship = Player('rocket.png', 350, 400, 65, 65,  5)
bullets = sprite.Group()

finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
    if not finish:
        window.blit(background, (0,0))
        monsters.update()
        monsters.draw(window)

        bullets.update()
        bullets.draw(window)

        ship.reset()
        ship.update()

        display.update()
    clock.tick(50)
