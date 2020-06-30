import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf

# Load the data.
df_points = pd.read_table("wdata.dat", 
                 sep="\s+", 
                 usecols=[0,1,3], header=None)
df_points.columns=['vx', 'vy', 'Nex']

# Build a regular grid with G_size-metre cells.
G_size = 2000j
extent = x_min, x_max, y_min, y_max = [df_points.vx.min(), df_points.vx.max(),
                                       df_points.vy.min(), df_points.vy.max()]
grid_x, grid_y = np.mgrid[x_min:x_max:G_size, y_min:y_max:G_size]

# Make the interpolator and do the interpolation.
rbfi = Rbf(df_points.vx, df_points.vy, df_points.Nex, function='gaussian') # , smooth=11, epsilon=21) #, multiquadric, gaussian, linear, )
di = rbfi(grid_x, grid_y)

# Make the plot.
plt.figure(figsize=(10, 8))
#plt.imshow(di.T, origin="lower", extent=extent, cmap='seismic')
cb = plt.scatter(df_points.vx, df_points.vy, s=60, cmap='seismic', c=df_points.Nex)#, edgecolor='#ffffff66')
plt.colorbar(cb, shrink=0.67)
plt.savefig('Interpolat_imhsow.png')
plt.show()
