
class InterpolationError(Exception):
    pass

def interpolate_using_previous(pointlist):
    '''
    Throw
        InterpolationError
            if a key has no non-null values

    Return
        pointlist without gaps
    '''
    pl = pointlist # alias
    npl = [] # new, interpolated pointlist

    if len(pl) < 1:
        raise InterpolationError('Empty list cannot be interpolated')

    first_nonnull = [None, None]

    # Find first non-nulls
    for i in [0, 1]:
        for p in pl:
            if p[i] is not None:
                first_nonnull[i] = p[i]
                break

    if first_nonnull[0] == None or first_nonnull[1] == None:
        # No good values found for every key
        raise InterpolationError('No non-null values to interpolate against: ' + str(first_nonnull))

    prev_nonnull = first_nonnull

    for p in pl:
        np = list(p)  # Copy point, this way we avoid modifying the original.
        for k in [0, 1]:
            if np[k] is None:
                np[k] = prev_nonnull[k]
            else:
                prev_nonnull[k] = np[k]
        npl.append(np)

    return npl
