'''
menu.py for use with The Foundry's Nuke compositing software
'''

### BEGIN IMPORTS ###
# built-in
import os
import nuke

# pyside qtgui (QClipboard)
try:
    from PySide import QtGui
except:
    from PySide2 import QtGui

### END IMPORTS ###


### BEGIN DEFINTIONS ###
### set new item definitions
def viewer_pipes():
    n = nuke.allNodes()

    for i in n:
        if i.Class() == "Viewer":
            if i.knob("hide_input").getValue == True:
                i.knob("hide_input").setValue(False)
            else:
                 i.knob("hide_input").setValue(True)

def curFrame():
    '''Return value of current frame'''
    return nuke.frame()

def firstFrameEval():
    n = nuke.thisNode()
    n['first_frame'].setValue(nuke.frame())

def guiOn():
    n = nuke.thisNode()
    n['disable'].setExpression("$gui ? 0:1")

def viewer_pipes():
    '''Hide input into Viewer nodes'''
    n = nuke.allNodes()

    for i in n:
        if i.Class() == "Viewer":
            if i.knob("hide_input").getValue == True:
                i.knob("hide_input").setValue(False)
            else:
                 i.knob("hide_input").setValue(True)

def guiSamples(gui=1, samples=16):
    '''Set selected scanline render samples to selected values'''
    for n in nuke.selectedNodes():
        if n.Class() == "ScanlineRender":
            n["samples"].setExpression("$gui ? " + gui + " : " + str(samples))

def guiCheck():
    for n in nuke.allNodes(recurseGroups=True):
        for knob in n.knobs():
            if n[knob].hasExpression():
                origExpression = n[knob].toScript()
                if "$gui" in origExpression:
                    print n.name(), knob

def copyRead():
    '''Copy paths in file knobs to clipboard'''
    files = []
    for n in nuke.selectedNodes():
        if n.Class() == "Read":
            files.append( n["file"].getValue() + ", " + str(int(n["first"].getValue())) + "-" + str(int(n["last"].getValue())))
    clip = QtGui.QClipboard().setText("\n".join(files))

### END DEFINITIONS ###


### BEGIN DEFAULTS SETUP ###
nuke.addOnUserCreate(firstFrameEval(), nodeClass='FrameHold')
nuke.knobDefault( 'EXPTool.mode', 'Stops' )

### END DEFAULTS SETUP ###


### BEGIN MENU SETUP ###
## FIN Pipeline Menu
finMenu = nuke.menu('Nuke').addMenu('FIN')
finMenu.addCommand('Toggle Viewer Pipes', 'viewer_pipes()', 'alt+t')
finMenu.addCommand('Copy Reads', 'copyRead()')

### END MENU SETUP ###
