from pygame.locals import *
import json


def save():
    with open("save_data.json", "w") as outfile:
        json.dump(save_data, outfile)


def load():
    with open("save_data.json", "r") as infile:
        data = json.load(infile)

    return data


def load_controls():
    with open("save_data.json", 'r') as infile:
        data = json.load(infile)

    return data["controls"]

save_data = load()

# The control for each function

default_controls = {"WALK_LEFT": K_a,
                    "WALK_RIGHT": K_d,
                    "JUMP": K_w,
                    "ACTION": K_SPACE,
                    "CROUCH": K_LCTRL}

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
