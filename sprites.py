# This file was created by: Yash Midde
# This code was informed by Chris Bradfield

import pygame as pg
from settings import *

class Player(pg.sprite.Sprite): #sprite that the player controls
    def __init__(self, game, x, y):
        #game is the class
        self.groups = game.all_sprites 
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) #player is the size of one tile
        self.image = game.player_img #places image art onto player
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0 #resets velocity of player
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        #player variables
        self.moneybag = 0 
        self.speed = 300
        self.lives = 3
        self.vaulthit = 0        

    def get_keys(self): #function used for keyboard events
        self.vx, self.vy = 0, 0 #resets velocity
        keys = pg.key.get_pressed() 
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED #negative x velocity shifts direction left
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  #positive x velocity shifts direction right
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  #negative y velocity shifts direction up
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED    #positive y velocity shifts direction down
        if keys[pg.K_e]:
            self.pew() #press e to shoot projectiles
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071 #velocity of player
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
            
    def collide_with_walls(self, dir): #method in pygame library to check if player collides with walls
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
    

    def collide_with_group(self, group, kill): #made possible by Aayush's question
        hits = pg.sprite.spritecollide(self, group, kill) #kill will remove sprite 
        if hits: 
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1 #adds value to moneybag when colliding with coin
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.vaulthit += 1
            if str(hits[0].__class__.__name__) == "Mob":
                self.lives -= 1 #subtracts life when collding with mob
            if str(hits[0].__class__.__name__) == "Vault" and self.moneybag == 10:
                self.vaulthit += 1 
            if str(hits[0].__class__.__name__) == "HealthRegen" and self.lives <= 3:
                self.lives += 1

    
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y

        #collision between player/environment
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        if self.collide_with_group(self.game.vault, False):
            print("You won!")
        if self.collide_with_group(self.game.coins, True):
            self.moneybag =+ 1
        if self.collide_with_group(self.game.mobs, True):
            self.lives -= 1
        self.collide_with_group(self.game.health_regen, True)
        
        
class Coin(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Vault(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.vault #tuple
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.vault_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PowerUp(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups #tuple
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.powerup_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class PewPew(pg.sprite.Sprite): #class for projectiles
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews #tuple
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((8, 8)) #projectiles are smaller
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
                
    def update(self):
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.mobs, True)
        self.rect.y -= self.speed

class Wall(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite): #class for enemies
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 10
    def collide_with_walls(self, dir): #mob collision with wall
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
    
    def update(self): #makes mob follow player
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

class HealthRegen(pg.sprite.Sprite):
    #method to init properties of the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.health_regen #tuple
        #init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.heart_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        #multiplying by tile size to create wall
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
