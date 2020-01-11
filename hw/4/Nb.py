"""nb.py"""

from math import log

from Col import Col 
from Num import Num
from Tbl import Tbl
from Row import Row
from Sym import Sym

class Nb():

	def __init__(self):

		self.tbls = {}
		self.things = {}
		self.m = 2
		self.k = 1
		self.n = -1
		self.classes = []
		self.count_tbl = 2
		self.tbl = Tbl(1)

	def NbTrain(self, i, row):

		if isinstance(row, list):
			if i == 0:
				for j in range(len(row)):

					if row[j][0] != "?": 

						self.tbl.headers.append(j)
						self.tbl.headers_text.append(row[j])

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
				row_for_tbl = []
				self.n += 1
				row_class = row[-1]

				self.NbEnsureClassExists(row_class)

				for j in range(len(row)):

					if j not in set(self.tbl.ignore_index):

						row_for_tbl.append(row[j])

						if row[j] == '?':
							row[j] = self.tbl.cols[j].mean

						if j in set(self.tbl.list_num):

							self.tbl.cols[self.tbl.headers.index(j)].addToNum(row[j])
							self.tbl.cols[self.tbl.headers.index(j)].updateMeanAndSdAdd(row[j])
							self.things[row_class].cols[self.tbl.headers.index(j)].addToNum(row[j])
							self.things[row_class].cols[self.tbl.headers.index(j)].updateMeanAndSdAdd(row[j])

						else:

							self.tbl.cols[self.tbl.headers.index(j)].addSym(row[j])
							self.things[row_class].cols[self.tbl.headers.index(j)].addSym(row[j])

				self.tbl.rows.append(Row(self.count_tbl, row_for_tbl))
				self.things[row_class].rows.append(Row(self.count_tbl, row_for_tbl))
				self.count_tbl+= 1


	def NbEnsureClassExists(self, row_class):

		if not row_class in self.things:
			self.things[row_class] = Tbl(1) 
			self.things[row_class].headers = self.tbl.headers
			self.things[row_class].xs = self.tbl.xs
			self.things[row_class].list_num = self.tbl.list_num

			local_count = 1

			for i in range(len(self.tbl.headers)):
				if self.tbl.headers[i] in self.tbl.list_num:
					self.things[row_class].cols.append(Num(local_count, self.tbl.headers[i], self.tbl.headers_text[i], 0, 0, 0))
				else:
					self.things[row_class].cols.append(Sym(local_count, self.tbl.headers[i], self.tbl.headers_text[i]))

				local_count += 1


	def NbClassify(self, row):

		most = -10 ** 64
		guess = ""
		for row_class in self.things:
			guess = row_class if guess == "" else guess
			like = self.bayesTheorem(row, len(self.things), self.things[row_class], row_class)
			if like > most:
				most = like
				guess = row_class
		return guess

	def bayesTheorem(self, row, nthings, thing, row_class):

		n1 = self.tbl.cols[len(row) - 1].cnt[row_class]

		like  = (n1  + self.k) / (self.n + self.k * nthings)
		prior = like
		like  = log(like) / log(2)

		for c in thing.xs:
			x = row[c]
			if c in thing.list_num:
				numlike = thing.cols[c].NumLike(x)
				if numlike:
					like += log(numlike) / log(2)
				else:
					like += numlike
			else:
				like += log(thing.cols[c].SymLike(x, prior, self.m)) / log(2)
		return like


