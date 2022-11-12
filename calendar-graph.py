#!/usr/bin/env python3

# pip install numpy

import requests
import colorsys
import cairo
import math
# import numpy as np
from bs4 import BeautifulSoup


RGB = lambda color: tuple(int(color[i:i+2], 16) for i in (1, 3, 5))

LIGHT_BACKGROUND = RGB('#ebedf0')
LIGHT_BORDER     = RGB('#1b1f23')
LIGHT_ALPHA      = 0.06

LIGHT_LEVEL_1 = RGB('#9be9a8')
LIGHT_LEVEL_2 = RGB('#40c463')
LIGHT_LEVEL_3 = RGB('#30a14e')
LIGHT_LEVEL_4 = RGB('#216e39')

LIGHT_HALLOWEEN_LEVEL_1 = RGB('#ffee4a')
LIGHT_HALLOWEEN_LEVEL_2 = RGB('#ffc501')
LIGHT_HALLOWEEN_LEVEL_3 = RGB('#fe9600')
LIGHT_HALLOWEEN_LEVEL_4 = RGB('#03001c')


DARK_BACKGROUND = RGB('#161b22')
DARK_BORDER     = RGB('#ffffff')
DARK_ALPHA      = 0.05

DARK_LEVEL_1 = RGB('#0e4429')
DARK_LEVEL_2 = RGB('#006d32')
DARK_LEVEL_3 = RGB('#26a641')
DARK_LEVEL_4 = RGB('#39d353')

DARK_HALLOWEEN_LEVEL_1 = RGB('#631c03')
DARK_HALLOWEEN_LEVEL_2 = RGB('#bd561d')
DARK_HALLOWEEN_LEVEL_3 = RGB('#fa7a18')
DARK_HALLOWEEN_LEVEL_4 = RGB('#fddf68')

# def request_user_input(prompt='> '):
#     """Request input from the user and return what has been entered."""
#     return raw_input(prompt)


def roundrect(context, x, y, width, height, r):
    context.save()
    context.translate(x, y)

    context.new_sub_path()
    context.arc(r, r, r, math.pi, 3*math.pi/2)
    context.arc(width-r, r, r, 3*math.pi/2, 0)
    context.arc(width-r, height-r, r, 0, math.pi/2)
    context.arc(r, height-r, r, math.pi/2, math.pi)
    context.close_path()

    context.restore()


def compute_rgb(background, level, green):
    if background[1] == green:
        return None

    alpha = (background[1] -  level[1]) / (background[1] - green)
    if alpha < 0 or alpha > 1:
        return None

    red = background[0] - (background[0] -  level[0]) / alpha
    blue = background[2] - (background[2] -  level[2]) / alpha
    return (math.ceil(red), green, math.ceil(blue), math.ceil(alpha*100)/100) if red >= 0 and red < 256 and blue >= 0 and blue < 256 else None

def check_green(green):
    l1 = compute_rgb(LIGHT_BACKGROUND, LIGHT_LEVEL_1, green)
    l2 = compute_rgb(LIGHT_BACKGROUND, LIGHT_LEVEL_2, green)
    l3 = compute_rgb(LIGHT_BACKGROUND, LIGHT_LEVEL_3, green)
    l4 = compute_rgb(LIGHT_BACKGROUND, LIGHT_LEVEL_4, green)

    if l1: print('level 1 = {}'.format(l1))
    if l2: print('level 2 = {}'.format(l2))
    if l3: print('level 3 = {}'.format(l3))
    if l4: print('level 4 = {}'.format(l4))

    # if (l1 and l2 and l3 and l4):
    #         # and abs(np.subtract(l1[0:3], l2[0:3])).max() < 1
    #         # and abs(np.subtract(l2[0:3], l3[0:3])).max() < 1
    #         # and abs(np.subtract(l3[0:3], l4[0:3])).max() < 1
    #         # and abs(np.subtract(l4[0:3], l1[0:3])).max() < 1):
    #     print(l1)
    #     print(l2)
    #     print(l3)
    #     print(l4)
    #     print()

def main():
    for i in range(256):
        check_green(i)
    # calendar = requests.get('https://github.com/users/Victor-Y-Fadeev/contributions'
    #     , params={'to': '2021-12-31'})
    # for rect in BeautifulSoup(calendar.text, "html.parser").find_all('rect'):
    #     print(rect.get('data-date'))

    # with cairo.SVGSurface("calendar-graph.svg", 823, 128) as surface:
    #     context = cairo.Context(surface)
    #     context.set_line_width(1)
    #     context.set_fill_rule(cairo.FillRule.EVEN_ODD)
    #     # context.set_line_join(cairo.LineJoin.BEVEL)

    #     context.save()
    #     context.translate(31, 20)
    #     for x in range(53):
    #         for y in range(7):
    #             roundrect(context, 15*x, 15*y, 11, 11, 2)
    #             context.set_source_rgb(*LIGHT_BACKGROUND)
    #             context.fill()
    #             context.stroke()

    #             roundrect(context, 15*x, 15*y, 11, 11, 2)
    #             context.set_source_rgba(*LIGHT_BORDER, LIGHT_ALPHA)
    #             context.stroke()

    #     context.restore()
    #     # context.stroke()


if __name__ == '__main__':
    main()
