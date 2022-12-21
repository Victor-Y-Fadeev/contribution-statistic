#!/usr/bin/env python3

import requests
import calendar
import colorsys
import math
import json
import os
from typing import Iterator
from bs4 import BeautifulSoup
from datetime import date
from cairo import SVGSurface, Context, FontSlant, FontWeight


FOUNDED = 2008
GIT_BASE = 'https://github.com'

SVG = '{}.svg'.format(os.path.splitext(__file__)[0])
JSON = '{}.json'.format(os.path.splitext(__file__)[0])


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

LIGHT_WINTER_COLOR = {
    1 : RGB('#0a3069'),
    2 : RGB('#0969da'),
    3 : RGB('#54aeff'),
    4 : RGB('#b6e3ff')
}

LIGHT_HALLOWEEN_COLOR = {
    1 : RGB('#ffee4a'),
    2 : RGB('#ffc501'),
    3 : RGB('#fe9600'),
    4 : RGB('#03001c')
}

LIGHT_GITLAB_COLOR = {
    1 : RGB('#acd5f2'),
    2 : RGB('#7fa8c9'),
    3 : RGB('#527ba0'),
    4 : RGB('#254e77')
}

LIGHT_NEW_COLOR = {
    1 : RGB('#d2dcff'),
    2 : RGB('#7992f5'),
    3 : RGB('#3f51ae'),
    4 : RGB('#2a2b59')
}

DARK_COLOR = {
    1 : RGB('#0e4429'),
    2 : RGB('#006d32'),
    3 : RGB('#26a641'),
    4 : RGB('#39d353')
}

DARK_WINTER_COLOR = {
    1 : RGB('#b6e3ff'),
    2 : RGB('#54aeff'),
    3 : RGB('#0969da'),
    4 : RGB('#0a3069')
}

DARK_HALLOWEEN_COLOR = {
    1 : RGB('#631c03'),
    2 : RGB('#bd561d'),
    3 : RGB('#fa7a18'),
    4 : RGB('#fddf68')
}

DARK_GITLAB_COLOR = {
    1 : RGB('#333861'),
    2 : RGB('#4a5593'),
    3 : RGB('#6172c5'),
    4 : RGB('#788ff7')
}

DARK_NEW_COLOR = {
    1 : RGB('#303470'),
    2 : RGB('#4e65cd'),
    3 : RGB('#97acff'),
    4 : RGB('#e9ebff')
}


FONT = 'Segoe UI'
SIZE = 12
LINE = 1

WIDTH = 11
HEIGHT = 11
RADIUS = 2

THEME = DARK_THEME
COLOR = DARK_WINTER_COLOR
SHIFT = 0 / 360
TEXT = 'Learn how we count contributions'


def mix_color(palette: tuple[int, ...]) -> tuple[float, float, float]:
    colors = tuple(colorsys.hsv_to_rgb(SHIFT + i / len(palette), 1, 1)
        for i in range(len(palette)) if palette[i])
    if not colors:
        return THEME['graph']

    mixed = colorsys.rgb_to_hsv(sum(i[0] for i in colors) / len(colors),
                                sum(i[1] for i in colors) / len(colors),
                                sum(i[2] for i in colors) / len(colors))

    return colorsys.hsv_to_rgb(mixed[0], mixed[1], 1)

def get_color(palette: tuple[int, ...]) -> tuple[float, float, float]:
    level = max(palette)
    if not level:
        return THEME['graph']
    if not SHIFT:
        return COLOR[level]

    hsv = colorsys.rgb_to_hsv(*COLOR[level])
    return colorsys.hsv_to_rgb(SHIFT + hsv[0], hsv[1], hsv[2])

