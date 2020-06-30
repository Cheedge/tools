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
G_size=50
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
#R = ((grid2d_x[0][0]-grid2d_x[1][0])**16+(grid2d_y[0][0]-grid2d_y[0][1])**16)**(1.0/16)
#3.1 make KDTree
Tree = KDTree(grid1d)
#3.2 make loop over KD_points to find nearest grids in grid1d.
N1, N2 = kd_points.shape
#print(N1, N2)
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
        #Gmesh = grid1d[k]
        #Next is to prove the index coorespondace between grid1d[k] and grid2d_x[idx_x][arbitrary], grid2d_y[arbitrary][idx_y]
    idx_x = int(ki/G_size)
    idx_y = ki%G_size
        #print(grid1d[k])
        #print(grid2d_x[idx_x][0], grid2d_y[0][idx_y])
        #print('\n')
        #3.3 give this kd_points[i] correspond df_points.Nex to New grid for pcolor
#        if (df_points['vx']==kd_points[i][0])&(df_points['vy']==kd_points[i][1]):
#          id_x = 
    Mesh_Nex[idx_x][idx_y] += df_points[(df_points['vx']==kd_points[i][0]) & (df_points['vy']==kd_points[i][1])]['Nex']
        ##Mesh_Nex = df_points[df_points['vx']==kd_points[i][0]][df_points['vy']==kd_points[i][1]]['Nex']
        #print(Mesh_Nex)
  else:
    k = idx
    idx_x = int(k/G_size)
    ind_y = k%G_size
    Mesh_Nex[idx_x][idx_y] += df_points[(df_points['vx']==kd_points[i][0]) & (df_points['vy']==kd_points[i][1])]['Nex']



#4, use pcolormesh to plot. 
#4.0  color and norm settings
#cmap = plt.get_cmap('RdBu')
cmap = plt.get_cmap('seismic')
levels = MaxNLocator(nbins=1000).tick_values(df_points.Nex.min(), df_points.Nex.max())
normal = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
#4.1 plot
fig, ax0 = plt.subplots(figsize=(10, 8))
#ax.plot(df_points.vx, df_points.vy, "kx", alpha=0.2)
#mapper = ax.scatter(df_grid.vx, df_grid.vy, c=df_grid.Nex, 
#                    cmap="viridis", 
#                    linewidths=0, 
#                    s=100, marker="o") #, norm=normal)
#plt.colorbar(mapper, ax=ax)
#scat = ax.scatter(x, y, c=z, s=200)
#fig.colorbar(scat)
#ax.margins(0.05)
im=plt.pcolormesh(grid2d_x, grid2d_y, Mesh_Nex, cmap=cmap, norm=normal, shading='flat', alpha=0.8)
plt.colorbar(im, ax=ax0)   
plt.savefig('KDtree_pcolormesh1.png')
   

fig, ax1 = plt.subplots(figsize = (10, 8)) 
cf = ax1.contourf(grid2d_x, grid2d_y, Mesh_Nex, levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax1) 


plt.savefig('KDtree_pcolormesh2.png')
