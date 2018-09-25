'''
@created: 13:17 (EST) Sun 7/29/2018

@last_modified: 10:05 (EST) Sun 09/25/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@description: visuals.py contains functions to convert data stored in the agent and
packet classes interacting over a network into vPython visualizations
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Initialize plot
def init_plot():
    plt.ion()
    fig = plt.figure()
    ax = Axes3D(fig)
    plt.axis('off')
    return fig,ax

#Extract information from board for plotting
def board_2_coords(board):
    axial_2_cart = np.array([[3**0.5,(3**0.5)/2.,0.5],
                             [0,3./2,1/(2*3**0.5)],
                             [0,0,(2./3)**0.5]])
    
    return [(np.matmul(axial_2_cart,np.array(c.i_id).T),
             c.HeldPackets != []) for c in board.getAllAgents()]
    
#Iterate existing plot
def iter_plot(board,fig,ax):
    coords = board_2_coords(board)
    
    #Plot agents with packets
    ax.scatter([c[0][0] for c in coords if c[1]],
               [c[0][1] for c in coords if c[1]],
               [c[0][2] for c in coords if c[1]],
               c = 'red')
    
    #Plot agents without packets
    ax.scatter([c[0][0] for c in coords if not c[1]],
               [c[0][1] for c in coords if not c[1]],
               [c[0][2] for c in coords if not c[1]],
               c = 'blue')
    #Draw
    fig.canvas.draw()
