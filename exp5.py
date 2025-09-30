import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def translate(points, tx, ty, tz):
    T = np.array([tx, ty, tz])
    return points + T

def scale(points, sx, sy, sz):
    S = np.diag([sx, sy, sz])
    return points @ S

def rotate_x(points, angle):
    rad = np.radians(angle)
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rad), -np.sin(rad)],
        [0, np.sin(rad), np.cos(rad)]
    ])
    return points @ Rx

def rotate_y(points, angle):
    rad = np.radians(angle)
    Ry = np.array([
        [np.cos(rad), 0, np.sin(rad)],
        [0, 1, 0],
        [-np.sin(rad), 0, np.cos(rad)]
    ])
    return points @ Ry

def rotate_z(points, angle):
    rad = np.radians(angle)
    Rz = np.array([
        [np.cos(rad), -np.sin(rad), 0],
        [np.sin(rad), np.cos(rad), 0],
        [0, 0, 1]
    ])
    return points @ Rz

def plot_object(ax, vertices, edges, color='b'):
    for edge in edges:
        xs, ys, zs = zip(*vertices[edge])
        ax.plot(xs, ys, zs, color=color)


cube_vertices = np.array([
    [0,0,0], [1,0,0], [1,1,0], [0,1,0],
    [0,0,1], [1,0,1], [1,1,1], [0,1,1]
])
cube_edges = [
    [0,1], [1,2], [2,3], [3,0],
    [4,5], [5,6], [6,7], [7,4],
    [0,4], [1,5], [2,6], [3,7]
]

pyramid_vertices = np.array([
    [0,0,0], [1,0,0], [1,1,0], [0,1,0], [0.5,0.5,1]
])
pyramid_edges = [
    [0,1], [1,2], [2,3], [3,0],
    [0,4], [1,4], [2,4], [3,4]
]

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

plot_object(ax1, cube_vertices, cube_edges, 'b')
plot_object(ax1, pyramid_vertices, pyramid_edges, 'g')
ax1.set_title('Original Objects')

cube_transformed = rotate_x(cube_vertices, 30)
cube_transformed = rotate_y(cube_transformed, 45)
cube_transformed = scale(cube_transformed, 1.5, 1, 0.5)
cube_transformed = translate(cube_transformed, 2, 0, 0)

pyramid_transformed = rotate_z(pyramid_vertices, 60)
pyramid_transformed = scale(pyramid_transformed, 1, 2, 1)
pyramid_transformed = translate(pyramid_transformed, -2, 0, 0)

plot_object(ax2, cube_transformed, cube_edges, 'r')
plot_object(ax2, pyramid_transformed, pyramid_edges, 'm')
ax2.set_title('Transformed Objects')

for ax in [ax1, ax2]:
    ax.set_xlim(-3, 4)
    ax.set_ylim(-3, 4)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

plt.show()