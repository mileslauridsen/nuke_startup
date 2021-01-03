# Color Palette
import colorsys
import random


def rgb_to_hsv(r,g,b):
    """ RGB tuple to HSV"""
    hsv = colorsys.rgb_to_hsv(r,g,b)
    return hsv


def hsv_to_rgb(h,s,v):
    """HSV tuple to RGB"""
    rgb = colorsys.hsv_to_rgb(h,s,v)
    return rgb


def clamp(value, max_val=1.0, min_val=0.0):
    """Clamp a floating value to a max or min. Defaults are 0.0 and 1.0"""
    clamped = max(min(value, max_val), min_val)
    return clamped


def luma(rgb):
    """
    r*0.2126 + g*0.7152 + b*0.0722
    :param rgb: tuple or list of 3 floats
    :return: float, bt.709 luminance
    """
    luma = rgb[0]*.02126 + rgb[1]*0.7152 + rgb[2]*0.0722
    return luma


def rand_check(rand_low, rand_high):
    """Given a low and high value, return values that are not equal"""
    if rand_low == rand_high:
        rand_high += 1
    return rand_low, rand_high


def randrange(rand_low, rand_high):
    rand_low, rand_high = rand_check(rand_low, rand_high)
    randrange = random.randrange(rand_low, rand_high)
    return randrange


def hue_shift(hue, percent, direction):
    """
    Given a hue, percent, and direction, shift the color wheel
    :param hue: float, a color hue value, 0-1
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :param direction: int, -1 or 1, positive or negative direction
    :return: float, shifted color
    """
    if direction > 0:
        hue_shifted = (((hue * 360) + (360 * percent)) % 360) / 360
    elif direction < 0:
        hue_shifted = (((hue * 360) - (360 * percent)) % 360) / 360
    return hue_shifted


def analogous(rgb, sat_mult, percent=0.0833):
    """
    Analogous color scheme based on main color.
    :param rgb: tuple of 3 floats, an rgb color
    :param sat_mult: float, multiplier to desaturate main colors
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making an analogous color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color03hue = hue_shift(hsv_color[0], percent, -1)
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = hsv_to_rgb(color03hue, hsv_color[1], hsv_color[2])
    color04rgb = hsv_to_rgb(color02hue, hsv_color[1] * sat_mult, hsv_color[2])
    color05rgb = hsv_to_rgb(color03hue, hsv_color[1] * sat_mult, hsv_color[2])

    analogous_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                      'color04': color04rgb, 'color05': color05rgb}

    return analogous_clrs


def analogous_spectrum(rgb, percent=0.0833):
    """
    Analogous color scheme spectrum based on main color.
    :param rgb: tuple of 3 floats, an rgb color
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making an analogous spectrum color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    color01hue = hue_shift(hsv_color[0], percent * 2, 1)
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color04hue = hue_shift(hsv_color[0], percent, -1)
    color05hue = hue_shift(hsv_color[0], percent * 2, -1)
    color01rgb = hsv_to_rgb(color01hue, hsv_color[1], hsv_color[2])
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = tuple(rgb)
    color04rgb = hsv_to_rgb(color04hue, hsv_color[1], hsv_color[2])
    color05rgb = hsv_to_rgb(color05hue, hsv_color[1], hsv_color[2])

    analogous_spectrum_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                      'color04': color04rgb, 'color05': color05rgb}

    return analogous_spectrum_clrs


def complementary(rgb, sat_mult, percent=0.5):
    """
    Colors that are opposite each other on the color wheel are considered
    to be complementary colors (example: red and green).
    :param rgb: tuple of 3 floats, an rgb color
    :param sat_mult: float, multiplier to desaturate main colors
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making a complementary color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    luminance = luma(rgb)
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = hsv_to_rgb(hsv_color[0], hsv_color[1] * sat_mult, hsv_color[2])
    color04rgb = hsv_to_rgb(color02hue, hsv_color[1] * sat_mult, hsv_color[2])
    color05rgb = (luminance, luminance, luminance)

    complementary_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                          'color04': color04rgb, 'color05': color05rgb}

    return complementary_clrs


def split_complement(rgb, sat_mult, percent=0.4167):
    """
    The split-complementary color scheme is a variation of the complementary color scheme.
    In addition to the base color, it uses the two colors adjacent to its complement.
    :param rgb: tuple of 3 floats, an rgb color
    :param sat_mult: float, multiplier to desaturate main colors
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making a split complementary color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color03hue = hue_shift(hsv_color[0], percent, -1)
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = hsv_to_rgb(color03hue, hsv_color[1], hsv_color[2])
    color04rgb = hsv_to_rgb(color02hue, hsv_color[1] * sat_mult, hsv_color[2])
    color05rgb = hsv_to_rgb(color03hue, hsv_color[1] * sat_mult, hsv_color[2])

    split_complement_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                            'color04': color04rgb, 'color05': color05rgb}

    return split_complement_clrs


