import pygame
import sys
from gi.repository import Gtk

class SlimeJumpGame:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.xx = 350
        self.yy = 250
        self.infected = False
        self.running = False
        
        # Dictionary to track key states
        self.keys = {
            'left': False,
            'right': False,
            'up': False,
            'down': False
        }
        
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.player = pygame.Rect((self.xx, self.yy, 50, 50))
        self.coord = [self.xx, self.yy]
        self.running = True
        self.infected = False
        
    def out_of_bound(self, C, W, H, player):
        w, h = C[0], C[1]
        if w > W or w < 0 or h > H or h < 0:
            return True
        return False
            
    def movement(self, P, C, k):
        if k[pygame.K_a] or k[pygame.K_LEFT]:
            P.move_ip(-1, 0)
            C[0] -= 1
        elif k[pygame.K_d] or k[pygame.K_RIGHT]:
            P.move_ip(1, 0)
            C[0] += 1
        elif k[pygame.K_w] or k[pygame.K_UP]:
            P.move_ip(0, -1)
            C[1] -= 1
        elif k[pygame.K_s] or k[pygame.K_DOWN]:
            P.move_ip(0, 1)
            C[1] += 1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    #----------------
    # Add these methods to handle GTK key events
    def key_press(self, keyval):
        # Map GTK key values to our internal state
        # Common GDK key values: 65361 (left), 65363 (right), 65362 (up), 65364 (down)
        # or ASCII values: 'a'=97, 'd'=100, 'w'=119, 's'=115
        print(f"Key pressed: {keyval}")  # Debug print
        
        if keyval in (65361, 97):  # Left arrow or 'a'
            self.keys['left'] = True
        elif keyval in (65363, 100):  # Right arrow or 'd'
            self.keys['right'] = True
        elif keyval in (65362, 119):  # Up arrow or 'w'
            self.keys['up'] = True
        elif keyval in (65364, 115):  # Down arrow or 's'
            self.keys['down'] = True
    
    def key_release(self, keyval):
        if keyval in (65361, 97):  # Left arrow or 'a'
            self.keys['left'] = False
        elif keyval in (65363, 100):  # Right arrow or 'd'
            self.keys['right'] = False
        elif keyval in (65362, 119):  # Up arrow or 'w'
            self.keys['up'] = False
        elif keyval in (65364, 115):  # Down arrow or 's'
            self.keys['down'] = False
    #------------------
    
    def update(self):
        #key = pygame.key.get_pressed()
        
        if not self.infected:
            self.movement_with_state(self.player, self.coord)#, key)
        else:
            self.movement(self.zombie, self.coord)#, key)
        
        if self.out_of_bound(self.coord, self.screen_width, self.screen_height, self.player):
            if not self.infected:
                self.zombie = pygame.Rect((self.xx, self.yy, 50, 50))
                self.infected = True
    
    #----------------
    # Add a new movement method that uses our key state dictionary
    def movement_with_state(self, P, C):
        if self.keys['left']:
            P.move_ip(-1, 0)
            C[0] -= 1
        if self.keys['right']:
            P.move_ip(1, 0)
            C[0] += 1
        if self.keys['up']:
            P.move_ip(0, -1)
            C[1] -= 1
        if self.keys['down']:
            P.move_ip(0, 1)
            C[1] += 1
    #-------------------

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        if not self.infected:
            pygame.draw.rect(self.screen, (255, 100, 100), self.player)
        else:
            pygame.draw.rect(self.screen, (100, 100, 34), self.zombie)
        
        pygame.display.update()
    
    def restart(self):
        self.xx = 350
        self.yy = 250
        self.player = pygame.Rect((self.xx, self.yy, 50, 50))
        self.coord = [self.xx, self.yy]
        self.infected = False
    
    def run(self):
        self.setup()
        
        while self.running:
            # Process GTK events
            while Gtk.events_pending():
                Gtk.main_iteration()
            
            self.handle_events()
            self.update()
            self.draw()
            
            # Add a small delay to reduce CPU usage
            pygame.time.delay(10)
        
        pygame.quit()
        sys.exit()
