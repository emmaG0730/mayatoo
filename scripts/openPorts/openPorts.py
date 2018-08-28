import maya.cmds as cmds

def main():
    if not cmds.commandPort(':7002', q=True):
        cmds.commandPort(n=':7002')