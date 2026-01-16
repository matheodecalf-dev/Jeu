import pygame
import math

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)
pygame.display.set_caption("jeu")

clock = pygame.time.Clock()
speed = 5
player = None

TILE_SIZE = 60
MAP_W = 40   
MAP_H = 40  

offset_x = 0
offset_y = 0
BASE_TILES_VISIBLE_Y = 20

class Player():
    def __init__(self,name):
        self.name = name
        self.x = WIDTH//2
        self.y = HEIGHT//2
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
            
    
        
    
def draw_map(offset_x, offset_y, tile_size):
    for y in range(MAP_H):
        for x in range(MAP_W):
            screen_x = x * tile_size - offset_x
            screen_y = y * tile_size - offset_y
            if (x + y) % 2 == 0:
                color = (80, 80, 80)
            else:
                color = (40, 40, 40)

            pygame.draw.rect(screen,color,(screen_x, screen_y, tile_size, tile_size))


def draw():
    global offset_x, offset_y
    screen.fill("black")

    mouse_x, mouse_y = pygame.mouse.get_pos()   


    dx = mouse_x - player.x
    dy = mouse_y - player.y
    angle = math.atan2(dy, dx) 

    tile_size = screen.get_height() // BASE_TILES_VISIBLE_Y
    world_speed = tile_size * 0.1

    vx = math.cos(angle) * world_speed
    vy = math.sin(angle) * world_speed
    sx = -vy
    sy = vx

    
     
    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:  
        offset_x += vx
        offset_y += vy

    if keys[pygame.K_s]:   
        offset_x -= vx
        offset_y -= vy

    if keys[pygame.K_d]:   
        offset_x += sx
        offset_y += sy

    if keys[pygame.K_q]: 
        offset_x -= sx
        offset_y -= sy

    draw_map(offset_x, offset_y, tile_size)
    player.draw(angle)

def update():
    player.update()
    draw()
    

def main():
    global screen, player
    running = True
    player = Player("Joueur Test")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()    

        
if __name__ == "__main__":

    main()         