#--------------------------------------------------------
#scripted by: Linh Nguyen
#description: Creates a starman rig based on the passed
#in data
#--------------------------------------------------------


###############################################################################
#"""# HiGGiE IMPORT METHOD START: IMPORT ADDITIONAL MODULES                   #
###############################################################################
import os
import sys
import maya.cmds as cmds
path = 'R:/Jx4/tools/dcc/maya/scripts/starmanExporter/';
module = path+'sm_readData.py';
sys.path.append(os.path.dirname(os.path.expanduser(module)));
import sm_readData# = reload();
###############################################################################
#"""# HiGGiE IMPORT METHOD END: IMPORT ADDITIONAL MODULES                     #
###############################################################################


class create_starman_rig(object):

    def __init__(self, name):
        self.name = name

    # takes in a list of dictionary items and allows to return a sibling value of
    # users choice
    def get_value_of(self, list_dict, keyA, valA, keyB):
        for i in list_dict:
            if i[keyA] == valA:
                return i[keyB]
            else:
                pass
        return None

    # creates a sphere using the passed in data
    # the spheres are constrained to the assigned joint
    def create_joint(self, joint_name, radius, parentJoint, root):
        self.joint_name = joint_name
        self.radius = radius
        self.root = root
        self.parentJoint = parentJoint

        cmds.select(d = True)
        print 'root =', self.root
        self.sm_joint = cmds.polySphere(radius = self.radius, name = self.joint_name)
        self.parent_const = cmds.parentConstraint(self.parentJoint, self.joint_name)
        self.parent = cmds.parent(self.joint_name, self.root)

    # creates a weapon hierarchy that enables the end sphere to always be placed at the
    # tip of the weapon
    def createWeapon(self, weapon_data):
        self.weapon_data = weapon_data
        self.weapon_start_list = []
        self.weapon_end_list = []

        for i in self.weapon_data:
            if i['attach_type'] == 'start':
                self.weapon_start_list.append(i)
                print 'start = ', i['name']
            elif i['attach_type'] == 'end':
                self.weapon_end_list.append(i)
                print 'end = ', i['name']
            else:
                print 'this should not happen'

        for i in self.weapon_start_list:
            self.create_joint(i['name'], i['radius'], i['parent'], i['root'])

        for i in self.weapon_end_list:
            # create end weapon locator for reference location
            self.end_weapon_loc = cmds.spaceLocator(name = i['parent'])
            self.end_weapon_loc_point_constrait = cmds.pointConstraint(i['root'], self.end_weapon_loc)
            
            cmds.delete(self.end_weapon_loc_point_constrait)
            cmds.parent(self.end_weapon_loc[0], i['root'])
            
            #HiGGiE: SET VALUES TO ZERO TO ORIENT TO PARENT
            cmds.setAttr(self.end_weapon_loc[0] + '.r',0,0,0);
            
            # shifts the weapon locator based on the offset data
            cmds.setAttr(self.end_weapon_loc[0] + '.translateX',i['offset']['x'])
            cmds.setAttr(self.end_weapon_loc[0] + '.translateY',i['offset']['y'])
            cmds.setAttr(self.end_weapon_loc[0] + '.translateZ',i['offset']['z'])

            self.weapon_joint = self.get_value_of(self.weapon_start_list,'name', i['root'], 'parent')
            self.end_weapon_loc_parent_constraint = cmds.parentConstraint(self.weapon_joint, self.end_weapon_loc[0], maintainOffset = True)
            self.create_joint(i['name'], i['radius'], i['parent'], self.weapon_start_list[0]['root'])#i['root'])

    def create_starman_group(self):
        self.sm_group = cmds.group(empty = True, name = 'Starman')
        return self.sm_group
    
    def create_trajectory(self, traj_name, traj_parent):
        self.traj_name = traj_name
        self.traj_parent = traj_parent
        
        self.traj_loc = cmds.spaceLocator(name = self.traj_name)
        self.traj_parent_constraint = cmds.parentConstraint(self.traj_parent, self.traj_loc[0])
        
        return self.traj_loc

def main(weapon):
    smd = sm_readData.starman_data('R:/Jx4/tools/dcc/maya/scripts/starmanExporter/starman_settings/sm_data.json')
    smd.read_data()
    sm_joint_data = smd.get_joint_data()
    sm_trajectory_data = smd.get_trajectory_data()
    smr = create_starman_rig('XYL')
    sm_group = smr.create_starman_group()

    sm_trajectory = smr.create_trajectory(sm_trajectory_data['name'], sm_trajectory_data['parent'])

    for i in sm_joint_data:
        smr.create_joint(i['name'], i['radius'], i['parent'], i['root'])
        
    createWeapon(weapon)#!
    
    cmds.parent(sm_trajectory, sm_group)

def createWeapon(weapon):
    smwd  = sm_readData.starman_data('R:/Jx4/tools/dcc/maya/scripts/starmanExporter/starman_settings/sm_weapon_data.json')
    smwd.read_data()
    sm_weapon_data = smwd.get_weapon_data(weapon)
    print sm_weapon_data
    smwr = create_starman_rig(weapon)

    smwr.createWeapon(sm_weapon_data)