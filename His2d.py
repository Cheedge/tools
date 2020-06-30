import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import gaussian_kde

#### define the map area
x1, x2, y1, y2 = -1, 1, -1, 1       
#### reading the point data and scatter plot by their position
#df = pd.read_csv("xxxxx.csv")
df = pd.read_table("wdata.dat", 
                 sep="\s+", 
                 usecols=[0,1,3], header=None)
df.columns=['vx', 'vy', 'Nex']    
x_grid,y_grid = np.linspace(x1,x2,500), np.linspace(y1,y2,500)
lon_x,lat_y = np.meshgrid(x_grid,y_grid)
grids = np.zeros(500*500).reshape(500,500)
#plt.pcolormesh(lon_x,lat_y,grids,cmap =  'gray', facecolor = 'none',edgecolor = 'k',zorder=3)
#plt.show()
fig, ax0 = plt.subplots(figsize=(10, 8))
h, xedge, yedge, image1=plt.hist2d(df.vx, df.vy, weights=df.Nex, bins=100, cmap="viridis")
plt.colorbar(image1, ax=ax0)
plt.savefig('Hist2d.png')
plt.show()

fig, ax1 = plt.subplots(figsize=(10, 8))
image2=plt.hexbin(df.vx, df.vy, C=df.Nex, bins=100, cmap="seismic", linewidths=1.0, gridsize=30, alpha=0.8) #, marginals=True) #, alpha=0.2)
plt.colorbar(image2, ax=ax1)
plt.savefig('Hexbin.png')
