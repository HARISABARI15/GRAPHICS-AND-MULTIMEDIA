import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def plot_poly3d(ax, vertices, faces, face_colors):
    poly3d = [[vertices[vert] for vert in face] for face in faces]
    collection = Poly3DCollection(poly3d, facecolors=face_colors, linewidths=1, edgecolors='k', alpha=0.8)
    ax.add_collection3d(collection)

# Cube definition
cube_vertices = np.array([
    [0,0,0], [1,0,0], [1,1,0], [0,1,0],
    [0,0,1], [1,0,1], [1,1,1], [0,1,1]
])
cube_faces = [
    [0,1,2,3], [4,5,6,7], [0,1,5,4],
    [2,3,7,6], [1,2,6,5], [0,3,7,4]
]
cube_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

# Pyramid definition
pyramid_vertices = np.array([
    [0,0,0], [1,0,0], [1,1,0], [0,1,0], [0.5,0.5,1]
])
pyramid_faces = [
    [0,1,2,3], [0,1,4], [1,2,4], [2,3,4], [3,0,4]
]
pyramid_colors = ['orange', 'purple', 'lime', 'pink', 'gray']

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

# Render cube with flat shading
plot_poly3d(ax1, cube_vertices, cube_faces, cube_colors)
ax1.set_title('Cube with Flat Shading')

# Render pyramid with flat shading
plot_poly3d(ax2, pyramid_vertices, pyramid_faces, pyramid_colors)
ax2.set_title('Pyramid with Flat Shading')

for ax in [ax1, ax2]:
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    ax.set_zlim(-1, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

plt.show()