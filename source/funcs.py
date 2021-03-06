import pygame

# Various functions for various pru


def pixel_perfect_collision(obj1_rect, obj1_hitmask, obj2_rect, obj2_hitmask):
    """
    If the function finds a collision, it will return True;
    if not, it will return False. If one of the objects is
    not the intended type, the function instead returns None.
    """
    try:
        # create attributes
        rect1, mask1 = obj1_rect, obj1_hitmask
        rect2, mask2 = obj2_rect, obj2_hitmask
        # initial examination
        if rect1.colliderect(rect2) is False:
            return False
    except AttributeError:
        return None

    # get the overlapping area
    clip = rect1.clip(rect2)

    # find where clip's top-left point is in both rectangles
    x1 = clip.left - rect1.left
    y1 = clip.top - rect1.top
    x2 = clip.left - rect2.left
    y2 = clip.top - rect2.top

    # cycle through clip's area of the hitmasks
    for y in range(clip.height):
        for x in range(clip.width):
            # returns True if neither pixel is blank
            if mask1[y1+y][x1+x] != 0 and mask2[y2+y][x2+x] != 0:
                return True

    # if there was neither collision nor error
    return False


def create_mask(surface):

    # Creates a mask for an image
    # where a value of 0 is nothing
    # and 1 is a pixel

    temp_mask = pygame.mask.from_surface(surface, 63)

    temp_mask_size = temp_mask.get_size()

    new_mask = []
    for y in range(temp_mask_size[1]):
        row = []
        for x in range(temp_mask_size[0]):
            row += [temp_mask.get_at((x, y))]
        new_mask += [row]

    return new_mask
