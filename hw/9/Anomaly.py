import csv
import random

from Col import Col
from Num import Num
from Row import Row
from Sym import Sym
from Tbl import Tbl
from unsupTree import unsupTree,Random_Projectiontree,cosine,distance
from decisionTree import decisionTree


from   copy  import deepcopy as kopy

class Anomaly:
    def __init__(self):
        self.far=0
        self.isanomaly= False
        self.side=""
        self.alpha=0.5
        self.tbl = Tbl(1)
        pass

    def detectAnomaly(self,unsupobj,x):
        self.far=0.0
        s=0.0
        besttupl, bestpts, mediandist=unsupobj.bestpivotpts(unsupobj.tbl)
        s=mediandist
        if (x < s) :
            side = "left"
        else:
            side= "right"
        if (s < 0.5):
            far = s * self.alpha;
            isanomaly = x < far
            isanomaly=True
            print("isanomaly",isanomaly)
        else :
            far = s+((1-s) * self.alpha)
            isanomaly = x > far
            isanomaly=True

        self.far=far
        self.isanomaly=isanomaly
        self.side=side
        return far,isanomaly,side

    def newrowdist(self,unsupobj,tbl,row):
        x=0.0
        pivotTupl=unsupobj.fastMap(tbl)
        cols = [tbl.cols[col] for col in tbl.xs]
        for i in range(0,len(row)):
            x=cosine(tbl.rows[pivotTupl[0]], tbl.rows[pivotTupl[1]], tbl.rows[i], pivotTupl[2], cols)
        return x
        pass



    def Anomalyrows(self, node,unsupobj, tbl, row,lvl):

        if(node.lvl==0): cnt=node.splitCount
        rowlist = []
        if(len(node.child)==0):
            if(self.isanomaly):
                rowlist.append(row)
                for i in range(0,len(row)):
                    rowlist.append(row[i])
                node.splitCount=len(rowlist)
                node.lvl=lvl
                inp = ""

                with open("newtblreadfile.csv", 'r') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    for row in spamreader:
                        inp += ''.join(row)
                        inp += "\n"

                newtbl = Tbl(1)
                newtbl.readData(inp)
                unsupTreeobj1 = unsupTree(newtbl)

                unsupTreeobj1.tree=unsupTreeobj1.split(newtbl,0)
                unsupTreeobj1.tree.lvl=node.lvl
                node=unsupTreeobj1.tree
                node.isRoot=False
        else:
            x= self.newrowdist(unsupobj, tbl, rowlist)
            far,isanomaly,side= self.detectAnomaly(unsupobj, x)
            self.isanomaly=self.isanomaly|isanomaly

            if(side=="left"):
                node.child.append(self.Anomalyrows(node.child[0],unsupobj,tbl,row,lvl+1))
            if (side == "right"):
                node.child.append(self.Anomalyrows(node.child[1],unsupobj,tbl, row,lvl+1))
            size=0
            for i in node.child:
                size=size+node.splitCount
            node.splitCount=size
            node.lvl=lvl
        return node