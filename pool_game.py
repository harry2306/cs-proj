from PIL import Image
import turtle
import math
import os

# Sets the working directory
# Converts jpg to gif and saves it
os.chdir("C:/Users/halva/pool")  
img = Image.open("pool_table.jpg")
img.save("pool_table1.gif")

# Sets up screen and background image
screen = turtle.Screen()
screen.setup(width=1740,height=980)
screen.bgpic("pool_table1.gif")
screen.tracer(0)

# Create the ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.shapesize(1.5,1.5)
ball.penup()
ball.speed(-10)



# Create the Cue Stick
cue = turtle.Turtle()
cue.shape('square')
cue.shapesize(stretch_wid = .7, stretch_len = 15)
cue.penup()



# Half Dimensions of Pool Table
width = 645
height = 346

# Define pockets
corner_radius = 40
pockets = [(-width,height), (width, height), (-width, -height), (width,-height), (0, height), (0,-height)]

# Ball Movement and Cue Aim
ball_speed = 5
dx = 1
dy = 1


def move():
    global dx, dy

    # Sets New Coordniate (For Movement) 
    ball.setx(ball.xcor()+dx*ball_speed)
    ball.sety(ball.ycor()+dy*ball_speed)

    # Check For Boundary Collisions
    x, y = ball.xcor(), ball.ycor()

    if abs(x) > width - corner_radius + 20:
        dx *= -1 # Reverses the incrementation of x (reverses the direction of movement)
    if abs(y) > height - corner_radius:
        dy *= -1

    # Check if Ball Falls in Pocket
    for (x1,y1) in pockets:
        if math.sqrt((x-x1)**2+(x-y1)**2) < corner_radius:
            ball.goto(0,0)
            print("pocketed")
            return




    screen.update()
    screen.ontimer(move,20)

def cue_update():
    global ball, cue
    # atan2 basically computes angle = tan^-1 y/x 
    w = 1740
    h = 980
    x, y = screen.getcanvas().winfo_pointerxy()
    window_w = screen.window_width()
    window_h = screen.window_height()
    error = 50
    if (window_w - error <= w <= window_w + error) and (window_h - error <= h <= window_h + error):
        x = (x - window_w) * (w / window_w)
        y = (window_h - y) * (h / window_h)
    else:
        x = (x - window_w // 2) * (w / window_w)
        y = (window_h // 2 - y) * (h / window_h)
    cue.goto(x , y) 
    angle = math.degrees(math.atan2(y-ball.ycor(),x-ball.xcor()))
    cue.setheading(angle)


def hit_ball(x,y):
    global dx,dy
    cue_update()
    angle = cue.heading()
    angle_r = math.radians(angle)
    dx = -math.cos(angle_r)*ball_speed
    dy = -math.sin(angle_r)*ball_speed
    move()

screen.onclick(hit_ball)
while True:
    cue_update()
    screen.update()


# Keeps the window open
screen.mainloop()