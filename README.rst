================
saccademodel-py
================

A least-squares optimal offline pattern recognition algorithm to find saccadic reaction time and saccade duration from tracked 2D gaze points.



1. Install
==========

With `pip
<https://pypi.python.org/pypi/saccademodel>`_::

    $ pip install saccademodel



2. Usage
========

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



3. API
======

3.1. saccademodel.fit(gazepointlist)
------------------------------------

Parameter:

- gazepointlist: a list of [x, y] points i.e. a list of lists.

Return dict with following keys:

- source_points: the points before the saccade
- saccade_points: the points in the saccade
- target_points: the points after the saccade.
- mean_squared_error: the average squared error from the model for a point.


3.2. saccademodel.version
-------------------------

The current version string::

    >>> saccademodel.version
    '1.2.3'



4. Algorithm description
========================

Let us say you have tracked the gaze points of the following event sequence:

1. A person looks at point (A).
2. An image appears at (B).
3. The person reacts to the image and starts to move their gaze toward (B). The *saccade* starts.
4. The gaze arrives to (B). The saccade ends.
5. The person looks at point (B).

Now you want to determine:

a. The time between events 2 and 3, called the *saccadic reaction time* or *SRT*.
b. The time between events 3 and 4, called the *saccade duration* or *SD*.

The *saccademodel* algorithm computes SRT and SD for you by fitting an ideal gaze path to the data. The workings of the algorithm resemble building a strictly straight road (ideal path) from A to B as quickly as possible but the building material warehouse is moving constantly in preplanned manner (gaze points). The algorithm finds the optimal start and end time of the construction so that the squared distance to the warehouse is kept as short as possible.

The ideal gaze path has the following structure. From t=0 to t=saccade_start the ideal gaze is exactly at point (A). From t=saccade_start to t=saccade_end the ideal gaze moves from (A) to (B) with constant velocity. From t=saccade_end to t=n the gaze remains at (B). The algorithm finds such times *saccade_start* and *saccade_end* that **minimize the mean squared error** between the ideal gaze path and the given tracked gaze points. In other words, the algorithm splits the data to three segments: source fixation, saccade, and target fixation in a way that the segments match the movement of the eye.

The algorithm works in the following manner. Two arbitrary time points *saccade_start* and *saccade_end* are chosen so that *saccade_start < saccade_end* and both are in the time limits of the data. Then, each possible value for *saccade_end* are iterated and total error is computed for each value. The variable *saccade_end* is then set to the value that gave the smallest error. The same is then repeated for *saccade_start*. If the value of the *saccade_start* changed, the same is again repeated for *saccade_end*. The iteration continues until neither of the values change. The iteration usually converges to this stationary state but sometimes remain oscillating between two or more value-pairs. To prevent this oscillation, the algorithm remembers the already computed value-pairs and their error and by that it can detect if same pairs are iterated again, which would lead to oscillation. If the start of oscillation is this way detected, the iteration is stopped and the remembered value-pair with the smallest error is chosen for the final values of *saccade_start* and *saccade_end*.

As the **greatest advantage**, when compared to velocity-based saccade recognition methods, normally distributed noise in the gaze points does not need to be filtered beforehand because the squared error approach. However, strong noise that is not normally distributed and clearly wrong data points need to be removed beforehand. Another advantage is an ability to detect if the gaze path from (A) to (B) was not continuous and straight. Strongly curved or multiple smaller saccades will yield relatively large mean squared error.

As the **greatest disadvantage**, the *saccademodel* algorithm is suitable only for offline analysis and therefore cannot be used in realtime setups. Another disadvantage is that it is algorithmically relatively slow, having time complexity of O(n^3). Still other disadvantage is possibly inaccurate results if the eye tracker is not calibrated well because then even an ideal saccade would not travel from (A) to (B) but from some (A') to some (B').



5. For developers
=================

5.1. Virtualenv
---------------

Use virtualenv::

    $ virtualenv -p python3.5 saccademodel-py
    $ cd saccademodel-py
    $ source bin/activate
    ...
    $ deactivate


5.2. Jupyter Notebook
---------------------

Usage::

    $ cd explore
    $ jupyter notebook

Install requirements::

    $ pip install --editable .[notebook]


5.3. Testing
------------

Follow `instructions to install pyenv
<http://sqa.stackexchange.com/a/15257/14918>`_ and then either run quick tests::

    $ python3.5 setup.py test

or comprehensive tests for multiple Python versions in ``tox.ini``::

    $ pyenv local 2.6.9 2.7.10 3.1.5 3.2.6 3.3.6 3.4.3 3.5.0
    $ eval "$(pyenv init -)"
    $ pyenv rehash
    $ tox

Install new pyenv environments by::

    $ pyenv install 3.4.5

Validate README.rst at `http://rst.ninjs.org/
<http://rst.ninjs.org/>`_


5.4. Publishing to PyPI
-----------------------

Follow `python packaging instructions
<https://python-packaging-user-guide.readthedocs.org/en/latest/distributing/>`_:

1.  Create an unpacked sdist: ``$ python setup.py sdist``
2.  Create a universal wheel: ``$ python setup.py bdist_wheel --universal``
3.  Go to `PyPI and register the project by filling the package form
    <https://pypi.python.org/pypi?%3Aaction=submit_form>`_ by uploading
    ``saccademodel.egg-info/PKG_INFO`` file.
4.  Upload the package with twine:

    1. Sign the dist: ``$ gpg --detach-sign -a dist/saccademodel-1.2.3*``
    2. Upload: ``twine upload dist/saccademodel-1.2.3*`` (will ask your PyPI password)

5. Package published!

Updating the package takes same steps except the 3rd.



6. Versioning
=============

`Semantic Versioning 2.0.0
<http://semver.org/>`_



7. License
==========

`MIT License
<https://opensource.org/licenses/MIT>`_
