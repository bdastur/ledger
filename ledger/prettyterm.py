#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

ATTRIBUTES = {
    'bold': 1,
    'dark': 2,
    'underline': 4,
    'blink': 5,
    'reverse': 7,
    'concealed': 8,
}


HIGHLIGHTS = {
    'grey': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'magenta': 45,
    'cyan': 46,
    'white': 47
}

COLORS = {
    'grey': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}


def format_string(text, color=None, highlight=None, attrs=None):
    """
    Format the given string, by apping color/highlight/attrs.
    You can apply a combination of any of them

    Args:
        color (optional): Possible values for text colors
            grey, red, green, yello, blue, magenta, cyan, white

        highlight: Possible values for text highlighting:
            grey, red, green, yellow, blue, magenta, cyan, white

        attrs: List of attributes to apply to text
            bold, dark, underline, blink, reverse, concealed.

    Usage:
        print prettyterm.fmtstring("Red String", color="red")
    """
    ENDFMT = '\033[0m'
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if highlight is not None:
            text = fmt_str % (HIGHLIGHTS[highlight], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += ENDFMT
    return text


def fmtstring(text, color=None, highlight=None, attrs=None):
    '''
    Return the formatted text.
    '''
    return format_string(text, color, highlight, attrs)


