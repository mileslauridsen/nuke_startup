"""
menu.py for use with The Foundry's Nuke compositing software
"""

# BEGIN IMPORTS
# built-ins
import os
import glob
import nuke
import nukescripts

# pyside qtgui (QClipboard)
from PySide2 import QtGui

# END IMPORTS


# BEGIN DEFINTIONS
def viewer_pipes():
    """
    Turn off all viewer pipes
    :return: None
    """
    nodes = nuke.allNodes()

    for i in nodes:
        if i.Class() == "Viewer":
            if i.knob("hide_input").getValue():
                i.knob("hide_input").setValue(False)
            else:
                i.knob("hide_input").setValue(True)


def gui_on():
    """
    Set expression on selected node to disable in GUI
    :return: None
    """
    node = nuke.thisNode()
    node['disable'].setExpression("$gui ? 0:1")


def gui_samples(gui=1, render=16):
    """
    Set selected scanline render samples to selected values
    :param gui: integer, value to use for samples in gui mode
    :param render: integer, value to use for samples in render mode
    :return: None
    """
    for node in nuke.selectedNodes():
        if node.Class() == "ScanlineRender":
            node["samples"].setExpression("$gui ? {} : {}".format(gui, render))


def gui_check():
    """
    Check all Nodes for any $gui expressions
    :return: None
    """
    for node in nuke.allNodes(recurseGroups=True):
        for knob in node.knobs():
            if node[knob].hasExpression():
                orig_expression = node[knob].toScript()
                if "$gui" in orig_expression:
                    print(node.name(), knob)


def read_from_write():
    """
    Create Read node with values from Write node
    :return: None
    """
    for node in nuke.selectedNodes():
        file = node['file'].getValue()
        proxy = node['proxy'].getValue()
        file_seq = glob.glob(file.replace("%04d", "*"))
        file_seq.sort()
        first = file_seq[0].split('.')[1]
        last = file_seq[-1].split('.')[1]
        read = nuke.nodes.Read(file=file, proxy=proxy, first=first, last=last)
        read.setXYpos(node.xpos(), node.ypos() + 100)


def copy_read_file_path():
    """
    Copy paths in file knobs to clipboard
    :return: None
    """
    files = []
    for node in nuke.selectedNodes():
        if node.Class() == "Read":
            files.append("{}, {}-{}".format(node['file'].getValue(),
                                            int(node['first'].getValue()),
                                            int(node['last'].getValue())))
    QtGui.QClipboard().setText("\n".join(files))


def copy_nuke_file_path():
    """
    Copy nuke script path to clipboard
    :return: None
    """
    nkfile = nuke.root().name()
    QtGui.QClipboard().setText(nkfile)


def multi_paste():
    """
    Copy contents of clipboard to every selected node.
    :return: None
    """
    for node in nuke.selectedNodes():
        nukescripts.misc.clean_selection_recursive()
        node.setSelected(True)
        nuke.nodePaste('%clipboard%')
        node.setSelected(False)


def curve_tool_min(mathtype="min"):
    """
    Provide math functions on the curve of measured min values in CurveTool node.
    :param mathtype: string, math type to operate on
    :return: three floats as tuple
    """
    for node in nuke.selectedNodes():
        if node.Class() == "CurveTool":
            red_min = node['minlumapixvalue'].animations()[0]
            green_min = node['minlumapixvalue'].animations()[1]
            blue_min = node['minlumapixvalue'].animations()[2]

            red_list = map(lambda key: key.y, red_min.keys())
            green_list = map(lambda key: key.y, green_min.keys())
            blue_list = map(lambda key: key.y, blue_min.keys())

            if mathtype is "min":
                red_min = min(red_list)
                green_min = min(green_list)
                blue_min = min(blue_list)

                return red_min, green_min, blue_min

            elif mathtype is "minavg":

                red_min_avg = sum(red_list)/len(red_list)
                green_min_avg = sum(green_list)/len(green_list)
                blue_min_avg = sum(blue_list)/len(blue_list)

                return red_min_avg, green_min_avg, blue_min_avg


