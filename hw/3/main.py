"""main.py"""

from Col import Col 
from Num import Num
from Tbl import Tbl
from Row import Row
from Sym import Sym
from abcd import Abcd

def main():

	count_tbl = 1
	count_row = 1
	count_col = 1

	output = ""

	s = """
	outlook, ?$temp,  <humid, wind, !play
	rainy, 68, 80, FALSE, yes # comments
	sunny, 85, 85,  FALSE, no
	sunny, 80, 90, TRUE, no
	overcast, 83, 86, FALSE, yes
	rainy, 70, 96, FALSE, yes
	rainy, 65, 70, TRUE, no
	overcast, 64, 65, TRUE, yes
	sunny, 72, 95, FALSE, no
	sunny, 69, 70, FALSE, yes
	rainy, 75, 80, FALSE, yes
	sunny, 75, 70, TRUE, yes
	overcast, 72, 90, TRUE, yes
	overcast, 81, 75, FALSE, yes
	rainy, 71, 91, TRUE, no
	"""

	tbl = Tbl(count_tbl)
	count_tbl += 1

	data = list(tbl.read(s))

	row = data[0]
	list_num = []
	list_syms = []
	list_goals = []
	list_xs = []
	weights = {}
	ignore_index = []
	classes = len(data[0])

	for i in range(len(data)):
		row = data[i]
		if isinstance(row, list):
			if i == 0:
				for j in range(len(row)):
					if row[j][0] != "?": 
						if row[j][0] in "<>$":
							list_num.append(j)
							tbl.cols.append(Num(count_tbl, j + 1, row[j], 0, 0, 0))
						else:
							tbl.syms.append(Sym(count_tbl, j + 1, row[j]))
							list_syms.append(j)

						if row[j][0] in "<>!":
							list_goals.append(j + 1)
						else:
							list_xs.append(j + 1)
						if row[j][0] == "<":
							weights[j + 1] = -1
						count_tbl += 1
					else:
						ignore_index.append(j)

			else:
				row_for_tbl = []
				for j in range(len(row)):
					if j not in set(ignore_index):
						if row[j] == '?':
							row[j] = tbl.cols[j].mean
						if j in set(list_num):
							tbl.cols[list_num.index(j)].addToNum(row[j])
							tbl.cols[list_num.index(j)].updateMeanAndSdAdd(row[j])
						else:
							tbl.syms[list_syms.index(j)].addSym(row[j])

						row_for_tbl.append(row[j])

				count_tbl+= 1

	f = open("output3.txt", "w+")

	f.write("t.cols\n")
	k = 1
	for i in tbl.cols:
		f.write("| " + str(k) + "\n")
		f.write("| | add: Num1\n") 
		f.write("| | col: "+ str(i.pos) + "\n")
		f.write("| | hi: "+ str(i.hi) + "\n")
		f.write("| | lo: "+ str(i.lo) + "\n")
		f.write("| | m2: "+ str(i.m2) + "\n")
		f.write("| | mu: "+ str(i.mean) + "\n")
		f.write("| | n: "+ str(i.count) + "\n")
		f.write("| | oid: "+ str(i.oid) + "\n")
		f.write("| | sd: "+ str(i.sd) + "\n")
		f.write("| | txt: "+ str(i.txt) + "\n")
		k += 1

	for i in tbl.syms:
		f.write("| " + str(k) + "\n")
		f.write("| | add: Sym1\n") 
		f.write("| | cnt: "+ str(i.cnt) + "\n")
		f.write("| | col: "+ str(i.pos) + "\n")
		f.write("| | mode: "+ str(i.mode) + "\n")
		f.write("| | most: "+ str(i.most) + "\n")
		f.write("| | n: "+ str(i.count) + "\n")
		f.write("| | oid: "+ str(i.oid) + "\n")
		f.write("| | txt: "+ str(i.txt) + "\n")
		k += 1

	f.write("t.my\n")
	f.write("| class: " + str(classes) + "\n")
	f.write("| | goals: " + ', '.join([str(elem) for elem in list_goals]) + "\n")
	f.write("| nums\n")
	for i in list_num:
		f.write("| | " + str(i + 1) + "\n")
	f.write("| syms\n")
	for i in list_syms:
		f.write("| | " + str(i + 1) + "\n")	
	f.write("| w \n| | ")
	f.write(str(weights))
	f.write("\n| xnums\n")
	f.write("| | xs: " + ', '.join([str(elem) for elem in list_xs]) + "\n")
	f.write("| | xsyms: " + ', '.join([str(elem) for elem in list_xs]) + "\n")	

main()

