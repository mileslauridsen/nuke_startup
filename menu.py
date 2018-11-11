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
def viewer_pipes():
    '''Turn off all viewer pipes'''
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
    '''Set expression on selected node to disable in GUI'''
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
    '''Check all Nodes for any $gui expressions'''
    for n in nuke.allNodes(recurseGroups=True):
        for knob in n.knobs():
            if n[knob].hasExpression():
                origExpression = n[knob].toScript()
                if "$gui" in origExpression:
                    print n.name(), knob

def copyReadFilePath():
    '''Copy paths in file knobs to clipboard'''
    files = []
    for n in nuke.selectedNodes():
        if n.Class() == "Read":
            files.append( n["file"].getValue() + ", " + str(int(n["first"].getValue())) + "-" + str(int(n["last"].getValue())))
    clip = QtGui.QClipboard().setText("\n".join(files))

def copyNukeFilePath():
    nkfile = nuke.root().name()
    QtGui.QClipboard().setText(nkfile)

def multiPaste():
    '''Copy contents of clipboard to every selected node.'''
    for n in nuke.selectedNodes():
        nukescripts.misc.clean_selection_recursive()
        n['selected'].setValue(True)
        nuke.nodePaste('%clipboard%')
        n['selected'].setValue(False)

def curveToolMin(mathtype="min"):
    '''Provide math functions on the curve of measured min values in CurveTool node.'''
    for n in nuke.selectedNodes():
        if n.Class() == "CurveTool":
            redMin = n['minlumapixvalue'].animations()[0]
            greenMin = n['minlumapixvalue'].animations()[1]
            blueMin = n['minlumapixvalue'].animations()[2]

            redList = map(lambda key: key.y, redMin.keys())
            greenList = map(lambda key: key.y, greenMin.keys())
            blueList = map(lambda key: key.y, blueMin.keys())

            if mathtype=="min":
                redMin = min(redList)
                greenMin = min(greenList)
                blueMin = min(blueList)

                return (redMin, greenMin, blueMin)

            elif mathtype=="minavg":

                redMinAvg = sum(redList)/len(redList)
                greenMinAvg = sum(greenList)/len(greenList)
                blueMinAvg = sum(blueList)/len(blueList)

                return (redMinAvg, greenMinAvg, blueMinAvg)

def curveToolMax(mathtype="max"):
    '''Provide math functions on the curve of measured max values in CurveTool node.'''
    for n in nuke.selectedNodes():
        if n.Class() == "CurveTool":
            redMax = n['maxlumapixvalue'].animations()[0]
            greenMax = n['maxlumapixvalue'].animations()[1]
            blueMax = n['maxlumapixvalue'].animations()[2]

            redList = map(lambda key: key.y, redMax.keys())
            greenList = map(lambda key: key.y, greenMax.keys())
            blueList = map(lambda key: key.y, blueMax.keys())

            if mathtype=="max":
                redMax = max(redList)
                greenMax = max(greenList)
                blueMax = max(blueList)

                return (redMax, greenMax, blueMax)

            elif mathtype=="maxavg":

                redMaxAvg = sum(redList)/len(redList)
                greenMaxAvg = sum(greenList)/len(greenList)
                blueMaxAvg = sum(blueList)/len(blueList)

                return (redMaxAvg, greenMaxAvg, blueMaxAvg)



### END DEFINITIONS ###


### BEGIN DEFAULTS SETUP ###
nuke.addOnUserCreate(firstFrameEval(), nodeClass='FrameHold')
nuke.knobDefault( 'EXPTool.mode', 'Stops' )
nuke.knobDefault("ContactSheet.roworder", 'TopBottom')
nuke.knobDefault("ContactSheet.colorder", 'LeftRight')
nuke.knobDefault("ContactSheet.roworder", 'TopBottom')
nuke.knobDefault("ContactSheet.rows", 'LeftRight')

### END DEFAULTS SETUP ###


### BEGIN MENU SETUP ###
## Miles Menu
milesMenu = nuke.menu('Nuke').addMenu('miles')
milesMenu.addCommand('Toggle Viewer Pipes', 'viewer_pipes()', 'alt+t')
milesMenu.addCommand('Copy Read File Path', 'copyReadFilePath()')
milesMenu.addCommand('Copy Nuke File Path', 'copyNukeFilePath()')
milesMenu.addCommand('Multi Paste', 'multiPaste()')

### END MENU SETUP ###
