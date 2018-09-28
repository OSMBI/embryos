'''
@created: 13:17 (EST) Sun 7/29/2018

@last_modified: 07:10 (EST) Sun 09/28/2018

@authors: 

@institution: Open-Source Mathematical Biology Intiative (OSMBI)

@description: visuals.py contains functions to convert data stored in the agent and
packet classes interacting over a network into vPython visualizations
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


class plot3dClass( object ):

    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot( 111, projection='3d' )
        self.surf = self.ax.scatter(1,1,1)
        # plt.draw() maybe you want to see this frame?

    def drawNow(self,var):
        self.surf.remove()
        self.surf = self.ax.scatter(var[0],var[1],var[2],c=var[3])
        plt.draw()                      # redraw the canvas
        self.fig.canvas.flush_events()
        time.sleep(1)
        
#Extract information from board for plotting
def board_2_coords(board):
    axial_2_cart = np.array([[1,0.5,0.5],
                            [0,(3**0.5)/2,1/(12**0.5)],
                            [0,0,(2/3.)**0.5]])
    #cart_2_axial = np.linalg.inv(axial_2_cart)
    
    first = [tuple(np.matmul(axial_2_cart,np.array(c.i_id).T).tolist()+['red'])\
            if c.HeldPackets != [] or c.ReceivedPackets != [] else \
            tuple(np.matmul(axial_2_cart,np.array(c.i_id).T).tolist()+['blue'])\
             for c in board.getAllAgents()]
    
    x = [f[0] for f in first]
    y = [f[1] for f in first]
    z = [f[2] for f in first]
    c = [f[3] for f in first]
    
    return (x,y,z,c)
