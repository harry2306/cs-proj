import math
from dataclasses import dataclass


@dataclass
class Player:
    group: str = None # ball type 
    num_balls: int = 0 # number of balls pocketed

@dataclass
class Ball:
    x: float # x-location (center)
    y: float # y-location (center)
    vx: float # x-velocity
    vy: float # y-velocity
    r: float  # radius
    m: float # mass
    sprite: str # image
    id: int
    group: str
    w: float = 0.0 # angular velocity
    angle: float = 0.0 # degree of rotation
    alive: bool = True

    def speed(self):
        return math.hypot(self.vx, self.vy)
    def copy(self):
        c = Ball(self.x,self.y,self.vx,self.vy,self.r,self.alive,self.sprite,self.id,
                 self.group,self.w,self.angle,self.alive)
        return c

    
@dataclass
class GlobalState:
    balls: list[Ball] = None # list of balls 
    turn: int = 0 # who's turn is it 0 for player 1, 1 for player 2
    player1: Player | None = None # player 1's Player object
    player2: Player | None = None # player 2's Player object 
    winner: Player | None = None
    illegal: bool = False
    just_switched: bool = False
    def __post_init__(self): # list becomes a global at the class level if we don't do this
        if self.balls is None:
            self.balls = []
    def switch(self):
        self.turn = 1 - self.turn
        self.just_switched = True
    def ball_positions(self):
        list = []
        for b in self.balls:
            if not b.alive:
                list.append(None)
            else:
                list.append((b.x,b.y))
        return list
    
    def active(self):
        list  = []
        for b in self.balls:
            if b.alive:
                list.append(1)
            else: 
                list.append(0)
        return list

    
@dataclass   
class ShotRecord:
    first_shot: bool = True
    shot: bool = False
    first_contact:int | None = None
    pocketed_balls: list[int] = None
    pocketed_striped: list[int] = None
    pocketed_solid: list[int] = None
    number_pocketed: int = None
    scratch: bool = False
    pocketed_eight: bool = False
    
    def __post_init__(self): # list becomes a global at the class level if we don't do this
        if self.pocketed_balls is None:
            self.pocketed_balls = []
    def reset(self):
        self.first_contact = None
        self.shot = False
        self.pocketed_balls = []
        self.scratch = False

@dataclass
class Config:
    LEFT: float
    RIGHT: float
    BOTTOM: float
    TOP: float
    POCKET_R: float
    POCKETS: list[tuple[float, float]]
    RESTITUTION_BALL: float
    RESTITUTION_WALL: float
    ROLLING_C: float
    SLIDING_R: float
    ROLL_EPS: float
    G: float
    STOP_EPS: float
    SUBSTEPS: int 
    FPS: int
    RADIUS1: float
    RADIUS2: float




