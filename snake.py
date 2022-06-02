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
        WIDTH = 310
        HEIGHT = 310
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
        size = 10
        max_x_tile = (WIDTH/size) - 1
        max_y_tile = (HEIGHT/size) - 1

        # GROUPS AND ARRAYS
        all_sprites = pygame.sprite.Group()
        

        # CLASSES


        class Snake(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()

                self.size = size
                self.x_tile = round((WIDTH/self.size)/2)
                self.y_tile = round((HEIGHT/self.size)/2)

                print(self.x_tile, self.y_tile)

                self.image = pygame.Surface((self.size,self.size))
                self.image.fill(WHITE)
                self.rect = self.image.get_rect(topleft = (self.size*self.x_tile, self.size*self.y_tile))

                self.snake_length = 0
                self.current_direction = pygame.K_RIGHT

            def update(self):
                match self.current_direction:
                    case pygame.K_UP:
                        self.y_tile -= 1
                    case pygame.K_DOWN:
                        self.y_tile += 1
                    case pygame.K_LEFT:
                        self.x_tile -= 1
                    case pygame.K_RIGHT:
                        self.x_tile += 1

                if self.x_tile < 0 or self.x_tile > max_x_tile or self.y_tile < 0 or self.y_tile > max_y_tile:
                    ResetGame()

                self.rect.topleft = (self.x_tile*self.size, self.y_tile*self.size)
        
        class Target(pygame.sprite.Sprite):
            def __init__(self, coord):
                super().__init__()

                self.size = size

                self.image = pygame.Surface((self.size,self.size))
                self.image.fill(WHITE)
                self.rect = self.image.get_rect(topleft = coord)

        # FUNCTIONS
        # General Game Functions:
        def DrawGame():
            window.fill((BLACK))
            all_sprites.draw(window)
            pygame.display.update()

        def NewTarget():
            target_x = random.randint(0,max_x_tile)*size
            target_y = random.randint(0,max_y_tile)*size
            target = Target((target_x, target_y))
            all_sprites.add(target)

        def ResetGame():
            all_sprites.empty()
            player.x_tile = round((WIDTH/size)/2)
            player.y_tile = round((HEIGHT/size)/2)
            all_sprites.add(player)
            NewTarget()

        # INITIALIZATION

        pygame.init()
        player = Snake()
        ResetGame()

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