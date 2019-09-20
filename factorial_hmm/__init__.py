from factorial_hmm.factorial_hmm import FactorialHMMDiscreteObserved, \
    FullDiscreteFactorialHMM, Indices

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()