# This file was created by: Chris Cozort
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        #game is the class
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0 
        self.speed=300
        self.lives = 3
        

    def get_keys(self):
        self.vx, self.vy = 0, 0 #resets velocity
        keys = pg.key.get_pressed() 
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pg.K_e]:
            print("trying to shoot...")
            self.pew()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)
        print(p.rect.x)
        print(p.rect.y)
    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            
    def collide_with_walls(self, dir): #method in pygame libraryto check if player collides with walls
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width #subtracting width so that the player is directly next to wall
                if self.vx < 0:
                    self.x = hits[0].rect.right #registration point is already on right so self.width is not needed
                self.vx = 0 #resets velocity
                self.rect.x = self.x #resetting position of rectangle to self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False) #method in pygame to check if player collides with walls
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    

    def collide_with_group(self, group, kill):#made possible by Aayush's question
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits: #if it hits the coin, add value to moneybag
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print("You just got powered up!")
            if str(hits[0].__class__.__name__) == "Mob":
                self.lives -= 1
                
                


    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        if self.collide_with_group(self.game.coins, True):
            self.moneybag =+ 1
        if self.collide_with_group(self.game.mobs, True):
            self.lives -= 1
        
        
        

class Coin(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups #tuple: list of groups that goes into sprites
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


    
    
class Wall(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((16, 16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("I created a pew pew...")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        # if hits:
        #     if str(hits[0].__class__.__name__) == "Coin":
        #         self.moneybag += 1
    def update(self):
        self.collide_with_group(self.game.coins, True)
        self.rect.y -= self.speed
        # pass
