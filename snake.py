# GAME INFORMATION
title = 'Rainbow Snake'
version = '1.0'
creator = 'Erienne McCray'
copyright = '2022'

# IMPORT MODULES:
from ast import Add
from ctypes import alignment
import pygame
import pygame_menu
from pygame_menu.widgets.core.selection import Selection
import random
import traceback

with open('traceback template.txt', 'w+') as f:

    try:
        # CONSTANTS:
        # Window and Game Variables:
        WIDTH = 450
        HEIGHT = 450
        FPS = 30

        # COLORS:
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (204,0,0)
        ORANGE = (230,145,56)
        YELLOW = (255,217,102)
        GREEN = (106,168,79)
        BLUE = (61,133,198)
        INDIGO = (103,78,167)
        PINK = (242,78,175)


        pride_array = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, PINK]

        # ADDITIONAL VARIABLES
        grid_size = 30
        sprite_size = grid_size - 2
        max_x_tile = (WIDTH/grid_size) - 1
        max_y_tile = (HEIGHT/grid_size) - 1
        initial_speed = FPS/2
        pride_colors = True
        rainbow_theme = pygame_menu.themes.THEME_DARK
        rainbow_theme.title_font_color = BLUE
        rainbow_theme.widget_font_color = GREEN

        rainbow_transparent = rainbow_theme
        rainbow_transparent.set_background_color_opacity(0.5)

        # GROUPS AND ARRAYS
        all_sprites = pygame.sprite.Group()
        all_targets = pygame.sprite.Group()
        all_followers = pygame.sprite.Group()


        # CLASSES
        class Snake(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()

                self.name = "Player"

                self.size = sprite_size
                self.timer_max = initial_speed
                self.timer_current = self.timer_max
                self.paused = False

                self.x_tile = round((WIDTH/grid_size)/2)
                self.y_tile = round((HEIGHT/grid_size)/2)
                self.prev_x_tile = self.x_tile
                self.prev_y_tile = self.y_tile

                self.image = pygame.Surface((self.size,self.size))
                if pride_colors:
                    self.image.fill(pride_array[0])
                else:
                    self.image.fill(WHITE)
                self.rect = self.image.get_rect(topleft = ((grid_size*self.x_tile)+1, (grid_size*self.y_tile)+1))

                self.snake_length = 0
                self.current_direction = pygame.K_RIGHT

            def update(self):
                self.prev_x_tile = self.x_tile
                self.prev_y_tile = self.y_tile

                if self.paused:
                    pass

                else: 
                    if self.timer_current <= 0:
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
                            self.paused = True
                            GameOver(self)

                        self.rect.topleft = ((self.x_tile*grid_size)+1, (self.y_tile*grid_size)+1)

                        self.timer_current = self.timer_max

                        target_collisions = pygame.sprite.spritecollide(self, all_targets, True)
                        for collision in target_collisions:
                            self.add_follower()
                            NewTarget()
                        
                        follower_collisions = pygame.sprite.spritecollide(self, all_followers, False)
                        for collision in follower_collisions:
                            if collision != all_followers.sprites()[0]:
                                self.paused = True
                                GameOver(self)

                        for follower in all_followers.sprites():
                            follower.move()

                    else:
                        self.timer_current -= 1
            
            def add_follower(self):
                follower_list = all_followers.sprites()
                self.snake_length += 1

                if self.snake_length <= 1:
                    follower = Follower(self, pride_array[self.snake_length%len(pride_array)])
                else:
                    follower = Follower(follower_list[-1], pride_array[self.snake_length%len(pride_array)])

                if self.timer_max >= FPS/10:
                    self.timer_max = int(self.timer_max*0.9)

                all_followers.add(follower)
                all_sprites.add(follower)

                
        class Follower(pygame.sprite.Sprite):
            def __init__(self, leader, color):
                super().__init__()
                self.size = sprite_size
                self.leader = leader

                self.x_tile = self.leader.x_tile
                self.y_tile = self.leader.y_tile
                self.prev_x_tile = self.x_tile
                self.prev_y_tile = self.y_tile

                self.image = pygame.Surface((self.size,self.size))
                if pride_colors:
                    self.image.fill(color)
                else:
                    self.image.fill(WHITE)
                self.rect = self.image.get_rect(topleft = ((grid_size*self.x_tile)+1, (grid_size*self.y_tile)+1))

            def move(self):
                #if player.timer_current == player.timer_max:
                    self.prev_x_tile = self.x_tile
                    self.prev_y_tile = self.y_tile

                    self.x_tile = self.leader.prev_x_tile
                    self.y_tile = self.leader.prev_y_tile

                    self.rect.topleft = ((self.x_tile*grid_size)+1, (self.y_tile*grid_size)+1)
                

        class Target(pygame.sprite.Sprite):
            def __init__(self, coord):
                super().__init__()

                self.size = sprite_size-2

                self.image = pygame.Surface((self.size,self.size))
                self.image.fill(WHITE)
                self.rect = self.image.get_rect(topleft = coord)

        class TempTarget(pygame.sprite.Sprite):
            def __init__(self, coord):
                super().__init__()

                self.size = sprite_size-2

                self.image = pygame.Surface((self.size,self.size))
                self.image.fill(BLACK)
                self.rect = self.image.get_rect(topleft = coord)

                collisions = pygame.sprite.spritecollide(self, all_followers, False)
                if len(collisions) == 0:
                    target = Target(self.rect.topleft)
                    all_sprites.add(target)
                    all_targets.add(target)
                else:
                    NewTarget()

        # FUNCTIONS
        # General Game Functions:
        def DrawGame():
            window.fill((BLACK))
            all_sprites.draw(window)
            pygame.display.update()

        def NewTarget():
            target_x = (random.randint(0,max_x_tile)*grid_size)+2
            target_y = (random.randint(0,max_y_tile)*grid_size)+2
            target = TempTarget((target_x, target_y))

        def ResetGame():
            all_sprites.empty()
            all_targets.empty()
            all_followers.empty()

            player.x_tile = round((WIDTH/grid_size)/2)
            player.y_tile = round((HEIGHT/grid_size)/2)
            player.timer_max = initial_speed
            player.timer_current = player.timer_max
            player.paused = False
            player.snake_length = 0

            all_sprites.add(player)

            NewTarget()

        def AddHighScore(name_box, score):
            name = name_box.get_value()
            DisplayHighScores()
            

        def DisplayHighScores():
            entry_height = 43

            try:
                scores_file = open("highscores.txt")
            except:
                menu.mainloop()

            scores_array = [x for x in scores_file]

            high_score_display = pygame_menu.Menu('High Scores', WIDTH, HEIGHT, theme = pygame_menu.themes.THEME_DARK)
            
            #scores_frame = high_score_display.add.frame_h(WIDTH, HEIGHT-200, max_width = WIDTH-1)

            scores_frame = high_score_display.add.frame_v(WIDTH-50, int(HEIGHT*0.7), max_height = int(HEIGHT/2))

            titles_frame = high_score_display.add.frame_h(WIDTH-100, 60)
            scores_frame.pack(titles_frame)

            titles_frame.pack(
                high_score_display.add.label("Username", font_color = PINK,),
                align = pygame_menu.locals.ALIGN_LEFT,
            )
            titles_frame.pack(
                high_score_display.add.label("Score", font_color = PINK,),
                align = pygame_menu.locals.ALIGN_RIGHT,
            )

            for id, entry in enumerate(scores_array):
                user = entry.split(",")[0]
                score = entry.split(",")[1]
                entry_frame = high_score_display.add.frame_h(WIDTH-100, entry_height)
                scores_frame.pack(entry_frame)
                entry_frame.pack(
                    high_score_display.add.label(user, font_size = 20, font_color = pride_array[id%len(pride_array)]),
                    align=pygame_menu.locals.ALIGN_LEFT
                )
                entry_frame.pack(
                    high_score_display.add.label(score, font_size = 20, font_color = pride_array[id%len(pride_array)]),
                    align=pygame_menu.locals.ALIGN_RIGHT
                )
                
            choice_frame = high_score_display.add.frame_h(WIDTH-50, 100)
            choice_frame.pack(
                high_score_display.add.button("Edit Scores"),
                align=pygame_menu.locals.ALIGN_LEFT
            )
            choice_frame.pack(
                high_score_display.add.button("Main Menu", menu.mainloop, window),
                align=pygame_menu.locals.ALIGN_RIGHT
            )

            high_score_display.mainloop(window)
           

        def GameOver(player):
            hs_menu = pygame_menu.Menu('Game Over', WIDTH, HEIGHT, theme = rainbow_transparent, overflow=False)
            add_score_menu = pygame_menu.Menu('', WIDTH, HEIGHT, theme = rainbow_transparent, overflow=False)
            score = player.snake_length*10

            hs_menu.add.label("Your score is: %s"%score, max_char=-1, font_color = RED)
            hs_menu.add.label("Would you like to record your high score?", max_char=-1, font_color = BLUE)
            hs_menu.add.button("Yes", add_score_menu)
            hs_menu.add.button("No", PlayGame)
            hs_menu.add.button("Quit", pygame_menu.events.EXIT)

            
            name_box = add_score_menu.add.text_input("Username: ", default=player.name)
            add_score_menu.add.label("Score: %s"%score)
            choice_frame = add_score_menu.add.frame_h(WIDTH, HEIGHT/2)
            choice_frame.pack(
                add_score_menu.add.button("Okay", AddHighScore, name_box, score),
                align=pygame_menu.locals.ALIGN_LEFT, margin=(2, 2)
            )
            choice_frame.pack(
                add_score_menu.add.button("Cancel", pygame_menu.events.BACK),
                align=pygame_menu.locals.ALIGN_RIGHT, margin=(2, 2)
            )

            hs_menu.mainloop(window)


        # INITIALIZATION

        pygame.init()
        player = Snake()
        ResetGame()

        # Create window and define cclock
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title + "-" + version)
        clock = pygame.time.Clock()

        # GAME LOOP
        def PlayGame():
            running = True
            paused = False

            ResetGame()

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
                                case pygame.K_SPACE:
                                    paused = not paused
                                case pygame.K_UP:
                                    if player.current_direction == pygame.K_LEFT or player.current_direction == pygame.K_RIGHT or player.snake_length == 0:
                                        player.current_direction = event.key
                                case pygame.K_DOWN:
                                    if player.current_direction == pygame.K_LEFT or player.current_direction == pygame.K_RIGHT or player.snake_length == 0:
                                        player.current_direction = event.key
                                case pygame.K_RIGHT:
                                    if player.current_direction == pygame.K_UP or player.current_direction == pygame.K_DOWN or player.snake_length == 0:
                                        player.current_direction = event.key
                                case pygame.K_LEFT:
                                    if player.current_direction == pygame.K_UP or player.current_direction == pygame.K_DOWN or player.snake_length == 0:
                                        player.current_direction = event.key

                # While not paused, run simulation
                if not paused:
                    all_sprites.update()

            
                DrawGame()

            pygame.QUIT


        # MENU CONFIGURATION
        menu = pygame_menu.Menu('Rainbow Snake', WIDTH, HEIGHT, theme = rainbow_theme)
        menu.add.button('Play', PlayGame)
        menu.add.button('High Scores', DisplayHighScores)
        menu.add.button('Quit', pygame_menu.events.EXIT)


        menu.mainloop(window)

    except:
        traceback.print_exc(file=f)