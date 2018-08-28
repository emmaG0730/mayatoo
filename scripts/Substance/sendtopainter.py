import maya.cmds as cmds
import os
import _winreg
from subprocess import Popen

# todo: option for user to define dest path? show user the dest path?
# todo: if spp file is stored on perforce we'll need to checkout the file as well


def export_scene():
    """Export current scene and return export file path."""
    try:
        # check for mesh
        mesh = cmds.ls(typ='mesh')
        if not mesh:
            cmds.warning('{0}: No mesh to export.'.format(__file__))
            return None
        else:
            cmds.select(mesh)
        # check plug-in
        if not cmds.pluginInfo('fbxmaya', q=True, l=True):
            cmds.loadPlugin('fbxmaya')

        file_path = cmds.file(q=True, exn=True)
        # todo: exclude unnecessary stuff for exporting, the engine only read .mesh now
        # painter doesn't support fbx 2016 yet
        # todo: checkout exported file from perforce
        return cmds.file(file_path, typ='DAE_FBX export', es=True)
    except:  # todo: too broad exception, need to narrow down
        cmds.warning('{0}: Failed to export scene.'.format(__file__))


def run_painter(mesh_path):
    """
    Run painter with input mesh file.
    Create painter project if it doesn't exist.
    Set export texture path under mesh folder.
    :param mesh_path: full path for input mesh
    """
    if not mesh_path:
        return
    try:
        # get substance path from registry
        try:
            painter_path_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                               'SOFTWARE\\Classes\\SubstancePainterProject\\shell\\open\\command')
            painter_path = _winreg.QueryValueEx(painter_path_key, '')[0].split(' "')[0][1:-1]
            _winreg.CloseKey(painter_path_key)
        except:  # todo: too broad exception, need to narrow down
            cmds.warning('{0}: Failed to find painter location.'.format(__file__))
        else:
            # painter_exe = os.environ.get('SUB_PAINTER_PATH')
            # get mesh dir
            folder = os.path.dirname(mesh_path)
            file_name = os.path.basename(mesh_path)
            file_base_name = file_name.split('.')[0]
            proj_folder = os.path.join(folder, 'Texture')
            if not os.path.exists(proj_folder):
                os.makedirs(proj_folder)
            proj_file = os.path.join(proj_folder, '{0}.spp'.format(file_base_name))
            # https://support.allegorithmic.com/documentation/display/SPDOC/Command+lines
            Popen([painter_path, proj_file,
                   '--mesh', mesh_path,
                   '--export-path', proj_folder
                   ])
    except:  # todo: too broad exception, need to narrow down
        cmds.warning('{0}: Failed to run Painter.'.format(__file__))


def main():
    run_painter(export_scene())




