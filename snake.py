# GAME INFORMATION
title = 'Rainbow Snake'
version = '1.0'
creator = 'Erienne McCray'
copyright = '2022'

# IMPORT MODULES
import pygame
import pygame_menu
import random
import traceback
import os
import sys

with open('traceback template.txt', 'w+') as f:

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
        DARK_GREY = (50,50,50)
        GREY=(150,150,150)
        WHITE = (255, 255, 255)
        BROWN = (125,55,0)
        RED = (204,0,0)
        ORANGE = (230,145,56)
        YELLOW = (255,217,102)
        GREEN = (106,168,79)
        LIGHT_GREEN = (7,213,105)
        DARK_GREEN =(74,129,35)
        LIGHT_BLUE = (3,194,252)
        BLUE = (61,133,198)
        INDIGO=(55,61,174)
        PURPLE = (103,78,167)
        LAVENDER = (180,124,220)
        PINK = (242,78,175)

        monochrome_array = [WHITE]
        rainbow_array = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        original_rainbow = [PINK,RED,ORANGE,YELLOW,GREEN,LIGHT_BLUE,INDIGO,PURPLE]
        philly_array=[BLACK, BROWN, RED,ORANGE,YELLOW,GREEN,BLUE, INDIGO]
        trans_array = [LIGHT_BLUE, PINK, WHITE, PINK]
        asexual_array = [BLACK,GREY,WHITE,PURPLE]
        bi_array = [BLUE,PURPLE,PINK]
        nb_array = [YELLOW,WHITE,PURPLE,BLACK]
        genderqueer_array = [LAVENDER, WHITE, DARK_GREEN]
        pan_array = [PINK,YELLOW,LIGHT_BLUE]
        polysexual_array = [PINK,LIGHT_GREEN,LIGHT_BLUE]

        color_choice_list = [
            ("Pride Rainbow", rainbow_array),
            ("Original Rainbow", original_rainbow),
            ("Philly Rainbow", philly_array),
            ("Trans Flag", trans_array),
            ("Asexual Pride", asexual_array),
            ("Bi Flag", bi_array),
            ("Pan Flag", pan_array),
            ("Nonbinary", nb_array),
            ("Genderqueer", genderqueer_array),
            ("Polysexual", polysexual_array),
            ("Monochrome", monochrome_array)
            ]

        # ADDITIONAL VARIABLES
        grid_size = 30
        sprite_size = grid_size - 2
        max_x_tile = (WIDTH/grid_size) - 1
        max_y_tile = (HEIGHT/grid_size) - 1
        initial_speed = FPS/2

        colors_array = rainbow_array
        selection_effect = pygame_menu.widgets.LeftArrowSelection().copy()
        selection_effect_1 = selection_effect.copy().set_background_color(colors_array[0%len(colors_array)]).set_color(colors_array[0%len(colors_array)])
        selection_effect_2 = selection_effect.copy().set_background_color(colors_array[1%len(colors_array)]).set_color(colors_array[1%len(colors_array)])
        selection_effect_3 = selection_effect.copy().set_background_color(colors_array[2%len(colors_array)]).set_color(colors_array[2%len(colors_array)])
        selection_effect_4 = selection_effect.copy().set_background_color(colors_array[3%len(colors_array)]).set_color(colors_array[3%len(colors_array)])
        selection_effect_5 = selection_effect.copy().set_background_color(colors_array[4%len(colors_array)]).set_color(colors_array[4%len(colors_array)])
        selection_effect_6 = selection_effect.copy().set_background_color(colors_array[5%len(colors_array)]).set_color(colors_array[5%len(colors_array)])
        selection_effect_7 = selection_effect.copy().set_background_color(colors_array[6%len(colors_array)]).set_color(colors_array[6%len(colors_array)])
        selection_effect_8 = selection_effect.copy().set_background_color(colors_array[7%len(colors_array)]).set_color(colors_array[7%len(colors_array)])

        selection_dict = {
                0:selection_effect_1.set_background_color(colors_array[0%len(colors_array)]).set_color(colors_array[0%len(colors_array)]),
                1:selection_effect_2.set_background_color(colors_array[1%len(colors_array)]).set_color(colors_array[1%len(colors_array)]),
                2:selection_effect_3.set_background_color(colors_array[2%len(colors_array)]).set_color(colors_array[2%len(colors_array)]),
                3:selection_effect_4.set_background_color(colors_array[3%len(colors_array)]).set_color(colors_array[3%len(colors_array)]),
                4:selection_effect_5.set_background_color(colors_array[4%len(colors_array)]).set_color(colors_array[4%len(colors_array)]),
                5:selection_effect_6.set_background_color(colors_array[5%len(colors_array)]).set_color(colors_array[5%len(colors_array)]),
                6:selection_effect_7.set_background_color(colors_array[6%len(colors_array)]).set_color(colors_array[6%len(colors_array)]),
                7:selection_effect_8.set_background_color(colors_array[7%len(colors_array)]).set_color(colors_array[7%len(colors_array)]),
            }

        rainbow_theme = pygame_menu.themes.THEME_DARK.copy()
        rainbow_theme.background_color=DARK_GREY
        rainbow_theme.selection_color = DARK_GREY
        rainbow_theme.widget_font_color = DARK_GREY
        rainbow_theme.widget_selection_effect = selection_effect

        difficulty = 10
        immortal = False

        running = True
        paused = False

        # GROUPS AND ARRAYS
        all_sprites = pygame.sprite.Group()
        all_targets = pygame.sprite.Group()
        all_followers = pygame.sprite.Group()
        all_menus = []


        # CLASSES
        class Snake(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()

                self.name = "Player"

                self.size = sprite_size
                self.timer_max = initial_speed
                self.timer_current = self.timer_max
                self.paused = False
                self.blocked = False

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
                            if immortal:
                                self.blocked = True
                                if self.x_tile < 0:
                                    self.x_tile = 0
                                if self.x_tile > max_x_tile:
                                    self.x_tile = max_x_tile
                                if self.y_tile < 0:
                                    self.y_tile = 0
                                if self.y_tile > max_y_tile:
                                    self.y_tile = max_y_tile
                            else:
                                self.paused = True
                                GameOver(self)
                        else:
                            self.blocked = False

                        self.rect.topleft = ((self.x_tile*grid_size)+1, (self.y_tile*grid_size)+1)

                        self.timer_current = self.timer_max

                        target_collisions = pygame.sprite.spritecollide(self, all_targets, True)
                        for collision in target_collisions:
                            self.add_follower()
                            NewTarget()
                        
                        follower_collisions = pygame.sprite.spritecollide(self, all_followers, False)
                        for collision in follower_collisions:
                            if collision != all_followers.sprites()[0]:
                                if immortal:
                                    pass
                                else:
                                    self.paused = True
                                    GameOver(self)

                        for follower in all_followers.sprites():
                            if self.blocked:
                                pass
                            else:
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

                if self.timer_max >= FPS/difficulty:
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
            window.fill((DARK_GREY))
            all_sprites.draw(window)
            pygame.display.update()


        def SetColors(array, *args, **kwargs):
            new_colors = array[0][1]
            global colors_array
            colors_array = new_colors

            global selection_effect_1
            global selection_effect_2
            global selection_effect_3
            global selection_effect_4
            global selection_effect_5
            global selection_effect_6
            global selection_effect_7
            global selection_effect_8
            global selection_dict

            selection_dict = {
                0:selection_effect_1.set_background_color(colors_array[0%len(colors_array)]).set_color(colors_array[0%len(colors_array)]),
                1:selection_effect_2.set_background_color(colors_array[1%len(colors_array)]).set_color(colors_array[1%len(colors_array)]),
                2:selection_effect_3.set_background_color(colors_array[2%len(colors_array)]).set_color(colors_array[2%len(colors_array)]),
                3:selection_effect_4.set_background_color(colors_array[3%len(colors_array)]).set_color(colors_array[3%len(colors_array)]),
                4:selection_effect_5.set_background_color(colors_array[4%len(colors_array)]).set_color(colors_array[4%len(colors_array)]),
                5:selection_effect_6.set_background_color(colors_array[5%len(colors_array)]).set_color(colors_array[5%len(colors_array)]),
                6:selection_effect_7.set_background_color(colors_array[6%len(colors_array)]).set_color(colors_array[6%len(colors_array)]),
                7:selection_effect_8.set_background_color(colors_array[7%len(colors_array)]).set_color(colors_array[7%len(colors_array)]),
            }
            
            global all_menus
            menu_list = all_menus.copy()

            for menu in menu_list:
                my_submenus = menu.get_submenus()
                for submenu in my_submenus:
                    menu_list.append(submenu)

            for menu in menu_list:
                my_widgets = menu.get_widgets()
                for id, widget in enumerate(my_widgets):
                    widget_color = widget.get_font_info()['color']
                    widget.update_font(style = {"color":colors_array[id%len(colors_array)]})
                    widget.set_selection_effect(selection_dict[id%len(selection_dict)])


        def SetDifficulty(value, *args, **kwargs):
            new_difficulty = value[0][1]
            global difficulty
            difficulty = new_difficulty

        def SetImmortality(value, *args, **kwargs):
            global immortal
            immortal = value

        def NewTarget():
            target_x = (random.randint(0,max_x_tile)*grid_size)+2
            target_y = (random.randint(0,max_y_tile)*grid_size)+2
            target = TempTarget((target_x, target_y))

        def ResetGame():
            all_sprites.empty()
            all_targets.empty()
            all_followers.empty()

            global paused
            paused = False

            player.x_tile = round((WIDTH/grid_size)/2)
            player.y_tile = round((HEIGHT/grid_size)/2)
            player.rect.topleft = ((player.x_tile*grid_size)+1, (player.y_tile*grid_size)+1)
            player.timer_max = initial_speed
            player.timer_current = player.timer_max
            player.paused = False
            player.snake_length = 0
            player.image.fill(colors_array[0])

            all_sprites.add(player)

            NewTarget()
            PlayGame()

        def ResumeGame():
            global paused
            paused = False
            PlayGame()

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

            if high_score_display not in all_menus:
                all_menus.append(high_score_display)

            #scores_frame = high_score_display.add.frame_v(WIDTH-50, (HEIGHT/2)+2, max_height = int(HEIGHT/2))

            top_choice_frame = high_score_display.add.frame_h(WIDTH-50, 60)
            top_choice_frame.pack(
                high_score_display.add.button("Edit Scores", edit_scores_menu, font_color = colors_array[4%len(colors_array)]).set_selection_effect(selection_effect_5),
                align=pygame_menu.locals.ALIGN_LEFT
            )
            top_choice_frame.pack(
                high_score_display.add.button("Main Menu", menu.mainloop, window, font_color = colors_array[5%len(colors_array)]).set_selection_effect(selection_effect_6),
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
            
            global selec

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
                

            edit_scores_menu.add.button("Delete All Scores", are_you_sure, font_color = colors_array[0%len(colors_array)])
            edit_scores_menu.add.button("Back",pygame_menu.events.BACK, font_color = colors_array[1%len(colors_array)])

            are_you_sure.add.label("Are you sure you wish to delete all scores?", max_char=-1, font_color = colors_array[0%len(colors_array)])
            are_you_sure.add.label("This action cannot be undone!", max_char=-1, font_color = colors_array[1%len(colors_array)])
            are_you_sure.add.button("Yes", DeleteAllScores, font_color = colors_array[2%len(colors_array)]).set_selection_effect(selection_effect_3)
            are_you_sure.add.button("Back",pygame_menu.events.BACK, font_color = colors_array[3%len(colors_array)]).set_selection_effect(selection_effect_4)

            high_score_display.mainloop(window)
            

        def GameOver(player):
            game_over_menu = pygame_menu.Menu('Game Over', WIDTH, HEIGHT, theme = rainbow_theme, overflow=False)
            add_score_menu = pygame_menu.Menu('', WIDTH, HEIGHT, theme = rainbow_theme, overflow=False)
            score = player.snake_length*10

            if game_over_menu not in all_menus:
                all_menus.append(game_over_menu)
                

            game_over_menu.add.label("Your score is: %s"%score, max_char=-1, font_color = colors_array[0%len(colors_array)])
            game_over_menu.add.label("Would you like to record your high score?", max_char=-1, font_color = colors_array[1%len(colors_array)])
            game_over_menu.add.button("Yes", add_score_menu, font_color = colors_array[2%len(colors_array)]).set_selection_effect(selection_effect_3)
            game_over_menu.add.button("No", menu, font_color = colors_array[3%len(colors_array)]).set_selection_effect(selection_effect_4)
            game_over_menu.add.button("Quit", pygame_menu.events.EXIT, font_color = colors_array[4%len(colors_array)]).set_selection_effect(selection_effect_5)

            
            name_box = add_score_menu.add.text_input("Username: ", default=player.name, font_color = colors_array[0%len(colors_array)])
            add_score_menu.add.label("Score: %s"%score, font_color = colors_array[1%len(colors_array)])
            choice_frame = add_score_menu.add.frame_h(WIDTH, HEIGHT/2)
            choice_frame.pack(
                add_score_menu.add.button("Okay", AddHighScore, name_box, score, font_color = colors_array[2%len(colors_array)]).set_selection_effect(selection_effect_3),
                align=pygame_menu.locals.ALIGN_LEFT, margin=(2, 2)
            )
            choice_frame.pack(
                add_score_menu.add.button("Cancel", pygame_menu.events.BACK, font_color = colors_array[3%len(colors_array)]).set_selection_effect(selection_effect_4),
                align=pygame_menu.locals.ALIGN_RIGHT, margin=(2, 2)
            )

            game_over_menu.mainloop(window)


        # INITIALIZATION

        pygame.init()
        player = Snake()

        # Create window and define cclock
        window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title + "-" + version)
        clock = pygame.time.Clock()

        

        # GAME LOOP
        def PlayGame(*args):
            global running
            global paused

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
                                    paused = True
                                    pause_menu.mainloop(window)
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
        color_selector = settings_menu.add.selector("Colors:\t",items = color_choice_list, onchange=SetColors, onreturn=SetColors, font_color = colors_array[0%len(colors_array)]).set_selection_effect(selection_effect_1)
        difficulty_selector = settings_menu.add.selector("Difficulty:\t", items=[("Medium",10), ("Hard", FPS), ("Easy", 5)], onchange=SetDifficulty, onreturn=SetDifficulty, font_color = colors_array[1%len(colors_array)]).set_selection_effect(selection_effect_2)
        settings_menu.add.label("Changes the maximum speed at which the snake travels.", max_char=-1, font_size = 15)
        settings_menu.add.toggle_switch("Immortality:\t", default=False, onchange=SetImmortality, state_text=("Off", "On"), state_values=(False, True), font_color = colors_array[2%len(colors_array)]).set_selection_effect(selection_effect_3)
        settings_menu.add.label("With this setting on, you literally can't die.", max_char=-1, font_size = 15)
        settings_menu.add.button("Back",pygame_menu.events.BACK, font_color = colors_array[3%len(colors_array)]).set_selection_effect(selection_effect_4)
        

        about_menu = pygame_menu.Menu("About", WIDTH, HEIGHT, theme = rainbow_theme,)
        about_menu.add.label("Copyright 2022 Erienne McCray", max_char=-1, font_color = colors_array[0%len(colors_array)], font_size =  20)
        about_menu.add.label("Rainbow Snake was created in June of 2022 \nin celebration of Pride month, \nand distributed for free.", max_char=-1, font_color = colors_array[1%len(colors_array)], font_size =  20)
        about_menu.add.label("All proceeds from this game will be donated to Out & Equal, an LGBTQ+ charity that advocates for LGBTQ+ people to express their authentic identities in their workplaces.", max_char=-1, font_color = colors_array[2%len(colors_array)], font_size =  20)
        about_menu.add.label("Thank you for playing!",max_char=-1, font_color = colors_array[3%len(colors_array)], font_size =  25)
        about_menu.add.button("Back",pygame_menu.events.BACK, font_color = colors_array[4%len(colors_array)]).set_selection_effect(selection_effect_5)


        menu = pygame_menu.Menu('Rainbow Snake', WIDTH, HEIGHT, theme = rainbow_theme,)
        menu.add.button('Play', ResetGame, font_color = colors_array[0%len(colors_array)]).set_selection_effect(selection_effect_1)
        menu.add.button('High Scores', DisplayHighScores, font_color = colors_array[1%len(colors_array)]).set_selection_effect(selection_effect_2)
        menu.add.button('Help', font_color = colors_array[2%len(colors_array)]).set_selection_effect(selection_effect_3)
        menu.add.button('Settings', settings_menu, font_color = colors_array[3%len(colors_array)]).set_selection_effect(selection_effect_4)
        menu.add.button('About', about_menu, font_color = colors_array[4%len(colors_array)]).set_selection_effect(selection_effect_5)
        menu.add.button('Quit', pygame_menu.events.EXIT, font_color = colors_array[5%len(colors_array)]).set_selection_effect(selection_effect_6)

        if menu not in all_menus:
            all_menus.append(menu)

        pause_menu = pygame_menu.Menu('', WIDTH-200, HEIGHT-200, theme = rainbow_theme)
        pause_menu.add.button("Resume", ResumeGame, font_color = colors_array[0%len(colors_array)]).set_selection_effect(selection_effect_1)
        pause_menu.add.button("Exit to Main", GameOver, player, font_color = colors_array[1%len(colors_array)]).set_selection_effect(selection_effect_2)
        pause_menu.add.button("Quit", pygame_menu.events.EXIT, font_color = colors_array[2%len(colors_array)]).set_selection_effect(selection_effect_3)

        if pause_menu not in all_menus:
            all_menus.append(pause_menu)


        SetColors((('Classic Rainbow', colors_array), 1))
        menu.mainloop(window)

    except:
        traceback.print_exc(file=f)
        #pass