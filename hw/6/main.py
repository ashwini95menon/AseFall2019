"""main.py"""

"""main_nb.py"""

import csv

from Tbl import Tbl
from Col import Col 
from Num import Num
from Row import Row
from Sym import Sym
from decisionTree import decisionTree 

def main(filename, yis):

	inp = ""

	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			inp += ''.join(row)
			inp += "\n"

	tbl = Tbl(1)
	tbl.readData(inp)

	dt = decisionTree()

	tree = dt.tree(tbl, len(tbl.cols)-1, yis)

	dt.showt(tree)

main("auto.csv", "Num")
# main("diabetes.csv", "Sym")