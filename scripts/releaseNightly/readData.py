#-----------------------------------------------------------------------------------#
# Scripted By: Linh Nguyen                                                          #
# Description: Allows for switching the Maya tools, Rigs, and Characters to         #
# Release or Nightly builds                                                         #
#-----------------------------------------------------------------------------------#

import json

# Reads the passed in release nightly data file
class rn_data(object):

    def __init__(self, data_path, version):
        self.data_path = data_path
        self.version = version
        self.read_data()

    # Reads the starman data file and returns a dictionary of values
    def read_data(self):
        with open(self.data_path) as self.data_file:
            self.data = json.load(self.data_file)

    # returns the maya prefs path
    def get_maya_pref(self):
        return self.data[self.version]['MAYA_PREF']

    # returns the maya module location
    def get_maya_module_location(self):
        return self.data[self.version]['MAYA_MODULE']

    def get_module_file_name(self):
        return self.data[self.version]['MODULE_FILE_NAME']

    def get_module_name(self):
        return self.data[self.version]['MODULE_NAME']

    def get_module_version(self):
        return self.data[self.version]['MODULE_VERSION']

    # returns data from the json file referring to the tools release section
    # mode
    # 0 = release
    # 1 = nightly
    # data
    # 0 = Tools Release Shelf Path
    # 1 = Tools Release Script Path
    # 2 = Module Pipeline Path
    # return types
    # maya shelf path = string
    # maya script path = string list
    # maya module name = string
    def get_tools(self, mode = 0, data = 0):
        if mode == 0 and data == 0:
            return self.data[self.version]['TOOLS']['RELEASE']['MAYA_SHELF_PATH']
        elif mode == 0 and data == 1:
            return self.data[self.version]['TOOLS']['RELEASE']['MAYA_SCRIPT_PATH']
        elif mode == 0 and data == 2:
            return self.data[self.version]['TOOLS']['RELEASE']['MODULE_PIPELINE_PATH']
        elif mode == 1 and data == 0:
            return self.data[self.version]['TOOLS']['NIGHTLY']['MAYA_SHELF_PATH']
        elif mode == 1 and data == 1:
            return self.data[self.version]['TOOLS']['NIGHTLY']['MAYA_SCRIPT_PATH']
        elif mode == 1 and data == 2:
            return self.data[self.version]['TOOLS']['NIGHTLY']['MODULE_PIPELINE_PATH']
        else:
            return None

    # returns data from the json file referring to the rigs release section
    # mode
    # 0 = release
    # 1 = nightly
    # data
    # 0 = Rig
    # 1 = Characters
    # 2 = Rig Environment Variable Name
    # return types
    # rig = string
    # characters = string list
    def get_rig(self, mode = 0, data = 0):
        if mode == 0 and data == 0:
            return self.data[self.version]['RIG']['RELEASE']['MAYA_RIG_PATH']
        elif mode == 0 and data == 1:
            return self.data[self.version]['RIG']['RELEASE']['MAYA_CHARACTER_PATH']
        elif mode == 0 and data == 2:
            return self.data[self.version]['RIG']['RELEASE']['RIG_ENV_VAR']
        elif mode == 1 and data == 0:
            return self.data[self.version]['RIG']['NIGHTLY']['MAYA_RIG_PATH']
        elif mode == 1 and data == 1:
            return self.data[self.version]['RIG']['NIGHTLY']['MAYA_CHARACTER_PATH']
        elif mode == 1 and data == 2:
            return self.data[self.version]['RIG']['NIGHTLY']['RIG_ENV_VAR']
        else:
            return None