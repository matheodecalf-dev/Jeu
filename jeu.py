import pygame
import math
import random

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)
pygame.display.set_caption("jeu")

clock = pygame.time.Clock()
speed = 5
player = None



BASE_TILES_VISIBLE_Y = 50

MAP = {} #(x,y) -> color
map_ = None
slashes = []
SLASHES_COOLDOWN = 32
slashes_cooldown = 0
angle = 0

class Player():
    def __init__(self,name):
        self.name = name
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.posx = 0
        self.posy = 0
        self.size = WIDTH // 20
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.fill((255, 0, 0))

    def draw(self,angle):
        rotated = pygame.transform.rotate(self.image, -math.degrees(angle))
        
        rect = rotated.get_rect(center=(self.x, self.y))

        screen.blit(rotated, rect)
    def update(self):
        self.x = screen.get_width() // 2
        self.y = screen.get_height() // 2  
        self.size = screen.get_height() // 20 
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA) 
        self.image.fill((255, 0, 0))


            
class SwordSlash:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.timer = 16  
        self.radius = player.size * 1.6
        self.width = player.size * 0.6

       
        offset = self.radius * 0.7
        hx = self.x + math.cos(angle) * offset
        hy = self.y + math.sin(angle) * offset
        self.hitbox = pygame.Rect(
            hx - self.width/2,
            hy - self.width/2,
            self.width,
            self.width
        )

    def update(self):
        self.timer -= 1

    def draw(self):
        
        start_angle = -self.angle - math.radians(35)
        end_angle = -self.angle + math.radians(35)

        pygame.draw.arc(
            screen,
            (155, 155, 155),
            (self.x - self.radius,self.y - self.radius,self.radius * 2,self.radius * 2),
            start_angle,
            end_angle,
            int(self.width * 0.2)
        )

        
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        
class Map():
    def __init__(self,seed=random.randint(1,2000)): 
        self.seed = seed
        self.x = 0
        self.y = 0
        self.joueurx = 0
        self.joueury = 0
        self.tile_size = screen.get_height() // BASE_TILES_VISIBLE_Y
        self.height_visible = screen.get_height() // self.tile_size +2
        self.width_visible = screen.get_width() // self.tile_size +2
        self.color = {}
    def update(self):
        self.tile_size = screen.get_height() // BASE_TILES_VISIBLE_Y
        self.height_visible = screen.get_height() // self.tile_size +2
        self.width_visible = screen.get_width() // self.tile_size +2
        self.x = self.joueurx - ((screen.get_width()/2)//self.tile_size)
        self.y = self.joueury - ((screen.get_height()/2)//self.tile_size)
        self.clean_colors()


    def clean_colors(self):
        margin = 5 

        keep_min_x = int(self.x) - margin
        keep_max_x = int(self.x + self.width_visible) + margin
        keep_min_y = int(self.y) - margin
        keep_max_y = int(self.y + self.height_visible) + margin

        to_delete = []

        for (x, y) in self.color:
            if not (keep_min_x <= x <= keep_max_x and keep_min_y <= y <= keep_max_y):
                to_delete.append((x, y))

        for key in to_delete:
            del self.color[key]
    def draw(self):
        
        start_tile_x = int(self.x)
        start_tile_y = int(self.y)
        end_tile_y = start_tile_y + self.height_visible
        end_tile_x = start_tile_x + self.width_visible

        

        for y in range(start_tile_y, end_tile_y):

            if y >= 0:
                for x in range(start_tile_x, end_tile_x):
                    if x >= 0:
                        screen_x = (x - self.x) * self.tile_size
                        screen_y = screen.get_height() - (y - self.y + 1) * self.tile_size  

                        if (x,y) in self.color:


                            pygame.draw.rect(screen,self.color[(x,y)],(screen_x, screen_y, self.tile_size, self.tile_size))
                        else:
                            self.color[(x,y)] = (0, random.randint(100,255), 0)
                            pygame.draw.rect(screen,self.color[(x,y)],(screen_x, screen_y, self.tile_size, self.tile_size))
                        




def draw():
    global offset_x, offset_y, map_, angle
    screen.fill("black")

    mouse_x, mouse_y = pygame.mouse.get_pos()   


    dx = mouse_x - player.x
    dy = mouse_y - player.y
    angle = math.atan2(dy, dx) 

    
    world_speed = map_.tile_size * 0.01

    vx = math.cos(angle) * world_speed
    vy = math.sin(angle) * world_speed
    sx = -vy
    sy = vx

    
     
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:  
        map_.joueurx += vx
        map_.joueury -= vy
        

    if keys[pygame.K_s]: 
        map_.joueurx -= vx
        map_.joueury += vy 
        

    if keys[pygame.K_d]: 
        map_.joueurx += sx
        map_.joueury -= sy
        
    if keys[pygame.K_q]: 
        map_.joueurx -= sx
        map_.joueury += sy 
        

    map_.draw()
    player.draw(angle)
    for slash in slashes[:]:
        slash.update()
        slash.draw()
        if slash.timer <= 0:
            slashes.remove(slash)

def update_var_temp():
    global slashes_cooldown
    slashes_cooldown += 1

def update():
    update_var_temp()
    player.update()
    map_.update()
    draw()


    

def main():
    global screen, player, map_, angle, slashes_cooldown, SLASHES_COOLDOWN
    running = True
    player = Player("Joueur Test")
    map_ = Map()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                world_center_x = map_.x + screen.get_width() / (2 * map_.tile_size)
                world_center_y = map_.y + screen.get_height() / (2 * map_.tile_size)
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                map_.x = map_.joueurx - (screen.get_width()// map_.tile_size)/2
                map_.y = map_.joueury - (screen.get_height()// map_.tile_size)/2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if slashes_cooldown > SLASHES_COOLDOWN:
                        slashes.append(SwordSlash(player.x, player.y, angle))  
                        slashes_cooldown = 0 


        update()
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()    

        
if __name__ == "__main__":

    main()         