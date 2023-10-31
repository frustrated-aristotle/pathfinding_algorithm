# RRT-Star-Acceleration
This is a python project, to accelerate the RRT* algorithm, by identifying obstacles "on-the-fly" and removing them from the sampling range.

The program starts from the following path :  Accelerated RRT star/PythonTests/rrt.py

A video clip presenting the project in action: rrt py extract obstacles.mp4

A python script located at path: Accelerated RRT star/PythonTests/extractRandom.py, locates all points inside the bounded rectangle, and extracts them from the sample range. It does so by identifying all the inner points of the rectangle, divided into two triangles by the main diagonal, and using the meshgrid method of numpy library to seperate integer points outside the rectangle from those inside it. Therefore, maximum precision is acheived, without having to settle for speed of execution.
Another calculation is made for the points on the main diagonal that are not included in the insidetriangle() function, and is made in the diagonal() function.
