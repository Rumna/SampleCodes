import re
import sys
import numpy as np
import math
import subprocess

name_rx = '\"[a-zA-Z]+[a-zA-Z\s]*[a-zA-Z]*\"'
num_rx = '-?\d+'
coord_rx = r'\(' + num_rx + '\s*,\s*' + num_rx + '\)'
cmd_a_rx = '\s*add\s+'+name_rx+'\s+('+coord_rx+'\s*){2,}\s*$'
cmd_m_rx = '\s*mod\s+' + name_rx + '\s*(' + coord_rx + '\s*){2,}\s*$'
cmd_rm_rx = '\s*rm\s+' + name_rx + '$'
cmd_gg="gg"

cmd_a_chk = re.compile(cmd_a_rx)
cmd_m_chk=re.compile(cmd_m_rx)
cmd_rm_chk=re.compile(cmd_rm_rx)
cmd_gg_chk=re.compile(cmd_gg)

all_streets={}
v=[]
point_list1=[]
point_list2=[]
processed_streets=[]
intersect_point_list=[]
endpoint_list=[]
list_of_points_list=[]
Vertices={}
reset_point_list=[]
single_intersect_points=[]
multiple_intersect_points=[]
multiple_points_index=[]
Edge_list=[]
t_Edge_list=[]

