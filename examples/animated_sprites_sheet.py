import pygame as pg

FPS = 30 
frames = ["Frame 1", "Frame 2", "Frame 3", "Frame 4"]

clock = pg.time.Clock()

current_frame = 0

last_update = 0 

def animate():
    global current_frame
    global last_update
    now = pg.time.get_ticks()
    if now - last_update > 350:
        print(frames[current_frame])
        current_frame = (current_frame + 1) % len(frames) #updates current_frame using modulo. 
        #1%4 = 1, 2%4 = 2, 3%4 = 3, 4%4 = 0
        last_update = now

while True:
    clock.tick(FPS)
    animate()
    
    