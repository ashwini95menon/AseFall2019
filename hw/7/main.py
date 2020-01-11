"""main.py"""

"""main_nb.py"""

import csv

# from Tbl import Tbl
from Col import Col 
from Num import Num
from Row import Row
from Sym import Sym
#from decisionTree import decisionTree
from Hw7 import Hw7

def main(filename, train_count):

    inp = ""

    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            inp += ''.join(row)
            inp += "\n"



    hw7cl = Hw7(inp)
    hw7cl


# main("pom310000.csv", 5)
main('xomo10000.csv', 20)