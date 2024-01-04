import pyglet
from pyglet import shapes
import random
from collections import namedtuple

# Color Class
class myColor:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

star_color = myColor(255, 255, 255)

DLMCount = 0

# Set up a window
myWindow = namedtuple('myWindow', ['X', 'Y'])
myWin = myWindow(800, 600)
game_window = pyglet.window.Window(myWin.X, myWin.Y, visible=True, resizable=False)

main_batch = pyglet.graphics.Batch()

width = myWin.X
height = myWin.Y

center_x = int(myWin.X/2)
center_y = int(myWin.Y/2)

# Set up the two top labels
level_label = pyglet.text.Label(text="Testing - Starfield!", x=400, y=575, anchor_x='center', batch=main_batch)

# Counter
counter = pyglet.window.FPSDisplay(window=game_window)

class Star:

    def __init__(self, *args, **kwargs):
        self.x = random.randint(-width, width)
        self.y = random.randint(-height, height)
        self.z = random.randint(center_y, width)
        self.pz = self.z
        self.batch = main_batch
        
        radius = maps(self.z, 0, width, 6, 0)
        self.circle = shapes.Circle(self.x, self.y, radius, color=(255, 255, 255), batch=self.batch)
        self.line = shapes.Line(0,0,0,0, 2, color=(255, 255, 255), batch=self.batch)

    def update(self):
        self.z -= 30
        if self.z < 1:
            self.x = random.randint(-width, width)
            self.y = random.randint(-height, height)
            self.z = random.randint(center_y, width)
            self.pz = self.z

        starx = self.x / self.z * center_y + center_x
        stary = self.y / self.z * center_y + center_y

        #radius = maps(star.z, 0, width, 6, 0)
        radius = maps(self.z, 0, width, 6, 0)
        #Ex: circle = shapes.Circle(700, 150, 100, color=(50, 225, 30), batch=self.batch)
        self.circle.x = starx
        self.circle.y = stary
        self.circle.color = (255,255, 255)
        #print('DLM: draw: starx: '+str(starx)+' stary: '+str(stary)+' radius: '+str(radius))
        #pygame.draw.circle(screen, star_color, (starx, stary), radius)

        prevx = self.x / self.pz * center_y + center_x
        prevy = self.y / self.pz * center_y + center_y

        self.pz = self.z

        #Ex: line = shapes.Line(100, 100, 100, 200, width=19, batch=self.batch)
        self.line.x = prevx
        self.line.y = prevy
        self.line.x2 = starx
        self.line.y2 = stary
        self.color = (255, 255, 255)
        #line = shapes.Line(prevx, prevy, starx, stary, 2, batch=self.batch)
        #pygame.draw.line(screen, star_color, (prevx, prevy), (starx, stary), 2)


    #def draw(self):


def maps(num, in_min, in_max, out_min, out_max):
    return out_min + (out_max - out_min) * (num - in_min) / (in_max - in_min)

def set_color(star):
    # The rgb values start at 0 (black) initially but gradually increase to 255 (white)
    # This causes the new stars to slowly fade onto the screen
    value = 255 - int((star.z * (255/width)))
    star_color.r, star_color.g, star_color.b = value, value, value

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#clock = pygame.time.Clock()

stars = []

def init():
    #print('DLM: init')
    #for i in range(500):
    for i in range(500):
        stars.append(Star(main_batch))
    #for star in stars:
    #    print('DLM: star.x: '+str(star.x)+' star.y: '+str(star.y)+' star.z: '+str(star.z)+' star.pz: '+str(star.pz))

@game_window.event
def on_draw():
    #print('DLM: on_draw')
    game_window.clear()
    
    #for star in stars:
    #    star.draw()

    main_batch.draw()

    counter.draw()

def update(dt):
    #print('DLM: update')
    # Things to do on the update
    for star in stars:
        star.update()
        set_color(star)

if __name__ == "__main__":
    # Start it up!
    init()

    # Update the game 60 times per second
    pyglet.clock.schedule_interval(update, 1 / 30.0)

    # Tell pyglet to do its thing
    pyglet.app.run()

