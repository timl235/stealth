import pygame
import spritesheet
import math
import random


class Arm(pygame.sprite.Sprite):

    sprite_sheet = None

    guard = None

    def __init__(self, guard):

        # Constructor
        pygame.sprite.Sprite.__init__(self)

        # Load the image
        self.sprite_sheet = spritesheet.SpriteSheet("resources/arms.png")

        self.arm_right = self.sprite_sheet.get_image(0, 0, 28, 12)
        self.arm_left = self.sprite_sheet.get_image(0, 12, 28, 12)

        self.image = self.arm_right

        self.guard = guard

        # Set a reference to the images rectangle
        self.rect = self.image.get_rect()

        self.rect.x = self.guard.rect.x + self.guard.rect.width / 4
        self.rect.y = self.guard.rect.y + self.guard.rect.height / 4

        self.start_x = self.rect.x
        self.start_y = self.rect.y

        self.degrees = 0
        self.counter = random.randrange(85, 115)

        # Sounds the guard makes
        self.gunshot_sound = self.guard.level.sound_engine.gunshot_sound
        self.shell_sound = self.guard.level.sound_engine.shell_sound
        self.shell_sound.set_volume(0.5)

        self.drop_delay = 0
        self.played_dropped = True

    def update(self):

        # Position the arm
        if self.guard.direction == "R":
            self.rect.x = self.guard.rect.x + self.guard.rect.width / 4
        else:
            self.rect.x = self.guard.rect.x + self.guard.rect.width * -0.4
        self.rect.y = self.guard.rect.y + self.guard.rect.height / 4

        if self.guard.direction == "R":
            self.image = self.arm_right
        else:
            self.image = self.arm_left

        # Calculate the angle at which to point at

        dx = self.guard.rect.x - self.guard.player.rect.x
        dy = self.guard.rect.y - self.guard.player.rect.y

        # Use trig to calculate the angle
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        self.degrees = math.degrees(rads)
        self.degrees = (self.degrees + 180) % 360

        # Rotate the image and reset the rect
        self.image = pygame.transform.rotate(self.image, self.degrees)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Align rectangle after rotation
        if self.degrees > 180:
            self.rect.top = self.guard.rect.y + (self.guard.rect.height * 0.25)
        else:
            self.rect.bottom = self.guard.rect.y + (self.guard.rect.height * 0.5)
        if self.guard.direction == "R":
            self.rect.left = self.guard.rect.left + self.guard.rect.width * 0.2
        else:
            self.rect.right = self.guard.rect.right - self.guard.rect.width * 0.2

        # If the guard is close enough to the player
        if self.guard.dist_to(self.guard.player.rect.x, self.guard.player.rect.y) < self.guard.follow_dist:
            if self.counter > 0:
                self.counter -= 1
            else:
                # Shoot a bullet once the timer is up
                # And play the sounds
                self.guard.level.entities.add(Bullet(self))
                self.guard.level.sound_engine.que_sound([self.gunshot_sound, 0])
                self.counter = random.randrange(85, 115)
                self.drop_delay = random.randrange(10, 20)
                self.played_dropped = False

        if self.drop_delay > 0:
            self.drop_delay -= 1
        else:
            if not self.played_dropped:
                # Play the shell drop sound when ready
                self.guard.level.sound_engine.que_sound([self.shell_sound, 0])
                self.played_dropped = True


class Bullet(pygame.sprite.Sprite):

    # Shot by the guards

    def __init__(self, parent):

        # Call the parents constructor
        pygame.sprite.Sprite.__init__(self)

        self.parent = parent

        # Set the direction for the bullet to travel in
        self.direction = parent.degrees - 360
        if self.direction < 0:
            self.direction = abs(self.direction)

        # The guards aren't always a perfect shot
        self.direction += random.randrange(-5, 5)

        # Load the image
        self.image = pygame.image.load("resources/bullet.png").convert()
        self.image = pygame.transform.rotate(self.image, self.direction)

        # Position the sprite
        self.rect = self.image.get_rect()
        self.rect.x = parent.rect.x
        self.rect.y = parent.rect.y

    def update(self):

        # Move along the direction it's facing
        self.rect.x += 15*math.cos(math.radians(self.direction))
        self.rect.y += 15*math.sin(math.radians(self.direction))

        # If the bullet hits platforms then it will disappear
        hit_list = pygame.sprite.spritecollide(self, self.parent.guard.level.platform_list, False)
        if len(hit_list):
            self.parent.guard.level.entities.remove(self)

        hit_list = pygame.sprite.spritecollide(self, self.parent.guard.level.obstacle_list, False)
        if len(hit_list):
            self.parent.guard.level.entities.remove(self)

        # Same if it goes off-screen
        if not 0 < self.rect.x < 1920:
            self.parent.guard.level.entities.remove(self)
        elif not 9 < self.rect.y < 1440:
            self.parent.guard.level.entities.remove(self)
