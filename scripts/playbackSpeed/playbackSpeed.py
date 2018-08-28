import maya.cmds as cmds
global v
global step
global enableVar
global playSpeed
global stepSpeed
global maxSpeed
global playSpeedSelectMenu
global step

def setVariables():
    global v
    global playSpeed
    global stepSpeed
    global maxSpeed
    global step
    try:
        v
    except NameError:
        v=0.0
        playSpeed = 0.0
        stepSpeed = 1.0
        maxSpeed = 1.0
        step = 1.0
        cmds.playbackOptions( ps=v)
        playSpeedSelectMenu = ''
    else:
        #v=1.0
        #cmds.playbackOptions( ps=v)
        showTheWindow()
        


def stepSpeedFloat():
    global playSpeed
    global stepSpeed
    global step
    cmds.playbackOptions(ps = 0.0)
    step = (cmds.floatSliderGrp(stepSpeed, q=True, value = True))
    print step
    cmds.playbackOptions( by=step)

def playAnim():
    global playSpeed
    global stepSpeed
    global maxSpeed
    print cmds.playbackOptions(q=True, mps = True)
    if cmds.play(q=True, state= True):
        cmds.play(st=False)
        print "pause "
    else:
        print "play"
        cmds.play(st = True)

def playSpeedChange():
    global playSpeedSelectMenu
    cmds.playbackOptions(ps = 0.0)
    currentValue = cmds.optionMenu(playSpeedSelectMenu, q=True,v=True)
    if currentValue == 'Half[15:fps]':
        print "15"
        cmds.playbackOptions(mps = 0.5)
    elif currentValue == 'Real-time[30:fps]':
        print "30"
        cmds.playbackOptions(mps = 1.0)
    elif currentValue == 'Twice[60:fps]':
        print "60"
        cmds.playbackOptions(mps = 2.0)
    elif currentValue == 'Free':
        print "free"
        cmds.playbackOptions(mps = 0.0)
    else:
        print "none of the above"
        cmds.playbackOptions(mps=1.0)

def showTheWindow():
    global playSpeed
    global stepSpeed
    global maxSpeed
    global v
    global playSpeedSelectMenu
    global step
    
    
    if (cmds.window("Playback_control", exists=True)):
        cmds.deleteUI("Playback_control")
    cmds.window('Playback_control')
    
    cmds.rowColumnLayout()
    cmds.separator()
    cmds.separator()
    
    cmds.text(al="center", l="change the playback speed of the scene")
    cmds.separator()
    cmds.separator()
    
    #playSpeed = cmds.floatSliderGrp(l="playback Speed",field = True,min=0.0,max=10.0,value=v,step=0.1,dc = 'playSpeedFloat()',cc='vis_toggle()')
    stepSpeed = cmds.floatSliderGrp(l="frame step", en = True,field = True, value = step, min = 0.1, max = 4.0, cc='stepSpeedFloat()',dc = 'stepSpeedFloat()')
    #step = (cmds.floatSliderGrp(stepSpeed, q=True, value = True))
    #slider_enabled = cmds.floatSliderGrp(playSpeed, query=True, value=True)
    
    cmds.separator()
    cmds.separator()
    
    
    playSpeedSelectMenu = cmds.optionMenu(w = 100,h=25, label = "Framerate: ", cc= 'playSpeedChange()')
    cmds.menuItem(label = "Real-time[30:fps]")
    cmds.menuItem(label = "Half[15:fps]")
    #cmds.menuItem(label = "Real-time[30:fps]")
    cmds.menuItem(label = "Twice[60:fps]")
    cmds.menuItem(label = "Free")
    
    cmds.separator()
    cmds.separator()
    
    cmds.button(l="Play / Pause Animation", command = 'playAnim()')
    cmds.separator()
    cmds.separator()
    
    cmds.showWindow()

setVariables()
