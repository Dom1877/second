#Создай собственный Шутер!
from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.SysFont('Arial', 50)
win = font1.render('You win!', True, (206,209,0)) 
lose = font1.render('You lose!', True, (180,3,0)) 
font2 = font.SysFont('Arial', 20)


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_asteroid = "asteroid.png"


score = 0
max_lost = 3
lost = 0
goal = 10


clock = time.Clock()
FPS = 60

ship = transform.scale(image.load(img_hero), (100, 100))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()    
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Bullet(Enemy):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_height = 700
win_width = 500
display.set_caption("shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10) 


monsters = sprite.Group() 
for i in range(1, 6): 
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
   monsters.add(monster) 

asteroids = sprite.Group() 
for i in range(1, 6):  
    asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))  
    asteroids.add(asteroid) 

bullets = sprite.Group()

finish = False

running = True
while running:
    for e in event.get():
        if e.type  == QUIT:
            running = False
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE: 
                ship.fire() 
                fire_sound.play() 

    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed enemies: " + str(lost), 1, (255, 255, 255))
        window. blit(text_lose, (10, 50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        asteroids.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
            asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))    
            asteroids.add(asteroid)  
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False): 
            sprite.spritecollide(ship, monsters, True) 
            sprite.spritecollide(ship, asteroid, True)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    time.delay(50)