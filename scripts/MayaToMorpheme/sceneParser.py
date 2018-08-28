import maya.cmds as cmds

def getKey(type):
    type = type.lower()

    sceneKey = {'control':'c_',
                'left':'L_',
                'middle':'M_',
                'right':'R_',
                'shape':'_SHP',
                'joint':'_JNT',
                'geometry':'_GEO'}

    if type in sceneKey:
        print sceneKey[type]
        return sceneKey[type]
    else:
        print type + ' is not a recognized type'
        return None

def getSceneItems(key):
    allObjs = cmds.ls()
    objList = [x for x in allObjs if key in x]

    return objList

def main():
    key = getKey('joint')
    joints = getSceneItems(key)

    for i in joints:
        print i
main()
