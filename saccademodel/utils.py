'''
Here we use two different concepts, times and indices:
    Time t  0 1 2 3 4 5
            | | | | | |
    Vector [ 2 3 1 2 1 ]
             | | | | |
    Index i  0 1 2 3 4
'''

def select_points_before_time(X, t):
    # Return points before given time index
    return select_first_points(X, t)

def select_points_after_time(X, t):
    # Return columns after given time index.
    return X[t:] # Python handles out of range cases by returning []

def select_first_points(X, n):
    # Return first max n points of X.
    return X[:n]

def select_last_points(X, n):
    # Return last max n points of X
    if n > 0:
        return X[-n:]
    else:
        return []

def select_points_time_to_time(X, t1, t2):
    # Return points according to the time interpretation of indices.
    # Precondition: t1 <= t2 and t1,t2 >= 0.
    # Return points from t1 to end, use .._to_time(X, t1, None)
    return X[t1:t2] # Element at index t2 is excluded

def mean_point(X):
    # Calculate mean of the points
    sum_x = 0
    sum_y = 0
    for p in X:
        sum_x += p[0]
        sum_y += p[1]
    n = len(X)
    return [float(sum_x) / n, float(sum_y) / n]

def weighted_mean_point(X, W):
    # Precondition: sum(W) = 1
    sum_x = 0.0
    sum_y = 0.0
    for p, w in zip(X, W):
        sum_x += w * p[0]
        sum_y += w * p[1]
    return [sum_x, sum_y]



class TimePairValueHistory(object):


    def __init__(self):
        self._history = {}
        self._min_value_t1 = -1
        self._min_value_t2 = -1
        self._min_value = float('inf')
        self._min_value_data = None


    def is_visited(self, t1, t2):
        k1 = str(t1)
        k2 = str(t2)
        if k1 in self._history:
            if k2 in self._history[k1]:
                return True
        return False


    def is_minimal(self, t1, t2):
        return t1 == self._min_value_t1 and t2 == self._min_value_t2


    def visit(self, t1, t2, value, data):
        '''
        Return nothing
        '''
        if self.is_visited(t1, t2):
            return

        k1 = str(t1)
        k2 = str(t2)
        if k1 not in self._history:
            self._history[k1] = {}
        self._history[k1][k2] = True

        if value < self._min_value:
            self._min_value = value
            self._min_value_t1 = t1
            self._min_value_t2 = t2
            self._min_value_data = data


    def get_minimum(self):
        '''
        Return
            (t1, t2, value) triple where the value is the minimal one.
        '''
        return (self._min_value_t1, self._min_value_t2,
                self._min_value,    self._min_value_data)
