# -*- coding: utf-8 -*-

"""
SSE --- Supervised Set Extraction

By default specifying number of sets to extract (2 or more) and giving
minimum and maximum values for both dip and dip direction the function
returns and saves on external files the various sets extracted as well as
the original point cloud with a column where every point belonging to a set
is labeled and also a file containing the point cloud with every set extracted
and not the rest of the cloud.
"""

import os
import pandas as pd
import random

path = os.getcwd()

""" If the point cloud has already computed normals and is yet loaded
   in the terminal or wherever you run the code just skip the line below.
   
   If not load the cloud as a pandas dataframe:
   the file must be a txt file with an header = [X, Y, Z, Nx, Ny, Nz, 
                                                 Dip (degrees), Dip direction
                                                 (degrees)] 
   and the separator must be the tab.
 """
 
df = pd.read_csv(input(), delimiter="\t")

num_set = int(input())
        

def get_k(n):
    
    k_min_dip = int(input(
        'Mininum value for k{0} dip: '.format(n)))
    k_max_dip = int(input(
        'Maximum value for k{0} dip: '.format(n)))

    k_min_dipdir = int(input(
        'Minimum value for k{0} dip direction: '.format(n)))
    k_max_dipdir = int(input(
        'Maximum value for k{0} dip direction: '.format(n)))

    return get_k(n)

    com = input('Dip direction complementary values (Y/N)? ')
    if com == 'Y' or com == 'y':
        
        while True:
            
            k_com_min_dipdir = int(input(
                'Minimum value for k{0} complementary dip direction: '.format(n)))
            k_com_max_dipdir = int(input(
                'Maximum value for k{0} complementary dip direction: '.format(n)))
        
        
            df['k{0}'.format(n)] = df['Dip (degrees)'].apply(
                lambda x: x>=k_min_dip and x<=k_max_dip) & df['Dip direction (degrees)'].apply(
                lambda x: (x>=k_com_min_dipdir and x<=k_com_max_dipdir) or (
                x>=k_min_dipdir and x<=k_max_dipdir))
                    
            k = df.loc[(df['Dip (degrees)'] >= k_min_dip) & (df['Dip (degrees)'] <= k_max_dip)
                    & (df['Dip direction (degrees)'] >= k_min_dipdir) & (df['Dip direction (degrees)'] <= k_max_dipdir)]
            
            k_com = df.loc[(df['Dip (degrees)'] >= k_min_dip) & (df['Dip (degrees)'] <= k_max_dip)
                    & (df['Dip direction (degrees)'] >= k_com_min_dipdir) & (df['Dip direction (degrees)'] <= k_com_max_dipdir)]
            
            k = pd.concat([k , k_com])
            k.loc[(k.R >= 0), 'R'] = random.randint(1, 255)
            k.loc[(k.G >= 0), 'G'] = random.randint(1, 255)
            k.loc[(k.B >= 0), 'B'] = random.randint(1, 255)
            k.to_csv(os.path.join(path, 'k{0}.txt'.format(n)), index=False, sep='\t')                
            break
            
    else:
        df['k{0}'.format(n)] = df['Dip (degrees)'].apply(
            lambda x: x>=k_min_dip and x<=k_max_dip) & df['Dip direction (degrees)'].apply(
            lambda x: x>=k_min_dipdir and x<=k_max_dipdir)
                
        k = df.loc[(df['Dip (degrees)'] >= k_min_dip) & (df['Dip (degrees)'] <= k_max_dip)
                & (df['Dip direction (degrees)'] >= k_min_dipdir) & (df['Dip direction (degrees)'] <= k_max_dipdir)]
        
        k.loc[(k.R >= 0), 'R'] = random.randint(1, 255)
        k.loc[(k.G >= 0), 'G'] = random.randint(1, 255)
        k.loc[(k.B >= 0), 'B'] = random.randint(1, 255)
        k.to_csv(os.path.join(path, 'k{0}.txt'.format(n)), index=False, sep='\t')


for n in range(1, num_set+1):    
    get_k(n)
        

#: below function and list comprehension to do for generate in the original
#: dataframe a column that has the values of the sets to be used later in the 
#: graphical representations

def get_set(row, names):
    for name in names:
        if row[name] == True:
            return name     

boolean_columns = [col for col in df.columns if col.startswith('k')]       
df['discontinuity set'] = df.apply(get_set, axis=1, names=boolean_columns)
df.drop([col for col in df.columns if col.startswith('k')], axis=1, inplace=True)
df.to_csv(os.path.join(path, 'data_file_ds_column.txt'), index=False, sep='\t')
df2 = df.dropna(subset=['discontinuity set'])
df2.to_csv(os.path.join(path, 'data_file_ext_ds.txt'), index=False, sep='\t')