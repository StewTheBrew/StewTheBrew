# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

""" If the point cloud has already computed normals and is yet loaded
   in the terminal or wherever you run the code just skip the step below.
   
   If not load the cloud as a pandas dataframe:
   the file must be a txt file with an header = [X, Y, Z, Nx, Ny, Nz] and the
   separator must be the tab.
   
   Commented code parts refers to the use of this process with structured arrays
   and not with dataframes
   """
df = pd.read_csv(input(), delimiter="\t")


N = df.iloc[:, 3:].to_numpy() #: 3 or where normals are in dataset

# def join_struct_arrays(arrays):
#     sizes = np.array([a.itemsize for a in arrays])
#     offsets = np.r_[0, sizes.cumsum()]
#     n = len(arrays[0])
#     joint = np.empty((n, offsets[-1]), dtype=np.uint8)
#     for a, size, offset in zip(arrays, sizes, offsets):
#         joint[:,offset:offset+size] = a.view(np.uint8).reshape(n,size)
#     dtype = sum((a.dtype.descr for a in arrays), [])
#     return joint.ravel().view(dtype)

def norms_to_dip_dipdir(self, degrees=True):
    
# def add_inclination(self, degrees=True):
    
    """ Adds inclination (with respect to z-axis) values to PointCloud.vertex
    
    This function expects the PointCloud to have a numpy structured array
    with normals x,y,z values (correctly named) as the corresponding vertex
    atribute, so N would be the first argument in the main function.
    
     Args:
        degrees (Optional[bool]): Set the oputput inclination units.
            If True(Default) set units to degrees.
            If False set units to radians.
    """
    #: set copy to False for efficience in large pointclouds
    # nx = self[0:, 0].astype(np.float64, copy=False)
    # nz = self[0:, 2].astype(np.float64, copy=False)
    #: get inclination
    global df
    # n_e = (0, 0, 1)    
    # n_e = np.array([n_e]).astype(np.float64, copy=False)
    # n_e = np.squeeze(np.asarray(n_e))
    # angle = np.arccos(np.dot(N, n_e))
    nx = self[0:, 0].astype(np.float64, copy=False)
    nz = self[0:, 2].astype(np.float64, copy=False)
    angle = np.arctan(np.abs(nx) / np.abs(nz))
    if degrees == False:
        inclination = np.array(angle, dtype=[('inr', 'f8')])
    else:
        inclination = np.array(180 * angle / np.pi) # ,dtype=[(
            # 'Dip (degrees)', 'f8')])
    #: merge the structured arrays and replace the old vertex attribute
    # self = join_struct_arrays([self, inclination])
    
    
    dip = pd.Series(inclination)
    df['Dip (degrees)'] = dip
    
# def add_orientation(self, degrees=True):
        
    """ Adds orientation (with respect to y-axis) values to PointCloud.vertex
    
    This function expects the PointCloud to have a numpy structured array
    with normals x,y,z values (correctly named) as the corresponding vertex
    atribute.
    
     Args:
        degrees (Optional[bool]): Set the oputput orientation units.
            If True(Default) set units to degrees.
            If False set units to radians.
    """  
    
    #: set copy to False for efficience in large pointclouds
    # nx = self[0:, 0].astype(np.float64, copy=False)
    ny = self[0:, 1].astype(np.float64, copy=False)
    
    #: get orientations
    angle2 = np.arctan(np.abs(nx) / np.abs(ny))
    
    #: mask for every quadrant
    q2 = np.logical_and((self[0:, 0]>0),(self[0:, 1]<0))
    q3 = np.logical_and((self[0:, 0]<0),(self[0:, 1]<0))
    q4 = np.logical_and((self[0:, 0]<0),(self[0:, 1]>0))
    
    #: apply modification for every quadrant
    angle2[q2] = np.pi - angle2[q2]
    angle2[q3] = np.pi + angle2[q3]
    angle2[q4] = (2*np.pi) - angle2[q4]
    
    if degrees == False:
        orientation = np.array(angle2, dtype=[('orir', 'f8')])
    else:
        orientation = np.array(180 * angle2 / np.pi) # dtype=[(
            # 'Dip direction (degrees)', 'f8')])
    

    #: merge the structured arrays and replace the old vertex attribute
    # self = join_struct_arrays([self, orientation])
    
    dip_dir = pd.Series(orientation)
    df['Dip direction (degrees)'] = dip_dir
        