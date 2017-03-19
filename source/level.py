import pygame

import platforms
import guards
import entities
import healthbar
import text
import constants
import terrain
import os


class Level:

    # Sprites associated with the level

    platform_list = None
    cosmetic_list = None
    obstacle_list = None
    keypads = None
    bombs = None
    doors = None
    guards = None
    entities = None
    level_text = None
    ladders = None
    lasers = None

    player = None

    # Background image
    background = None

    # How far the level has scrolled
    world_shift_x = 0
    world_shift_y = 0
    at_edge_x = False
    at_edge_y = False

    start_x = 0
    start_y = 0

    def __init__(self, player):

        # Constructor

        self.platform_list = pygame.sprite.Group()
        self.cosmetic_list = pygame.sprite.Group()
        self.obstacle_list = pygame.sprite.Group()
        self.keypads = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.guards = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.level_text = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

        self.player = player

        self.keypad_array = []
        self.door_no = 0

        self.layer_range = 0

    def update(self):

        # Update everything in the level
        self.platform_list.update()
        self.cosmetic_list.update()
        self.obstacle_list.update()
        self.ladders.update()
        self.keypads.update()
        self.bombs.update()
        self.guards.update()
        self.entities.update()
        self.level_text.update()
        self.lasers.update()

    def draw(self, display):

        # Draw everything on this level
        display.fill(constants.BLACK)
        display.blit(self.background, (0, 0))

        # Draw the sights from cameras
        for laser in self.lasers.sprites():
            laser.draw(display)

        # Draw the sprite lists
        for layer in range(self.layer_range):

            platforms = [platform for platform in self.platform_list.sprites() if platform.layer == layer+1]
            for platform in platforms:
                platform.draw(display)

            cosmetics = [cosmetic for cosmetic in self.cosmetic_list.sprites() if cosmetic.layer == layer+1]
            for cosmetic in cosmetics:
                cosmetic.draw(display)

            obstacles = [obstacle for obstacle in self.obstacle_list.sprites() if obstacle.layer == layer+1]
            for obstacle in obstacles:
                obstacle.draw(display)

            ladders = [ladder for ladder in self.ladders.sprites() if ladder.layer == layer+1]
            for ladder in ladders:
                ladder.draw(display)

        self.level_text.draw(display)
        self.keypads.draw(display)
        self.bombs.draw(display)
        self.guards.draw(display)

        self.entities.draw(display)

    def shift_world(self, shift_x, shift_y):

        # Scroll the level left/right
        self.world_shift_x += shift_x

        self.at_edge_x = False
        # Set boundaries
        if self.world_shift_x >= 0:
            self.at_edge_x = True
            self.world_shift_x = 0

        elif self.world_shift_x <= -(960 + (960 - constants.SCREEN_WIDTH)):
            self.at_edge_x = True
            self.world_shift_x = -(960 + (960 - constants.SCREEN_WIDTH))

        if not self.at_edge_x:
            # Move everything in the level
            for platform in self.platform_list:
                platform.rect.x += shift_x
            for cosmetic in self.cosmetic_list:
                cosmetic.rect.x += shift_x
            for obstacle in self.obstacle_list:
                obstacle.rect.x += shift_x
            for ladder in self.ladders:
                ladder.rect.x += shift_x
            for keypad in self.keypads:
                keypad.rect.x += shift_x
            for bomb in self.bombs:
                bomb.rect.x += shift_x
            for guard in self.guards:
                guard.rect.x += shift_x
            for entity in self.entities:
                entity.rect.x += shift_x
            for text in self.level_text:
                text.rect.x += shift_x

        self.world_shift_y += shift_y

        self.at_edge_y = False
        if self.world_shift_y <= 0:
            self.at_edge_y = True
            self.world_shift_y = 0

        elif self.world_shift_y >= (720 + (720 - constants.SCREEN_HEIGHT)):
            self.at_edge_y = True
            self.world_shift_y = (720 + (720 - constants.SCREEN_HEIGHT))

        if not self.at_edge_y:
            # Move everything in the level
            for platform in self.platform_list:
                platform.rect.y -= shift_y
            for cosmetic in self.cosmetic_list:
                cosmetic.rect.y -= shift_y
            for obstacle in self.obstacle_list:
                obstacle.rect.y -= shift_y
            for ladder in self.ladders:
                ladder.rect.y -= shift_y
            for keypad in self.keypads:
                keypad.rect.y -= shift_y
            for bomb in self.bombs:
                bomb.rect.y -= shift_y
            for guard in self.guards:
                guard.rect.y -= shift_y
            for entity in self.entities:
                entity.rect.y -= shift_y
            for text in self.level_text:
                text.rect.y -= shift_y

    def reset_world(self):

        # Moves platforms back to their original position
        for platform in self.platform_list:
            platform.rect.x = platform.start_x
            platform.rect.y = platform.start_y

        for cosmetic in self.cosmetic_list:
            cosmetic.rect.x = cosmetic.start_x
            cosmetic.rect.y = cosmetic.start_y

        for obstacle in self.obstacle_list:
            obstacle.rect.x = obstacle.start_x
            obstacle.rect.y = obstacle.start_y

        for ladder in self.ladders:
            ladder.rect.x = ladder.start_x
            ladder.rect.y = ladder.start_y

        for keypad in self.keypads:
            keypad.rect.x = keypad.start_x
            keypad.rect.y = keypad.start_y

        for bomb in self.bombs:
            bomb.rect.x = bomb.start_x
            bomb.rect.y = bomb.start_y

        for guard in self.guards:
            guard.rect.x = guard.start_x
            guard.rect.y = guard.start_y

        for entity in self.entities:
            entity.rect.x = entity.start_x
            entity.rect.y = entity.start_y

        for text in self.level_text:
            text.rect.x = text.start_x
            text.rect.y = text.start_y

        self.world_shift_x = 0
        self.world_shift_y = 0

    def set_scrolling(self):

        self.shift_world(self.start_x, self.start_y)

    def create_platform(self, tile, x, y, layer):
        platform = platforms.Platform(tile, x, y, layer)
        self.platform_list.add(platform)

    def create_cosmetic(self, tile, x, y, layer):
        platform = platforms.Platform(tile, x, y, layer)
        self.cosmetic_list.add(platform)

    def create_obstacle(self, tile, x, y, layer):
        platform = platforms.Platform(tile, x, y, layer)
        self.obstacle_list.add(platform)

    def create_anim_obs(self, tile, x, y, layer):
        platform = platforms.AnimatedPlatform(tile, x, y, layer)
        self.obstacle_list.add(platform)

    def create_keypad(self, x, y):
        new_keypad = entities.Keypad(x, y)

        new_keypad.progress_bar = healthbar.ProgressBar()
        new_keypad.progress_bar.parent = new_keypad
        new_keypad.progress_bar.level = self
        new_keypad.progress_bar.rect.x = new_keypad.rect.centerx
        new_keypad.progress_bar.rect.y = new_keypad.rect.y - 20
        new_keypad.progress_bar.start_x = new_keypad.progress_bar.rect.x
        new_keypad.progress_bar.start_y = new_keypad.progress_bar.rect.y
        self.entities.add(new_keypad.progress_bar)

        self.keypads.add(new_keypad)
        self.keypad_array.append(new_keypad)

    def create_bomb(self, x, y):
        new_bomb = entities.Bomb(x, y)

        new_bomb.progress_bar = healthbar.ProgressBar()
        new_bomb.progress_bar.parent = new_bomb
        new_bomb.progress_bar.level = self
        self.entities.add(new_bomb.progress_bar)

        self.bombs.add(new_bomb)

    def create_door(self, tile, x, y, layer):
        new_door = entities.Door(tile, x, y, layer)

        new_door.level = self
        new_door.door_no = self.door_no

        self.platform_list.add(new_door)
        self.doors.add(new_door)

    def create_guard(self, x, y):
        new_guard = guards.Guard(x, y)

        new_guard.level = self
        new_guard.player = self.player
        self.entities.add(new_guard.torch)

        self.guards.add(new_guard)

    def create_hguard(self, x, y):
        new_hguard = guards.HostileGuard(x, y)

        new_hguard.level = self
        new_hguard.player = self.player
        self.entities.add(new_hguard.arm)

        self.guards.add(new_hguard)

    def create_ladder(self, tile, x, y, layer):
        new_ladder = platforms.Platform(tile, x, y, layer)
        self.ladders.add(new_ladder)

    def create_camera(self, tile, x, y):
        new_camera = entities.Camera(x, y, tile, self)
        new_laser = entities.Laser(new_camera, self.player)
        new_camera.laser = new_laser
        new_camera.camera_no = self.door_no

        self.entities.add(new_camera)
        self.lasers.add(new_laser)

    def render(self, data):

        self.door_no = 0
        self.keypad_array = []

        layer = 1
        n = 0
        for tile in data:
            position = tile[0]
            tile_data = tile[1]

            if 'type' not in tile_data:
                print(tile)

            if tile_data['type'] == "Door":
                self.door_no += 1
                if 35 < tile_data['tile'] < 38:
                    self.create_camera(platforms.platforms[tile_data['tile']-1],
                                       position[0]*24, position[1]*24)
                else:
                    self.create_door(platforms.platforms[tile_data['tile']-1],
                                     position[0]*24, position[1]*24, layer)

            elif tile_data['type'] == "Entity":

                if tile_data['tile'] == 40:
                    self.create_keypad((position[0]*24)+6, (position[1]*24)+5)

                elif tile_data['tile'] == 38:
                    self.create_guard(position[0]*24, (position[1]*24)-24)

                elif tile_data['tile'] == 41:
                    self.create_bomb(position[0]*24, position[1]*24)

                elif tile_data['tile'] == 42:
                    self.create_hguard(position[0]*24, (position[1]*24)-24)

            elif tile_data['type'] == "Solid":
                if tile_data['tile'] == 26:
                    self.create_platform(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, (position[1]*24)+20, layer)
                else:
                    self.create_platform(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)

            elif tile_data['type'] == "Cosmetic":
                if tile_data['tile'] == 25:
                    self.create_ladder(platforms.platforms[tile_data['tile']-1],
                                       position[0]*24, position[1]*24, layer)
                else:
                    self.create_cosmetic(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)

            elif tile_data['type'] == "Obstacle":
                if tile_data['tile'] == 23:
                    self.create_anim_obs(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)
                else:
                    self.create_obstacle(platforms.platforms[tile_data['tile']-1],
                                         position[0]*24, position[1]*24, layer)
            n += 1
            if n % 4800 == 0:
                layer += 1