def roundrect(context: Context, x: float, y: float,
              width: float, height: float, r: float):
    context.save()
    context.translate(x, y)

    context.new_sub_path()
    context.arc(r, r, r, math.pi, 3 * math.pi / 2)
    context.arc(width - r, r, r, 3 * math.pi / 2, 0)
    context.arc(width - r, height - r, r, 0, math.pi / 2)
    context.arc(r, height - r, r, math.pi / 2, math.pi)
    context.close_path()

    context.restore()

def calendar_table(context: Context, data: dict[date, dict[str, int]]):
    weekday = lambda day: (day.weekday() + 1) % 7
    location = lambda day: (weekday(date(day.year, 1, 1))
                            + int(day.strftime('%j')) - 1)

    current = max(data).year
    merged = dict(((math.floor(loc / 7), loc % 7), dict((day.year, value)
        for day, value in data.items() if location(day) == loc))
            for loc in range(weekday(date(current, 1, 1)),
                52 * 7 + 1 + weekday(date(current, 12, 31))))

    first = min(data).year
    converted = dict((loc, tuple(value[year]['level'] if value and year in value
        else 0 for year in range(first, current + 1)))
            for loc, value in merged.items())

    for (x, y), palette in converted.items():
        roundrect(context, 15 * x, 15 * y, WIDTH, HEIGHT, RADIUS)
        context.set_source_rgb(*get_color(palette))
        context.fill_preserve()
        context.stroke()

        roundrect(context, 15 * x, 15 * y, WIDTH, HEIGHT, RADIUS)
        context.set_source_rgba(*THEME['border'], THEME['alpha'])
        context.stroke()

def calendar_graph(context: Context, data: dict[date, dict[str, int]]):
    context.save()
    context.set_source_rgb(*THEME['background'])
    context.set_line_width(LINE)
    context.paint()

    context.select_font_face(FONT, FontSlant.NORMAL, FontWeight.NORMAL)
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

def draw_image(data: dict[date, dict[str, int]], width: float, height: float):
    with SVGSurface(SVG, 823, 128) as surface:
        context = Context(surface)

        lines = TEXT.split('\n')
        calendar_graph(context, data)

def contributions(username: str) -> Iterator[tuple[date, dict[str, int]]]:
    """Pull contributions from GitHub since its founded (2008).

    Args:
        username: Your GitHub username.

    Returns:
        Dictionary key-value iterator with date key.
        Value is a dictionary with two int values.
        The 'count' key means the number of commits.
        The 'level' key is the cell light from 1 to 4.
    """
    for year in range(FOUNDED, date.today().year + 1):
        calendar = requests.get(
            '{}/users/{}/contributions'.format(GIT_BASE, username),
            params={'from': '{}-01-01'.format(year)})

        for rect in BeautifulSoup(calendar.text,
                                  'html.parser').find_all('rect'):
            day = rect.get('data-date')
            if day:
                count = int(rect.get('data-count'))
                if count:
                    yield date.fromisoformat(day), {'count' : count,
                        'level' : int(rect.get('data-level'))}

def save(data: dict[date, dict[str, int]]):
    """Save contribution dictionary to JSON with script matching name.

    Args:
        data: Dictionary of date keys with commits count and light levels.
    """
    with open(JSON, 'w') as file:
        json.dump(dict((key.isoformat(), value)
            for key, value in data.items()), file)

def load() -> dict[date, dict[str, int]]:
    """Load contribution dictionary from JSON with script matching name.

    Returns:
        Dictionary key-value iterator with date key.
        Value is a dictionary with two int values.
        The 'count' key means the number of commits.
        The 'level' key is the cell light from 1 to 4.
    """
    with open(JSON, 'r') as file:
        return dict((date.fromisoformat(key), value)
            for key, value in json.load(file).items())


def main():
    # data = dict(contributions('Victor-Y-Fadeev'))
    # save(data)
    data = load()
    # data = dict(filter(lambda item: item[0].year == 2021, data.items()))

    with SVGSurface(SVG, 823, 128) as surface:
        context = Context(surface)
        calendar_graph(context, data)

if __name__ == '__main__':
    main()
