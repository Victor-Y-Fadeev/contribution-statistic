#!/usr/bin/env python3

import requests
import colorsys
import cairo
import math
from bs4 import BeautifulSoup


RGB = lambda color: tuple(int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))

LIGHT_THEME = {
    'background': RGB('#ffffff'),
    'font'      : RGB('#24292f'),
    'graph'     : RGB('#ebedf0'),
    'border'    : RGB('#1b1f23'),
    'alpha'     : 0.06
}

DARK_THEME = {
    'background': RGB('#0d1117'),
    'font'      : RGB('#c9d1d9'),
    'graph'     : RGB('#161b22'),
    'border'    : RGB('#ffffff'),
    'alpha'     : 0.05
}


LIGHT_COLOR = {
    1 : RGB('#9be9a8'),
    2 : RGB('#40c463'),
    3 : RGB('#30a14e'),
    4 : RGB('#216e39')
}

LIGHT_HALLOWEEN_COLOR = {
    1 : RGB('#ffee4a'),
    2 : RGB('#ffc501'),
    3 : RGB('#fe9600'),
    4 : RGB('#03001c')
}

DARK_COLOR = {
    1 : RGB('#0e4429'),
    2 : RGB('#006d32'),
    3 : RGB('#26a641'),
    4 : RGB('#39d353')
}

DARK_HALLOWEEN_COLOR = {
    1 : RGB('#631c03'),
    2 : RGB('#bd561d'),
    3 : RGB('#fa7a18'),
    4 : RGB('#fddf68')
}


FONT = "Segoe UI"
SIZE = 12
LINE = 1

WIDTH = 11
HEIGHT = 11
RADIUS = 2

THEME = DARK_THEME
COLOR = DARK_COLOR


# def request_user_input(prompt='> '):
#     """Request input from the user and return what has been entered."""
#     return raw_input(prompt)


def roundrect(context, x, y, width, height, r):
    context.save()
    context.translate(x, y)

    context.new_sub_path()
    context.arc(r, r, r, math.pi, 3 * math.pi / 2)
    context.arc(width - r, r, r, 3 * math.pi / 2, 0)
    context.arc(width - r, height - r, r, 0, math.pi / 2)
    context.arc(r, height - r, r, math.pi / 2, math.pi)
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
    if red >= 0 and red < 256 and blue >= 0 and blue < 256:
        return (math.ceil(red), green, math.ceil(blue), math.ceil(alpha * 100) / 100)
    else:
        return None

def check_green(green):
    l1 = compute_rgb(THEME['graph'], COLOR[1], green)
    l2 = compute_rgb(THEME['graph'], COLOR[2], green)
    l3 = compute_rgb(THEME['graph'], COLOR[3], green)
    l4 = compute_rgb(THEME['graph'], COLOR[4], green)

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

    if l1: print('level 1 = {}'.format(l1))
    if l2: print('level 2 = {}'.format(l2))
    if l3: print('level 3 = {}'.format(l3))
    if l4: print('level 4 = {}'.format(l4))

def main():
    # calendar = requests.get('https://github.com/users/Victor-Y-Fadeev/contributions'
    #     , params={'to': '2021-12-31'})
    # for rect in BeautifulSoup(calendar.text, "html.parser").find_all('rect'):
    #     print(rect.get('data-date'))

    with cairo.SVGSurface("calendar-graph.svg", 823, 128) as surface:
        context = cairo.Context(surface)
        # context.set_fill_rule(cairo.FillRule.EVEN_ODD)
        # context.set_line_join(cairo.LineJoin.BEVEL)
        # context.set_operator(cairo.OPERATOR_SOURCE)

        context.save()
        context.set_source_rgb(*THEME['background'])
        context.paint()
        context.restore()

        # -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji"
        context.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_source_rgb(*THEME['font'])
        context.set_font_size(SIZE)

        context.move_to(0, 45)
        context.show_text("Mon")
        context.move_to(0, 76)
        context.show_text("Wed")
        context.move_to(0, 105)
        context.show_text("Fri")

        context.set_line_width(LINE)

        context.save()
        context.translate(31, 20)
        for x in range(53):
            for y in range(7):
                roundrect(context, 15 * x, 15 * y, WIDTH, HEIGHT, RADIUS)
                context.set_source_rgb(*THEME['graph'])
                context.fill_preserve()
                context.stroke()

                roundrect(context, 15 * x, 15 * y, WIDTH, HEIGHT, RADIUS)
                context.set_source_rgba(*THEME['border'], THEME['alpha'])
                context.stroke()

        context.restore()
        # context.stroke()

if __name__ == '__main__':
    main()
