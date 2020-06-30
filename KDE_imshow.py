from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_table("wdata.dat", 
                 sep="\s+", 
                 usecols=[0,1,3], header=None)
df.columns=['vx', 'vy', 'Nex']

#1, set Points to vstack([x, y]) that is ([xa, xb, xc, ...][ya, yb, yc, ...])
points = np.vstack([df.vx, df.vy])
kde = gaussian_kde(points, weights=df.Nex, bw_method=0.03)

#2, make Grids use mgrid Grid_x, and Grid_y (size*size)
size=100
grid_x, grid_y = np.mgrid[df.vx.min():df.vx.max():size*1j, df.vy.min():df.vy.max():size*1j]
#grid_x, grid_y = np.meshgrid(np.linspace(df.vx.min(), df.vx.max(), size), np.linspace(df.vy.min(), df.vy.max(), size))

ex = kde.evaluate(np.vstack([grid_x.ravel(), grid_y.ravel()]))
#ex = kde(np.vstack([grid_x.flatten(), grid_y.flatten()]))

fig, ax0 = plt.subplots(figsize=(10, 8))

a=plt.pcolormesh(grid_x, grid_y, ex.reshape(grid_x.shape))
plt.colorbar(a, ax=ax0)
plt.savefig('KDE_pcolormesh.png')
plt.show()

fig, ax1 = plt.subplots(figsize=(10, 8))
# Plot the result as an image
b=plt.imshow(ex.reshape(grid_x.shape),
          # origin='lower', #aspect='auto',
         #   extent=[-3.5, 3.5, -6, 6],
           cmap='seismic')
cb = plt.colorbar(b, ax=ax1)
cb.set_label("density")
plt.savefig('KDE_imshow.png')

fig, ax2 = plt.subplots(figsize=(10, 8))
image=plt.hexbin(df.vx, df.vy, C=df.Nex, bins=100, cmap="seismic", linewidths=1.0, gridsize=30, alpha=0.8) #, marginals=True) #, alpha=0.2)
plt.colorbar(image, ax=ax2)
plt.savefig('KDE_hexbin.png')
