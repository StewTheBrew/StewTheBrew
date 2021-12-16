# -*- coding: utf-8 -*-
"""
AUTOMATED CLUSTERING: K-MEANS & GAUSSIAN MIXTURE

Use these functions to plot data with KDE but having the centers of clusters
calculated by automatic clustering techniques. You have to specify numbers of 
clusters previously, so a base knowledge on the case is required, also, if possible,
it is advisable to plot the data first without clustering so to have an idea in
this sense. Both can be improved, expecially the Gaussian Mixture that could
implement others parameters. Check the doc on https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html
"""

import os 
import pandas as pd
import numpy as np
import seaborn as sns
import mplstereonet
import pickle
import matplotlib.pyplot as plt


path = os.getcwd()

"""HERE CHANGE df TO poles IF YOU ARE RUNNING THE CODE AFTER THE IPDE or
 just upload the IPDE result as df so you don't have to change this in the
 whole code
 -------------------------------------------------------------------------
 """
 
df = pd.read_csv(input(), delimiter="\t") 
                                          
dp = pd.DataFrame()
dp['Dip (degrees)'] = df['Dip (degrees)'] 
dp['Dip direction (degrees)'] = df['Dip direction (degrees)']

def k_means():
    from sklearn.cluster import KMeans
    n = input("Number of clusters: ")
 
    k_means = KMeans(n_clusters=int(n))
    
    k_means.fit(dp)
    

    k_means.labels_
    labels, index = np.unique(k_means.labels_, return_inverse=True)
    centers = k_means.cluster_centers_
    km_df = pd.DataFrame(centers)
    km_df['Cluster'] = km_df.index
    
    s = km_df[0:][1]
    d = km_df[0:][0]
    a = s + 90
    

        
    strikes = df['Dip direction (degrees)']
    dips = df['Dip (degrees)']
    
    azimuth = strikes + 90
    
    lons, lats = mplstereonet.pole(azimuth, dips)
    lons2, lats2 = mplstereonet.pole(a, d)
    
    def k_means_fig():  
        fig, ax = mplstereonet.subplots()
        
        sns.kdeplot(data=df, x=lons, y=lats, hue=index, palette='viridis',
                    linewidths=.7, legend=False)
        
        
        sns.scatterplot(data=km_df, x=lons2, y=lats2, color='r', legend=False)
                      # , hue=labels, palette='viridis')
        ax.grid(True)
        with open(os.path.join(path, 'k_means_plot.pkl'),'wb') as fig_:
            pickle.dump(ax, fig_)
        plt.close(fig)
        return fig
    

    k_means_fig()
    if __name__ == '__main__':

        with open(os.path.join(path, 'k_means_plot.pkl'), 'rb') as fig_:
                ax = pickle.load(fig_)

        plt.show()
    
    km_df_ = pd.DataFrame()
    km_df_['Dip'] = km_df.iloc[0:, 0]
    km_df_['Dip_direction'] = km_df.iloc[0:, 1]
    km_df_['Cluster'] = km_df.iloc[0:, 2]
    print(km_df_)

def gaussian_mixture():
    from sklearn.mixture import GaussianMixture
    n = input("Number of clusters: ")
    
    gm = GaussianMixture(n_components=int(n)).fit(dp)
    
    centers = gm.means_
    gm_df = pd.DataFrame(centers)
    gm_df['Cluster'] = gm_df.index
    
    strikes = df['Dip direction (degrees)']
    dips = df['Dip (degrees)']
    azimuth = strikes + 90
    
    s = gm_df[0:][1]
    d = gm_df[0:][0]
    a = s + 90
    ### Convert our strikes and dips to stereonet coordinates
    
    lons, lats = mplstereonet.pole(azimuth, dips)
    lons2, lats2 = mplstereonet.pole(a, d)
    
    def gauss_mix_fig():
        fig, ax = mplstereonet.subplots()
        
        sns.kdeplot(data=df, x=lons, y=lats, color='k',
                        linewidths=.7, legend=False)
        
        
        sns.scatterplot(data=gm_df, x=lons2, y=lats2, color='r', legend=False)
        #               , hue='Cluster', palette='viridis')
        
        ax.grid(True)
        with open(os.path.join(path, 'gauss_mix_plot.pkl'),'wb') as fig_:
            pickle.dump(ax, fig_)
        plt.close(fig)
        return fig
    
    gauss_mix_fig()
    
    if __name__ == '__main__':

        with open(os.path.join(path, 'gauss_mix_plot.pkl'), 'rb') as fig_:
                ax = pickle.load(fig_)

        plt.show()
    
    gm_df_ = pd.DataFrame()
    gm_df_['Dip'] = gm_df.iloc[0:, 0]
    gm_df_['Dip_direction'] = gm_df.iloc[0:, 1]
    gm_df_['Cluster'] = gm_df.iloc[0:, 2]
    
    print(gm_df_)