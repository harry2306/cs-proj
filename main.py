import math
import pygame
import os
from engine.state import Ball, ShotRecord, Config, Player, GlobalState
from engine.physics import *
'''from engine.ai import *'''


# ------------------- FILE MANAGEMENT --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# ------------------- Configuration   -------------------
WIDTH, HEIGHT = 1200, 700
TABLE_W, TABLE_H = 900,450
LEFT = (WIDTH  - TABLE_W) / 2
RIGHT = LEFT + TABLE_W
BOTTOM = (HEIGHT - TABLE_H) / 2
TOP    = BOTTOM + TABLE_H
POCKET_R = 27
RESTITUTION_BALL = 0.97  # bounciness ball-ball
RESTITUTION_WALL = 0.90  # bounciness vs cushion
POCKETS = [
    (LEFT, BOTTOM), (LEFT, TOP), (RIGHT, BOTTOM), (RIGHT, TOP),
    ((LEFT+RIGHT)/2, BOTTOM), ((LEFT+RIGHT)/2, TOP)
]
ROLLING_C = 0.03 # rolling coefficient
SLIDING_R = 0.35 # sliding resistance
G = 2000
STOP_EPS = 6.0
ROLL_EPS = 8.0 # belows this the ball begins to roll completely
SUBSTEPS = 4
FPS = 144  # higher FPS = more stable collisions
PHYS_R = 11.5
BALL_M = 1.0 #ball massTABLE_W, TABLE_H = 900, 450
DRAW_R = 15
#---------------------------------------------------------------

cfg = Config(LEFT, RIGHT, 
       BOTTOM, TOP, 
       POCKET_R, POCKETS,
       RESTITUTION_BALL, RESTITUTION_WALL,
       ROLLING_C, SLIDING_R,
       ROLL_EPS, G,
       STOP_EPS, SUBSTEPS,
       FPS, PHYS_R, DRAW_R
       )




# ---------------- HELPER FUNCTIONS ----------------------
def return_path(image):
    path = os.path.join(ASSETS_DIR, image)
    return path

def load_sprites():
    """
    Loads a scaled down version of the pngs in a list and returns it
    """
    BALL_IMGS = {
        "white": pygame.image.load(return_path("cue.png")).convert_alpha(),
        "black": pygame.image.load(return_path("black.png")).convert_alpha(), #convert_alpha() cuts the transparent background out returns pygame object
        "green": pygame.image.load(return_path("green.png")).convert_alpha(),
        "red": pygame.image.load(return_path("red.png")).convert_alpha(),
        "blue": pygame.image.load(return_path("blue.png")).convert_alpha(),
        "yellow": pygame.image.load(return_path("yellow.png")).convert_alpha(),
        "orange": pygame.image.load(return_path("orange.png")).convert_alpha(),
        "purple": pygame.image.load(return_path("purple.png")).convert_alpha(),
        "brown": pygame.image.load(return_path("brown.png")).convert_alpha(),
     
        "sred": pygame.image.load(return_path("sred.png")).convert_alpha(),
        "sgreen": pygame.image.load(return_path("sgreen.png")).convert_alpha(),
        "sblue": pygame.image.load(return_path("sblue.png")).convert_alpha(),
        "syellow": pygame.image.load(return_path("syellow.png")).convert_alpha(),
        "sorange": pygame.image.load(return_path("sorange.png")).convert_alpha(),
        "spurple": pygame.image.load(return_path("spurple.png")).convert_alpha(),
        "sbrown": pygame.image.load(return_path("sbrown.png")).convert_alpha()
        }
    for i in BALL_IMGS:
        BALL_IMGS[i] = pygame.transform.smoothscale(BALL_IMGS[i], (DRAW_R*2, DRAW_R*2))

    return BALL_IMGS

def rotation_cache(img, step_deg = 6):
    """
    returns a list of a image begin rotated around
    """
    cache = []
    for i in range(0,360, step_deg):
        cache.append(pygame.transform.rotate(img,-i))
    return cache


# ------------------- Math helpers -------------------

