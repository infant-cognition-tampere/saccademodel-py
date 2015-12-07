================
saccademodel-py
================

A least-squares optimal offline method to find saccadic reaction time and saccade duration from tracked gaze points.

You have tracked the gaze points of the following event sequence:

1. A person looks at point (A). An image appears at (B).
2. The person reacts to the image and starts to move their gaze toward (B). The *saccade* starts.
3. The gaze arrives to (B). The saccade ends.
4. The person looks at point (B).

Now you want to determine:

a. The time between events 1 and 2, called the *saccadic reaction time* or *SRT*.
b. The time between events 2 and 3, called the *saccade duration* or *SD*. Saccadic execution time, SET?

The *saccademodel* algorithm computes the times for you by fitting an ideal gaze path to the data. The ideal gaze path has the following structure. From t=0 to t=saccade_start the ideal gaze is exactly at point (A). From t=saccade_start to t=saccade_end the ideal gaze moves from (A) to (B) with constant velocity. From t=saccade_end to t=n the gaze remains at (B). The algorithm finds such times *saccade_start* and *saccade_end* that **minimize the mean squared error** between the ideal gaze path and the given tracked gaze points. In other words, the algorithm splits the data to three segments: source fixation, saccade, and target fixation.

As the **greatest advantage**, when compared to velocity-based saccade recognition methods, data does not need to be filtered beforehand because the squared error approach does that by itself. Even though filtering would yield smaller total squared error, it does not affect the estimates of *saccade_start* and *saccade_end*. However, if the noise in the data is nonstationary, some special noise filtering methods might be needed.

As the **greatest disadvantage**, the *saccademodel* algorithm is suitable only for offline analysis and therefore cannot be used in realtime setups.



Install
=======

With `pip
<http://example.com>`_::

    $ pip install saccademodel



Usage
=====

The data structure **pointlist** is used thoroughly. It is a list of points, where each point is a list [x, y].

The usage is simple::

    >>> import saccademodel
    >>> rawdata = [
        [130.012, 404.231],
        [129.234, 403.478],
        [None, None],
        [133.983, 450.044],
        ...
    ]
    >>> results = saccademodel.fit(rawdata)
    >>> print(results)
    {
        'source_points': [[344.682, 200.115], ...],
        'saccade_points': [[324.233, 202.393], ...],
        'target_points': [[556.423, 112.607], ...],
        'mean_squared_error': 0.000166802
    }

Note that the lengths of the returned lists can be used to determine saccadic reaction time and duration. For example, given the points from the appearance of stimulus, the saccadic reaction time is captured in the length of ``source_points`` and the saccade duration in ``saccade_points``. If the frame rate is known, you can convert the lengths to seconds by::

    >>> framerate = 300.0  # samples per second
    >>> saccadic_reaction_time = len(results.source_points) / framerate
    >>> saccade_duration = len(results.saccade_points) / framerate


API
===

saccademodel.fit(gazepointlist)
-------------------------------

Parameter:

- gazepointlist: a list of [x, y] points i.e. a list of lists.

Return dict with following keys:

- source_points: the points before the saccade
- saccade_points: the points in the saccade
- target_points: the points after the saccade.
- mean_squared_error: the average squared error from the model for a point.


saccademodel.version
--------------------




For developers
==============

Use virtualenv::

    $ virtualenv -p python3.5 saccademodel-py
    $ cd saccademodel-py
    $ source bin/activate
    ...
    $ deactivate

Dev. requirements:

For `$ jupyter notebook` you need to install the following with `pip`:
- jupyter
- bokeh
  - redis
  - numpy
  - pandas

Testing
-------

Follow `instructions to install pyenv
<http://sqa.stackexchange.com/a/15257/14918>`_ and then either run quick tests::

    $ python2.7 setup.py test

or comprehensive tests for multiple Python versions in ``tox.ini``::

    $ eval "$(pyenv init -)"
    $ pyenv rehash
    $ tox



Versioning
==========

`Semantic Versioning 2.0.0
<http://semver.org/>`_



License
=======

`MIT License
<http://github.com/axelpale/nudged-py/blob/master/LICENSE>`_
