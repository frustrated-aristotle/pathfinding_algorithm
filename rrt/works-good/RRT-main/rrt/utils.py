import os
from collections import namedtuple
from dataclasses import dataclass
import imageio
import numpy as np
from typing import Any


@dataclass
class Node:
    x: float
    y: float
    parent_node: Any
    cost: Any

def find_nearest_node(nodes, new_node):

    dist_list = []
    for node in nodes:
        vector = np.array([new_node.x - node.x, new_node.y - node.y])
        dist_list.append(np.linalg.norm(vector))
    min_dist_idx = dist_list.index(np.min(dist_list))
    return nodes[min_dist_idx]

def find_neighbors(nodes, new_node, rad):
    epsilon = 1e-2
    neighbors = []
    for node in nodes:
        vector = np.array([new_node.x - node.x, new_node.y - node.y])
        distance = np.linalg.norm(vector)
        if distance <= rad + epsilon:
            neighbors.append(node)
    return neighbors

def get_distance(node1, node2):
    
    vector = np.array([node2.x - node1.x, node2.y - node1.y])
    return np.linalg.norm(vector)  

def get_step_point(nearest_node, new_node, stepsize):
    vec_displ = np.array([new_node.x - nearest_node.x, new_node.y - nearest_node.y])
    unit_vec = vec_displ / np.linalg.norm(vec_displ)
    step_sized_vec = unit_vec * stepsize

    x_path_end = nearest_node.x + step_sized_vec[0]
    y_path_end = nearest_node.y + step_sized_vec[1]
    return Node(x_path_end, y_path_end, nearest_node, None)

def check_collision(collision_ck_map, nearest_node, one_step_target):

    x_path = np.linspace(nearest_node.x, one_step_target.x, 200)
    y_path = np.linspace(nearest_node.y, one_step_target.y, 200)

    height, width = collision_ck_map.shape
    
    # Out of bound
    if one_step_target.x >= width or one_step_target.y >= height:
        return True

    for coord in zip(x_path, y_path):
        x_coord, y_coord = int(coord[0]), int(coord[1])
        if collision_ck_map[y_coord, x_coord] == 0:
            return True
    return False

def check_arrival(one_step_target, target_node, stepsize):
    vec_displ = np.array([target_node.x - one_step_target.x, target_node.y - one_step_target.y])
    distance = np.linalg.norm(vec_displ)
    if distance <= stepsize:
        return True
    return False


def make_gif(image_dir='images'):
    images = []
    for file_name in sorted(os.listdir(image_dir)):
        if file_name.endswith('.jpg'):
            file_path = os.path.join(image_dir, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave('figure.gif', images, duration=0.01)
