#--------------------------------------------------------
#scripted by: Linh Nguyen
#description: Batch exports the starman rig
#--------------------------------------------------------
#try:
import maya.standalone
maya.standalone.initialize()
#except:
#    pass
#import time
import maya.cmds as cmds
import json
import sys
sys.path.append('R:/Jx4/tools/external/p4/')
import P4
import os
try:
    import sm_exportRig as sm_exportRig
except:
    import starmanExporter.sm_exportRig as sm_exportRig
import logging
import datetime

class batch_starman(object):

    def __init__(self, data_path, file_paths):
        self.p4 = P4.P4()
        self.data_path = data_path
        self.file_paths = file_paths
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

    def get_character(self,filepath):
        self.p4.connect()
        self.clientData = self.p4.fetch_client()
        self.p4.disconnect()
        self.clientRoot = self.clientData['Root'].replace('\\', '/')
        character = (filepath.replace(self.clientRoot, '').split('/'))[4]

        #return character
        return 'MaleAdult'

    # Reads the starman data file and returns a dictionary of values
    def read_data(self):
        with open(self.data_path) as self.data_file:
            self.data = json.load(self.data_file)
        print self.data['MaleAdult']['export_data']['starman_data_file']

    # Loops through the list of Maya files and exports the data
    def batch_export(self, fileList):
        for i in fileList:
            character = self.get_character(i)
            print i
            print fileList[i]
            print character
            self.open_maya_file(i, fileList[i], character)

    def get_export_data(self, character):
        self.export_data = self.data[character]['export_data']

    def get_file_list(self):
        with open(self.file_paths) as self.file_paths_file:
            self.file_path_list = json.load(self.file_paths_file)
            return self.file_path_list


    # Opens the passed in Maya file
    def open_maya_file(self, maya_file, json_file, character):
        self.get_export_data(character)
        spaces1 = len('Finished generating ' + json_file)

        print '-' * spaces1
        print 'Opening', self.directory + maya_file
        self.logging.info('Opening', self.directory + maya_file)
        print self.export_data['starman_data_file'],\
            maya_file,\
            self.export_data['namespace'],\
            self.export_data['data_type'],\
            self.export_data['master_controller'],\
            json_file + '/'
        print '-' * spaces1
        print '\n'
        cmds.file(self.directory + maya_file, force=True, open=True)
        self.export_starman(self.export_data['starman_data_file'],
                            maya_file,
                            self.export_data['namespace'],
                            self.export_data['data_type'],
                            self.export_data['master_controller'],
                            json_file)
                            #self.export_data['export_location'] + character + '/')
        print '-' * spaces1
        print 'Finished generating', json_file
        self.logging.info('Finished generating', json_file)
        print '-' * spaces1
        print '\n'

    def export_starman(self, data_path, filename, namespace, type, master_control, export_location):
        sm_export = sm_exportRig.sm_export_rig(data_path, filename, namespace, type, master_control, export_location, self.logging)
        sm_export.check_scene()
        sm_export.export_scene()


def main():
    #start_time = time.time()
    path = 'r:/Jx4/tools/'
    mayaScriptPath = path + 'dcc/maya/nightly/scripts/'
    starman = batch_starman(mayaScriptPath + '/DataFiles/starman_export_data.json',
                            path + 'internal/animationExplorer\data\starman.json')
                            #path + 'internal/animationPipeline/data/animation_starman_export_data.json')
    starman.read_data()
    fileList = starman.get_file_list()
    starman.batch_export(fileList)
    #print("--- %s seconds ---" % (time.time() - start_time))

main()