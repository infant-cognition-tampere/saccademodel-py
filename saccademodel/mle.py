
from .triangle import Triangle


def saccade_model_mle(gazepoints, src_xy, tgt_xy, init_t_start, init_t_end):
    '''

    Parameter
        gazepoints
        src_xy, 2D list, best quess for saccade start location
        tgt_xy, 2D list, best guess for saccade end location
        init_t_start, best guess for saccade start time
        init_t_end, best guess for saccade end time
    Return
        t_start
            optimal saccade start time.
            gazepoint[t_start] is the first saccade point.
        t_end
            optimal saccade end time.
            gazepoint[t_end - 1] is the last saccade point.
        mse, mean squared error of the model

    Here we use two different concepts, times and indices:
        Time t  0 1 2 3 4 5
                | | | | | |
        Vector [ 2 3 1 2 1 ]
                 | | | | |
        Index i  0 1 2 3 4
    '''

    # Alias
    g = gazepoints

    # Max t, Max index
    max_t = len(g)
    max_i = max_t - 1

    # Dynamic programming memories:
    # 1) For each index i, store the summed square error in t=0..i+1
    #    so that source_mem[0] gives summed square error in t=0..1
    #    and that source_mem[max_i] gives summed square error in t=0..max_t.
    #    Because target_mem[k] = target_mem[k-1] + square_error(k)
    #    calculate values dynamically from the start.
    source_mem = [None for _ in range(max_t)]
    # 2) For each index i, j, i<=j, store the summed square error in t=i..j+1
    #    so that saccade_mem[0][0] gives summed square error in t=0..1
    #    and that saccade_mem[max_i][max_i] gives s.s.e. in t=max_t-1..max_t.
    #    Because i <= j, saccade_mem is upper triangular matrix max_t x max_t
    saccade_mem_n = (max_t * (max_t + 1)) // 2
    saccade_mem = Triangle(max_t, [None for _ in range(saccade_mem_n)])
    # 3) For each index i, store the summed square error in t=i..max_t
    #    so that target_mem[0] gives summed square error in t=0..max_t
    #    and that target_mem[max_i] gives s.s.e. in t=max_t-1..max_t.
    #    Because target_mem[k] = square_error(k) + target_mem[k+1]
    #    calculate values dynamically from the end.
    target_mem = [None for _ in range(max_t)]


    def square_error(index, mu):
        p = g[index]
        dx = p[0] - mu[0]
        dy = p[1] - mu[1]
        return dx * dx + dy * dy


    def source_objective(t_start):
        '''
        Return
            summed square error between t=0 and t=t_start
        '''
        if t_start == 0:
            return 0
        if source_mem[t_start - 1] is not None:
            return source_mem[t_start - 1]
        # else calculate
        for i in range(0, t_start):
            if source_mem[i] is not None:
                continue
            else:
                serr = square_error(i, src_xy)
                if i == 0:
                    source_mem[i] = serr
                else:
                    source_mem[i] = serr + source_mem[i - 1]
        return source_mem[t_start - 1]


    def saccade_objective(t_start, t_end):
        '''
        Return
            summed square error between t=t_start and t=t_end
        '''
        if t_start == t_end:
            return 0
        # Now dt = t_end - t_start > 0
        if saccade_mem[t_start, t_end - 1] is not None:
            # Error from t_start to t_end is already computed
            return saccade_mem[t_start, t_end - 1]
        # else calculate
        sse = 0

        for i in range(t_start, t_end):
            ## Alpha in (0, 1] and gives the progression of the saccade.
            ## Five options (osp = optimal saccade point):
            ## 1) the first osp is at src_xy and
            ##    the last osp is apart from tgt_xy.
            # alpha = float(i - t_start) / (t_end - t_start)
            ## 2) the first osp is apart from src_xy and
            ##    the last osp is at tgt_xy.
            # alpha = float(i + 1 - t_start) / (t_end - t_start)
            ## 3) the first osp is at src_xy and
            ##    the last osp is at tgt_xy.
            # alpha = float(i - t_start) / (t_end - 1 - t_start)
            ## 4) the first osp is apart from src_xy and
            ##    the last osp is apart from tgt_xy.
            # alpha = float(i + 1 - t_start) / (t_end + 1 - t_start)
            ## 5) the first osp is middleway at and apart from src_xy and
            ##    the last osp is middleway at and apart from tgt_xy.
            alpha = float(i + 0.5 - t_start) / (t_end - t_start)
            # Take weighted mean of the source and target points.
            mu = [0, 0]
            mu[0] = src_xy[0] * (1 - alpha) + tgt_xy[0] * alpha
            mu[1] = src_xy[1] * (1 - alpha) + tgt_xy[1] * alpha
            sse += square_error(i, mu)
        saccade_mem[t_start, t_end - 1] = sse
        return sse


    def target_objective(t_end):
        '''
        Return
            summed square error between t=t_end and t=t_max
        '''
        if max_t <= t_end:
            # t_end is not suitable for index
            return 0
        if target_mem[t_end] is not None:
            # Already computed
            return target_mem[t_end]
        for i in range(max_i, t_end - 1, -1):
            # i_first = max_i
            # i_last = t_end
            if target_mem[i] is not None:
                # Already computed
                continue
            else:
                serr = square_error(i, tgt_xy)
                if i == max_i:
                    # No previous sum
                    target_mem[i] = serr
                else:
                    target_mem[i] = serr + target_mem[i + 1]
        return target_mem[t_end]


    def find_optimal_t_start(t_end):
        '''
        Given t_end, find t_start such that the sum of source_objective and
        saccade_objective is minimized.

        Return
            t_start, optimal
            src_sse, source summed squared error
            sacc_sse, saccade summed squared error
        '''
        min_sse = float('inf')
        min_src_sse = float('inf')
        min_sacc_sse = float('inf')
        t_min_sse = 0
        for t in range(0, t_end + 1):
            src_sse = source_objective(t)
            sacc_sse = saccade_objective(t, t_end)
            sse = src_sse + sacc_sse
            if sse < min_sse:
                min_sse = sse
                min_src_sse = src_sse
                min_sacc_sse = sacc_sse
                t_min_sse = t
        return t_min_sse, min_src_sse, min_sacc_sse


    def find_optimal_t_end(t_start):
        '''
        Given t_start, find t_end such that the sum of saccade_objective and
        target_objective is minimized.

        Return
            t_end, optimal
            sacc_sse, saccade summed squared error
            target_sse, target summed squared error
        '''
        min_sse = float('inf')
        min_sacc_sse = float('inf')
        min_tgt_sse = float('inf')
        t_min_sse = 0
        for t in range(t_start, max_t + 1):
            sacc_sse = saccade_objective(t_start, t)
            tgt_sse  = target_objective(t)
            sse = sacc_sse + tgt_sse
            if sse < min_sse:
                min_sse = sse
                min_sacc_sse = sacc_sse
                min_tgt_sse = tgt_sse
                t_min_sse = t
        return t_min_sse, min_sacc_sse, min_tgt_sse


    # Put limits to initial times
    t_start = min(init_t_start, max_t)
    t_end   = min(init_t_end  , max_t)
    # Ensure order, swap if needed
    if t_end < t_start:
        t_temp = t_end
        t_end = t_start
        t_start = t_temp

    sum_sse = float('inf')
    #import pdb; pdb.set_trace()

    # Iterate until no change (converged). Place iteration limits for bugs.
    for i in range(20):
        t_start_hat, source_sse, saccade_sse = find_optimal_t_start(t_end)
        t_end_hat, saccade_sse, target_sse = find_optimal_t_end(t_start_hat)
        sum_sse = source_sse + saccade_sse + target_sse
        if t_start_hat == t_start and t_end_hat == t_end:
            # print 'MLE iterations: ' + str(i)
            # print 't_start: ' + str(t_start)
            # print 't_end: ' + str(t_end)
            # print 'sum_sse: ' + str(sum_sse)
            break
        else:
            t_start = t_start_hat
            t_end   = t_end_hat

    # Mean squared error
    mse = float(sum_sse) / len(g)
    return t_start, t_end, mse, source_sse, saccade_sse, target_sse
