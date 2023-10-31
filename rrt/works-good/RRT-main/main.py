import argparse
import pathlib
import shutil
import os
import cv2

from rrt.solve import rrt_solver, rrt_star_solver


def pick_start_target_pos(event, x, y, flags, param):
    coordinates = param[0]
    image = param[1]
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(coordinates) == 0:
            cv2.circle(image, (x,y), 5, (0,0,255), 25)
        elif len(coordinates) == 2:
            cv2.circle(image, (x,y), 5, (255,0,0), 25)
        else:
            return None
        coordinates.append(x)
        coordinates.append(y)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--map', type=str, default='map.png', help='path to map file')
    parser.add_argument('--stepsize', type=int, default=30, help='step size')
    parser.add_argument('--alg', type=str, default='rrtstar', help='rrtstar or rrt')
    parser.add_argument('--radius', type=float, default=35, help='radius for rrtstar')
    args = parser.parse_args()

    if os.path.exists('images'):
        shutil.rmtree('images')
    pathlib.Path('images').mkdir(parents=True, exist_ok=True)

    map = args.map
    world_map = cv2.imread(map, cv2.IMREAD_COLOR)
    stepsize = args.stepsize
    coordinates=[]

    window_name = 'Path Planning'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, pick_start_target_pos, param=[coordinates, world_map])

    while True:
        cv2.imshow(window_name, world_map)
        cv2.putText(world_map, 'Choose start/target position', (200,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 2)
        if len(coordinates) == 4:
            cv2.waitKey(1000)
            break
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break

    start = (coordinates[0], coordinates[1])
    target = (coordinates[2], coordinates[3])

    if args.alg == 'rrtstar':
        rrt_star_solver(map, start, target, stepsize, args.radius)
    else:
        rrt_solver(map, start, target, stepsize)
