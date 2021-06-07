"""
init.py for use with The Foundry's Nuke compositing software
"""

import os
import pathlib
import nuke

os.chdir(pathlib.Path(__file__).parent.absolute())

GIZMO_PATH = './gizmos'
nuke.pluginAddPath(GIZMO_PATH)

gizmo_dirs = os.listdir(GIZMO_PATH)

for g in gizmo_dirs:
    new_gizmo = os.path.join(GIZMO_PATH, g)
    nuke.pluginAddPath(new_gizmo)
