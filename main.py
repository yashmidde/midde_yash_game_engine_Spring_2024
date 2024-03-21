# This file was created by: Yash Midde
# import libraries and modules



import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path


'''
goals: collecting coins without dying, reach vault
feedback: coin collection/colliding enemy (lose health) 
rules: health bar, can't collide with enemies
freedom:

ideas:
projectile
startscreen/death screen/end screen (with restart button)
health bar
vault (after collecting all the coins, the player has to reach vault to win game)
spawning mobs
new levels
loot boxes
pickaxe to destroy walls
moving camera
'''



# creating a class called game
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        #load memory from hardrive
        
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images') #linking image folder for game art

        self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.png')).convert_alpha()
        self.powerup_img = pg.image.load(path.join(self.img_folder, 'powerup.png')).convert_alpha() 
        self.wall_img = pg.image.load(path.join(self.img_folder, 'wall.png')).convert_alpha()
        self.player_img = pg.image.load(path.join(self.img_folder, 'Wizard.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'mob.png')).convert_alpha()
        self.vault_img = pg.image.load(path.join(self.img_folder, 'chest.png')).convert_alpha()
        self.heart_img = pg.image.load(path.join(self.img_folder, 'heart.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(self.game_folder, 'map.txt'), 'rt') as f: #connecting map.txt to main code, printing map
            for line in f:
                print(line) 
                self.map_data.append(line)

    # Create run method which runs the whole game
    def new(self):
        #places sprite, wall, coin etc. in group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.health_regen = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.vault = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1': #1 in map.txt will print wall
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row) #P in map.txt will print the player
                if tile == '2':
                    self.player = Coin(self, col, row) #2 in map.txt will print a coin
                if tile == '3':
                    self.player = PowerUp(self, col, row) #3 in map.txt will print a coin
                if tile == 'M':
                    self.mob = Mob(self, col, row) #M in map.txt will print a mob
                if tile == '4':
                    Vault(self, col, row) #4 in map.txt will print a vault
                if tile == 'H':
                    HealthRegen(self, col, row) #H in map.txt will print a vault


    #method which runs the whole game
    def run(self): 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()#input
            self.update()#process
            self.draw()#output

    def quit(self): #closes window in Windows
         pg.quit()
         sys.exit()

    def update(self): 
        self.restart() #restarts game
        self.all_sprites.update() #updates every single sprite

    
    def draw_grid(self): #gridlines for game
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    

    #function used for writing text in game
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    
   
    def draw(self):
            keys = pg.key.get_pressed()
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)

            # "moneybag" indicator at top of screen, coin counter
            self.draw_text(self.screen, str(self.player.moneybag), 50, YELLOW, 1.5, 1.25)

            #healthbar
            pg.draw.rect(self.screen, RED, pg.Rect(360, 45, 300, 40))
            if self.player.lives >= 3: #start
                pg.draw.rect(self.screen, GREEN, pg.Rect(360, 45, 300, 40))
            if self.player.lives == 2: #size changes when life is lost
                pg.draw.rect(self.screen, GREEN, pg.Rect(360, 45, 200, 40)) 
            if self.player.lives == 1: #size changes when life is lost
                pg.draw.rect(self.screen, GREEN, pg.Rect(360, 45, 100, 40)) 
            if self.player.lives <= 0: 
                #death screen
                self.screen.fill(BGCOLOR)
                self.draw_text(self.screen, str("You DIED!"), 100, WHITE, 10, 9.5) 
                self.draw_text(self.screen, str("Press R to play again"), 50, WHITE, 10, 14)

            
            if self.player.vaulthit >= 1 and self.player.moneybag == 10: #vaulthit is variable used when player reaches vault
                #win screen
                self.screen.fill(BGCOLOR)
                self.draw_text(self.screen, str("You WON!"), 100, WHITE, 10, 9.5) #win screen
                self.draw_text(self.screen, str("Press R to play again"), 50, WHITE, 10, 14)
            pg.display.flip()


    def events(self): #events are what human does
         for event in pg.event.get():
            if event.type == pg.QUIT: #quitting window
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
                
    def show_start_screen(self): #start screen, shows how to play
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "PRESS ANY KEY TO BEGIN!", 64, WHITE, 4, 5)
        self.draw_text(self.screen, "Collect all 10 coins and return them to the vault to win!", 32, WHITE, 4, 8)
        self.draw_text(self.screen, "Use projectiles (E) to protect yourself from your enemies,", 32, WHITE, 4, 10)
        self.draw_text(self.screen, "but make sure your projectiles don't destroy any coins!", 32, WHITE, 4, 11)
        self.draw_text(self.screen, "Powerups are placed around the map that give you a speedboost.", 32, WHITE, 4, 13)
        self.draw_text(self.screen, "Press R at any time to restart", 32, WHITE, 4, 15)
        
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self): #function so that game starts when player hits any key
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def restart(self): #restarts entire game by clearing variables/resetting map, whenever R is pressed 
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            for s in self.all_sprites:
                s.kill() #kills all existing sprites to save data
            self.player.moneybag = 0 #resets moneybag
            self.map_data = [] #resets map
            self.player.lives = 3 #resets healthbar
            with open(path.join(self.game_folder, 'map.txt'), 'rt') as f: #recreating map
                for line in f:
                    print(line) 
                    self.map_data.append(line)
            # repopulate the level with stuff
            for row, tiles in enumerate(self.map_data):
                print(row)
                for col, tile in enumerate(tiles):
                    print(col)
                    if tile == '1':
                        print("a wall at", row, col)
                        Wall(self, col, row)
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == '2':
                        self.player = Coin(self, col, row)
                    if tile == 'M':
                        self.mob = Mob(self, col, row)
                    if tile == '3':
                        self.player = PowerUp(self, col, row)
                    if tile == '4':
                        Vault(self, col, row)
                    if tile == 'H':
                        HealthRegen(self, col, row) #H in map.txt will print a vault

        

        
# Instantiate the game... d
g = Game()
# use game method run to run
g.show_start_screen()


while True:
    g.new()
    g.run()
    # g.show_go_screen()