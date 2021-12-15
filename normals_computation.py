# -*- coding: utf-8 -*-

""" Normals computation starting from txt, csv, ply or other 3D point cloud 
  object files.
  df will be a pandas dataframe that contains the whole point cloud for
  further analysis
  """
  
import os
import numpy as np
import open3d as o3d
import pandas as pd

path = os.getcwd()



# Method of normals computing with a consistent tangent plane estimation

def norms_compute_ctp():
    pcd = o3d.io.read_point_cloud(input(), 
                          format='xyzrgb') # Point cloud path
    radius_ = input() # Searching radius threshold
    max_nn_ = input() # Maximum nearest neighbors points estimation
    ctp = input() # Consistent tangent plane 
                  # (could be same as MaxNN or higher)
    pcd.estimate_normals(
search_param=o3d.geometry.KDTreeSearchParamHybrid
(radius=radius_, max_nn=max_nn_))
    pcd.normalize_normals()
    pcd.orient_normals_consistent_tangent_plane(k = ctp)
    o3d.io.write_point_cloud(os.path.join(path, "pcd_xyzn.xyzn"), pcd)
    df = pd.read_csv(os.path.join(path, "pcd_xyzn.xyzn"), delimiter=" ", header=None)
    df.to_csv(os.path.join(path, "pcd_xyzn.txt"), index=False, 
              sep="\t", header=["//X", "Y", "Z", "Nx", "Ny", "Nz"])
    df = pd.read_csv(os.path.join(path, "pcd_xyzn.txt"), delimiter='\t')
    return df



# Method of normals computing with the heuristic preferred orientation

def norms_compute_ho():
    pcd = o3d.io.read_point_cloud(input(), 
                          format='xyzrgb') # Point cloud path
    radius_ = input() # Searching radius threshold
    max_nn_ = input() # Maximum nearest neighbors points estimation
    hpo = str(input()) # could be - or + X, Y, Z
    pcd.estimate_normals(
search_param=o3d.geometry.KDTreeSearchParamHybrid
(radius=radius_, max_nn=max_nn_))
    pcd.normalize_normals()
    
    o3d.io.write_point_cloud(os.path.join(path, "pcd_xyzn.xyzn"), pcd)
    df = pd.read_csv(os.path.join(path, "pcd_xyzn.xyzn"), delimiter=" ", header=None)
    df.to_csv(os.path.join(path, "pcd_xyzn.txt"), index=False, 
              sep="\t", header=["//X", "Y", "Z", "Nx", "Ny", "Nz"])
    df = pd.read_csv(os.path.join(path, "pcd_xyzn.txt"), delimiter='\t')
    
    if hpo == '+X' or hpo == '+x':
        x = np.abs(df.iloc[:, 3])
        df.iloc[:, 3] = x
    elif hpo == '-X' or hpo == '-x':
        x = np.negative(df.iloc[:, 3])
        df.iloc[:, 3] = x
    elif hpo == '+Y' or hpo == '+y':
        y = np.abs(df.iloc[:, 4])
        df.iloc[:, 4] = y
    elif hpo == '-Y' or hpo == '-y':
        y = np.negative(df.iloc[:, 4])
        df.iloc[:, 4] = y
    elif hpo == '+Z' or hpo == '+z':
        z = np.abs(df.iloc[:, 5])
        df.iloc[:, 5] = z
    elif hpo == '-Z' or hpo == '-z':
        z = np.negative(df.iloc[:, 5])
        df.iloc[:, 5] = z
        
    return df




