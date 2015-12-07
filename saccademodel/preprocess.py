from .interpolate import interpolate_using_previous

def gaze_repair(pointlist):
    '''
    Fill gaps in the gazepoints.

    Parameter
      pointlist
        list of [x, y] lists
    Return
      pointlist
    '''

    repaired = interpolate_using_previous(pointlist)

    return repaired
