#!/usr/bin/env python3

import requests
# import colorsys
# import itertools
import calendar
import cairo
import math
import json
from bs4 import BeautifulSoup
from datetime import date


GIT_BASE = 'https://github.com'
USERNAME = 'Victor-Y-Fadeev'

FOUNDED = 2008
YEAR = date.today().year

SVG = 'calendar-graph.svg'
JSON = 'calendar-graph.json'


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


FONT = 'Segoe UI'
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

def generator(n):
    for difference in range(1, 1 + math.floor(240 / (n - 1))):
        for initial in range(241 - difference * (n - 1)):
            yield (abs(n * (initial + difference * (n - 1) / 2) - 360)
                + abs(n * difference - 360), initial, difference)

def generate_color(n):
    progression = min(generator(n), key=lambda x: x[0])[1:]
    print([progression[0] + i * progression[1] for i in range(n)])

def coordinates(day):
    location = int(day.strftime('%j')) + (day.replace(month=1, day=1).weekday() + 1) % 7
    return location

def calendar_table(context, data):
    first = min(data).year
    last = max(data).year

    location = lambda day: ((day.replace(month=1, day=1).weekday() + 1) % 7
                            + int(day.strftime('%j')))

    converted = dict(((math.floor(loc / 7), loc % 7), dict((day.year, value)
        for day, value in data.items() if location(day) == loc))
            for loc in range(53 * 7))

    # generate_color(10)
    for x in range(53):
        for y in range(7):
            roundrect(context, 15 * x, 15 * y, WIDTH, HEIGHT, RADIUS)
            context.set_source_rgb(*THEME['graph'])
            context.fill_preserve()
            context.stroke()

            roundrect(context, 15 * x, 15 * y, WIDTH, HEIGHT, RADIUS)
            context.set_source_rgba(*THEME['border'], THEME['alpha'])
            context.stroke()

def calendar_graph(context, data):
    context.save()
    context.set_source_rgb(*THEME['background'])
    context.set_line_width(LINE)
    context.paint()

    context.select_font_face(FONT, cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_NORMAL)
    context.set_source_rgb(*THEME['font'])
    context.set_font_size(SIZE)

    context.move_to(0, 45)
    context.show_text('Mon')
    context.move_to(0, 76)
    context.show_text('Wed')
    context.move_to(0, 105)
    context.show_text('Fri')

    weeks = calendar.Calendar()
    weeks.setfirstweekday(calendar.SUNDAY)
    weeks = ((len(i[0]) - int(i[0][0][0].month != i[0][0][-1].month
        and i[0][0][-1].month != 1), i[0][0][-1].strftime('%b'))
            for i in weeks.yeardatescalendar(max(data).year, 1))

    context.save()
    context.translate(31, 12)
    for week in weeks:
        context.move_to(0, 0)
        context.show_text(week[1])
        context.translate(15 * week[0], 0)

    context.restore()
    context.translate(31, 20)
    calendar_table(context, data)
    context.restore()

def github(year):
    calendar = requests.get(
        '{}/users/{}/contributions'.format(GIT_BASE, USERNAME),
        params={'from': '{}-01-01'.format(year)})

    for rect in BeautifulSoup(calendar.text, 'html.parser').find_all('rect'):
        day = rect.get('data-date')
        if day:
            count = int(rect.get('data-count'))
            if count:
                yield date.fromisoformat(day), {'count' : count,
                    'level' : int(rect.get('data-level'))}

def contributions():
    for year in range(FOUNDED, YEAR + 1):
        for item in github(year):
            yield item

def save(data):
    with open(JSON, 'w') as file:
        json.dump(dict((key.isoformat(), value)
            for key, value in data.items()), file)

def load():
    with open(JSON, 'r') as file:
        return dict((date.fromisoformat(key), value)
            for key, value in json.load(file).items())

def main():
    # data = dict(contributions())
    # save(data)
    data = load()

    with cairo.SVGSurface(SVG, 823, 128) as surface:
        context = cairo.Context(surface)
        calendar_graph(context, data)

if __name__ == '__main__':
    main()
