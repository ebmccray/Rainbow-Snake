# GAME INFORMATION
title = 'Rainbow Snake'
version = '1.0'
creator = 'Erienne McCray'
copyright = '2022'

# IMPORT MODULES:
import pygame
import pygame_menu
import random
import traceback
import os
import sys

#with open('traceback template.txt', 'w+') as f:

try:
    # DISTRIBUTION
    def resource_path(relative_path):
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

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
    LIGHT_BLUE = (3,194,252)
    BLUE = (61,133,198)
    INDIGO = (103,78,167)
    PINK = (242,78,175)

    monochrome_array = [WHITE]
    rainbow_array = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, PINK]
    trans_array = [LIGHT_BLUE, PINK, WHITE, PINK]

    color_choice_list = [
        ("Classic Rainbow", rainbow_array),
        ("Trans Flag", trans_array),
        ("Monochrome", monochrome_array),
        ]

    # ADDITIONAL VARIABLES
    grid_size = 30
    sprite_size = grid_size - 2
    max_x_tile = (WIDTH/grid_size) - 1
    max_y_tile = (HEIGHT/grid_size) - 1
    initial_speed = FPS/2
    rainbow_theme = pygame_menu.themes.THEME_DARK.copy()

    rainbow_transparent = rainbow_theme.copy()
    rainbow_transparent.set_background_color_opacity(0.5)

    colors_array = rainbow_array

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
            self.image.fill(colors_array[0])
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
                follower = Follower(self, colors_array[self.snake_length%len(colors_array)])
            else:
                follower = Follower(follower_list[-1], colors_array[self.snake_length%len(colors_array)])

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

            self.image.fill(color)
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

    def SetColors(array, **kwargs):
        new_colors = array[0][1]
        global colors_array
        colors_array = new_colors

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
        player.rect.topleft = ((player.x_tile*grid_size)+1, (player.y_tile*grid_size)+1)
        player.timer_max = initial_speed
        player.timer_current = player.timer_max
        player.paused = False
        player.snake_length = 0

        all_sprites.add(player)

        NewTarget()

    def AddHighScore(name_box, score):
        name = name_box.get_value()
        path = resource_path("assets/highscores.txt")
        
        scores_file = open(path,"a")
        scores_file.write("%s,%s\n"%(name, score))
        scores_file.close()
        
        DisplayHighScores()

    def DeleteAllScores():
        try: 
            path = resource_path("assets/highscores.txt")
            os.remove(path)
        except: 
            pass

        menu.mainloop(window)
        

    def DisplayHighScores():
        entry_height = 43

        try:
            path = resource_path("assets/highscores.txt")
            scores_file = open(path)
            scores_array = [x for x in scores_file]
            scores_file.close()
        except:
            scores_array = ["No scores to display,"]

        sort = lambda x : x.split(",")[1]

        scores_array.sort(key = sort, reverse = True)

        high_score_display = pygame_menu.Menu('High Scores', WIDTH, HEIGHT, theme = rainbow_theme)
        edit_scores_menu = pygame_menu.Menu('Edit Scores', WIDTH, HEIGHT, theme =rainbow_theme)
        are_you_sure = pygame_menu.Menu('Edit Scores', WIDTH, HEIGHT, theme = rainbow_theme)

        #scores_frame = high_score_display.add.frame_v(WIDTH-50, (HEIGHT/2)+2, max_height = int(HEIGHT/2))

        top_choice_frame = high_score_display.add.frame_h(WIDTH-50, 60)
        top_choice_frame.pack(
            high_score_display.add.button("Edit Scores", edit_scores_menu, font_color = colors_array[4%len(colors_array)]),
            align=pygame_menu.locals.ALIGN_LEFT
        )
        top_choice_frame.pack(
            high_score_display.add.button("Main Menu", menu.mainloop, window, font_color = colors_array[5%len(colors_array)]),
            align=pygame_menu.locals.ALIGN_RIGHT
        )

        titles_frame = high_score_display.add.frame_h(WIDTH-100, 60)
        #scores_frame.pack(titles_frame)

        titles_frame.pack(
            high_score_display.add.label("Username", font_color = colors_array[6%len(colors_array)],),
            align = pygame_menu.locals.ALIGN_LEFT,
        )
        titles_frame.pack(
            high_score_display.add.label("Score", font_color = colors_array[6%len(colors_array)],),
            align = pygame_menu.locals.ALIGN_RIGHT,
        )

        for id, entry in enumerate(scores_array):
            user = entry.split(",")[0]
            try:
                score = entry.split(",")[1]
            except:
                score = ""
            entry_frame = high_score_display.add.frame_h(WIDTH-100, entry_height)
            #scores_frame.pack(entry_frame)
            entry_frame.pack(
                high_score_display.add.label(user, font_size = 20, font_color = colors_array[id%len(colors_array)]),
                align=pygame_menu.locals.ALIGN_LEFT
            )
            entry_frame.pack(
                high_score_display.add.label(score, font_size = 20, font_color = colors_array[id%len(colors_array)]),
                align=pygame_menu.locals.ALIGN_RIGHT
            )
            
        '''choice_frame = high_score_display.add.frame_h(WIDTH-50, 100)
        choice_frame.pack(
            high_score_display.add.button("Edit Scores"),
            align=pygame_menu.locals.ALIGN_LEFT
        )
        choice_frame.pack(
            high_score_display.add.button("Main Menu", menu.mainloop, window),
            align=pygame_menu.locals.ALIGN_RIGHT
        )'''

        edit_scores_menu.add.button("Delete All Scores", are_you_sure, font_color = colors_array[0%len(colors_array)])
        edit_scores_menu.add.button("Back",pygame_menu.events.BACK, font_color = colors_array[1%len(colors_array)])

        are_you_sure.add.label("Are you sure you wish to delete all scores?", max_char=-1, font_color = colors_array[0%len(colors_array)])
        are_you_sure.add.label("This action cannot be undone!", max_char=-1, font_color = colors_array[1%len(colors_array)])
        are_you_sure.add.button("Yes", DeleteAllScores, font_color = colors_array[2%len(colors_array)])
        are_you_sure.add.button("Back",pygame_menu.events.BACK, font_color = colors_array[3%len(colors_array)])

        high_score_display.mainloop(window)
        

    def GameOver(player):
        hs_menu = pygame_menu.Menu('Game Over', WIDTH, HEIGHT, theme = rainbow_transparent, overflow=False)
        add_score_menu = pygame_menu.Menu('', WIDTH, HEIGHT, theme = rainbow_transparent, overflow=False)
        score = player.snake_length*10

        hs_menu.add.label("Your score is: %s"%score, max_char=-1, font_color = colors_array[0%len(colors_array)])
        hs_menu.add.label("Would you like to record your high score?", max_char=-1, font_color = colors_array[1%len(colors_array)])
        hs_menu.add.button("Yes", add_score_menu, font_color = colors_array[2%len(colors_array)])
        hs_menu.add.button("No", menu, font_color = colors_array[3%len(colors_array)])
        hs_menu.add.button("Quit", pygame_menu.events.EXIT, font_color = colors_array[4%len(colors_array)])

        
        name_box = add_score_menu.add.text_input("Username: ", default=player.name, font_color = colors_array[0%len(colors_array)])
        add_score_menu.add.label("Score: %s"%score, font_color = colors_array[1%len(colors_array)])
        choice_frame = add_score_menu.add.frame_h(WIDTH, HEIGHT/2)
        choice_frame.pack(
            add_score_menu.add.button("Okay", AddHighScore, name_box, score, font_color = colors_array[2%len(colors_array)]),
            align=pygame_menu.locals.ALIGN_LEFT, margin=(2, 2)
        )
        choice_frame.pack(
            add_score_menu.add.button("Cancel", pygame_menu.events.BACK, font_color = colors_array[3%len(colors_array)]),
            align=pygame_menu.locals.ALIGN_RIGHT, margin=(2, 2)
        )

        hs_menu.mainloop(window)


    # INITIALIZATION

    pygame.init()
    player = Snake()

    # Create window and define cclock
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(title + "-" + version)
    clock = pygame.time.Clock()

    # GAME LOOP
    def PlayGame():
        ResetGame()

        running = True
        paused = False

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
    settings_menu = pygame_menu.Menu('Settings', WIDTH, HEIGHT, theme = rainbow_theme,)
    settings_menu.add.label("Demonstration purposes only", font_color = colors_array[0%len(colors_array)])
    selector = settings_menu.add.selector("Colors:\t",items = color_choice_list, onchange=SetColors, onreturn=SetColors, font_color = colors_array[0%len(colors_array)])


    menu = pygame_menu.Menu('Rainbow Snake', WIDTH, HEIGHT, theme = rainbow_theme,)
    menu.add.button('Play', PlayGame, font_color = colors_array[0%len(colors_array)])
    menu.add.button('High Scores', DisplayHighScores, font_color = colors_array[1%len(colors_array)])
    menu.add.button('Help', font_color = colors_array[2%len(colors_array)])
    menu.add.button('Settings', font_color = colors_array[3%len(colors_array)])
    menu.add.button('About', font_color = colors_array[4%len(colors_array)])
    menu.add.button('Quit', pygame_menu.events.EXIT, font_color = colors_array[5%len(colors_array)])


    menu.mainloop(window)

except:
    #traceback.print_exc(file=f)
    pass