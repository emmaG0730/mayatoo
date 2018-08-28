#--------------------------------------------------------
#scripted by: Linh Nguyen
#description: Batch exports the starman rig
#--------------------------------------------------------
try:
    import maya.standalone
    maya.standalone.initialize()
except:
    pass

import maya.cmds as cmds
import json
import sys
import os
try:
    import sm_exportWeapon as sm_exportWeapon
except:
    import starmanExporter.sm_exportWeapon as sm_exportWeapon
import logging
import datetime

class batch_starman(object):

    def __init__(self, data_path):
        self.data_path = data_path
        self.directory = ''
        self.logpath = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/logs/'
        self.current_time = datetime.datetime.now()
        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)
        self.logging = logging.getLogger(__name__)
        hdlr = logging.FileHandler(self.logpath + 'starman_'
                                   + str(self.current_time.year) + '_'
                                   + str(self.current_time.month) + '_'
                                   + str(self.current_time.day) + '_'
                                   + str(self.current_time.hour) + '_'
                                   + str(self.current_time.minute) + '_'
                                   + str(self.current_time.second) + '_' +  '.log')
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logging.addHandler(hdlr)
        self.logging.setLevel(logging.INFO)

    # Opens the passed in Maya file
    def open_maya_file(self, maya_file, character):
        self.get_export_data(character)
        spaces1 = len('Finished generating ' + self.export_data['export_location'] + (maya_file.split('.'))[0] + '.json')

        print '-' * spaces1
        print 'Opening', self.directory + maya_file
        self.logging.info('Opening', self.directory + maya_file)
        print '-' * spaces1
        print '\n'
        cmds.file(self.directory + maya_file, force=True, open=True)
        self.export_starman(self.export_data['starman_data_file'],
                            maya_file,
                            self.export_data['namespace'],
                            self.export_data['data_type'],
                            self.export_data['master_controller'],
                            self.export_data['export_location'])
        print '-' * spaces1
        print 'Finished generating', self.export_data['export_location'] + (maya_file.split('.'))[0] + '.json'
        self.logging.info('Finished generating', self.export_data['export_location'] + (maya_file.split('.'))[0] + '.json')
        print '-' * spaces1
        print '\n'


    def export_starman(self, data_path, filename, namespace, type, master_control, export_location):
        sm_export = sm_exportWeapon.sm_export_rig(data_path, filename, namespace, type, master_control, export_location, self.logging)
        sm_export.check_scene()
        sm_export.export_scene()

    # Reads the starman data file and returns a dictionary of values
    def read_data(self):
        with open(self.data_path) as self.data_file:
            self.data = json.load(self.data_file)

    # Loops through the list of Maya files and exports the data
    def batch_export(self):
        for i in self.data:
            self.animation_directories = self.get_export_directories(i)
            for self.directory in self.animation_directories:
                self.get_file_list(self.directory)
                for animation in self.file_list:
                    self.open_maya_file(animation,i)

    def get_export_data(self, character):
        self.export_data = self.data[character]['export_data']

    def get_export_directories(self, character):
        return self.data[character]['animation_directories']

    def get_file_list(self, directory):
        self.file_list = []
        for file in os.listdir(directory):
            if file.endswith(".ma"):
                self.file_list.append(file)

def main():
    path = os.path.join(sys.path[0],'../DataFiles/starman_weapon_export_data.json')
    starman = batch_starman(path)
    starman.read_data()
    starman.batch_export()

main()