def curve_tool_max(mathtype="max"):
    """
    Provide math functions on the curve of measured max values in CurveTool node.
    :param mathtype: string, mathtype to operate on
    :return:
    """
    for node in nuke.selectedNodes():
        if node.Class() == "CurveTool":
            red_max = node['maxlumapixvalue'].animations()[0]
            green_max = node['maxlumapixvalue'].animations()[1]
            blue_max = node['maxlumapixvalue'].animations()[2]

            red_list = map(lambda key: key.y, red_max.keys())
            green_list = map(lambda key: key.y, green_max.keys())
            blue_list = map(lambda key: key.y, blue_max.keys())

            if mathtype is "max":
                red_max = max(red_list)
                green_max = max(green_list)
                blue_max = max(blue_list)

                return red_max, green_max, blue_max

            elif mathtype is "maxavg":

                red_max_avg = sum(red_list)/len(red_list)
                green_max_avg = sum(green_list)/len(green_list)
                blue_max_avg = sum(blue_list)/len(blue_list)

                return red_max_avg, green_max_avg, blue_max_avg


def ray_render_add_channels():
    """
    Add utility and beauty aovs to ray render
    :return: None
    """
    nuke.Layer('__Pworld', ['x', 'y', 'z'])
    nuke.Layer('__Nworld', ['x', 'y', 'z'])
    nuke.Layer('__motion', ['red', 'green', 'blue'])
    nuke.Layer('__direct_diffuse', ['red', 'green', 'blue'])
    nuke.Layer('__direct_specular', ['red', 'green', 'blue'])
    nuke.Layer('__indirect_specular', ['red', 'green', 'blue'])
    nuke.Layer('__incandescence', ['red', 'green', 'blue'])
    node = nuke.thisNode()
    node['AOV_Point'].setValue('__Pworld')
    node['AOV_Normal'].setValue('__Nworld')
    node['AOV_Motion'].setValue('__motion')
    node['AOV_Direct_Diffuse'].setValue('__direct_diffuse')
    node['AOV_Direct_Specular'].setValue('__direct_specular')
    node['AOV_Reflection'].setValue('__indirect_specular')
    node['AOV_Emissive'].setValue('__incandescence')

# END DEFINITIONS


# BEGIN DEFAULTS SETUP
nuke.addOnUserCreate(lambda:nuke.thisNode()['first_frame'].setValue(nuke.frame()),
                     nodeClass='FrameHold')
nuke.knobDefault('ContactSheet.roworder', 'TopBottom')
nuke.knobDefault('ContactSheet.colorder', 'LeftRight')
nuke.knobDefault('ContactSheet.center', 'True')
nuke.knobDefault('Read.label', 'Frames\n[value first] - [value last]')
nuke.knobDefault('Copy.bbox', 'A')
nuke.knobDefault('Remove.operation', 'keep')
nuke.knobDefault('Remove.channels', 'rgba')
nuke.knobDefault('Multiply.channels', 'rgba')
nuke.knobDefault('Invert.channels', 'rgba')
nuke.knobDefault('Add.channels', 'rgb')
nuke.knobDefault('EXPTool.mode', 'Stops')
nuke.knobDefault('Blur.label', '[value size]')
nuke.knobDefault('Blur.channels', 'rgba')
nuke.knobDefault('Defocus.channels', 'rgba')
nuke.knobDefault('Defocus.label', '[value defocus]')
nuke.knobDefault('Keymix.channels', 'rgba')
nuke.knobDefault('Dissolve.channels', 'rgba')

# rayrender
nuke.knobDefault('RayRender.output_shader_vectors', '0')
nuke.addOnUserCreate(ray_render_add_channels, nodeClass="RayRender")

# END DEFAULTS SETUP


# BEGIN MENU SETUP
# Miles Menu
milesMenu = nuke.menu('Nuke').addMenu('miles')
milesMenu.addCommand('Toggle Viewer Pipes', 'viewer_pipes()', 'alt+t')
milesMenu.addCommand('Read From Write', 'read_from_write()', 'alt+r')
milesMenu.addCommand('Copy Read File Path', 'copy_read_file_path()')
milesMenu.addCommand('Copy Nuke File Path', 'copy_nuke_file_path()')
milesMenu.addCommand('Multi Paste', 'multi_paste()', 'ctrl+shift+v')

# Load nuke_startup gizmos
GIZMO_PATH = './gizmos'
gizmo_dirs = os.listdir(GIZMO_PATH)

for g in gizmo_dirs:
    nuke.menu('Nodes').addCommand("nuke_startup/{}".format(g), "nuke.createNode('{}')".format(g))

# END MENU SETUP
