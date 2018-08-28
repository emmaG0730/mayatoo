###############################################################################
#CREATOR: SEAN "HiGGiE" HIGGINBOTTOM                                          #
###############################################################################
from functools import wraps
import maya.cmds as py
###############################################################################
#"""# ADDS FUNCTION TO AN UNDO CHUNK                                          #
###############################################################################  
def undo(chunk):
    @wraps(chunk)
    def undoFunction(*args, **kwargs):
        try:
            py.undoInfo(ock=1);
            return chunk(*args,**kwargs);
        finally:
            py.undoInfo(cck=1);
    return undoFunction