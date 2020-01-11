"""main.py"""

import csv

from ZeroR import ZeroR
from abcd import Abcd
from Tbl import Tbl

def main(filename):

	inp = ""
	train_count = 3

	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			inp += ''.join(row)
			inp += "\n"

	tbl = Tbl(1)
	data = list(tbl.read(inp))

	z = ZeroR(1)
	abcd = Abcd("rx", "data")

	for i in range(len(data)):

		row = data[i]

		if i < train_count:
			z.zeroRTrain(i, row)

		else:
			classified = z.zeroRClassify(row)
			abcd.abcd1(row[-1], classified)
			z.zeroRTrain(i, row)

	print("output for " + filename + "\n")
	abcd.abcdReport()
	print("\n")

main("weathernon.csv")
main("diabetes.csv")

