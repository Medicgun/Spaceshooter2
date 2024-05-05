from pygame import *
from random import randint
from time import sleep
from time import time as time_counter

font.init()

# global variables
score = 0
lost = 3
reload = False
shots = 0

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 10:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < 700 - 80:
            self.rect.x += self.speed

    def fire(self):
        new_bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 50, 15)
        bullets.add(new_bullet)
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost # call the global variable

        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost -= 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)

player = Player("rocket.png", 255, 420, 65, 65, 10)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(80, 620), 50, 85, 65, randint(1, 2))
    enemies.add(enemy)

#asteroid obstacle
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(80, 620), 50, 85, 65, 2)
    asteroids.add(asteroid)


bullets = sprite.Group()

window = display.set_mode((700, 500))
background = transform.scale(
    image.load("galaxy.jpg"),
    (700, 500)
)

# music backgrond
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play(-1)

fire_sound = mixer.Sound("fire.ogg")

clock = time.Clock()
game = True
finish = False

while game:
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()

        # handle with the enemies
        enemies.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()


        # statistics
        score_stat = font.SysFont('Arial', 30).render("Score: " + str(score), 1, (255, 255, 255))
        life_stat = font.SysFont('Arial', 30).render("Lives: " + str(lost), 1, (255, 255, 255))
        window.blit(score_stat, (10, 10))
        window.blit(life_stat, (10, 40))

        if not reload:
            collides_en  = sprite.spritecollide(player, enemies, True)
            collides_as = sprite.spritecollide(player, asteroids, True)

            if collides_en:
                lost -= 1
                reload = True
                event_time = time_counter()
                new_enemy = Enemy("ufo.png", randint(80, 620), 50, 85, 65, randint(1, 2))
                enemies.add(new_enemy)
        
            if collides_as:
                lost -= 1
                reload = True
                event_time = time_counter()
                new_asteroid = Asteroid("asteroid.png", randint(80, 620), 50, 85, 65, 2)
                asteroids.add(new_asteroid)

        #Reloading
        if reload:
            reload_text = font.SysFont('Arial', 30).render("WAIT! RELOADING...", 1, (255, 30, 50))     
            window.blit(reload_text, (250, 400))   
            new_time = time_counter() 
            change_time = new_time - event_time
            if change_time >= 0.7:
                reload = False
                shots = 0


        #lost condition
        if lost < 0:
            finish = True
            lose_text = font.SysFont('Arial', 60).render("YOU LOST!", 1, (255, 0, 0))
            window.blit(lose_text, [220, 200])
            mixer.music.stop()

        #win condition
        if score >= 10:
            finish = True
            lost_text = font.SysFont('Arial', 60).render("YOU WIN!", 1, (20, 50, 250))
            window.blit(lost_text, (220, 200))
            mixer.music.stop()

        collides = sprite.groupcollide(
            bullets, 
            enemies,  
            True,
            True
        )
        for collide in collides:
            score += 1
            new_enemy = Enemy("ufo.png", randint(80, 620), 50, 85, 65, randint(1, 5))
            #add new enemy to the group
            enemies.add(new_enemy)

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN and not finish and not reload:
            if e.key == K_SPACE:
                player.fire()
                fire_sound.play()
                shots = shots + 1
                if shots >= 5:
                    shots = 0
                    reload = True 
                    event_time = time_counter()               

    clock.tick(60)
    display.update()