class Point(object):
    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__ (self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return str(self.src) + '-->' + str(self.dst)

def intersect (l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
    xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    if xden==0.0:
        return 0
    else:
        xcoor =  xnum / xden

    ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if yden==0.0:
        return 0.0
    else:
        ycoor = ynum / yden

    if min(x1, x2) <= xcoor <= max(x1, x2) and min(y1,y2) <= ycoor <= max(y1, y2):
        if min(x3, x4) <= xcoor <= max(x3, x4) and min(y3, y4) <= ycoor <= max(y3, y4):
                return Point (xcoor, ycoor)

    else:
        return 0


class Street:
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.all_streets = {}

    def add_street(self, name, coord):
        name=name.lower()
        if name not in all_streets:
            all_streets[name]=coord

        else:
            raise Exception ('Street already present and cannot be added, use "mod" to modify it')

    def mod_street(self,name,coord):
        name = name.lower()
        if name in all_streets:
            all_streets[name]=coord

        else:
            raise Exception ('"mod" specified for a street that does not exist')

    def remove_street(self, name):
        name = name.lower()
        if name in all_streets:
            all_streets.pop(name)

        else:
            raise Exception ('"rm" specified for a street that does not exist')

def print_all(all_streets):
        global point_list1
        global point_list2
        global multiple_intersect_points
        global t_Edge_list
        all_st_keys = list(all_streets.keys())
        v.clear()
        point_list1.clear()
        point_list2.clear()
        processed_streets.clear()
        intersect_point_list.clear()
        endpoint_list.clear()
        list_of_points_list.clear()
        Vertices.clear()
        reset_point_list.clear()
        single_intersect_points.clear()
        multiple_intersect_points.clear()
        multiple_points_index.clear()
        Edge_list.clear()
        t_Edge_list.clear()
        for i in all_streets.keys():
            if i in processed_streets:
                continue
            else:
                temp = i;
                val1 = all_streets[temp]
                for j in val1:
                    t = str(j)
                    n = eval(t)
                    point_list1.append(n[0])
                    point_list1.append(n[1])
            for k in all_streets.keys():
                if k == temp or k in processed_streets:
                    continue
                else:
                    val2 = all_streets[k]
                    for l in val2:
                        t2 = str(l)
                        n2 = eval(t2)
                        point_list2.append(n2[0])
                        point_list2.append(n2[1])
                for x in range(0, len(point_list1) - 3, 2):
                    p1 = Point(point_list1[x], point_list1[x + 1])
                    p2 = Point(point_list1[x + 2], point_list1[x + 3])
                    l1 = Line(p1, p2)
                    for y in range(0, len(point_list2) - 3, 2):
                        p3 = Point(point_list2[y], point_list2[y + 1])
                        p4 = Point(point_list2[y + 2], point_list2[y + 3])
                        l2 = Line(p3, p4)
                        intersect_points = intersect(l1, l2)
                        if intersect_points != 0:
                            if str(intersect_points) not in v:
                                v.append(str(intersect_points))
                                intersect_point_list.append(str(intersect_points))

                            if str(p1) not in v:
                                v.append(str(p1))

                            if str(p2) not in v:
                                v.append(str(p2))

                            if str(p3) not in v:
                                v.append(str(p3))

                            if str(p4) not in v:
                                v.append(str(p4))

                            list_of_points_list.append([str(p1), str(p2), str(intersect_points)])
                            list_of_points_list.append([str(p3), str(p4), str(intersect_points)])
                point_list2 = []
            processed_streets.append(temp)
            point_list1 = []

        i = 1
        for a in range(0, len(v), 1):
            Vertices[i] = v[a]
            i = i + 1

            if v[a] not in intersect_point_list:
                endpoint_list.append(v[a])

        for r in list_of_points_list:
            if r not in reset_point_list:
                reset_point_list.append(r)

        for i in range(len(reset_point_list) - 1):
            for j in range(i + 1, len(reset_point_list), 1):
                if (reset_point_list[i][0] == reset_point_list[j][0] and \
                    reset_point_list[i][1] == reset_point_list[j][1]) or \
                        (reset_point_list[i][0] == reset_point_list[j][1] and \
                        reset_point_list[i][1] == reset_point_list[j][0]):
                    if reset_point_list[i][0] not in multiple_intersect_points:
                        multiple_intersect_points.append(reset_point_list[i][0])

                    if reset_point_list[i][1] not in multiple_intersect_points:
                        multiple_intersect_points.append(reset_point_list[i][1])

                    if reset_point_list[i][2] not in multiple_intersect_points:
                        multiple_intersect_points.append(reset_point_list[i][2])

                    if reset_point_list[j][2] not in multiple_intersect_points:
                        multiple_intersect_points.append(reset_point_list[j][2])

                    if i not in multiple_points_index:
                        multiple_points_index.append(i)
                    if j not in multiple_points_index:
                        multiple_points_index.append(j)

        for i in range(len(reset_point_list)):
            if i not in multiple_points_index:
                single_intersect_points.append(reset_point_list[i])

        multiple_intersect_points = sorted(multiple_intersect_points)

        for t in range(len(single_intersect_points)):
            single_intersect_points[t] = sorted(single_intersect_points[t])

        for i in single_intersect_points:
            for l in range(0, len(i) - 1, 1):
                for k, val in Vertices.items():
                    if i[l] == val:
                        t_Edge_list.append(k)

                for k, val in Vertices.items():
                    if i[l + 1] == val:
                        t_Edge_list.append(k)

                Edge_list.append(t_Edge_list)
                t_Edge_list = []

        t_Edge_list = []
        for i in range(0, len(multiple_intersect_points) - 1, 1):
            for k, val in Vertices.items():
                if multiple_intersect_points[i] == val:
                    t_Edge_list.append(k)

            for k, val in Vertices.items():
                if multiple_intersect_points[i + 1] == val:
                    t_Edge_list.append(k)

            Edge_list.append(t_Edge_list)
            t_Edge_list = []

        print('V={ ')
        for k in Vertices:
            print(str(k) + str(': ') + (Vertices[k]))
        print(' }')

        print('E= {')
        for i in range(len(Edge_list)):
            if i == len(Edge_list)-1:
                print('<{},{}>'.format(Edge_list[i][0],Edge_list[i][1]))

            else:
                print('<{},{}>,'.format(Edge_list[i][0], Edge_list[i][1]))
        print('}')

def main():
    while True:
        try:
            cmd = sys.stdin.readline()
            cmd=cmd.strip()
            if cmd=="":
                break
            if cmd_gg_chk.match(cmd):
                print_all(all_streets)
            elif cmd_a_chk.match(cmd) or cmd_m_chk.match(cmd) or cmd_rm_chk.match(cmd):
                name = re.findall(name_rx,cmd)[0]
                coords = [ tuple([ float(num) for num in re.findall(num_rx,coord) ])\
                    for coord in re.findall(coord_rx,cmd)]
                s=Street(name,coords)
                if cmd_a_chk.match(cmd):
                    s.add_street(name, coords)

                if cmd_m_chk.match(cmd):
                    s.mod_street(name,coords)

                if cmd_rm_chk.match(cmd):
                    s.remove_street(name)
            else:
                print('Error: Invalid input')
        except KeyboardInterrupt:
            print('Thank you for your input')
            sys.exit(0)
        except Exception as ex:
            print("Error: ", str(ex))
    sys.exit(0)

if __name__ == '__main__':
    main()
