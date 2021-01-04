import os
import nuke

giz_path = './gizmos'
gizmo_dirs = os.listdir(giz_path)

for g in gizmo_dirs:
    new_gizmo = os.path.join(giz_path, g)
    nuke.pluginAddPath(new_gizmo)