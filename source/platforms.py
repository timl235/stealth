import pygame
import spritesheet

# This is the location of each tile on the spritesheet
GROUND1 = (0, 0, 24, 24)
GROUND2 = (24, 0, 24, 24)
GROUND3 = (48, 0, 24, 24)
GROUND4 = (72, 0, 24, 24)
GROUND5 = (96, 0, 24, 24)
GROUND6 = (120, 0, 24, 24)
GROUND7 = (144, 0, 24, 24)
GROUND8 = (168, 0, 24, 24)
GROUND9 = (0, 24, 24, 24)
GROUND10 = (24, 24, 24, 24)
GROUND11 = (48, 24, 24, 24)
GROUND12 = (72, 24, 24, 24)
GROUND13 = (96, 24, 24, 24)
GROUND14 = (120, 24, 24, 24)
GROUND15 = (144, 24, 24, 24)
GROUND16 = (168, 24, 24, 24)
CRATE = (0, 48, 24, 24)
GIRDER1 = (24, 48, 24, 24)
GIRDER2 = (48, 48, 24, 24)
GIRDER3 = (72, 48, 24, 24)
LAMP = (120, 48, 24, 24)
CHAIN = (144, 48, 24, 24)
ACID_TOP = (
    (168, 48, 24, 24),
    (168, 72, 24, 24)
)
ACID = (144, 72, 24, 24)
LADDER = (124, 72, 16, 24)
VENT_BOTTOM = (0, 72, 24, 4)
VENT_TOP = (24, 92, 24, 4)
VENT = (48, 72, 24, 24)
BACKGROUND = (72, 72, 24, 24)
BACKGROUND_GIRDER1 = (96, 72, 24, 24)
BACKGROUND_CRATE = (0, 96, 24, 24)
DOOR = (96, 48, 24, 24)
DOOR_HORIZONTAL = (24, 96, 24, 24)
BACKGROUND_GIRDER2 = (48, 96, 24, 24)
BACKGROUND_GIRDER3 = (72, 96, 24, 24)
CAMERA1 = (96, 96, 24, 24)
CAMERA2 = (120, 96, 24, 24)
POWER_SUPPLY = (144, 96, 24, 48)
MEDIUM_CRATE = (0, 120, 24, 24)
SAND = (24, 120, 24, 24)
SKY = (0, 0, 480, 2304)

# A tuple of all the platforms
platforms = (
    GROUND1, GROUND2, GROUND3, GROUND4, GROUND5,
    GROUND6, GROUND7, GROUND8, GROUND9, GROUND10,
    GROUND11, GROUND12, GROUND13, GROUND14, GROUND15,
    GROUND16, CRATE, GIRDER1, GIRDER2, GIRDER3,
    LAMP, CHAIN, ACID_TOP, ACID, LADDER, VENT_TOP,
    VENT_BOTTOM, VENT, BACKGROUND, BACKGROUND_GIRDER1,
    BACKGROUND_CRATE, DOOR, DOOR_HORIZONTAL,
    BACKGROUND_GIRDER2, BACKGROUND_GIRDER3,
    POWER_SUPPLY, MEDIUM_CRATE, SAND, SKY, CAMERA1,
    CAMERA2
)


class Platform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data, x, y, layer=1):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")

        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        # The layer the tile is in
        self.layer = layer

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class AnimatedPlatform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data, x, y, layer=1):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = spritesheet.SpriteSheet("resources/terrain.png")

        self.images = []

        # Take the image for each frame from the spritesheet
        # And add it to the list of frames

        for sprite in sprite_sheet_data:
            new_image = self.sprite_sheet.get_image(sprite[0],
                                                    sprite[1],
                                                    sprite[2],
                                                    sprite[3])
            self.images.append(new_image)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.start_x = x
        self.start_y = y

        # A timer var for animation

        self.tick = 0
        self.frame = 0

        # The layer the tile is in
        self.layer = layer

    def update(self):

        self.tick += 1
        # Change the image when ready
        if self.tick % 10 == 0:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]

    def draw(self, display):

        # Draw to the display
        display.blit(self.image, (self.rect.x, self.rect.y))
