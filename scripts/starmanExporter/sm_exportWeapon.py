#--------------------------------------------------------
#scripted by: Linh Nguyen
#description: Exports the starman rig
#--------------------------------------------------------

###############################################################################
#"""# HiGGiE IMPORT METHOD START: IMPORT ADDITIONAL MODULES                   #
###############################################################################
import os
import sys
import logging
import maya.cmds as cmds
path = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/';
module = path+'sm_readData.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import sm_readData# = reload();
###############################################################################
#"""# HiGGiE IMPORT METHOD END: IMPORT ADDITIONAL MODULES                     #
###############################################################################

class sm_export_rig(object):

    def __init__(self, data_path, filename, namespace, type, master_control, export_location, logging, weapon):
        self.data_path = data_path
        self.filename = filename
        self.namespace = namespace
        self.type = type
        self.logging = logging
        self.startFrame = 0
        self.endFrame = 0
        self.master_control = master_control
        self.filepath = export_location
        self.smr = sm_readData.starman_data(self.data_path)
        self.smr.read_data()
        self.weapon_data = self.smr.get_weapon_data(weapon)
        self.check_scene_type()
        self.get_loop_status()


    def check_scene_type(self):
        self.filetype = (self.filename.split('_'))[0]

    def get_loop_status(self):
        if self.filetype == 'CHAR':
            self.b_loop = cmds.getAttr(self.master_control + '.LOOP')
            self.b_loop = self.convert_binary_bool(self.b_loop)
            self.export_scene()#!
        elif self.filetype == 'RIG':
            self.b_loop = cmds.getAttr(self.master_control + '.LOOP')
            self.b_loop = self.convert_binary_bool(self.b_loop)
            self.export_scene()#!
        elif self.filetype == 'ANIM':
            if cmds.objExists(self.namespace + ':' + self.master_control):
                self.b_loop = cmds.getAttr(self.namespace + self.master_control + '.LOOP')
                self.b_loop = self.convert_binary_bool(self.b_loop)
                self.export_scene()#!
        else:
            cmds.error("Missing Loop Data")
            pass

    def convert_binary_bool(self, binary_value):
        if binary_value == 0:
            return False
        elif binary_value == 1:
            return True
        else:
            return False

    def check_scene(self):
        for i in self.weapon_data:
            if self.filetype == 'CHAR' or self.filetype == 'RIG':
                status = self.check_exist(i['name'])

            elif self.filetype == 'ANIM':
                status = self.check_exist(self.namespace + i['name'])
            else:
                cmds.error('Cannot determine scene type')

    # returns the item with the longest set of characters
    def find_longest_string(self, list, item, key):
        longest_string = 0
        if key == None:
            for i in list:
                char_count = len(i[item])
                if char_count > longest_string:
                    longest_string = char_count
        else:
            for i in list:
                char_count = len(str(i[item][key]))
                if char_count > longest_string:
                    longest_string = char_count
        return longest_string

    # checks scene if all the parts of the starman rig exists
    def check_exist(self, object):
        self.object = object
        print self.object
        if cmds.objExists(self.object):
            return self.object
        else:
            cmds.error ('Warning:',self.object,'does not exist')
            return False

    # finds the current animation range
    def get_animation_range(self):
        print '>>>>>>>>>>>>>>>', self.namespace +  self.master_control
        if cmds.objExists(self.namespace +  self.master_control):
            self.startFrame = cmds.playbackOptions(min=1,q=1);
            self.endFrame = cmds.playbackOptions(max=1,q=1);
        else:
            print 'No object name ' + 'b_M_pelvis_v1_JNT' + ' was found'
            print 'No object name ' + self.master_control + ' was found'
            cmds.error('No object name ' + 'b_M_pelvis_v1_JNT' + ' was found')
            cmds.error('No object name ' + self.master_control + ' was found')

    # takes in a list of dictionary items and allows to return a sibling value of
    # users choice
    def get_value_of(self, list_dict, keyA, valA, keyB):
        for i in list_dict:
            if i[keyA] == valA:
                return i[keyB]
            else:
                pass
        return None

    # returns a list of the rig position data
    def get_rig_data(self):
        self.rig_data = []
        if self.type == 'integer':
            for object in self.weapon_data:
                object_position = {
                    "x": int(round(cmds.getAttr(object['name'] + '.translateX'))),
                    "y": int(round(cmds.getAttr(object['name'] + '.translateY'))),
                    "z": int(round(cmds.getAttr(object['name'] + '.translateZ')))
                }
                object_data = [object['name'], object_position]
                self.rig_data.append(object_data)

        elif self.type == 'float':
            for object in self.weapon_data:
                object_position = {
                    "x": cmds.getAttr(object['name'] + '.translateX'),
                    "y": cmds.getAttr(object['name'] + '.translateY'),
                    "z": cmds.getAttr(object['name'] + '.translateZ')
                }
                object_data = [object['name'], object_position]
                self.rig_data.append(object_data)
        else:
            cmds.error ('Invalid data type.  Needs integer or float')

    # Returns a list of the positional data from the starman components
    def get_frame_data(self):
        frame_data = []
        if self.type == 'integer':
            for object in self.weapon_data:
                object_position = {
                                        "x" : int(cmds.getAttr(self.namespace + object['name'] + '.translateX')),
                                        "y" : int(cmds.getAttr(self.namespace + object['name'] + '.translateY')),
                                        "z" : int(cmds.getAttr(self.namespace + object['name'] + '.translateZ'))
                }
                object_data = [object['name'], object_position]
                frame_data.append(object_data)

        elif self.type == 'float':
            for object in self.joint_data:
                object_position = {
                                        "x" : cmds.getAttr(self.namespace + object['name'] + '.translateX'),
                                        "y" : cmds.getAttr(self.namespace + object['name'] + '.translateY'),
                                        "z" : cmds.getAttr(self.namespace + object['name'] + '.translateZ')
                }
                object_data = [object['name'], object_position]
                frame_data.append(object_data)
        else:
            cmds.error('Invalid data type.  Needs integer or float')
            pass

        return frame_data

    # parses through all of the frames in the animation and stores a list of frame data
    def get_animation_data(self):
        self.animation_data = []
        self.get_animation_range()
        for frame in range (int(self.endFrame)+1):
            cmds.currentTime(frame)
            self.animation_data.append(self.get_frame_data())

    # generates the string data for the List section
    def write_rig_position_data(self):
        name_char_count = self.find_longest_string(self.rig_data, 0, None)
        x_count = self.find_longest_string(self.rig_data, 1, 'x')
        y_count = self.find_longest_string(self.rig_data, 1, 'y')
        z_count = self.find_longest_string(self.rig_data, 1, 'z')
        position_counts = [x_count, y_count, z_count]
        position_max = max(position_counts)

        self.rig_json = '    "Radius" : 50,\n\n    "Sphere" : [\n'
        for i in self.rig_data:
            name_spacing = (name_char_count + 2) - (len(i[0]))

            x_spacing = (position_max + 1) - (len(str(i[1]['x'])))
            y_spacing = (position_max + 1) - (len(str(i[1]['y'])))
            z_spacing = (position_max + 1) - (len(str(i[1]['z'])))

            radius = self.get_value_of(self.joint_data, 'name', i[0], 'radius')
            self.rig_json += '    {"Name" : "' + i[0] \
                  + '",' + (' ' * name_spacing) + '"Radius" : '+ str(radius) \
                  + ', "Color" : {"r" : 1.0, "g" : 0.0, "b" : 0.0, "a" : 1.0 }, "Position" : {"x" : ' + str(i[1]['x']) \
                  + ',' +  (' ' * x_spacing ) + '"y" : ' + str(i[1]['y']) \
                  + ',' +  (' ' * y_spacing ) + ' "z" : ' + str(i[1]['z']) + (' ' * z_spacing) + '}}'
            if i != self.rig_data[-1]:
                self.rig_json += ',\n'
            else:
                self.rig_json += ']'

    # generates the string data for the Connect section
    def write_capsule_data(self):
        name_char_count = self.find_longest_string(self.rig_data, 0, None)

        self.capsules_json = '    "Capsules" : [\n'
        for i in self.rig_data:
            name_spacing = (name_char_count + 2) - (len(i[0]))

            self.capsules_json += '    {"a" : "' + self.rig_data[0][0] + '", "b" : "' + i[0] + '"' + (' ' * name_spacing) + '}'
            if i != self.rig_data[-1]:
                self.capsules_json += ',\n'
            else:
                self.capsules_json += ']'

    def write_rig_data(self):
        self.write_rig_position_data()
        self.write_capsule_data()
        self.rig_export_data = "{\n"
        self.rig_export_data += self.rig_json + '\n    ,\n\n' \
                                + self.capsules_json + '\n}'
        self.write_file(self.rig_export_data)

    def write_file(self, data):
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        self.exported_file = open(self.filepath + (self.filename.split('.'))[0] + '_BODY_weap.json', 'w')
        self.exported_file.write(data)
        self.exported_file.close()

    def write_animation_data(self):
        self.animation_json = '{\n    "Name" : "' \
                              + (self.filename.split('.'))[0] + '_BODY_weap' \
                              + '",\n    "Loop" : ' + (str(self.b_loop)).lower() \
                              + ',\n    "Type" : "keyframe",\n    "Frames" : [\n'
        name_char_count = self.find_longest_string(self.animation_data[0], 0, None)
        for i in range(len(self.animation_data)):
            x_count = self.find_longest_string(self.animation_data[i], 1, 'x')
            y_count = self.find_longest_string(self.animation_data[i], 1, 'y')
            z_count = self.find_longest_string(self.animation_data[i], 1, 'z')
            position_counts = [x_count, y_count, z_count]
            position_max = max(position_counts)
            time_spacing = (4) - len(str(i))


            self.animation_json += '        {"Time" : ' + str(i) +  ',' + (' ' * time_spacing) + '"Pose" :['
            for j in self.animation_data[i]:
                name_spacing = (name_char_count + 1) - (len(j[0]))

                x_spacing = (position_max + 1) - (len(str(j[1]['x'])))
                y_spacing = (position_max + 1) - (len(str(j[1]['y'])))
                z_spacing = (position_max + 1) - (len(str(j[1]['z'])))

                if j == self.animation_data[i][0]:
                    self.animation_json += '{"Name" : "' + j[0]\
                                           +  '",' + (' ' * (name_spacing)) + '"Position" : {"x" :' + str(j[1]['x']) \
                                           + ',' +  (' ' * x_spacing ) + '"y" :' + str(j[1]['y']) \
                                           + ',' +  (' ' * y_spacing ) + '"z" :' + str(j[1]['z']) \
                                           + (' ' * z_spacing ) +  "}}"
                else:
                    self.animation_json += '                                {"Name" : "' + j[0] \
                                           +  '",' + (' ' * name_spacing) + '"Position" : {"x" :' + str(j[1]['x'])\
                                           + ',' +  (' ' * x_spacing ) + '"y" :' + str(j[1]['y'])\
                                           + ',' +  (' ' * y_spacing ) + '"z" :' + str(j[1]['z']) \
                                           + (' ' * z_spacing ) + "}}"
                if j != self.animation_data[i][-1]:
                    self.animation_json += ',\n'
                else:
                    self.animation_json +=' ]},\n'
        self.animation_json = self.animation_json[:-2]
        self.animation_json += '\n    ]\n }'

        self.write_file(self.animation_json)

    def export_scene(self):
        if self.filetype == 'CHAR' or self.filetype == 'RIG':
            self.get_rig_data()
            self.write_rig_data()
        elif self.filetype == 'ANIM':
            self.get_animation_data()
            self.write_animation_data()
        else:
            cmds.error('Unknown Filetype')

#def main():
#    log = logging.getLogger(__name__)
#    sm_export = sm_export_rig('R:/Jx4/tools/dcc/maya/scripts/starmanExporter/starman_settings/sm_weapon_data.json',
#                              'ANIM_MA_airAttackKnockDown01_01.ma',
#                              'RiGGiE:',
#                              'integer',
#                              'c_M_character_v1_GRP',
#                              'R:/Jx4/client/GameWorld/Character/starMan/MaleAdult/weapon/',
#                              log
#                              )
#    sm_export.check_scene_type()
#    sm_export.check_scene()
#    sm_export.export_scene()
#main()