import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import KDTree

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

from scipy.stats import gaussian_kde

#1, Points 
#1.1 served as df_points (vx, vy, Nex) size=rows
df_points = pd.read_table("wdata.dat", sep="\s+",usecols=[0, 1, 3], header=None)
df_points.columns = ['vx', 'vy', 'Nex']
#1.2 use 1D Points (size=(2*rows, 1)) in KDtree.query_ball_points()
kd_points = np.c_[df_points.vx, df_points.vy]
#print(df_points)
#print(kd_points)

#2, Grids 2D and 1D
G_size=100
#grid1d_x, grid1d_y = np.linspace(df_points.vx.min(), df_points.vx.max(), G_size), np.linspace(df_points.vy.min(), df_points.vy.max(), G_size)
#      !grid1d = np.c_[grid1d_x, grid1d_y]
#2.1 use Grid_2d_X and Grid_2d_Y (both size are Grids_size*Grids_size) to serve for the pcolomesh([X, Y],Z)
grid2d_x, grid2d_y = np.mgrid[df_points.vx.min():df_points.vx.max():G_size*1j, df_points.vy.min():df_points.vy.max():G_size*1j]
#print(grid2d_x.shape)
#print(grid2d_y.shape)
#2.2 construct the 1D Grids (size=(Grids_size*Grids_size, 1)+(Grids_size*Grids_size, 1)=(G_szie*G_size, 2)) to served the KDTree()
grid1d = np.c_[grid2d_x.ravel(), grid2d_y.ravel()]
#print(grid1d, '\n', grid1d[11], '\n')

#3, find nearest Grids 1D
#3.0 make a range of R and initiolize Mesh_Nex which used for contain the Nex values as a new mesh (size=(G_size-1)*(G_size-1)) for pcolormesh ploting.
#print(grid1d_x[0], grid1d_x[1])
#print(grid2d_x[0][0], grid2d_x[1][0])
#print(grid1d_y[0], grid1d_y[1])
#print(grid1d, grid2d_y[0][0], grid2d_y[0][1])
Mesh_Nex = np.zeros((G_size)*(G_size)).reshape(G_size, G_size)
#print(Mesh_Nex.shape)
R = np.sqrt((grid2d_x[0][0]-grid2d_x[1][0])**2+(grid2d_y[0][0]-grid2d_y[0][1])**2)
#3.1 make KDTree
Tree = KDTree(grid1d)
#3.2 make loop over KD_points to find nearest grids in grid1d.
N1, N2 = kd_points.shape
#print(N1, N2)
#3.0.1 make the G_point grid
G_point_x = np.zeros(N1)
G_point_y = np.zeros(N1)
G_Nex = np.zeros(N1)
j = 0
for i in range(0, N1, 1):
  idx = Tree.query_ball_point(kd_points[i], r=R)
  #print(type(idx))
#print(len(idx))
  #3.2.1 compare different grid1d[idx], and calaulte distance |grid1d[k]-kd_points[i]|;
  if len(idx)>1:
    dis = 999
    ki = 0
    for k in idx:
      dis_t = np.sqrt((grid1d[k][0]-kd_points[i][0])**2+(grid1d[k][1]-kd_points[i][1])**2)
      if (dis > dis_t):
        dis, dis_t = dis_t, dis
        ki = k
        #3.2.2 give grid1d's x, y to the new gired Gmesh
        #FIND POINTS CORRESPOND X, Y TO MAKE A KDE USED POINT MATRIX KDE_X, KDE_Y (PSIZE, PSIZE)
        #ALSO GIVES A NEW KDE USED KDE_X, KDE_Y CORRESPOND KDE_NEX (P_SIZE, 1)
        #Next is to prove the index coorespondace between grid1d[k] and grid2d_x[idx_x][arbitrary], grid2d_y[arbitrary][idx_y]
    idx_x = int(ki/G_size)
    idx_y = ki%G_size
        #print(grid1d[ki])
        #print(grid2d_x[idx_x][0], grid2d_y[0][idx_y])
        #print('\n')
    G_point_x[j] = grid2d_x[idx_x][0]
    G_point_y[j] = grid2d_y[1][idx_y]
    G_Nex[j] += df_points[(df_points['vx']==kd_points[i][0]) & (df_points['vy']==kd_points[i][1])]['Nex']
    j += 1
        #3.3 give this kd_points[i] correspond df_points.Nex to New grid for pcolor
#        if (df_points['vx']==kd_points[i][0])&(df_points['vy']==kd_points[i][1]):
#          id_x = 
    #Mesh_Nex[idx_x][idx_y] += df_points[(df_points['vx']==kd_points[i][0]) & (df_points['vy']==kd_points[i][1])]['Nex']
        ##Mesh_Nex = df_points[df_points['vx']==kd_points[i][0]][df_points['vy']==kd_points[i][1]]['Nex']
        #print(Mesh_Nex)
  else:
    k = idx
    idx_x = int(k/G_size)
    ind_y = k%G_size
    G_point_x[j] = grid2d_x[idx_x][0]
    G_point_y[j] = grid2d_y[1][idx_y]
    G_Nex[j] += df_points[(df_points['vx']==kd_points[i][0]) & (df_points['vy']==kd_points[i][1])]['Nex']
    j += 1
    #Mesh_Nex[idx_x][idx_y] += df_points[(df_points['vx']==kd_points[i][0]) & (df_points['vy']==kd_points[i][1])]['Nex']

#4, use kde to smear, and then plot
#print(type(G_point_x))
new_points = np.vstack([G_point_x, G_point_y])
kde = gaussian_kde(new_points, bw_method=0.02, weights=G_Nex)
ex = kde.evaluate(np.vstack([grid2d_x.ravel(), grid2d_y.ravel()]))
#cmap = plt.get_cmap('seismic')
cmap = plt.get_cmap('inferno')
levels = MaxNLocator(nbins=10).tick_values(df_points.Nex.min(), df_points.Nex.max())
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
fig, ax = plt.subplots(figsize=(10, 8))
im=plt.pcolormesh(grid2d_x, grid2d_y, ex.reshape(grid2d_x.shape), cmap=cmap, shading='flat', alpha=0.8)
plt.colorbar(im, ax=ax)

plt.savefig('kde_kdtree_pcolormesh.png')
plt.show()
