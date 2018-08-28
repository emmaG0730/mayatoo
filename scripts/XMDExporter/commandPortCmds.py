import maya.cmds as cmds
import globalVariables as gv

# writes data to temp file
def writeArguments(data):
    print "writing arguments"
    file = open(gv.EXTERNALMAYA + '\\mayaargs.txt','w')
    file.write(data)
    file.close()

# Gets the current playback time range and returns the start and end values
def getCurRange():
    startFrame = cmds.playbackOptions(query=True, min=True)
    endFrame = cmds.playbackOptions(query=True, max=True)
    print startFrame, endFrame
    writeArguments(str(startFrame) + ',' + str(endFrame))
    return startFrame, endFrame

# Gets current animation range based on the b_M_pelvis_v1_JNT
def getAnimRange():
    try:
        startFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="first")
        endFrame = cmds.findKeyframe("b_M_pelvis_v1_JNT", which="last")
        print startFrame, endFrame
        writeArguments(str(startFrame) + ',' + str(endFrame))
        return startFrame, endFrame
    except:
        print "No object name b_M_pelvis_v1_JNT was found"

# Reads temp argument file to get the xmd export path, start frame, and end frame
def readArguments():
    print "reading arguments"
    argsfile = open(gv.EXTERNALMAYA + '\\mayaargs.txt', 'r')
    for line in argsfile:
        print line
        paths = line.split(',')
        xmdpath = paths[0].replace('\\', '/')
        startframe = paths[1]
        endframe = paths[2]

    argsfile.close()
    print xmdpath, startframe, endframe
    return xmdpath, startframe, endframe

# Exports the current file to XMD
def exportAnim():
    print "exporting animation"
    xmdpath, startframe, endframe = readArguments()
    filePath = cmds.file(query=True, loc=True)
    fileName = (((filePath.split('/'))[-1]).split('.'))[0]
    xmdoptions = XMDAnimSettings(startframe, endframe)

    cmds.file(xmdpath + '/' + fileName + '.xmd', type='XMD Export', ea=True, options=xmdoptions, force=True)

    print xmdpath + '/' + fileName + '.xmd', 'has been generated'

# Settings for XMD export
def XMDAnimSettings(start, end):
    xmdoptions = ("-ascii=1;"                      # 0 = binary output, 1 = ascii output
                  "-layers=0;"                     # Display Layers
                  "-rlayers=0;"                    # Render Layers
                  "-sets=0;"                       # Object Sets
                  "-stripNamespaces=1;"            # If true, namespaces are stripped from node names on export (including References)
                  "-dynamic_keyable_attrs=1;"      # If true, dynamic attributes are exported
                  "-dynamic_nonkeyable_attrs=0;"   # If true, dynamic non keyable attributes are exported
                  "-remove_scale=1;"               # Remove scale on export
                  "-scaling_factor=1.0;"           # Scaling Factor
                  "-material=0;"                   # Materials
                  "-textures=0;"                   # Texturing
                  "-shaders=0;"                    # Hardware Shaders
                  "-texture_filtering=0;"          # Extra Texture Info
                  "-camera=0;"                     # Cameras
                  "-light=0;"                      # Lights
                  "-locator=0;"                    # Locators
                  "-mesh=0;"                       # Meshes
                  "-nurbscurve=0;"                 # Nurbs Curves
                  "-nurbssurface=0;"               # Nurbs Surfaces
                  "-volumes=0;"                    # Volume Primitives
                  "-vtxcolours=0;"                 # Export Vertex Colours
                  "-vtxnormals=0;"                 # Export Vertex Normals
                  "-vtxuvs=0;"                     # Export Texture Coordinates
                  "-selective=0;"                  # Extract Important Xforms only
                  "-constraints=0;"                # Constraints
                  "-ik=0;"                         # Ik Chains
                  "-compact=0;"                    # Remove Orients & Pivots
                  "-blendshape=1;"                 # Blend Shapes
                  "-clusters=0;"                   # Clusters
                  "-jiggle=0;"                     # Jiggle deformers
                  "-lattice=0;"                    # Lattices (FFD's)
                  "-jointcluster=0;"               # Rigid Skinning
                  "-skinning=1;"                   # Smooth Skinning (SkinClusters)
                  "-nonlinear=0;"                  # Non-Linear Deformers
                  "-wire=0;"                       # Wire Deformers
                  "-wrap=0;"                       # Wrap Deformers
                  "-sculpt=0;"                     # Sculpt Deformers
                  "-field=0;"                      # Dynamics Fields
                  "-particles=0;"                  # Particles
                  "-anim=1;"                       # Animation
                  #"-sampled=1;"                   # Sampled animation
                  #"-animcurves=0;"                # Animation Curves
                  "-timeline=0;"                   # Use Timeline
                  "-start=" + str(start) + ";"     # Start Frame
                  "-end=" + str(end) + ";")        # End Frame
    return xmdoptions