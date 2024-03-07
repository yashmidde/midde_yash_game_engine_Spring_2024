# This file was created by: Chris Cozort
#added this comment to prove github is listening
# import libraries and modules



import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path


'''
goals: collecting coins without dying
feedback: coin collection/colliding enemy (lose health) 
rules: health bar, can't collide with enemies
freedom: movement

ideas:
kill/shoot
startscreen
health bar
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
        game_folder = path.dirname(__file__)
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f: #connecting map.txt to main code, printing map
            for line in f:
                print(line) 
                self.map_data.append(line)

    # Create run method which runs the whole game
    def new(self):
        print("create new game...")
        #places sprite in group
        self.all_sprites = pg.sprite.Group()
        #places wall in group
        self.walls = pg.sprite.Group()
        #places coin in group
        self.coins = pg.sprite.Group()
        #places powerup in coin
        self.power_ups = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col) #1 in map.txt will print a wall
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row) #P in map.txt will print the player
                if tile == '2':
                    self.player = Coin(self, col, row) #2 in map.txt will print a coin
                if tile == '3':
                    self.player = PowerUp(self, col, row) #2 in map.txt will print a coin
                if tile == 'M':
                    self.mob = Mob(self, col, row)
        
        #self.player1 = Player(self, 1, 1)
        #x and y value for wall
        #for x in range(10, 20):
            #Wall(self, x, 5)

    #method which runs the whole game
    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()#input
            self.update()#process
            self.draw()#output
    def quit(self):
         #closes window in Windows
         pg.quit()
         sys.exit()

    def update(self):
        self.all_sprites.update() #every single sprite

    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    #moneybag
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)
    
   
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)
            self.draw_text(self.screen, "Lives:" + str(self.player.lives), 64, WHITE, 13, 1)
            pg.draw.rect(self.screen, RED, pg.Rect(450, 100, 150, 10))
            pg.display.flip()


    def events(self):
         #event is what human does
         for event in pg.event.get():
            if event.type == pg.QUIT:
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
                
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen", 64, WHITE, 1, 1)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


        
    
    
# Instantiate the game... 
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()