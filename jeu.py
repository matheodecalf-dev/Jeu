import pygame


pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((500, 600), pygame.RESIZABLE)
pygame.display.set_caption("jeu")

clock = pygame.time.Clock()

def main():
    global screen
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
        screen.fill("black")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()    

        
if __name__ == "__main__":

    main()         