from pygame.locals import *
import json


def save():
    # Save all of the data into the savefile
    with open("save_data.json", "w") as outfile:
        json.dump(save_data, outfile)


def load(x=None):
    # Open the data
    with open("save_data.json", "r") as infile:
        data = json.load(infile)

    # Return the data that's been asked for
    if x is None:
        return data
    else:
        return data[x]

# Load the data
save_data = load()

# The control for each function

default_controls = {"WALK_LEFT": K_a,
                    "WALK_RIGHT": K_d,
                    "JUMP": K_w,
                    "ACTION": K_SPACE,
                    "CROUCH": K_LCTRL,
                    "RESTART": K_r}

# Pygame and tkinter have different keycodes
# so this is used to translate
trans_dict = {65: 97,
              66: 98,
              67: 99,
              68: 100,
              69: 101,
              70: 102,
              71: 103,
              72: 104,
              73: 105,
              74: 106,
              75: 107,
              76: 108,
              77: 109,
              78: 110,
              79: 111,
              80: 112,
              81: 113,
              82: 114,
              83: 115,
              84: 116,
              85: 117,
              86: 118,
              87: 119,
              88: 120,
              89: 121,
              90: 122,
              20: 301,
              16: 304,
              17: 306,
              18: 308,
              219: 91,
              91: 311,
              223: 96,
              189: 45,
              187: 61,
              221: 93,
              186: 59,
              192: 39,
              222: 92,
              188: 44,
              190: 46,
              191: 47,
              93: 319,
              112: 282,
              113: 283,
              114: 284,
              115: 285,
              116: 286,
              117: 287,
              118: 288,
              119: 289,
              120: 290,
              121: 291,
              122: 292,
              123: 293,
              37: 276,
              38: 273,
              39: 275,
              40: 274,
              145: 302,
              144: 300,
              111: 267,
              106: 268,
              109: 269,
              103: 263,
              104: 264,
              105: 265,
              107: 270,
              100: 260,
              101: 261,
              102: 262,
              97: 257,
              98: 258,
              99: 259,
              13: 271,
              96: 256,
              110: 266,
              220: 60}
