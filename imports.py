import numpy as np
import numpy.ma as ma
from scipy.interpolate import LinearNDInterpolator as lint
import sys
assert sys.version_info < (2,8)
try:
    import cPickle as pickle
except ImportError:
    import pickle
