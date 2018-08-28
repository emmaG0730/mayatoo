import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

def getMesh():
    # get the active selection
    selected = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selected)
    hilited = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getHiliteList(hilited)
    if hilited.length() > 0:
        selected.merge(hilited, 0)
    # dir(OpenMaya.MGlobal)
    return OpenMaya.MItSelectionList(selected, OpenMaya.MFn.kMesh)


def getMeshObject(iterMesh=None):
    if iterMesh is None: iterMesh = getMesh()
    meshObject = None
    if not iterMesh.isDone():
        dagPath = OpenMaya.MDagPath()
        iterMesh.getDagPath(dagPath)
        return dagPath.node()
    else:
        return meshObject


def getMeshPath():
    iterMesh = getMesh()
    if not iterMesh.isDone():
        dagPath = OpenMaya.MDagPath()
        iterMesh.getDagPath(dagPath)
        return dagPath


def getMeshMaterialOrder(path=None):
    if path is None: path = getMeshPath()

    meshFn = OpenMaya.MFnMesh(path)
    shaders = OpenMaya.MObjectArray()
    faces = OpenMaya.MIntArray()
    meshFn.getConnectedShaders(0, shaders, faces)

    material_names = []
    for i in range(shaders.length()):
        shader = shaders[i]
        shader_node = OpenMaya.MFnDependencyNode(shader)
        shader_name = shader_node.name()
        mat_name = cmds.listConnections(shader_name + '.surfaceShader')
        material_names.append(mat_name)

    return material_names

def resetMeshMaterialOrder(path=None):
    if path is None: path = getMeshPath()
    mesh_name = path.partialPathName()

    meshFn = OpenMaya.MFnMesh(path)
    shaders = OpenMaya.MObjectArray()
    faces = OpenMaya.MIntArray()
    meshFn.getConnectedShaders(0, shaders, faces)

    face_ids_fbx = []
    shader_names = []
    material_names = []
    shader_faces = []

    if shaders.length() > 1:
        for i in range(faces.length()):
            id = faces[i]
            if not id in face_ids_fbx: face_ids_fbx.append(id)
        for i in range(shaders.length()):
            shader = shaders[i]
            shader_node = OpenMaya.MFnDependencyNode(shader)
            shader_name = shader_node.name()
            mat_name = cmds.listConnections(shader_name + '.surfaceShader')
            material_names.append(mat_name)

            shader_sets = cmds.sets(shader_name, q=1)
            shader_names.append(shader_name)
            shader_faces.append(shader_sets)

        materials = []
        for k, id in enumerate(face_ids_fbx):
            set = mesh_name if (k == 0) else shader_faces[id]
            cmds.sets(set, e=1, fe=shader_names[id])
            materials.append(material_names[id])

        return materials
    else:
        return None

print "previous material order >> ", getMeshMaterialOrder()
print "adjusted material order >> ", resetMeshMaterialOrder()