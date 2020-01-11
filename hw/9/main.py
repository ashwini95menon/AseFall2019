"""main.py"""

import csv
import random

from Col import Col 
from Num import Num
from Row import Row
from Sym import Sym
from Tbl import Tbl
from unsupTree import unsupTree,Random_Projectiontree,showt
from decisionTree import decisionTree
from Anomaly import Anomaly
from Probes import Probes

from   copy  import deepcopy as kopy


def incrementalRpTreeAnomolous(tbl,newtbl):
    unsupTreeobj = unsupTree(newtbl)
    unsupTreeobj.split(newtbl, 0)
    unsupTreeobj
    node = unsupTreeobj.tree
    print("Incremental RP tree")

    for i in range(500, 5001):
        newrow=tbl.rows[i].lst
        an = Anomaly()
        an.isanomaly = False
        node = an.Anomalyrows(node, unsupTreeobj, tbl, newrow, 0)
        unsupTreeobj.tree = node

    print("\n")
    # showt(node)
    return node


def main(filename):

    inp = ""

    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            inp += ''.join(row)
            inp += "\n"


    tbl = Tbl(1)
    tbl.readData(inp)

    newtbl2=tbl
    unsupTreeobj1 = unsupTree(newtbl2)
    showt(unsupTreeobj1.tree)

    clusters = unsupTreeobj1.leaves
    probestree=[]
    counter=0
    samecounter=0
    find=0

    for i in range(0,100):
        random_leaf_id = int(random.random() * len(clusters))
        cluster=clusters[random_leaf_id]
        leafnode=cluster.leaves
        random_child_id = int(random.random() * len(leafnode))
        prbe=Probes(leafnode[random_child_id])
        prbe.befor=cluster.leaves
        probestree.append(prbe)

    for i in range(0,20):
        newtbl2=tbl
        unsupTreeobj1 = unsupTree(newtbl2)
        node=unsupTreeobj1.tree
        leaves=node.leaves
        for j in range(0,100):
            probe=probestree[i]
            id=probe.row.oid
            for k in leaves:
                if(id==k.oid):
                    find=find+1
                    probe.after.append(k)
                    break

            same=True
            before=probe.befor
            after=probe.after
            for x in range(1,len(before)):
                num=before[x]
                num2=after[0]
                same=same & num.same(num2,0.95,0.38)
                if not same: break

            if same:
                samecounter=samecounter+1
            counter=counter+1

    baseline=samecounter/counter
    print("baseline",baseline)
    print("number of probes AFTER",find)
    print("\n")
    print("Incremental RPtree")
    print("\n")
    counter = 0
    samecounter = 0
    find = 0
    for y in range(0,20):
        random_rows_num1 = random.sample(range(1, len(tbl.rows)), 500)
        row_data1 = []
        newtbl3 = Tbl(1)
        newtbl3.addcol([col.txt for col in tbl.cols])

        for i in random_rows_num1:
            row_data1.append(tbl.rows[i].lst)

        for i in range(len(row_data1)):
            newtbl3.addrow(row_data1[i])

        incremntlnode=incrementalRpTreeAnomolous(tbl, newtbl3)

        leaves = incremntlnode.leaves
        for j in range(0, 100):
            probe1 = probestree[i]
            id = probe1.row.oid
            for k in leaves:
                if (id in k):
                    find = find + 1
                    probe1.after.append(k.leaves)
                    break

            same = True
            before = probe1.befor
            after=probe1.after
            for x in range(1, len(before)):
                num=before[x]
                num2=after[x]
                same = same & num.same(num2,0.95,0.38)
                if not same: break

            if same:
                samecounter = samecounter + 1
            counter = counter + 1

    score = samecounter / counter
    print("score", score)
    print("number of probes AFTER", find)
    print("\n")


main('xomo10000.csv')
# main('pom310000.csv')