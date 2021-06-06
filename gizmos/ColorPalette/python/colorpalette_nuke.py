# nuke functions to operate on gizmo
import nuke
import colorpalette


def color_scheme_set(scheme, rgb, sat_mult):
    if scheme == "Analogous":
        colors = colorpalette.analogous(rgb, sat_mult)
    elif scheme == "Analogous Spectrum":
        colors = colorpalette.analogous_spectrum(rgb)
    elif scheme == "Complementary":
        colors = colorpalette.complementary(rgb, sat_mult)
    elif scheme == "Split Complementary":
        colors = colorpalette.split_complement(rgb, sat_mult)
    elif scheme == "Triadic":
        colors = colorpalette.triadic(rgb, sat_mult)
    elif scheme == "Square":
        colors = colorpalette.square(rgb)
    elif scheme == "Rectangular":
        colors = colorpalette.rectangular(rgb)
    elif scheme == "Shades":
        colors = colorpalette.shades(rgb, dark=0.05)
    else:
        print("Color Scheme Not Available")
    return colors


def update_groups():
    n = nuke.thisNode()
    scheme = n['color_schemes_pulldown'].value()
    sat_mult = n['saturation_multiplier'].value()
    alpha = [1.0]
    color_names = ['color01', 'color02', 'color03', 'color04', 'color05']

    # group 01
    if not n['color_group_01_lock'].value():
        group01 = ['color01', 'color02', 'color03', 'color04', 'color05']
        seed_color01 = n['color01'].value()
        seed_color01.pop()
        colors = color_scheme_set(scheme, seed_color01, sat_mult)
        count = 0
        for c in group01:
            n[c].setValue(list(colors[color_names[count]]) + alpha)
            count+=1

    # group 02
    if not n['color_group_02_lock'].value():
        group02 = ['color06', 'color07', 'color08', 'color09', 'color10']
        seed_color02 = n['color06'].value()
        seed_color02.pop()
        colors = color_scheme_set(scheme, seed_color02, sat_mult)
        count = 0
        for c in group02:
            n[c].setValue(list(colors[color_names[count]]) + alpha)
            count += 1

    # group 03
    if not n['color_group_03_lock'].value():
        group03 = ['color11', 'color12', 'color13', 'color14', 'color15']
        seed_color03 = n['color11'].value()
        seed_color03.pop()
        colors = color_scheme_set(scheme, seed_color03, sat_mult)
        count = 0
        for c in group03:
            n[c].setValue(list(colors[color_names[count]]) + alpha)
            count += 1

    # group 04
    if not n['color_group_04_lock'].value():
        group04 = ['color16', 'color17', 'color18', 'color19', 'color20']
        seed_color04 = n['color16'].value()
        seed_color04.pop()
        colors = color_scheme_set(scheme, seed_color04, sat_mult)
        count = 0
        for c in group04:
            n[c].setValue(list(colors[color_names[count]]) + alpha)
            count += 1
