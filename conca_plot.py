# -*- coding: utf-8 -*-
"""
Plot of the Conca Azzurra (Massa Lubrense -NA) 3D point cloud on which you can
manually select points of interest. They will be displayed when hoovering the mouse
on the plot
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplstereonet
import pickle

path = os.getcwd()

df = pd.read_csv("finestra Conca2 txt - Cloud - subsampled.txt", delimiter="\t")

def ginput():
    try:
        pts = plt.ginput(n=-1, timeout=0)
        plt.show()
        pts_ = np.array(pts)
    except:
        print('''
        No point/pole selected
        
        ''')
        
def fig():
    strikes = df['Dip direction (degrees)']
    dips = df['Dip (degrees)']
    
    azimuth = strikes + 90
    
    lons, lats = mplstereonet.pole(azimuth, dips)
      
    fig, ax = mplstereonet.subplots()
    
    sns.scatterplot(data=df, x=lons, y=lats, size=3, legend=False)
    sns.kdeplot(data=df, x=lons, y=lats, color="k", linewidths=0.7)
    
    ax.grid()
    with open(os.path.join(path, 'plot.pkl'),'wb') as fig_:
        pickle.dump(ax, fig_)
    plt.close(fig)
    return fig

fig()


if __name__ == '__main__':

    with open(os.path.join(path, 'plot.pkl'), 'rb') as fig_:
            ax = pickle.load(fig_)
    ginput()