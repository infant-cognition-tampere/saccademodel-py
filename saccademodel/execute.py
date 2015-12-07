from .preprocess import gaze_repair
from math import floor
from .em import saccade_model_em

def fit(pointlist):
    '''
    Parameter
      pointlist
        [[x0,y0], [x1,y1], ...]
    '''

    gapless_pointlist = gaze_repair(pointlist)
    src, sacc, tgt, mle = saccade_model_em(gapless_pointlist)

    return {
        'source_points': src,
        'saccade_points': sacc,
        'target_points': tgt,
        'mean_squared_error': mle
    }