def draw_balls(screen, balls, balls_imgs, rot_cache):
    for b in balls:
        if not b.alive:
            continue
        deg = math.degrees(b.angle) % 360
        idx = int(deg // 6) % len(rot_cache[b.sprite])
        img = rot_cache[b.sprite][idx]
        rec = img.get_rect(center=(int(b.x), int(b.y)))
        screen.blit(img,rec)

def points_from_slope(x0,y0,x1,m):
    return y0 + m*(x1 - x0)

def solid_or_striped(b: Ball):
    if b.id == 0:
        return None
    if b.id == 8:
        return None
    if b.id >= 1 and b.id <= 7:
        return "solid"
    else:
        return "striped"
    

balls = [
        Ball(WIDTH/2-300, HEIGHT/2, 0, 0, PHYS_R, BALL_M, "white", 0, "cue"), 
        Ball(WIDTH/2+346, HEIGHT/2, 0, 0, PHYS_R, BALL_M, "yellow", 1, "solid"),
        Ball(WIDTH/2+323, HEIGHT/2+11.5, 0, 0, PHYS_R, BALL_M, "blue", 2, "solid"),
        Ball(WIDTH/2+300, HEIGHT/2+23, 0, 0, PHYS_R, BALL_M, "red", 3, "solid"),
        Ball(WIDTH/2+277, HEIGHT/2+34.5, 0, 0, PHYS_R, BALL_M, "purple", 4, "solid"),
        Ball(WIDTH/2+254, HEIGHT/2-46, 0, 0, PHYS_R, BALL_M, "orange", 5, "solid"),
        Ball(WIDTH/2+254, HEIGHT/2+23, 0, 0, PHYS_R, BALL_M, "green", 6, "solid"),
        Ball(WIDTH/2+277, HEIGHT/2-11.5, 0, 0, PHYS_R, BALL_M, "brown", 7, "solid"),
        Ball(WIDTH/2+300, HEIGHT/2, 0, 0, PHYS_R, BALL_M, "black", 8, "eight"),
        Ball(WIDTH/2+323, HEIGHT/2-11.5, 0, 0, PHYS_R, BALL_M, "syellow", 9, "striped"),
        Ball(WIDTH/2+300, HEIGHT/2-23, 0, 0, PHYS_R, BALL_M, "sblue", 10, "striped"),
        Ball(WIDTH/2+277, HEIGHT/2-34.5, 0, 0, PHYS_R, BALL_M, "sred", 11, "striped"),
        Ball(WIDTH/2+254, HEIGHT/2+46, 0, 0, PHYS_R, BALL_M, "spurple", 12, "striped"),
        Ball(WIDTH/2+254, HEIGHT/2-23, 0, 0, PHYS_R, BALL_M, "sorange", 13, "striped"),
        Ball(WIDTH/2+277, HEIGHT/2+11.5, 0, 0, PHYS_R, BALL_M, "sgreen", 14, "striped"),
        Ball(WIDTH/2+254, HEIGHT/2, 0, 0, PHYS_R, BALL_M, "sbrown", 15, "striped"),
    ]


# ------------------- Game -------------------
def main():
    pygame.init() 
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
    clock = pygame.time.Clock() # creates clock object that helps measure time
    balls_imgs = load_sprites()
    cache_rot = {}
    for key, img in balls_imgs.items():
        cache_rot[key] = rotation_cache(img)
    player1 = Player()
    player2 = Player()
    global_state = GlobalState()
    i=1
    global_state.player1 = player1
    global_state.player2 = player2
    global_state.balls = balls
    AIMING = False
    PROCESSING = False
    HALT = True
    cue = global_state.balls[0]
    running = True
    currentshot = ShotRecord()
    cnt = 1
    font = pygame.font.Font(None,36)
    done = False
    text2 = font.render("Choose striped or solids:", True, (255,255,255))
    skip = False
    player1 = Player()
    player2  = Player()
    switch = False
    illegal = False
    pygame.display.set_caption("Pool Game")
    while running: # while-loop will equate to one frame
        dt_frame = clock.tick(FPS) / 1000.0 # clock.tick(FPS) returns the time since the last frame in (ms)
        dt = dt_frame / SUBSTEPS #dt_frame time since last frame in (s) split into SUBSTEPS parts
        
        if global_state.turn == 0:
            if not skip and not done and any (1 <= x <= 7 for x in currentshot.pocketed_balls) and any(9 <= x <= 15 for x in currentshot.pocketed_balls):
                    skip = True
                    text = ""
            if cue.alive == False and HALT:
                cue.alive = True
                print("hi")
                global_state.switch()
                switch = True
            for event in pygame.event.get(): #pygame.event is all the events currently waiting in the queue
                if event.type == pygame.QUIT: #event.type tells you what kind of event
                    running = False

                # click-drag-release to strike cue ball (only when table is still)
                if event.type == pygame.KEYDOWN and not done and skip:
                    if event.key == pygame.K_RETURN:
                        done = True
                        skip = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (switch or illegal):
                    cue.x, cue.y = event.pos
                    switch = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not PROCESSING and not skip: #event.button == 1 checks for left click
                    AIMING = True
                    cnt = 0
                    if cue.alive and not any_moving(balls):
                        AIMING = True

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and AIMING:
                    AIMING = False
                    PROCESSING = True
                    '''
                    if len(currentshot.pocketed_balls) == 0:
                        print("hi")
                        global_state.switch()
                    '''
                    currentshot.reset()
                    HALT = False
                    mx, my = pygame.mouse.get_pos()

                    # how much we pulled back
                    dx = balls[0].x - mx
                    dy =  balls[0].y - my

                    power = 6.0  # tune
                    cue.vx = dx * power
                    cue.vy = dy * power
            '''else:
                action = AI(global_state,cfg, cfg.POCKETS)
                if not action:
                    speed = action.power
                    vx = speed*math.cos(math.radians(action.angle))
                    vy = speed*math.sin(math.radians(action.angle))
                    balls[0].vx = vx
                    balls[0].vy = vy'''


        # -------- Physics --------
        hit = (False, None, None)
        for _ in range(SUBSTEPS): # _ signifies to loop it range # of times but we don't need the loop index
            for b in balls:
                if not b.alive:
                    continue
                apply_friction(b, dt, cfg) # apply friction
                integrate(b, dt) # update ball position
                da = b.w * dt
                b.angle += da
                resolve_ball_wall(b, cfg) # check and update for wall collison

            # pairwise collisions
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    a, b = balls[i], balls[j]
                    if a.alive and b.alive:
                        hit = resolve_ball_ball(a, b, cfg)
                        if hit[0] and cnt == 0:
                            cnt = 1
                            if hit[1].id == 0:
                                currentshot.first_contact = hit[2].id
                            else:
                                currentshot.first_contact = hit[1].id
        if PROCESSING:
            for b in balls:
                    if b.alive:
                        id = check_pockets(b, cfg)
                        if id is not None:
                            (currentshot.pocketed_balls).append(id)
        

        halt = True
        for b in balls:
            if b.vx != 0 and b.vy != 0:
                halt = False
        if halt:
            PROCESSING = False
            HALT = True
        # -------- Draw --------
        screen.fill((15, 15, 15))

        # table felt
        felt = pygame.image.load(return_path("felt.png")).convert_alpha()
        screen.blit(felt, (LEFT,BOTTOM))

        rails = pygame.image.load(return_path("rails.png")).convert_alpha()
        rails = pygame.transform.smoothscale(rails, (900*1.05, 450*1.119))
        screen.blit(rails,(LEFT-24,BOTTOM-25))
        # rails

        # pockets
        pocket_img =  pygame.image.load(return_path("pocket.png")).convert_alpha()
        w = pocket_img.get_width()
        scale = 50 / w
        pocket_img = pygame.transform.smoothscale(pocket_img, (scale*w, scale*w))
        for (px, py) in POCKETS:
            rect = pocket_img.get_rect(center = (px,py))
            screen.blit(pocket_img,rect)

        if global_state.active()[8] == 0:
            global_state.winner = player2
            game_over = pygame.image.load(return_path("gameover.png")).convert_alpha()
            w,h = game_over.get_size()
            game_over = pygame.transform.smoothscale(game_over,(w/3,h/3))
            center = screen.get_rect().center
            w,h = game_over.get_size()
            screen.blit(game_over,(center[0]-w/2,center[1]-h/2))

        if switch:
            cursor_img = pygame.image.load(return_path("cue.png")).convert_alpha()
            cursor_img = pygame.transform.smoothscale(cursor_img, (DRAW_R*2, DRAW_R*2))
            x, y = pygame.mouse.get_pos()
            screen.blit(cursor_img, (x-PHYS_R,y-PHYS_R))
        else:
            cursor_img = pygame.image.load(return_path("cursor.png")).convert_alpha()
            tx, ty = -80,18
            rect = img.get_rect()
            ox, oy = rect.center
            vec = pygame.math.Vector2(tx-ox,ty-oy)
            w,h = cursor_img.get_size()
            scaled_cursor = pygame.transform.smoothscale(cursor_img, (w/5,h/5))
            cursor_img = pygame.transform.rotate(scaled_cursor, 135)
            pygame.mouse.set_visible(False)
            mx, my = pygame.mouse.get_pos()
            wx = balls[0].x
            wy = balls[0].y
            dx,dy = mx-wx, -1*(my-wy)
            angle = math.degrees(math.atan2(dy,dx))
            v_rot = vec.rotate(-angle)
            cursor_img = pygame.transform.rotate(cursor_img,angle)
            rot_rect = cursor_img.get_rect()
            rot_rect.center = (mx-v_rot.x, my-v_rot.y)
            screen.blit(cursor_img, rot_rect)

        # balls
        draw_balls(screen,balls,balls_imgs, cache_rot)



        # aim line
        if AIMING and cue.alive:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(screen, (235, 235, 180), (int(cue.x), int(cue.y)), (mx, my), 2)
            lst = []
            cx,cy = balls[0].x, balls[0].y
            dx,dy = cx - mx, cy - my
            normalizer = math.hypot(dx,dy)
            if normalizer < 1e-9:
                normalizer = 0.0000001
            ux,uy = dx/normalizer, dy/normalizer
            bol = []
            for b in balls:
                if not b.alive or b is cue:
                    continue
                bx, by = b.x, b.y
                ox, oy = cx - bx, cy - by
                R = cue.r+b.r
                b2 = 2*(ox*ux+oy*uy)
                c = (ox**2 + oy**2) - R**2
                disc = b2**2-4*c
                if disc < 0 and disc > -1e-6:
                    disc = 0
                if disc < 0:
                    continue
                t1 = (-b2 - math.sqrt(disc)) / 2
                t2 = (-b2 + math.sqrt(disc)) / 2
                if t1 >= 0: 
                    lst.append(t1)
                    bol.append(b)
                    continue
                if t2 >= 0: 
                    lst.append(t2)
                    bol.append(b)
                    continue  
            tx, ty = cue.x, cue.y 
            qx, qy = 0, 0
            if lst:
                t = min(lst)
                idx = lst.index(min(lst))
                bc = bol[idx]
                tx, ty = cx+ux*t, cy+uy*t 
                qx, qy = (bc.x - tx)/2, (bc.y-ty)/2
            pygame.draw.line(screen, (235,235,180),(int(cue.x), int(cue.y)),(tx+qx, ty+qy), 2)
            if lst:
                dx, dy = bc.x-tx, bc.y-ty
                d = math.hypot(dx,dy)
                if (d<=2*PHYS_R+0.05):
                    if d > 1e-9:
                        dx /= d
                        dy /= d
                    nx,ny = bc.x+dx*80, bc.y+dy*80
                    pygame.draw.line(screen, (235,235,180),(bc.x,bc.y),(nx, ny), 2)

        if done:
                if text == "striped":
                    player1.group = "striped"
                    print(player1.group)
                elif text == "solid":
                    player1.group = "solid"
        if skip and HALT:
            screen.blit(text2,(0,0))
            typed = font.render(text, True, (255, 255, 255))
            screen.blit(typed, (20, 60))

        pygame.display.flip() #updates the screen

    pygame.quit()

if __name__ == "__main__":
    # if we decide to import this file into another file it will not run the main() due to the
    # above line. __name__ is only __main__ when ran directly as python pool_engine.py
    main()

