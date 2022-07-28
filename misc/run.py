import plotly.graph_objects as go
from pyshtools.expand import SHExpandLSQ
import pyshtools as pysh
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

def calculate_density(pts, xyzs, sigma=0.01):
    """
    calculate the projected density on the unit sphere
    """
    vals = np.zeros(len(xyzs))
    pi = np.pi
    for pt in pts:
        t0, p0, h = pt
        x0, y0, z0 = np.sin(t0)*np.cos(p0), np.sin(t0)*np.sin(p0), np.cos(t0)
        dst = np.linalg.norm(xyzs - np.array([x0, y0, z0]), axis=1)
        vals += h*np.exp(-(dst**2/(2.0*sigma**2)))
    return vals

def hkl2tp(h, k, l):
    #convert hkl to theta and phi
    mp = [h,k,l]
    r = np.linalg.norm(mp)
            
    theta = np.arctan2(mp[1],mp[0])
    phi = np.arccos(mp[2]/r)

    #return theta, phi
    return phi, theta

def fibonacci_sphere(samples=1000):
    """
    Sampling the sphere grids
    
    Args:
        samples: number of pts to generate

    Returns:
        3D points array in Cartesian coordinates
    """
    points = []
    phi = np.pi * (3. - np.sqrt(5.))  # golden angle in radians
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = np.sqrt(1 - y * y)  # radius at y
        theta = phi * i  # golden angle increment
        x = np.cos(theta) * radius
        z = np.sin(theta) * radius
        points.append((x, y, z))

    return np.array(points)


def xyz2sph(xyzs, radian=True):
    """
    convert the vectors (x, y, z) to the sphere representation (theta, phi)

    Args:
        xyzs: 3D xyz coordinates
        radian: return in radian (otherwise degree)
    """
    pts = np.zeros([len(xyzs), 2])   
    for i, r_vec in enumerate(xyzs):
        r_mag = np.linalg.norm(r_vec)
        theta0 = np.arccos(r_vec[2]/r_mag)
        if abs((r_vec[2] / r_mag) - 1.0) < 10.**(-8.):
            theta0 = 0.0
        elif abs((r_vec[2] / r_mag) + 1.0) < 10.**(-8.):
            theta0 = np.pi
       
        if r_vec[0] < 0.:
            phi0 = np.pi + np.arctan(r_vec[1] / r_vec[0])
        elif 0. < r_vec[0] and r_vec[1] < 0.:
            phi0 = 2 * np.pi + np.arctan(r_vec[1] / r_vec[0])
        elif 0. < r_vec[0] and 0. <= r_vec[1]:
            phi0 = np.arctan(r_vec[1] / r_vec[0])
        elif r_vec[0] == 0. and 0. < r_vec[1]:
            phi0 = 0.5 * np.pi
        elif r_vec[0] == 0. and r_vec[1] < 0.:
            phi0 = 1.5 * np.pi
        else:
            phi0 = 0.
        pts[i, :] = [theta0, phi0]
    if not radian:
        pts = np.degree(pts)

    return pts

def expand_sph(pts, l_max, norm=4, csphase=-1):
    """
    Transform the grid points to spherical harmonics

    Args:
        pts: 3D array 
            (thetas, phis, vals) with a length of N

        lmax: Integer
            The maximum degree of spherical harmonic.

        coeff_norm: integer
            The normalization of SHExpandLSQ(). 
            1 (default) = Geodesy 4-pi normalized harmonics;
            2 = Schmidt semi-normalized harmonics; 
            3 = unnormalized harmonics; 
            4 = orthonormal harmonics.

        csphase: Integer
            whether (-1) or not (1) apply the Condon-Shortley phase factor.

    Return:
        cilm: float, dimension (2, lmax+1, lmax+1)
            Coefficients of the spherican harmonic

        chi2: float
            The residual sum of squares misfit for an overdetermined inversion.
    """
    thetas, phis, vals = pts[:,0], pts[:,1], pts[:,2]
    thetas = np.degrees(thetas) - 90
    phis = np.degrees(phis)
    cilm, chi2 = SHExpandLSQ(vals, thetas, phis, l_max, norm=norm, csphase=csphase)

    return cilm, chi2


# Number of grids and Gaussian width
sigma, n = 0.2, 10000
xyzs = fibonacci_sphere(n)

grids = np.zeros([n, 3])
grids[:, :2] = xyz2sph(xyzs)

data = np.loadtxt('stereograph.txt', skiprows=1)
h, k, l, I = data[:, 0], data[:, 1], data[:, 2], data[:, 8]

pts = []
for i in range(len(h)):
    p, r = hkl2tp(h[i], k[i], l[i])
    pts.append([p, r, I[i]])
pts = np.array(pts)

vals = calculate_density(pts, xyzs, sigma=sigma)

# plotly 3D interactive figure
marker_data1 = go.Scatter3d(x=xyzs[:,0], y=xyzs[:,1], z=xyzs[:,2],
                            mode = 'markers',
                            marker = dict(color=vals,
                                     size=14, #vals*scale,
                                     colorbar=dict(thickness=20),
                                     opacity=0.1)
                                   )

layout = go.Layout(scene=dict(aspectmode='data'))
fig=go.Figure(data=marker_data1, layout=layout)
fig.update_scenes(camera_projection_type='orthographic')
fig.write_html("test.html")

# matplotlib figure
fig1 = plt.figure(figsize=(9, 4))
gs = gridspec.GridSpec(nrows=1, ncols=2, 
                       wspace=0.15, width_ratios=[0.7, 1])
 
grids[:, 2] = vals
cilm, chi2 = expand_sph(grids, 18) #spherical harmonics expansion
coef = pysh.SHCoeffs.from_array(cilm)
grid = coef.expand()
ax1 = fig1.add_subplot(gs[0, 0])
ax2 = fig1.add_subplot(gs[0, 1])
grid.plot3d(0, 0, ax=ax1)
grid.plot(ax=ax2, tick_interval=[120, 90])
ax2.set_xlim([1, 359])
plt.savefig('test.png')
