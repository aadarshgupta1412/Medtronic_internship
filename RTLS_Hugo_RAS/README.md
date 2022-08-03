# About

1. The file lidar.py contains program to choose certain maximum distannce and angle range to project points in certain directions upto the distance provided. The program can also be used for visualizing complete 360 degree points at a certain points.
2. The file pointer.py is built to choose an initial point of an object (say surgical arm setup) and another point as final location (on second click), depict the instantaneous location of the object (mouse pointer) pointing towards initial point to give directions to reach back to start point.

# Directions to implement

lidar.py
1. Mount a 2D LiDAR (taken RPLiDAR A1 M8 for purpose) on a digital caliper and vary the height of setup from base. 
2. Save the point cloud data as txt files in the format as x.txt where x is the height in mm.
3. Change the location of all txt files into a single repository and replace the directory path in program.

pointer.py
1. Run the code and a new opencv window will open.
2. Click and select two distinct points and then move in the direction of arrow-head.
3. Once pointer reaches the initial point, a 'REACHED!' message is shown on the window.
