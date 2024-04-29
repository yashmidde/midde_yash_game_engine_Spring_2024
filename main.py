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
--------------------------------------------------------------------------------------------



5 things fun:
Collecting all the coins and getting back to the vault
Trying to avoid mobs and not die
Shooting mobs with projectiles
Colllecting all the power ups/health regen
The map/sprites



Ideas:

- Moving camera up, obstacles/mobs get progressively harder with final boss mob at the end 
    -adds fun because it creates an element of progress and progressing difficulty for the player
- a way to 'spend' your coins 
    - adds fun because it offers a reward for the player that they can continue over time and actually use
    - ex: extra armor, different tools, different skins
- loot chests
    - adds fun because it adds an element of surprise
    - "loadout" with differen tools (pickaxe, grenade, etc.)
- environment hazards (fire, water, trees)
    - adds fun because it creates a realistic element and also offers more unique gameplay experiences


release version
- a way to 'spend' your coins 
    - adds fun because it offers a reward for the player that they can continue over time and actually use
    - ex: extra armor, different tools, different skins
    - game should be continuous; player should be able to "pause" and go to an item shop to purchase 
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
        self.paused = False
        #load memory from hardrive
         # Initialization code...

        # Define the items available in the shop with their prices
        self.shop_items = {
            "Armor (B)": 3,
            "Sword (M)": 5,
            "Potion (N)": 10
        }

        self.armorprice = 3

        # Initialize player's currency
        self.moneybag = 0

    def show_item_shop(self):           
        # Display the item shop on the screen
        self.paused = True
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Item Shop", 64, WHITE, 4, 5)
        
        # Display items and prices
        y_offset = 8
        for item, price in self.shop_items.items():
            self.draw_text(self.screen, f"{item}: {price} coins (press twice to purchase)", 32, WHITE, 4, y_offset)
            y_offset += 2

        # Show player's current currency
        self.draw_text(self.screen, f"Your Coins: {self.player.moneybag}", 32, WHITE, 4, y_offset + 2)

        pg.display.flip()
        self.wait_for_key()

    def buy_armor(self):
        if self.player.moneybag >= 3:
            print("You just bought armor")
            self.draw_text(self.screen, f"New Balance: {self.player.moneybag - 3}", 32, WHITE, 25, 20)
            self.player.moneybag -= 3
            self.player.lives += 3
            
        

            
            #if item == "Armor":
                #self.moneybag -= 3
        pg.display.flip()
        self.wait_for_key()


        
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
        self.bell_img = pg.image.load(path.join(self.img_folder, 'theBell.png')).convert_alpha()
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
            if not self.paused:
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
            if self.paused:
                self.draw_text(self.screen, "Paused", 64, WHITE, WIDTH / 2, HEIGHT / 2)
            else:
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_p:  # Call pass function when 'P' key is pressed
                    self.pass_function()
                if event.key == pg.K_o:  # Show item shop when 's' key is pressed
                    self.show_item_shop()
                elif event.key == pg.K_b:  # Example: Buy an item when 'b' key is pressed
                    self.buy_armor()  # Change "Armor" to the selected item
            # Other event handling code...
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
    def pass_function(self):
        # Pause or unpause the game when 'P' key is pressed
        self.paused = not self.paused

# Instantiate the game...
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()


# Instantiate the game...
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()


# Instantiate the game... d
g = Game()
# use game method run to run
g.show_start_screen()


while True:
    g.new()
    g.run()
    # g.show_go_screen()