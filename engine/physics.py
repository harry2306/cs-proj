import math
from .state import Ball, ShotRecord, Config


def apply_friction(ball: Ball, dt: float, cfg: Config):
    s = ball.speed()
    # speed with respect to the angular velocity w (at the start its non we're simply sliding)
    v_slide = s - ball.w*ball.r
    if s < 1e-6: # if speed is below a 1e^-9 just set the velocities to 0
        ball.vx = ball.vy = 0.0
        ball.w = 0
        return
    nx, ny = ball.vx/s, ball.vy/s
    
    if abs(v_slide) > cfg.ROLL_EPS:
        decel = cfg.SLIDING_R*cfg.G
        v_new = max(0,s - decel*dt)
        alpha = 2.5* decel/ball.r # angular acceleration
        ball.w += math.copysign(alpha*dt, v_slide) 

        ball.vx = nx*v_new
        ball.vy = ny*v_new

    else: 
        # constant-magnitude decel opposite velocity
        decel = cfg.ROLLING_C*cfg.G # Given by the linear model of motiom
        dv = decel*dt
        v_new = max(0,s - dv)
        ball.w = v_new/ball.r
        ball.vx = nx * v_new # decelerate vx
        ball.vy = ny * v_new # declare vy
        if v_new < cfg.STOP_EPS:
            ball.vx = ball.vy = 0
            ball.w = 0

def integrate(ball: Ball, dt: float):
    # how much has the ball traveled in dt timeg
    ball.x += ball.vx * dt
    ball.y += ball.vy * dt

def resolve_ball_wall(ball: Ball, cfg: Config):
    # Keep center inside bounds [LEFT+R, RIGHT-R] x [BOTTOM+R, TOP-R]
    minx = cfg.LEFT + ball.r
    maxx = cfg.RIGHT - ball.r
    miny = cfg.BOTTOM + ball.r
    maxy = cfg.TOP - ball.r

    if ball.x < minx:
        ball.x = minx
        ball.vx = -ball.vx * cfg.RESTITUTION_WALL
    elif ball.x > maxx:
        ball.x = maxx
        ball.vx = -ball.vx * cfg.RESTITUTION_WALL

    if ball.y < miny:
        ball.y = miny
        ball.vy = -ball.vy * cfg.RESTITUTION_WALL
    elif ball.y > maxy:
        ball.y = maxy
        ball.vy = -ball.vy * cfg.RESTITUTION_WALL

def resolve_ball_ball(a: Ball, b: Ball, cfg: Config):
    # classic impulse-based elastic collision with overlap correction
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy) # distance apart
    min_dist = a.r + b.r # minimal distance
    if dist >= min_dist:
        return False, None, None

    # normal vector between the two balls
    nx = dx / dist
    ny = dy / dist

    # positional correction
    overlap = min_dist - dist 
    total_m = a.m + b.m # total mass
    # pushing them along the normal so they do not overlap
    a.x -= nx * overlap * (b.m / total_m) # nx*overlap is the overlap in the x-direciton
    a.y -= ny * overlap * (b.m / total_m) # ny*overlap is the overlap in the y-direction
    b.x += nx * overlap * (a.m / total_m)
    b.y += ny * overlap * (a.m / total_m)

    # relative velocity along normal
    rvx = b.vx - a.vx
    rvy = b.vy - a.vy
    vel_along_normal = rvx * nx + rvy * ny

    # if separating, no impulse
    if vel_along_normal > 0:
        return False, None, None

    e = cfg.RESTITUTION_BALL
    j = -(1 + e) * vel_along_normal
    j /= (1 / a.m) + (1 / b.m)

    imp_x = j * nx
    imp_y = j * ny

    a.vx -= imp_x / a.m
    a.vy -= imp_y / a.m
    b.vx += imp_x / b.m
    b.vy += imp_y / b.m

    white = False
    if b.id == 0 or a.id == 0:
        white = True

    return white, b, a

def check_pockets(ball: Ball, cfg: Config):
    pocket = None
    for (px, py) in cfg.POCKETS:
        if math.hypot(ball.x - px, ball.y - py) <= cfg.POCKET_R:
            ball.alive = False
            ball.vx = ball.vy = 0.0
            pocket = ball.id
    return pocket

def any_moving(balls):
    for b in balls:
        if b.alive and (abs(b.vx) > 0.1 or abs(b.vy) > 0.1):
            return True
    return False