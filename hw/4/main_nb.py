"""main_nb.py"""

import csv

from Nb import Nb
from abcd import Abcd
from Tbl import Tbl
from Col import Col 
from Num import Num
from Row import Row
from Sym import Sym

def main(filename, train_count):

	inp = ""

	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			inp += ''.join(row)
			inp += "\n"

	tbl = Tbl(1)
	data = list(tbl.read(inp))

	nb = Nb()
	abcd = Abcd("rx", "data")

	for i in range(len(data)):

		row = data[i]

		if i < train_count:
			nb.NbTrain(i, row)

		else:
			classified = nb.NbClassify(row)
			abcd.abcd1(row[-1], classified)
			nb.NbTrain(i, row)

	print("output for " + filename + "\n")
	abcd.abcdReport()
	print("\n")

main("weathernon.csv", 5)
main("diabetes.csv", 20)