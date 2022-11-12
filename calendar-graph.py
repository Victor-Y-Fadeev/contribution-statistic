#!/usr/bin/env python3

# import requests
# import colorsys
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

THEME = LIGHT_THEME
COLOR = LIGHT_COLOR


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

def calendar_graph(context):
    context.save()
    context.set_source_rgb(*THEME['background'])
    context.set_line_width(LINE)
    context.paint()

    context.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_source_rgb(*THEME['font'])
    context.set_font_size(SIZE)

    context.move_to(0, 45)
    context.show_text("Mon")
    context.move_to(0, 76)
    context.show_text("Wed")
    context.move_to(0, 105)
    context.show_text("Fri")

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

def main():
    # calendar = requests.get('https://github.com/users/Victor-Y-Fadeev/contributions'
    #     , params={'to': '2021-12-31'})
    # for rect in BeautifulSoup(calendar.text, "html.parser").find_all('rect'):
    #     print(rect.get('data-date'))

    with cairo.SVGSurface("calendar-graph.svg", 823, 128) as surface:
        context = cairo.Context(surface)
        calendar_graph(context)

if __name__ == '__main__':
    main()
