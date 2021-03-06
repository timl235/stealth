import pygame
from pygame.locals import *

import game as g
import spritesheet
import text
import constants


class Button(pygame.sprite.Sprite):

    # Generic button class
    # This can be used for any button on the menu

    def __init__(self, sprite_sheet, sprite_sheet_data, x, y, command):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        # Set the sprites images
        self.sprite_sheet = spritesheet.SpriteSheet(sprite_sheet)

        self.image_inactive = self.sprite_sheet.get_image_srcalpha(sprite_sheet_data[0][0],
                                                                   sprite_sheet_data[0][1],
                                                                   sprite_sheet_data[0][2],
                                                                   sprite_sheet_data[0][3])

        self.image_active = self.sprite_sheet.get_image_srcalpha(sprite_sheet_data[1][0],
                                                                 sprite_sheet_data[1][1],
                                                                 sprite_sheet_data[1][2],
                                                                 sprite_sheet_data[1][3])

        self.image = self.image_inactive

        # Correct the sprites position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set the command
        self.command = command

    def update(self):

        # Get the mouse pointer position
        mouse_pos = pygame.mouse.get_pos()

        # Check if the mouse is touching the button
        touching_pointer = self.rect.collidepoint(mouse_pos)
        if touching_pointer:  # If it is then switch the image
            if self.image != self.image_active:
                self.image = self.image_active
        else:
            if self.image != self.image_inactive:
                self.image = self.image_inactive


class Menu:

    # This is the games menu

    def __init__(self, parent):

        # Assign attributes from input
        self.parent = parent

        # Set the display to draw to and the clock for timing
        self.display = parent.game_display
        self.clock = parent.clock

        # Set the background
        self.background_large = pygame.image.load("resources/menubackground.png").convert()
        self.background_small = pygame.image.load("resources/menubackgroundsmall.png").convert()

        self.background = self.background_large

        # Create the content of the menu
        self.play_button = Button("resources/menubuttons.png", ((0, 0, 360, 80), (360, 0, 360, 80)),
                                  300, 426, lambda: self.game.run(True))
        self.quit_button = Button("resources/menubuttons.png", ((0, 80, 360, 80), (360, 80, 360, 80)),
                                  262, 502, "quit")
        self.continue_button = Button("resources/menubuttons.png", ((0, 160, 360, 80), (360, 160, 360, 80)),
                                      338, 350, lambda: self.game.run(False))

        self.title_big = text.Text("Stealth", 200, 165, 100)
        self.title_small = text.Text("Stealth", 150, 124, 80)

        # Fill the group with everything on that screen of the menu
        self.main_menu = pygame.sprite.Group()
        self.main_menu.add(self.play_button)
        self.main_menu.add(self.quit_button)
        self.main_menu.add(self.continue_button)
        self.main_menu.add(self.title_big)

        # The screen that is currently displayed
        self.current_screen = None

        # Lag mode
        self.lagging = False

        if self.parent.small:
            self.toggle_lag()

        # Create an instance of the game class
        self.game = g.Game(self)

    def run(self):

        # Load the music
        pygame.mixer.music.load("resources/menu_music.mp3")
        pygame.mixer.music.set_volume(0.75)

        # Set the current screen
        self.current_screen = self.main_menu

        # Play the music
        pygame.mixer.music.play(-1)

        game_exit = False

        while not game_exit:

            # Event loop
            for event in pygame.event.get():
                if event.type == QUIT:  # Quit closes the application
                    game_exit = True

                if event.type == MOUSEBUTTONUP:

                    if event.button == 1:
                        # Check if any buttons were clicked
                        mouse_pos = pygame.mouse.get_pos()

                        buttons_clicked = [x for x in self.current_screen if x.rect.collidepoint(mouse_pos)
                                           and isinstance(x, Button)]

                        for button in buttons_clicked:
                            if button.command is not None:

                                # Execute the buttons command

                                if button.command == "quit":  # Special case for quitting game
                                    game_exit = True

                                else:
                                    button.command()

            # Update the sprites
            self.current_screen.update()

            # Draw to the display
            self.display.fill(constants.BLACK)
            self.display.blit(self.background, (0, 0))

            self.current_screen.draw(self.display)

            # Update and limit to 60fps
            pygame.display.update()
            self.clock.tick(60)

        pygame.mouse.set_visible(False)

    def toggle_lag(self):

        # This re-sizes the screen
        # and realigns the menu to still look correct even on the smaller display size

        if not self.lagging:
            self.lagging = True
            self.display = self.parent.set_screen_size(720, 540)
            self.background = self.background_small
            self.main_menu.remove(self.title_big)
            self.main_menu.add(self.title_small)

            self.play_button.rect.topleft = (180, 346)
            self.quit_button.rect.topleft = (142, 422)
            self.continue_button.rect.topleft = (218, 270)

        else:
            self.lagging = False
            self.display = self.parent.set_screen_size(960, 720)
            self.background = self.background_large
            self.main_menu.remove(self.title_small)
            self.main_menu.add(self.title_big)

            self.play_button.rect.topleft = (300, 426)
            self.quit_button.rect.topleft = (262, 502)
            self.continue_button.rect.topleft = (338, 350)
