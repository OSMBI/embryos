'''
@created: 13:17 (EST) Sun 7/29/2018

@last_modified: 21:54 (EST) Sun 7/30/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@description: visuals.py contains functions to convert data stored in the agent and
packet classes interacting over a network into vPython visualizations
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

#Basis transform from 3D axial to 3D cartesian
axial_2_cart = np.array([[3**0.5,(3**0.5)/2.,0.5],
                         [0,3./2,1/(2*3**0.5)],
                         [0,0,(2./3)**0.5]])

