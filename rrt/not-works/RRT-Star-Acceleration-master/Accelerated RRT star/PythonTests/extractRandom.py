import numpy as np
import math
import itertools
import random
from shapely.geometry import LineString

def insidetriangle(x_list,y_list):
    
    xs=np.array((x_list[0],x_list[1],x_list[2]),dtype=int)
    ys=np.array((y_list[0],y_list[1],y_list[2]),dtype=int)

    # The possible range of coordinates that can be returned
    x_range=np.arange(np.min(xs),np.max(xs)+1)
    y_range=np.arange(np.min(ys),np.max(ys)+1)

    # Set the grid of coordinates on which the triangle lies. The centre of the
    # triangle serves as a criterion for what is inside or outside the triangle.
    X,Y=np.meshgrid( x_range,y_range )
    xc=np.mean(xs)
    yc=np.mean(ys)

    # From the array 'triangle', points that lie outside the triangle will be
    # set to 'False'.
    triangle = np.ones(X.shape,dtype=bool)
    for i in range(3):
        ii=(i+1)%3
        if xs[i]==xs[ii]:
         if xc>xs[i]:
            include = (X > xs[i])
         else:
            include = (X < xs[i])
        else:
            slope=(ys[ii]-ys[i])/(xs[ii]-xs[i])
            poly=np.poly1d([slope,ys[i]-xs[i]*slope])

            if yc>poly(xc):
                include = (Y > poly(X))
            else:
                include = (Y < poly(X))
        triangle*=include

    # Output: 2 arrays with the x- and y- coordinates of the points inside the
    # triangle.
    result = (np.dstack((X[triangle],Y[triangle]))).tolist()    #zipping them
    result = list(itertools.chain.from_iterable(result))    #flattening the array
    result = list(map(tuple,result))    #make list of tuples
    
    return (result)

#extract all points on the diagonal
def diagonal(first_dpoint, second_dpoint):

    ls = LineString([first_dpoint, second_dpoint])

    xy = list()

    for f in range(0, int(math.ceil(ls.length)) + 1):
        p = ls.interpolate(f).coords[0]
        pr = tuple(map(round, p))
        if pr not in xy:
            xy.append(pr)

    return (xy)


def update_excluded(obstacle,excluded, to_allow_range):

    if(obstacle == []):
       return;

    new_obstacle = sorted(obstacle , key=lambda k: [k[0], k[1]]) #sort by x value. in case of tie then by y
    dist = dict()
    x0=new_obstacle[0][0]
    y0=new_obstacle[0][1]
    p0=(x0,y0)
    for x, y in new_obstacle[1:]:
        dist[x,y] = math.hypot(x - x0, y - y0)

    sorted_dists = sorted(dist, key=lambda x: dist[x])  #sort by distance from base point, all points of rectangle

    first_parameter_list = list()
    first_parameter_list.extend(tuple((x0,sorted_dists[0][0],sorted_dists[1][0])))
    second_parameter_list = list()
    second_parameter_list.extend(tuple((y0,sorted_dists[0][1],sorted_dists[1][1])))

    first_triangle = insidetriangle(first_parameter_list, second_parameter_list)

    first_parameter_list.clear()
    second_parameter_list.clear()
    first_parameter_list.extend(tuple((sorted_dists[2][0],sorted_dists[0][0],sorted_dists[1][0])))
    second_parameter_list.extend(tuple((sorted_dists[2][1],sorted_dists[0][1],sorted_dists[1][1])))

    second_triangle = insidetriangle(first_parameter_list, second_parameter_list)

    diagon =  diagonal(sorted_dists[0],sorted_dists[1])

    excluded.clear()
    excluded = set(first_triangle + second_triangle + diagon)
    to_allow_range_temp=list((set(to_allow_range) - excluded))
    to_allow_range.clear();
    to_allow_range.extend(to_allow_range_temp)

