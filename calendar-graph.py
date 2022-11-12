#!/usr/bin/env python3

# pip install beautifulsoup4
# pip install requests
# pip install pycairo

import requests
from bs4 import BeautifulSoup
import cairo
import math
import colorsys


RGB = lambda color: tuple(int(color[i:i+2], 16)/255 for i in (1, 3, 5))

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


def main():
    # calendar = requests.get('https://github.com/users/Victor-Y-Fadeev/contributions'
    #     , params={'to': '2021-12-31'})
    # for rect in BeautifulSoup(calendar.text, "html.parser").find_all('rect'):
    #     print(rect.get('data-date'))

    with cairo.SVGSurface("calendar-graph.svg", 823, 128) as surface:
        context = cairo.Context(surface)
        context.set_line_width(1)
        context.set_fill_rule(cairo.FillRule.EVEN_ODD)
        # context.set_line_join(cairo.LineJoin.BEVEL)

        context.save()
        context.translate(31, 20)
        for x in range(53):
            for y in range(7):
                roundrect(context, 15*x, 15*y, 11, 11, 2)
                context.set_source_rgb(*LIGHT_BACKGROUND)
                context.fill()
                context.stroke()

                roundrect(context, 15*x, 15*y, 11, 11, 2)
                context.set_source_rgba(*LIGHT_BORDER, LIGHT_ALPHA)
                context.stroke()

        context.restore()

        context.stroke()


if __name__ == '__main__':
    main()
