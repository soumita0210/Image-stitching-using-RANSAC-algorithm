"""
RANSAC Algorithm Problem
(Due date: Oct. 23, 3 P.M., 2019)
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
You can use the library random
Hint: It is recommended to record the two initial points each time, such that you will Not 
start from this two points in next iteration.
"""
import random
def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    # TODO: implement this function.
    #raise NotImplementedError
    
    length=len(input_points)
    pointlist=[]
    
    inlier_points_name=[]
    outlier_points_name=[]
    min_d=10000
    
    for i in range(k):
        n1=random.randrange(0,length)
        n2=random.randrange(0,length)
        
        inl=[]
        outl=[]
        counter=0
        dist=0
        
        if (n1!=n2):
            pl=[n1,n2]
            pl_rev=[n2,n1]
        
            if(pl not in pointlist and pl_rev not in pointlist):
                pointlist.append(pl)
                
                p1=input_points[n1]['value']
                p2=input_points[n2]['value']
                if(p1[0]==p2[0]):
                    xc=1
                    yc=0
                    intercept=-p1[0]
                elif(p1[1]==p2[1]):
                    xc=0
                    yc=1
                    intercept=-p2[0]
                else:
                    xc=(p2[1]-p1[1])/(p2[0]-p1[0])
                    yc=-1
                    intercept=p2[1]-xc*p2[0]
                    
                for j in range(length):
                    pi=input_points[j]['value']
                    pdist= (abs(xc*pi[0]+yc*pi[1]+intercept))/((xc**2+yc**2)**0.5)
                    
                    if(pdist<t):
                        inl.append(input_points[j]['name'])
                        dist+=pdist
                        counter+=1
                    else:
                        outl.append(input_points[j]['name'])
                
                
                if((counter-2)>=d):
                    dist/=(counter-2)
                    if(dist<min_d):
                        min_d=dist
                        inlier_points_name=inl
                        outlier_points_name=outl
                        
    return (inlier_points_name,outlier_points_name)


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()


