"""ZeroR.py"""

from Col import Col 
from Num import Num
from Tbl import Tbl
from Row import Row
from Sym import Sym

class ZeroR():

	def __init__(self, t_id):

		self.tbl = Tbl(t_id)
		self.count_tbl = t_id + 1

	def zeroRTrain(self, i, row):

		if isinstance(row, list):
			if i == 0:
				for j in range(len(row)):

					if row[j][0] != "?": 
						self.tbl.headers.append(j)

						if row[j][0] not in "<>!":
							self.tbl.xs.append(j)

						if row[j][0] in "<>$":
							self.tbl.list_num.append(j)
							self.tbl.cols.append(Num(self.count_tbl, j + 1, row[j], 0, 0, 0))
						else:
							self.tbl.cols.append(Sym(self.count_tbl, j + 1, row[j]))
						
						self.count_tbl += 1
					else:
						self.tbl.ignore_index.append(j)

			else:
				for j in range(len(row)):
					if j not in set(self.tbl.ignore_index):
						if row[j] == '?':
							row[j] = self.tbl.cols[j].mean
						if j in set(self.tbl.list_num):
							self.tbl.cols[self.tbl.headers.index(j)].addToNum(row[j])
							self.tbl.cols[self.tbl.headers.index(j)].updateMeanAndSdAdd(row[j])
						else:
							self.tbl.cols[self.tbl.headers.index(j)].addSym(row[j])
							
				self.count_tbl+= 1

	def zeroRClassify(self, row):

		return self.tbl.cols[-1].mode


