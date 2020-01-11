import csv
import random

from Col import Col
from Num import Num
from Row import Row
from Sym import Sym
from Tbl import Tbl
from unsupTree import unsupTree,Random_Projectiontree,cosine,distance,showt
from decisionTree import decisionTree

from   copy  import deepcopy as kopy

class Probes:
    def __init__(self,row):
        self.row=row
        self.befor=[]
        self.after=[]
