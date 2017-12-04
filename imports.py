import numpy as np
import numpy.ma as ma
from scipy.interpolate import LinearNDInterpolator as lint
try:
    import cPickle as pickle
except ImportError:
    import pickle
