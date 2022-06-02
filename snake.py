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
        FPS = 60

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

        # FUNCTIONS
        # General Game Functions:
        def DrawGame():
            window.fill((BLACK))
            all_sprites.draw(window)
            pygame.display.update()

        # INITIALIZATION
        pygame.init()

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
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_RETURN:
                        pass
                    elif key == pygame.K_SPACE:
                        paused = not paused

            # While not paused, run simulation
            if not paused:
                all_sprites.update()

        
            DrawGame()

        pygame.QUIT

    except:
        traceback.print_exc(file=f)