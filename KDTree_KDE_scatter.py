import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from scipy.spatial import KDTree

from scipy.stats import gaussian_kde
from scipy.interpolate import Rbf

#x=np.loadtxt('', usecols=(0))
#y=np.loadtxt('', usecols=(1))
#z=np.loadtxt('', usecols=(2))
df_points = pd.read_table("wdata.dat", 
                 sep="\s+", 
                 usecols=[0,1,3], header=None)
df_points.columns=['vx', 'vy', 'Nex']

levels = MaxNLocator(nbins=15).tick_values(df_points.Nex.min(), df_points.Nex.max())

# pick the desired colormap, sensible levels, and define a normalization
# instance which takes data values and translates those into levels.
cmap = plt.get_cmap('RdBu')
#cmap = plt.get_cmap('seismic')
normal = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

GSIZE=1000
X, Y = np.mgrid[df_points.vx.min():df_points.vx.max():GSIZE*1j, df_points.vy.min():df_points.vy.max():GSIZE*1j]


#convert to 1D grid mesh array and 1D point array
grid = np.c_[X.ravel(), Y.ravel()]
#print(grid.shape)
points = np.c_[df_points.vx, df_points.vy]
#print(df_points.vx.shape)
#print(points.shape)

tree = KDTree(grid)
dist, indices = tree.query(points)

#print(indices.shape, dist.shape)
#print(tree.query(points))
grid_values = df_points.groupby(indices).Nex.sum()
#print(grid_values.shape, len(indices))



#print(df_points.v)
#print('\n')
#print(grid_values)
df_grid = pd.DataFrame(grid, columns=["vx", "vy"])
df_grid["Nex"] = grid_values
#print(df_grid.vx.shape, df_grid.Nex.shape)


fig, ax=plt.subplots(figsize=(10, 8))
rbfi = Rbf(df_points.vx, df_points.vy, df_points.Nex, function='gaussian') # , smooth=11, epsilon=21) #, multiquadric, gaussian, linear, )
di = rbfi(X, Y)
image=plt.imshow(di.T, origin="lower") #, cmap='seismic') #, extent=extent)
plt.colorbar(image, ax=ax)
plt.savefig('KDTree_imshow.png')


fig, ax0 = plt.subplots(figsize=(10, 8))
ax0.plot(df_points.vx, df_points.vy, 'kv', alpha=0.2)
mapper = ax0.scatter(df_grid.vx, df_grid.vy, c=df_grid.Nex, 
                    cmap="viridis", 
                    #cmap='seismic',
                    linewidths=0.0, 
                    s=100, marker="o") #, norm=normal)
plt.colorbar(mapper, ax=ax0);
#plt.show()
#print(df_grid.vx.shape, df_grid.Nex.shape)
plt.savefig('KDTree_scatter.png')


#kde plot
grid_points = np.vstack([df_points.vx, df_points.vy])
kde = gaussian_kde(grid_points, bw_method=0.1, weights=df_points.Nex)
#ex = k(np.vstack([X.flatten(), Y.flatten()]))
#ex = k(np.vstack([df_grid.vx, df_grid.vy]))
#ex = kde.evaluate(np.vstack([X.ravel(), Y.ravel()]))
ex = kde.evaluate(np.vstack([df_grid.vx, df_grid.vy]))

fig, ax1 = plt.subplots(figsize=(10, 8))
#ax1.plot(df_points.vx, df_points.vy, 'kx', alpha=0.2)
im = ax1.scatter(df_grid.vx, df_grid.vy, c=ex.reshape(df_grid.vx.shape), 
                    cmap="seismic", 
                    linewidths=1.5, 
                    s=100, marker="o") #, norm=normal)
plt.colorbar(im, ax=ax1);
plt.savefig('KDE_KDTree_scatter.png')
