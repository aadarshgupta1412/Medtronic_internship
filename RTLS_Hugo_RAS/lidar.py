import io
import os
import math
import matplotlib.pyplot as plt
import numpy as np

def points(angle, dist, d):
    new_dist, new_angle = [], []
    for i in range(0, len(angle)):
        if dist[i]<d:
            new_dist.append(dist[i])
            new_angle.append(angle[i])
    return new_angle, new_dist

def smaller(angle, p1, p2):
    min = 0
    if angle[p1]<angle[p2]:
        min = angle[p2]
        return min
    else:
        min = angle[p1]
        return min
    
def larger1(angle, p3, p4):
    max = 0
    if angle[p3]<angle[p4]:
        max = angle[p3]
        return max
    
    else:
        max = angle[p4]
        return max
    
def larger2(angle, p3, p4):
    max = 0
    if angle[p3]>angle[p4]:
        max = angle[p3]
        return max
    
    else:
        max = angle[p4]
        return max
    
def check_type(angle):
    up, lp, mv = 0, 0, 0
    min, max, ty = 0, 0, 0
    for i in range(0, len(angle)):
        if i == len(angle)-1:
            mv = angle[i]
            ty, min, max = 0, angle[0], angle[len(angle)-1]
            return ty, min, max, mv
        if angle[i]<angle[i+1]:
            continue
        else:
            up, lp = i, i+1
            ty, min, max, mv = 1, smaller(angle, 0, i+1), larger1(angle, i, len(angle)-1), larger2(angle, i, len(angle)-1)
            return ty, min, max, mv

def project_full(angle, dist):
    ty, min, max, mv = check_type(angle)
    proj = []
    new_angle = angle
    mid = 0
    
    if ty == 0:
        mid = (min+max)/2
        for i in range(0, len(new_angle)):
            ang = (new_angle[i]-mid)*math.pi*2/360
            proj.append(dist[i]*math.sin(ang))
    
    else:
        mid = (min+max+360)/2
        for i in range(0, len(new_angle)):
            if angle[i]<=mid:
                ang = (new_angle[i]-mid)*math.pi*2/360
                proj.append(dist[i]*math.sin(ang))
            else:
                ang = (new_angle[i]+360-mid)*math.pi*2/360
                proj.append(dist[i]*math.sin(ang))
    return proj, mid

def in_range(ang, range1, range2):
    x = range1>180.0
    y = range2>180.0
    if x==True and y==True:
        range1-=360
        range2-=360
        if ang>=range1 and ang<=range2:
            return True
        else:
            return False
    if x==True and y==False:
        range1-=360
        if ang>=range1 and ang<=range2:
            return True
        else:
            return False
    if x==False and y==True:
        range2-=360
        if ang<=range1 and ang>=range2:
            return True
        else:
            return False
    else:
        if ang>=range1 and ang<=range2:
            return True
        else:
            return False

def project_angle1(angle, dist, ang_l, ang_h):
    proj = []
    new_angle = angle
    mid = (ang_h+ang_l)/2
    for i in range(0, len(new_angle)):
        if new_angle[i]<180:
            if in_range(new_angle[i], ang_l, ang_h):
                ang = (new_angle[i]-mid)*math.pi*2/360
                proj.append(dist[i]*math.sin(ang))
        else:
            if in_range(new_angle[i]-360, ang_l, ang_h):
                ang = (new_angle[i]-mid)*math.pi*2/360
                proj.append(dist[i]*math.sin(ang))

    return proj, mid

def project_angle(angle, dist, ang_l, ang_h):
    proj = []
    new_angle = angle
    mid = (ang_h+ang_l)/2
    for i in range(0, len(new_angle)):
        if new_angle[i]>=ang_l and new_angle[i]<=ang_h:
            ang = (new_angle[i]-mid)*math.pi*2/360
            proj.append(dist[i]*math.sin(ang))
    return proj, mid

path = "C:\\Users\\guptaa83\\OneDrive\\Documents\\ldata1\\"  # directory path of the txt files
data_path = os.listdir(path)
for i in data_path:
    file_name = path+i
    with open(file_name, 'r') as f:
        lines = f.read().split('\n')
    angle, dist = [], []
    for j in range(3, len(lines)-1):
        sep = lines[j].split('\n')
        angle.append(float(sep[0]))
        dist.append(float(sep[1]))
    angle, dist = points(angle, dist, 650)   # distance upto which we want to visualize
    p, mid = project_angle(angle, dist, 150, 210) # the angles between which we want to visualize
    new = file_name.replace("C:\\Users\\guptaa83\\OneDrive\\Documents\\ldata1\\", '') # update the directory to the data file
    index = new.replace('.txt', '')
    index = int(index)
    y = [index]*len(p)
    plt.scatter(p, y, s=5, marker='o', color='red')
plt.show()









































































