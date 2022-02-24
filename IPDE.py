# -*- coding: utf-8 -*-
"""
IPDE --- Iterative Pole Density Estimation

This function allows to highlight on the dataset only the points that have
a proven coplanarity on the basis of a minimum density threshold (K) chosen 
by the user. The analysis is performed on sample points (S) of the 3D point 
cloud, the number of which is always chosen by the user. In addition, 
the angular tolerance range can be specified to identify coplanarity.


The function can be coupled to a facilitating mechanism that divides the 
dataset into chunks, if this is very large and/or if you intend to start the 
analysis on a large amount of sample points (high S value).
The analysis can therefore be carried out in the basic mode, or sequentially 
with the division into chunks (faster), or in multiprocessing mode -beta- 
(even faster).

**************************************************************************
The progressbar is implemented to see the progress in realtime BUT IT WILL NOT
WORK IF YOU RUN THE CODE ON A EDITOR SUCH AS SPYDER, JUPYTER NOTEBOOK, VISUAL
STUDIO CODE ETC. IN THE IDLE IT WILL WORK BUT THEY ARE SOLVING SOME GRAPHICAL
ISSUE THAT YOU MIGHT INCUR IN, SO PLEASE UPLOAD THE PROGRESSBAR TO THE LATEST VERSION.
THE BEST WAY IS RUNNING THE CODE ON A TERMINAL
**************************************************************************
 
A manual selection of poles inside the resultant KDE plot is provided. Click the 
left button of the mouse to select a point, click the right button to delete 
the last choice made and click the middle button when you have finished selecting
all the points of interest. It returns the selected points in output when the 
plot is closed.

The system stores automatically the plot in the path folder, so you can reload
it without having to compute all again.

If you prefer to rely upon automated clustering methods, just couple the IPDE
function with the clustering functions in the auto_clustering.py file.

----------------------------------------------------------------------------
If you have further doubts please read the comments in the code or just ask
"""

import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import progressbar
import pickle


path = os.getcwd()

widgets=[
    ' [', progressbar.Timer(), '] ',
    ' ', progressbar.Percentage(), ' ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]

df = pd.read_csv(input(), delimiter="\t")

#: below the function to manually select points on a polar stereoplot

def ginput():
    try:
        pts = plt.ginput(n=-1, timeout=0)
        plt.show()
        
        
        pts_ = np.array(pts)
        
        pts_df = pd.DataFrame(pts_)
        
        pts_df1 = pd.DataFrame()
        pts_df1['Dip_direction'] = pts_df.iloc[0:][0]*180/np.pi
        
        pts_df1['Dip'] = pts_df.iloc[0:][1]
        
        def transform_row(r):
            if r.Dip_direction >= 0: 
                r.Dip_direction = r.Dip_direction
            else:
                r.Dip_direction = r.Dip_direction + 360
                
        pts_df1.apply(transform_row, axis=1)
        print(pts_df1)            
    except:
        print('''
        No point/pole selected
        
        ''')
   
        
   
#: call the function below if at any step you incur in the problem of having NaN
#: or infinite values in the dataset

def clean_dataset(df): 
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)


        
poles = pd.DataFrame()

dp = pd.DataFrame()
dp['Dip (degrees)'] = df['Dip (degrees)']
dp['Dip direction (degrees)'] = df['Dip direction (degrees)']