class Level01(Level):

    def __init__(self, player, write_data=False, fast=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level1.json")
        tile_file = os.path.join("level_data", "layouts", "level1")
        type_file = os.path.join("level_data", "tile_types", "level1")

        # How many layers the level has
        self.layer_range = 2

        level = terrain.LevelData(save_file, tile_file, type_file, "level1")
        if write_data:
            level.write_data(fast)

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)

        # Add the level text
        level_text = text.LevelText("Left/right arrows or A/D to walk", 48, 960)
        self.level_text.add(level_text)
        level_text = text.LevelText("Up arrow or W to jump", 48, 990)
        self.level_text.add(level_text)
        level_text = text.LevelText("Don't fall!", 615, 600)
        self.level_text.add(level_text)
        level_text = text.LevelText("Nearly there...", 975, 600)
        self.level_text.add(level_text)
        level_text = text.LevelText("Down we go", 1750, 450)
        self.level_text.add(level_text)

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level02(Level):

    def __init__(self, player, write_data=False, fast=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level2.json")
        tile_file = os.path.join("level_data", "layouts", "level2")
        type_file = os.path.join("level_data", "tile_types", "level2")

        # How many layers the level has
        self.layer_range = 2

        self.door_linkup = {0: 1,
                            1: 1,
                            2: 0,
                            3: 0,
                            4: 2,
                            5: 2,
                            6: 2,
                            7: 2,
                            8: 2}

        level = terrain.LevelData(save_file, tile_file, type_file, "level2")
        if write_data:
            level.write_data(fast)

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("Watch out for the acid!", 100, 1300)
        self.level_text.add(level_text)
        level_text = text.LevelText("Nice!", 850, 1150)
        self.level_text.add(level_text)
        level_text = text.LevelText("This is tricky,", 50, 860)
        self.level_text.add(level_text)
        level_text = text.LevelText("good luck!", 50, 885)
        self.level_text.add(level_text)
        level_text = text.LevelText("Almost there...", 100, 435)
        self.level_text.add(level_text)
        level_text = text.LevelText("Use space bar to hack the keypad.", 360, 50)
        self.level_text.add(level_text)
        level_text = text.LevelText("Once the keypad is hacked,", 360, 75)
        self.level_text.add(level_text)
        level_text = text.LevelText("the door will open.", 360, 100)
        self.level_text.add(level_text)
        level_text = text.LevelText("And again", 585, 270)
        self.level_text.add(level_text)
        level_text = text.LevelText("Jump!", 800, 370)
        self.level_text.add(level_text)
        level_text = text.LevelText("Congrats!", 1150, 700)
        self.level_text.add(level_text)
        level_text = text.LevelText("Choose your path", 1300, 625)
        self.level_text.add(level_text)

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level03(Level):

    def __init__(self, player, write_data=False, fast=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        save_file = os.path.join("level_data", "level3.json")
        tile_file = os.path.join("level_data", "layouts", "level3")
        type_file = os.path.join("level_data", "tile_types", "level3")

        # How many layers the level has
        self.layer_range = 2

        self.door_linkup = {0: 0,
                            1: 0}

        level = terrain.LevelData(save_file, tile_file, type_file, "level3")
        if write_data:
            level.write_data(fast)

        # Load the data
        level_data = level.load_data()

        # Then render
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("Watch out for the guards!", 110, 1075)
        self.level_text.add(level_text)
        level_text = text.LevelText("They're searching with torches,", 110, 1100)
        self.level_text.add(level_text)
        level_text = text.LevelText("Make sure they don't catch you!", 110, 1125)
        self.level_text.add(level_text)
        level_text = text.LevelText("Try to find a way to get past the guard.", 110, 1150)
        self.level_text.add(level_text)
        level_text = text.LevelText("Press the jump key", 700, 1300)
        self.level_text.add(level_text)
        level_text = text.LevelText("to climb ladders!", 700, 1325)
        self.level_text.add(level_text)
        level_text = text.LevelText("Here's another guard.", 500, 900)
        self.level_text.add(level_text)
        level_text = text.LevelText("Let go to slide down ladders.", 800, 800)
        self.level_text.add(level_text)
        level_text = text.LevelText("These are tricky jumps!", 1120, 1355)
        self.level_text.add(level_text)
        level_text = text.LevelText("Press your crouch key", 1635, 1060)
        self.level_text.add(level_text)
        level_text = text.LevelText("to slide through", 1635, 1085)
        self.level_text.add(level_text)
        level_text = text.LevelText("tight spaces.", 1635, 1110)
        self.level_text.add(level_text)
        level_text = text.LevelText("Jump onto", 1200, 875)
        self.level_text.add(level_text)
        level_text = text.LevelText("the ladders.", 1200, 900)
        self.level_text.add(level_text)
        level_text = text.LevelText("You can also crouch", 920, 350)
        self.level_text.add(level_text)
        level_text = text.LevelText("under torches!", 920, 375)
        self.level_text.add(level_text)
        level_text = text.LevelText("Good job!", 200, 200)
        self.level_text.add(level_text)
        level_text = text.LevelText("Watch out here...", 1275, 425)
        self.level_text.add(level_text)

        # Set start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to start position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level04(Level):

    def __init__(self, player, write_data=False, fast=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        self.save_file = os.path.join("level_data", "level4.json")
        self.tile_file = os.path.join("level_data", "layouts", "level4")
        self.type_file = os.path.join("level_data", "tile_types", "level4")

        # How many layers the level has
        self.layer_range = 2

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 0,
                            3: 1,
                            4: 1}

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level4")

        if write_data:
            level.write_data(fast)

        # Load the data
        level_data = level.load_data()

        # Render it
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Add the level text
        level_text = text.LevelText("Up we go!", 80, 1060)
        self.level_text.add(level_text)
        level_text = text.LevelText("Crawl through ventilation shafts", 144, 90)
        self.level_text.add(level_text)
        level_text = text.LevelText("Doors aren't", 664, 130)
        self.level_text.add(level_text)
        level_text = text.LevelText("always vertical", 664, 155)
        self.level_text.add(level_text)
        level_text = text.LevelText("Slide through here!", 588, 476)
        self.level_text.add(level_text)
        level_text = text.LevelText("You'll need to hang about on these ladders.", 1200, 1350)
        self.level_text.add(level_text)
        level_text = text.LevelText("Here's some complex jumps", 1500, 700)
        self.level_text.add(level_text)

        # Set the start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to the starting position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level05(Level):

    def __init__(self, player, write_data=False, fast=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png").convert()

        self.save_file = os.path.join("level_data", "level5.json")
        self.tile_file = os.path.join("level_data", "layouts", "level5")
        self.type_file = os.path.join("level_data", "tile_types", "level5")

        # How many layers the level has
        self.layer_range = 2

        self.door_linkup = {0: 0,
                            1: 0,
                            2: 1,
                            3: 1,
                            4: 2,
                            5: 2}

        level = terrain.LevelData(self.save_file, self.type_file, self.type_file, "level5")

        if write_data:
            level.write_data(fast)

        # Load the data
        level_data = level.load_data()

        # Then render it
        self.render(level_data)
        for door in self.doors.sprites():
            door.set_keypad()

        # Set the start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to the starting position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)


class Level06(Level):

    def __init__(self, player, write_data=False, fast=False):

        # Call the parents constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background.png")

        self.save_file = os.path.join("level_data", "level6.json")
        self.tile_file = os.path.join("level_data", "layouts", "level6")
        self.type_file = os.path.join("level_data", "tile_types", "level6")

        # How many layers the level has
        self.layer_range = 1

        level = terrain.LevelData(self.save_file, self.tile_file, self.type_file, "level6")

        if write_data:
            level.write_data(fast)

        # Load the data
        level_data = level.load_data()

        # Then render it
        self.render(level_data)

        # Set the start position
        self.start_x = 0
        self.start_y = 719

        # Scroll to the starting position
        self.reset_world()
        self.shift_world(self.start_x, self.start_y)
