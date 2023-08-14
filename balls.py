#! First pygame project
# Brownian Balls
"""
#Basic structure of pygame programs:
while True:
    events()
    logics()
    render()

"""

import pygame, sys, random
from math import sin, cos, radians, sqrt
from pygame.locals import *

#color variables
BG = (213, 233, 246)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY =(0, 122, 204)

class Ball():
    """
    Defines fundamental proerties of sprite ball
    """
    def __init__(self, surface, x, y, r, color): 
        self.surface = surface
        self.x, self.y = x, y       #position
        self.dx, self.dy = 0, 0     #velocity 
        self.r = r                  #radius
        self.color = color          #color
        self.theta = 0              #theta for velocity direction
    
    
    def pressed(self, event):
        #key mapping dictionary
        map ={
            K_LEFT : 180,
            K_RIGHT : 0,
            K_UP : 90,
            K_DOWN : 270,
            K_a : 180,
            K_d : 0,
            K_w : 90,
            K_s : 270,
            K_q : 135,
            K_e : 45,
            K_z : 225,
            K_c : 315
        }

        if event.key in map.keys():
            self.vel(map[event.key])

    def update(self):

        #checks for wall strike
        self.wall_bounce()
        
        #updates position as per current velocity
        self.x += self.dx
        self.y += self.dy

    def wall_bounce(self):
        #updates velocity according to wall touch
        wall = self.wall_touch()
        if wall == "r":
            self.vel(180)
        elif wall == "l":
            self.vel(0)
        elif wall == "t":
            self.vel(270)
        elif wall == "b":
            self.vel(90)

    def wall_touch(self):
        #reurns "t", "b", "l", "r" for respective walls
        if self.x + self.r > 488:
            return "r"
        elif self.x - self.r < 12:
            return "l"
        elif self.y - self.r < 12:
            return "t"
        elif self.y + self.r > 488:
            return "b"
    
    def vel(self, theta):
        """
        Updates velocity based on polar coordinate theta
        """

        self.dx = int(5 * cos(radians(theta)))
        self.dy = int(-5 * sin(radians(theta)))

    def draw(self):
        """
        Draw own body in surface
        """
        self.update()
        pos = (self.x, self.y) 
        pygame.draw.circle(self.surface, self.color, pos, int(self.r))   
        
    def pause(self):
        self.dx = 0
        self.dy = 0


class Autoball(Ball):
    """
    Class for balls which moves automatically on screen
    """

    def __init__(self, surface, x, y, r, color):

        #initialize basic properties using parent's method
        Ball.__init__(self,surface, x, y, r, color)

        #collision records
        self.collision_pair = [0, 0]       #pair of value to represent succesive collision
        self.rand_start()    


    def rand_start(self):
        #introduce theta for random direction
        theta = random.choice([a for a in range(0, 360, 10)])
        self.vel(theta)


    def collides_with(self,other,touch = False):
        """
        Returns True for collision
        Returns false otherwise
        """

        #Determines collision based on center seperation:
        x = self.x - other.x
        y = self.y - other.y
        sep = sqrt( x*x + y*y )
        collide = sep < self.r + other.r

           
        #Updates the collision record
        self.collision_pair.append(collide)
        self.collision_pair = self.collision_pair[1:]

        #retruns true as soon as touches if touch os true
        if touch and self.collision_pair[1] == 1:
            return True

        #update score when collision ends to avoid multiple scoring
        if self.collision_pair[0]  == 1 and self.collision_pair[1] == 0:
            return True

        return False



    def wall_bounce(self):
        """
        Overrides parent method wall_bounce
        Updates velocity in random possible directions
        """

        wall = self.wall_touch()
        theta = None
        if wall == 'r':
            theta = [a for a in range(100, 270, 10)]
        elif wall == 'l':
            theta = [a for a in range(280, 450, 10)]
        elif wall == 't':
            theta = [a for a in range(190, 360, 10)]
        elif wall == 'b':
            theta = [a for a in range(10, 180, 10)]
        
        #theta exists if and only if ball strikes in wall
        if theta:
            
            #random direction
            theta = random.choice(theta)
            self.vel(theta)
    