def IPDE():
        
    thres = int(input('K (pole threshold): '))
    
    seed = int(input('S (covering density sampling): '))
    
    dip_t = int(input('Dip angle threshold: '))
    
    dip_dir_t = int(input('Dip direction angle threshold: '))
   
    global df
    global poles
    global widgets
    
    
    def random_seed_chunked(n):
        
        rand_row = dp.sample(replace=True)
        
        rand_dip = rand_row.iloc[0,0]
        rand_dipdir = rand_row.iloc[0,1]
        
        values = chunks[c].loc[(chunks[c]['Dip (degrees)'] >= rand_dip - dip_t) & (chunks[c]['Dip (degrees)']
                 <= rand_dip + dip_t) & (chunks[c]['Dip direction (degrees)'] >= rand_dipdir -
                 dip_dir_t) & (chunks[c]['Dip direction (degrees)'] <= rand_dipdir + dip_dir_t)]
    
        values_size = len(values.index)
        # global df1
        global poles
        
        # def condition_X():
        #     df1 = df[~df.isin(values)].dropna()
        #     global values_size     
        
        if values_size > thres:
            poles = pd.concat([poles , values]) 
        else:
            del values 
        
        
    def random_seed(n):
        
        rand_row = dp.sample(replace=True)
        
        rand_dip = rand_row.iloc[0,0]
        rand_dipdir = rand_row.iloc[0,1]
        
        values = df.loc[(df['Dip (degrees)'] >= rand_dip - dip_t) & (df['Dip (degrees)']
                 <= rand_dip + dip_t) & (df['Dip direction (degrees)'] >= rand_dipdir -
                 dip_dir_t) & (df['Dip direction (degrees)'] <= rand_dipdir + dip_dir_t)]
    
        values_size = len(values.index)
        # global df1
        global poles
        
        # def condition_X():
        #     df1 = df[~df.isin(values)].dropna()
        #     global values_size     
        
        if values_size > thres:
            poles = pd.concat([poles , values])            
        else:
            del values       
    
        """READ THIS!!!:
            Here you just have to delete comment out the loop(s) that you don't want to run.
            Functionality is commented on top of each loop
            SAME IF YOU DON'T WANT TO SAVE STORE SETS (MOST COMMON)
        """
        
    #: BASIC ANALYSIS
    for n in progressbar.progressbar(range(seed+1), widgets=widgets):
          
        random_seed(n)
    
        poles = poles.drop_duplicates()
    
    
    #: SEQUENTIAL ANALYSIS OF CHUNKS N.B. IF YOU RUN THIS OR MULTIPROCESSING
    #: YOU SHOULD CONSISTENTLY LOW K AND S VALUES!!!
    for i in range(3, 20):
        chunk = math.floor(len(df)/i)
        if chunk == len(df)/i:
            n_chunks = math.floor(len(df)/chunk)
            chunks = np.array_split(df, n_chunks)
            
            for c in range(n_chunks):
                for n in progressbar.progressbar(range(seed+1), widgets=widgets): 
                        
                    random_seed_chunked(n)
                    poles = poles.drop_duplicates()
            break
        else:
            continue
      
        
    #: MULTIPROCESSING ANALYSIS OF CHUNKS
    import multiprocessing

    for i in range(3, 20):
        chunk = math.floor(len(df)/i)
        if chunk == len(df)/i:
            n_chunks = math.floor(len(df)/chunk)
            chunks = np.array_split(df, n_chunks)
            break
        else:
            continue
    pool = multiprocessing.Pool(4) #: here I passed a pool of 4 worker processes
                                   #: you can pass 2 or if you don’t pass anything
                                   #: then it will create a worker process pool based
                                   #: on the cores available in the processor
    pool.map(func=random_seed, iterable=df, chunksize=n_chunks)
    pool.close()
    pool.join()
    poles = poles.drop_duplicates()
            

        
    poles.to_csv(os.path.join(path, 'ipde_poles_dataset.txt'), index=False, sep='\t')


#: Lines below runs the function and creates variables to be utilized for plotting       
IPDE()
dp1 = pd.DataFrame()
dp1['Dip (degrees)'] = poles['Dip (degrees)']
dp1['Dip direction (degrees)'] = poles['Dip direction (degrees)']
   

             

#: Below the manual selection clustering version to plot data.
#: The polar projection is here implemented, because yet there are some bugs
#: with plotting the manual clustering with mplstereonet. Hope to solve them
#: quickly in the future


def ipde_manual_fig():
    poles['Dip direction (degrees)'] = poles['Dip direction (degrees)']*np.pi/180
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    
    sns.scatterplot(data=poles, x='Dip direction (degrees)',
      y='Dip (degrees)', legend=False)
    
    sns.kdeplot(data=poles, x='Dip direction (degrees)', y='Dip (degrees)',
                linewidths=0.7, color="k", legend=False)
    
    plt.gca().set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''])
    plt.gca().set_ylim(0, 90)
    plt.ylabel(' ')
    plt.xlabel(' ')
    plt.gca().set_theta_zero_location('N')
    plt.gca().set_theta_direction(-1)
    with open(os.path.join(path, 'poles_mplot.pkl'),'wb') as fig_:
        pickle.dump(ax, fig_)
    plt.close(fig)
    return fig

ipde_manual_fig()


if __name__ == '__main__':

    with open(os.path.join(path, 'poles_mplot.pkl'), 'rb') as fig_:
            ax = pickle.load(fig_)

    ginput()
  
    
  
#: if you just want to visualize data on the Schmidt equiareal projection 
#: without point picking run the code below instead of the previous one
#: (you can check values anyway just hoovering the mouse on the plot) AND
#: DELETE OR COMMENT OUT THE BLOCK YOU WON'T USE

import mplstereonet

def ipde_fig():
    strikes = poles['Dip direction (degrees)']
    dips = poles['Dip (degrees)']
    
    azimuth = strikes + 90
    
    lons, lats = mplstereonet.pole(azimuth, dips)
      
    fig, ax = mplstereonet.subplots()
    
    sns.scatterplot(data=poles, x=lons, y=lats, size=3, legend=False)
    sns.kdeplot(data=poles, x=lons, y=lats, color="k", linewidths=0.7)
    
    ax.grid()
    with open(os.path.join(path, 'poles_splot.pkl'),'wb') as fig_:
        pickle.dump(ax, fig_)
    plt.close(fig)
    return fig

ipde_fig()


if __name__ == '__main__':

    with open(os.path.join(path, 'poles_splot.pkl'), 'rb') as fig_:
            ax = pickle.load(fig_)

    plt.show()
