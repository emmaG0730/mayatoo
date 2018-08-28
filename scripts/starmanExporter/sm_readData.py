#--------------------------------------------------------
#scripted by: Linh Nguyen
#description: Gets the needed data from the sm_data file.
#--------------------------------------------------------

import json

# Reads the passed in starman data file
class starman_data(object):

    def __init__(self, data_path):
        self.data_path = data_path

    # Reads the starman data file and returns a dictionary of values
    def read_data(self):
        with open(self.data_path) as self.data_file:
            self.data = json.load(self.data_file)

    def get_trajectory_data(self):
        return self.data['trajectory'][0]

    def get_joint_data(self):
        return self.data['starman_joints']

    # accepted weapon types - weapon_01, weapon_02, weapon_10
    def get_weapon_data(self, weaponType):
        print self.data
        return self.data[weaponType]