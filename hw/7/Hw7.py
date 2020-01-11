import csv
from math import log
from Tbl import Tbl
from Col import Col
from Num import Num
from Row import Row
from Sym import Sym
from sys import path
import os, random, math
from collections import defaultdict
path.append(os.path.abspath("..") + "\\3")
from   lib   import THE,Pretty,same,first,last,ordered

seed = random.seed

class Hw7:
    def __init__(self,fle):
        seed(1)
        self.tbl = Tbl(1)
        self.tbl.readData(fle)
        self.tbls = {}
        self.things = {}
        self.m = 2
        self.k = 1
        self.n = -1
        self.classes = []
        self.count_tbl = 2
        self.tree = self.split(self.tbl, 0)

        showt(self.tree)

    def fastMap(self, tbl):
        cols = [tbl.cols[col] for col in tbl.xs]
        randompt = random.randint(0, len(tbl.rows)-1)
        firstPivotpts = []
        for row in range(0, len(tbl.rows)):
            dist = distance(tbl.rows[randompt], tbl.rows[row], cols)
            firstPivotpts.append((row, dist))
        firstPivotpts.sort(key=lambda x: x[1])
        firstPivotptsLength=len(firstPivotpts)
        firstPivotidx = firstPivotpts[math.floor(firstPivotptsLength * 0.9)][0]
        secondPivotpts = []
        for row in range(0, len(tbl.rows)):
            dist = distance(tbl.rows[firstPivotidx], tbl.rows[row], cols)
            secondPivotpts.append((row, dist))
        secondPivotpts.sort(key=lambda x: x[1])
        secondPivotptsLength=len(firstPivotpts)
        secondPivotidx = secondPivotpts[math.floor(secondPivotptsLength * 0.9)][0]
        dist = secondPivotpts[math.floor(secondPivotptsLength * 0.9)][1]
        # print("frstidx",firstPivotidx)
        # print("scndidx",secondPivotidx)
        # print("dist",dist)
        return (firstPivotidx, secondPivotidx, dist)

    def bestpivotpts(self, tbl):
        n = 10
        initial = len(tbl.rows)

        besttupl = None
        bestpts = None
        while n > 0:
            n -= 1
            pivotTupl = self.fastMap(tbl)
            rwdistList = []
            cols = [tbl.cols[col] for col in tbl.xs]
            for row in range(0, len(tbl.rows)):
                dist = cosine(tbl.rows[pivotTupl[0]], tbl.rows[pivotTupl[1]], tbl.rows[row], pivotTupl[2], cols)
                rwdistList.append((row, dist))
            rwdistList.sort(key=lambda x: x[1])
            mediandist = None
            index = (len(rwdistList) - 1) // 2
            if (len(rwdistList) % 2):
                mediandist = rwdistList[index][1]
            else:
                mediandist = (rwdistList[index][1] + rwdistList[index + 1][1]) / 2.0
            pointset = set()
            for point in rwdistList:
                if point[1] < mediandist:
                    pointset.add(point[0])
            right = abs(len(pointset) - (len(rwdistList) - len(pointset)))

            if right < initial:
                initial = right
                bestpts = pointset
                besttupl = pivotTupl

        return besttupl, bestpts


    def split(self, tbl, lvl):

        node = Random_Projectiontree()
        left_tbl = Tbl(1)
        right_tbl = Tbl(1)
        if (len(tbl.rows) < 2 * pow(len(self.tbl.rows), 1 / 2)):
            for each in tbl.headers:

                if tbl.cols[each].txt[0]=="<" or tbl.cols[each].txt[0]==">":
                    node.leaves.append(tbl.cols[each])

            node.lvl,node.splitCount = lvl,len(tbl.rows)
            return node
        else:
            besttupl, bestpts = self.bestpivotpts(tbl)
            left_tbl.addcol([col.txt for col in tbl.cols])
            right_tbl.addcol([col.txt for col in tbl.cols])
            for idx, each in enumerate(tbl.rows):
                 if idx in bestpts:
                     right_tbl.addrow(each.lst)
                 else:
                     left_tbl.addrow(each.lst)
            splitCount = len(left_tbl.rows) + len(right_tbl.rows)

            node.child.append(self.split(left_tbl, lvl + 1))
            node.child.append(self.split(right_tbl, lvl + 1))
            node.splitCount = splitCount
            node.lvl = lvl
            return node

class Random_Projectiontree:
    def __init__(self):
        self.child = []
        self.leaves = []
        self.lvl = 0
        self.isRoot = False
        self.splitCount = 0

def showt(root):
    if root.isRoot:
        for col in root.leaves:
            print(col.txt + " = ", end=" ")
            if (isinstance(col, Num)):
                print("{0} ({1})".format(col.mean, col.sd), end=" ")
            else:
                print("{0} ({1})".format(col.mode, col.variety()), end=" ")
    if not root.isRoot:
        for _ in range(root.lvl):
            print("|. ", end=" ")
    print(root.splitCount)
    if len(root.child) == 0:
        for _ in range(root.lvl - 1):
            print("|. ", end=" ")
        for col in root.leaves:
            print(col.txt + " = ", end=" ")
            if (isinstance(col, Num)):
                print("{0} ({1})".format(col.mean, col.sd), end=" ")
            else:
                print("{0} ({1})".format(col.mode, col.variety()), end=" ")
        print("")
    else:
        for each in root.child:
            showt(each)

def distance(row1, row2, cols):
    d, n, p = 0, 0, 2
    for col in cols:
        n += 1
        d0 = col.dist(row1.lst[col.pos], row2.lst[col.pos])
        d += d0 ** p
    return d ** (1 / p) / n ** (1 / p)

def cosine(x, y, z, dist, cols):
    return (distance(x, z, cols) ** 2 + dist ** 2 - distance(y, z, cols) ** 2) / (2 * dist)
