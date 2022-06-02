# GAME INFORMATION
title = 'Snake'
version = '1.0'
creator = 'Erienne McCray'
copyright = '2022'

# IMPORT MODULES:
import pygame
import random
import traceback

with open('traceback template.txt', 'w+') as f:

    try:
        # CONSTANTS:
        # Window and Game Variables:
        WIDTH = 300
        HEIGHT = 300
        FPS = 3

        # COLORS:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        YELLOW = (255, 255, 0)
        CYAN = (0, 255, 255)
        MAGENTA = (255, 0, 255)

        # ADDITIONAL VARIABLES

        # GROUPS AND ARRAYS
        all_sprites = pygame.sprite.Group()

        # CLASSES

        class Snake(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()

                self.size = 10

                self.image = pygame.Surface((self.size,self.size))
                self.image.fill(WHITE)
                self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT/2))

                self.snake_length = 0
                self.current_direction = pygame.K_LEFT

            def update(self):
                match self.current_direction:
                    case pygame.K_UP:
                        self.rect.centery -= self.size
                    case pygame.K_DOWN:
                        self.rect.centery += self.size
                    case pygame.K_LEFT:
                        self.rect.centerx -= self.size
                    case pygame.K_RIGHT:
                        self.rect.centerx += self.size
                

        # FUNCTIONS
        # General Game Functions:
        def DrawGame():
            window.fill((BLACK))
            all_sprites.draw(window)
            pygame.display.update()

        # INITIALIZATION
        pygame.init()
        player = Snake()
        all_sprites.add(player)

        # Create window and define cclock
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title + "-" + version)
        clock = pygame.time.Clock()

        # SIM LOOP
        running = True
        paused = False

        # Set-up before game runs

        while running:
            # Set FPS
            clock.tick(FPS)

            # Check for user input
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_RETURN:
                                pass
                            case pygame.K_SPACE:
                                paused = not paused
                            case pygame.K_UP:
                                player.current_direction = event.key
                            case pygame.K_DOWN:
                                player.current_direction = event.key
                            case pygame.K_RIGHT:
                                player.current_direction = event.key
                            case pygame.K_LEFT:
                                player.current_direction = event.key

            # While not paused, run simulation
            if not paused:
                all_sprites.update()

        
            DrawGame()

        pygame.QUIT

    except:
        traceback.print_exc(file=f)