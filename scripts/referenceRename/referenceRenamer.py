import maya.cmds as cmds
from functools import partial
#import pymel.core as pm
global textFieldGrpVar
global listReferences
global a 
global b
defaults = ['UI', 'shared']

def num_children(ns):
    return ns.count(':')


namespaces = [ns for ns in cmds.namespaceInfo(lon=True, r=True) if ns not in defaults]
#print namespaces

properNs=[]
nestedNs = []
topNs = []

for i in namespaces:
    print num_children(i)
    if num_children(i) >=2:
        print i
    else:
        properNs.append(i)
#print properNs

for f in properNs:
    print num_children(f)
    if num_children(f) >= 1:
        print f
        nestedNs.append(f)
    else:
        print f
        topNs.append(f)
print nestedNs
print topNs

for n in nestedNs:
    cmds.namespace(removeNamespace=n, mergeNamespaceWithParent=True)

refs = cmds.ls(rf=True)
newRefs = []
#print refs
for x in refs:
    print x
    if ":" in x:
        print x
    else:
        newRefs.append(x)
        print "not in x"
#print newRefs



def removeNS(nameS):
    global a
    global b
    print "running removeNS on : " + nameS
    a=cmds.referenceQuery( nameS,rfn=True,tr=True )
    #print a
    b = cmds.referenceQuery( a,filename=True )
    #print b
    
def printItem(this_textScrollList):
    ret = cmds.textScrollList( this_textScrollList, q=True, si=True )
    print 'ret:', ret
    cmds.select(ret)
    selectedObject = cmds.ls(selection=True, long=True)
    newSel = ''.join(selectedObject)
    
    print newSel
    removeNS(newSel)
    
    
def newName():
    value = cmds.textFieldGrp(textFieldGrpVar,text=1,q=1)
    currSel=cmds.ls(rf=True)
    #print value
    cmds.file( b, e=1, namespace=value)
    
    
if len(namespaces) == 0:
    print 'there arent any referenced objects'
else:
    
    cmds.window('Reference Renamer')
    cmds.rowColumnLayout()
    cmds.text(al="center", l="Select a reference object and change it's namespace")
    cmds.separator()
    textFieldGrpVar = cmds.textFieldGrp( label='new name', editable = True)
    cmds.separator()
    test = cmds.textFieldGrp(textFieldGrpVar, q=1, text=1)
    cmds.separator()
    cmds.text(al="center", l="Reference List")
    s=cmds.textScrollList( numberOfRows=len(namespaces),si='', allowMultiSelection=True,append=newRefs, h= 60)
    cmds.textScrollList(s, e=True, sc=partial(printItem, s) ) 
    cmds.separator()
    cmds.button( l = 'Change Name!', c='newName()')
    cmds.showWindow()
    