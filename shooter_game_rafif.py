from pygame import *
from random import *
from time import time as timer

window = display.set_mode((700, 800))
display.set_caption('SHOOTER')
bg = transform.scale(image.load('tartarus.jpg'), (700, 800))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, sizex, sizey, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (sizex, sizey))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 65:
            self.rect.x += self.speed    

    def fire(self):
        bullet = Bullet('damn.png', self.rect.centerx - 10, self.rect.top, 80, 180, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 1000:
            self.rect.y = 0
            self.rect.x = randint(0, 700 - 80)
            lost = lost + 1

class Bullet(GameSprite): 
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()
bullets = sprite.Group()


#monster1 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster2 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster3 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster4 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster5 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster6 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster7 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster8 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster9 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))
#monster10 = Enemy('sekir.png', randint(0, 620), 130, 160, 50, randint(1, 5))

#Membuat group Monster
#monsters = sprite.Group()
#monsters.add(monster1)
#monsters.add(monster3)
#monsters.add(monster4)
#monsters.add(monster5)
#monsters.add(monster6)
#monsters.add(monster7)
#monsters.add(monster8)
#monsters.add(monster9)
#monsters.add(monster10)

monsters = sprite.Group()
for i in range(1, 11):
    monster = Enemy('sekir.png', randint(80, 700 - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)


asteroids = sprite.Group()
for i in range(2):
    asteroid= Enemy('asteroid.png', randint(80, 700), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)



player = Player('satanael.webp', 5, 550, 200, 150, 10)

mixer.init()
mixer.music.load('no more what ifs.ogg')
mixer.music.play()
fireS = mixer.Sound('fire.ogg')

font.init()

lost = 0

font2 = font.Font(None, 36)
score = 0 

clock = time.Clock()
FPS = 60

finish = False
run = True

life = 3
reltime = False
numfire = 5


while run:
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if numfire > 0 and reltime == False:
                    numfire -=1
                    player.fire()
                    fireS.play()
                if numfire <= 0 and reltime == False:
                    start_reltime = timer()
                    reltime == True
    
    if not finish:
        window.blit(bg, (0, 0))
        if reltime:
            current_time = timer()
            if current_time - start_reltime < 5:
                #reload = font2.render('Reload...', 1, (255, 255, 255))
                #window.blit(reload, (350, 400))
                text_lose = font2.render('Reload...', 1, (255, 255, 255))
                window.blit(text_lose, (200, 200)) 
            else:
                numfire = 5
                reltime = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        if collides:
            monster = Enemy('Sekir.png', randint(0, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            score += 1
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        text_score = font2.render("Score: " + str(score), 1, (255, 255, 255))
        
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        window.blit(text_lose, (10, 50)) #Menampilkan jumlah miss
        window.blit(text_score, (10, 20)) #Menampilkan jumlah score
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        
        if score == 10:
            finish = True
            text_win = font2.render('YOU WIN!!!', 1, (255, 255, 255))
            window.blit(text_win, (200, 200))
        if sprite.spritecollide(player, asteroids, False):
            life -= 1 
        if sprite.spritecollide(player, monsters, False):
            life -= 1
        if life == 0:
            finish = True
            text_lose = font2.render('YOU LOSE...', 1, (255, 255, 255))
            window.blit(text_lose, (200, 200)) 
        text_life = font2.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))

        if lost > 5:
            finish = True
            text_lose = font2.render('you lose...', 1, (255, 255, 255))
            window.blit(text_lose, (200, 200))
    display.update()











