import math, random
from .state import GlobalState
from .physics import *
from dataclasses import dataclass


PHYS_R = 11.5

@dataclass
class action:
    angle: int = 0
    power: int = 0
    target_ball: int = -1
    hit_point: tuple[float,float] | None = None
    intended_pocket: tuple[float,float] | None = None


def clone(state:GlobalState):
    clone = GlobalState()
    clone.balls = [b.copy() for b in state.balls]
    clone.player1 = state.player1_b
    clone.player2 = state.player2_b
    clone.turn = state.turn
    return clone

def blocked(x1,y1,x2,y2, ball_position):
    dx,dy = x2-x1,y2-y1
    blocked = False
    list = []
    R = 2*PHYS_R 
    n = math.hypot(dx, dy)
    num = int(n/R)
    dx, dy = dx/n, dy/n
    for x,y in ball_position:
        for i in range(num):
            t = R*(i+1)
            if math.hypot(x1+t*dx-x,y1+t*dy-y) <= R:
                blocked = True
                break
    return blocked

def position_to_hit(x1,y1,x2,y2):
    ux,uy = x2-x1,y2-y1
    n = math.hypot(ux,uy)
    ux, uy = ux/n, uy/n
    R = 2*PHYS_R
    ux, uy = x1-R*ux, y1-R*uy
    return ux,uy


def target_balls(state:GlobalState, pocket_loc):
    ball_positions = state.ball_positions()
    actives = state.active()
    list = [x for x in range(len(ball_positions))]
    length = len(list)
    if state.turn == 0:
        type = state.player1.group
    else:
        type = state.player2.group
    lst_hit = [None]
    pocket = []
    pckt = []
    overall = []
    x2,y2 = ball_positions[0]
    for i in range(1,length):
        if actives[i] == 0:
            continue
        x1,y1 = ball_positions[i]
        for x,y in pocket_loc:
            x3,y3 = position_to_hit(x1,y1,x,y)
            if state.balls[i].sprite == type and not blocked(x1,y1,x,y,ball_positions) and blocked(x2,y2,x3,y3,ball_positions):
                lst_hit.append(position_to_hit(x1,y1,x,y))
                pckt.append(x,y)
        if not lst_hit:
            overall.append(None)
            pckt.append(None)
            continue
        overall.append(lst_hit)
        pocket.append(pckt)
        pckt = []
        lst_hit = []
    return overall, pocket

def size_possible(state:GlobalState):
    size = 0
    overall = target_balls(state)
    for o in overall:
        if o is None:
            continue
        size += len(o)
    return size


def calc_action(state:GlobalState, overall,pocket):
    ball_positions = state.ball_positions()
    action1 = []
    subaction = []
    ux, uy = ball_positions[0]
    for j in range(len(overall)):
        if overall[j] is None:
            action1.append(None)
        else:
            for i in range(len(overall[j])):
                act = action()
                if overall[j][i] is None:
                    continue
                x, y = overall[j][i]
                dx, dy = x - ux, y - uy
                angle = math.degrees(math.atan2(dy,dx))
                dist =  math.hypot(pocket[j][i][0]-x, pocket[j][i][1]-y) 
                if dist < 50:
                    power = 2
                elif dist < 100:
                    power = 3
                else:
                    power = 4
                act.angle = angle
                act.power = power
                act.target_ball = j
                act.intended_pocket = (pocket[j][i][0], pocket[j][i][1]) 
                act.hit_point = (x,y)
                subaction.append(act)
            action1.append(subaction)
            subaction = []
    return action1

def simulate_action(action,state:GlobalState, cfg):
    # convert (angle, power) into cue-ball velocity
    speed = action.power * 5
    events = {"first_contact": None, "pocketed": [], "foul": False, "scratch": False}
    vx = speed*math.cos(math.radians(action.angle))
    vy = speed*math.sin(math.radians(action.angle))
    state.balls[0].vx = vx
    state.balls[0].vy = vy
    dt = 2
    while any_moving(state.balls):
        for i in range(len(state.balls)):
            if not state.balls[i].alive:
                continue
            apply_friction(state.balls[i],dt,cfg)
            integrate(state.balls[i],dt)
            da = state.balls[i].w*dt
            state.balls[i].angle += da
            resolve_ball_wall(state.balls[i],cfg)
            for j in range(i + 1, len(state.balls)):
                a, b = state.balls[i], state.balls[j]
                if a.alive and b.alive:
                    hit = resolve_ball_ball(a, b, cfg)
                    if hit[0] and events["first_contact"] is None:
                        if b.sprite != state.player2.group:
                            events["foul"] = True
                            events["first_contact"] = b.sprite
                        else:
                            events["first_contact"] = b.sprite
                if(check_pockets(state.balls[j],cfg) is not None):
                    events["pocketed"].append(state.balls[j])
            if(check_pockets(state.balls[i],cfg) is not None):
                    if i == 0:
                        events["scratch"] = True
                    else:
                        events["pocketed"].append(state.balls[i])
    return state, events

def hardness(state:GlobalState, act:action):
    cx, cy = state.ball_positions()[0]
    hx, hy = act.hit_point
    px, py = act.intended_pocket
    return (math.hypot(hx-cx, hy-cy) + math.hypot(px-hx, py-hy)) / 100.0





def jitter(act, diff, hardness): 
    # diff corresponds to how accurate we want the AI to be
    # hardness corresponds to the hardness of the shot
    # diff = 1 means 0 inaccuracy
    # diff closer to 0 means higher inaccuracy
    inacc = 1 - diff
    # sd for angle
    angle_sd = (2 + hardness)*inacc
    angle_error = random.gauss(0.0,angle_sd)
    power_sd = (2+hardness)*inacc
    power_error = random.gauss(0.0,power_sd)

    act2 = action()
    act2.angle = act.angle + angle_error
    act2.power = max(1, act.power + power_error)
    act2.target_ball = act.target_ball
    act2.hit_point = act.hit_point
    return act2

def score(state:GlobalState,events):
    score = 0 
    if events["scratch"] or events["foul"]:
        score = -100
    for i in events["pocketed"]:
        if i.sprite == state.player2.group:
            score += 20
        else:
            score -= 20
    score += size_possible(state)
    return score

def best_shot(state:GlobalState, cfg):
    shot_pkt = target_balls(state)
    actions = calc_action(state,shot_pkt)
    max_score = 0
    idx = None
    for i in range(len(actions)):
        if actions[i] is None:
            continue
        else:
            for j in range(len(actions[i])):
                score = score(simulate_action(actions[i][j],state,cfg))
                if score > max_score:
                    max_score = score
                    idx = i, j
    return actions[idx[0]][idx[1]]


def fallback(state:GlobalState):
    state.balls[0].vx = 5

def flatten_actions(actionlist):
    out = []
    for group in actionlist:
        if group is None:
            continue
        out.extend(group)
    return out




def AI(state:GlobalState,cfg, pocket_loc, diff = 0.8, K=30):
    overall, pockets = target_balls(state, pocket_loc)
    action_lists = calc_action(state,overall,pockets)
    actions = flatten_actions(action_lists)
    if not actions:
        return fallback(state)
    best_Q = -1e18
    best = None
    for a in actions:
        total = 0.0
        hard = hardness(state,a)
        
        for _ in range(K):
            s = clone(state)
            a2 = jitter(a,diff,hard)
            s_after, events = simulate_action(a2,s,cfg)
            total += score(s_after,events)

        Q = total / K
        if Q > best_Q:
            best_Q = Q
            best = a

    return best





    
    





       