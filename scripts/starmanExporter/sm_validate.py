#--------------------------------------------------------
#scripted by: Linh Nguyen
#description: Checks scene a validates if the data is
#correct for the starman rig generation.
#--------------------------------------------------------

class sm_validate(object):

    def __init__(self, name):
        self.name = name

    def check_group(self):
        print 'checking scene'