def triadic(rgb, sat_mult, percent=0.33):
    """
    A triadic color scheme uses colors that are evenly spaced around the color wheel.
    :param rgb: tuple of 3 floats, an rgb color
    :param sat_mult: float, multiplier to desaturate main colors
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making a triadic color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color03hue = hue_shift(hsv_color[0], percent, -1)
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = hsv_to_rgb(color03hue, hsv_color[1], hsv_color[2])
    color04rgb = hsv_to_rgb(color02hue, hsv_color[1] * sat_mult, hsv_color[2])
    color05rgb = hsv_to_rgb(color03hue, hsv_color[1] * sat_mult, hsv_color[2])

    triadic_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                    'color04': color04rgb, 'color05': color05rgb}

    return triadic_clrs


def rectangular(rgb, percent=0.1666):
    """
    The rectangle or tetradic color scheme uses four colors arranged into two complementary pairs.
    :param rgb: tuple of 3 floats, an rgb color
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making a rectangular color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    luminance = luma(rgb)
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color03hue = hue_shift(hsv_color[0], 0.5, 1)
    color04hue = hue_shift(color02hue, 0.5, 1)
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = hsv_to_rgb(color03hue, hsv_color[1], hsv_color[2])
    color04rgb = hsv_to_rgb(color04hue, hsv_color[1], hsv_color[2])
    color05rgb = (luminance, luminance, luminance)

    rectangular_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                        'color04': color04rgb, 'color05': color05rgb}

    return rectangular_clrs


def square(rgb, percent=0.25):
    """
    The square color scheme is similar to the rectangle,
    but with all four colors spaced evenly around the color circle.
    :param rgb: tuple of 3 floats, an rgb color
    :param percent: float, percentage to shift the hue 0.0-1.0 (0-360)
    :return: dict of 5 colors making a square color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    luminance = luma(rgb)
    color02hue = hue_shift(hsv_color[0], percent, 1)
    color03hue = hue_shift(hsv_color[0], percent*2, 1)
    color04hue = hue_shift(hsv_color[0], percent*3, 1)
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(color02hue, hsv_color[1], hsv_color[2])
    color03rgb = hsv_to_rgb(color03hue, hsv_color[1], hsv_color[2])
    color04rgb = hsv_to_rgb(color04hue, hsv_color[1], hsv_color[2])
    color05rgb = (luminance, luminance, luminance)

    square_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                     'color04': color04rgb, 'color05': color05rgb}

    return square_clrs


def shades(rgb, dark=0.05):
    """
    Darker shades divided from input rgb to dark value
    :param rgb: tuple of 3 floats, an rgb color
    :param dark: darkness value of darkest color
    :return: dict of 5 colors making a shaded color scheme
    """
    hsv_color = rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    value_div = 0.25
    color02value = (hsv_color[2] - dark) * ((value_div*3) - 0)/(1-0) + dark
    color03value = (hsv_color[2] - dark) * ((value_div*2) - 0)/(1-0) + dark
    color04value = (hsv_color[2] - dark) * ((value_div*1) - 0)/(1-0) + dark
    color05value = dark
    color01rgb = tuple(rgb)
    color02rgb = hsv_to_rgb(hsv_color[0], hsv_color[1], color02value)
    color03rgb = hsv_to_rgb(hsv_color[0], hsv_color[1], color03value)
    color04rgb = hsv_to_rgb(hsv_color[0], hsv_color[1], color04value)
    color05rgb = hsv_to_rgb(hsv_color[0], hsv_color[1], color05value)

    shade_clrs = {'color01': color01rgb, 'color02': color02rgb, 'color03': color03rgb,
                   'color04': color04rgb, 'color05': color05rgb}

    return shade_clrs


def tint(rgb):
    """adding white to a pure hue"""
    pass


def tone(rgb):
    """adding gray to a pure hue"""
    pass