class App():
    """
    Fundamental loops and logics of game
    """
    def __init__(self):
        self.active = True
        self.display_sur = None
        self.size = self.width, self.height = 500, 500
        
    def on_init(self):
        #system initialization
        pygame.init()
        self.display_sur = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Brownian Balls')
        self.running = True
        self.clock = pygame.time.Clock()

        #variables initialization    
        self.background = pygame.Surface((self.width + 1,self.height + 1))
        self.small_font = pygame.font.Font('OpenSans-Regular.ttf', 16)
        self.large_font = pygame.font.Font('OpenSans-Regular.ttf', 50)
        self.copyright = pygame.font.Font('OpenSans-Regular.ttf', 10)
        self.ball = Ball(self.background, 50, 50, 20, RED)
        self.good = Autoball(self.background, 200, 200, 5, GREEN)  
        self.bad = Autoball(self.background, 400, 400, 20, BLACK)
        self.reducer = Autoball(self.background, 200, 200, 5, WHITE)
        self.score = 0    
        self.level = 1
        self.over = False

    #checks for keystrokes
    def on_event(self, event):

        if self.over and event.type == KEYDOWN:
            self.score = 0
            self.over = False
            self.ball.r = 20
            self.good.rand_start()
            self.bad.rand_start()
            self.reducer.rand_start()

        if event.type == QUIT:
            self.running = False
        if event.type == KEYDOWN:
            self.ball.pressed(event)    #updates ball accordingly
                        
    #game logics
    def on_logics(self): 
        if self.good.collides_with(self.ball):
            self.score += 20
            if self.score % 100 == 0 and self.ball.r > 1:
                self.ball.r -= 1
            
        if self.reducer.collides_with(self.ball):
            self.score -= 10
            if self.score < 0:
                self.ball.r += 2
            else:
                self.ball.r += 0.5
        if self.bad.collides_with(self.ball, touch = True):
            self.over = True
            
        if self.score == -100:
            self.over = True
        
        self.level = self.score // 100 + 1
        
        if self.score < 0:
            self.level = 0
            


    #rendering output
    def on_render(self):
        self.background.fill(BG)
        pygame.draw.rect(self.background,BLACK,(10,10,480,480), 2 )
        
        #score board
        self.scoretext = self.small_font.render(f'SCORE: {self.score}     LEVEL: {self.level}', True, BLACK)
        self.scoreboard = self.scoretext.get_rect(center = (100, self.height - 30))
        
        #copyright name
        self.name = self.copyright.render('@Nelson', True, BLACK)
        self.namebox = self.name.get_rect(center = (self.width - 50, self.height - 20))

        self.controls = self.small_font.render('Control Keys: Arrows A S W D Q E Z C', True, SKY)
        self.controlbox = self.controls.get_rect(center = (int(self.width/2), 25))

        #calls for ball drawing function
        self.good.draw()
        self.ball.draw()
        self.bad.draw()
        self.reducer.draw()
        self.display_sur.blit(self.background,(0,0))
        self.display_sur.blit(self.scoretext, self.scoreboard)
        self.display_sur.blit(self.name, self.namebox)
        self.display_sur.blit(self.controls, self.controlbox)
        if self.over:
            self.game_over()
                
        pygame.display.update()
        
    def game_over(self):
        text = self.large_font.render("YOU GOT TRAPPED", True, BLACK)
        box = text.get_rect(center = (int(self.width/2), int(self.height/2)))
        self.display_sur.blit(text, box)
        self.ball.pause()
        self.good.pause()
        self.reducer.pause()
        self.bad.pause()
    
    def on_exit(self):
        pygame.quit()
        sys.exit()
    
    #main execeution of program
    def on_execute(self):

        #calls starting method and check for improper iniaitialization 
        if self.on_init() == False:
            self._running = False
        
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_logics()
            self.on_render()
            self.clock.tick(40)
        self.on_exit()


if __name__ == "__main__":
    app = App()
    app.on_execute()
        

            