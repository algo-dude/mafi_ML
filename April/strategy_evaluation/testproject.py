import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import util as ut
import ManualStrategy as ms
import experiment1 as exp1
import experiment2 as exp2

def author():
    print ("not student")

if __name__ == "__main__":

    #In sample Manual Strategy
    ms.InSample()

    #Out sample Manual Strategy
    ms.OutOfSample()

    #Calling experiment1 script

    np.random.seed(123456)
    exp1.InSample()

    # Calling experiment2 script

    np.random.seed(123456)
    exp2.test_code()