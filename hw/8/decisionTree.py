"""dt.py"""

from math import log

from Col import Col 
from Num import Num
from Tbl import Tbl
from Row import Row
from Sym import Sym
from div import Div2
from   lib   import THE,Pretty,same,first,last,ordered
from   copy  import deepcopy as kopy
from boot import *

class decisionTree():

	def __init__(self):

		self.tbls = {}
		self.things = {}
		self.m = 2
		self.k = 1
		self.n = -1
		self.classes = []
		self.count_tbl = 2
		self.tbl = Tbl(1)

	def makeList(i, data, yis):
		c = data.cols[-1]
		if yis == "Num":
			data = c.numList
			y_lst = Num(2, c.pos, c.txt, 0, 0, 0)
		else:
			data = c.symList
			y_lst = Sym(2, c.pos, c.txt)
		for i in data:
			if yis == "Num":
				y_lst.addToNum(i[1])
			else:
				y_lst.addSym(i[1])

		return y_lst

	def split(i, lst, l, cut, col, yis):

		if l != 0:
			splits = []

			splits.append([])
			splits.append([])
			splits.append([])

			tbl1 = Tbl(1)
			tbl3 = Tbl(3)
			tbl2 = Tbl(2)

			tbl1.rows = kopy(lst.rows[0:l])
			tbl3.rows = kopy(lst.rows[l:cut])
			tbl2.rows = kopy(lst.rows[cut:])

			for c in lst.cols:
				if isinstance(c, Num):
					col1 = Num(1, c.pos, c.txt, 0, 0, 0)
					col2 = Num(1, c.pos, c.txt, 0, 0, 0)
					col3 = Num(1, c.pos, c.txt, 0, 0, 0)

					for i in range(len(c.numList)):
						if i < l:
							col1.addToNum(c.numList[i])
						elif i < cut:
							col2.addToNum(c.numList[i])
						else:
							col3.addToNum(c.numList[i])

					if c.txt == col:

						splits[0].append(col1.lo)
						splits[0].append(col1.hi)
						splits[1].append(col2.lo)
						splits[1].append(col2.hi)
						splits[2].append(col3.lo)
						splits[2].append(col3.hi)

				elif isinstance(c, Sym):
					col1 = Sym(2, c.pos, c.txt)
					col2 = Sym(2, c.pos, c.txt)
					col3 = Sym(2, c.pos, c.txt)

					for i in range(len(c.symList)):
						if i < l:
							col1.addSym(c.symList[i])
						elif i < cut:
							col2.addSym(c.symList[i])
						else:
							col3.addSym(c.symList[i])


				tbl1.cols.append(col1)
				tbl2.cols.append(col2)
				tbl3.cols.append(col3)

			splits[0].append(tbl1)
			splits[1].append(tbl2)
			splits[2].append(tbl3)

			if yis == "Sym":
				splits[0].append(tbl1.cols[-1].mode)
				splits[1].append(tbl2.cols[-1].mode)
				splits[2].append(tbl3.cols[-1].mode)
			else:

				splits[0].append(tbl1.cols[-1].mean)
				splits[1].append(tbl2.cols[-1].mean)
				splits[2].append(tbl3.cols[-1].mean)

		else:

			splits = []

			splits.append([])
			splits.append([])

			tbl1 = Tbl(1)
			tbl2 = Tbl(2)

			tbl1.rows = kopy(lst.rows[l:cut])
			tbl2.rows = kopy(lst.rows[cut:])

			for c in lst.cols:
				if isinstance(c, Num):
					col1 = Num(1, c.pos, c.txt, 0, 0, 0)
					col2 = Num(1, c.pos, c.txt, 0, 0, 0)
					for i in range(len(c.numList)):
						if i < cut:
							col1.addToNum(c.numList[i])
						else:
							col2.addToNum(c.numList[i])

					if c.txt == col:


						splits[0].append(col1.lo)
						splits[0].append(col1.hi)
						splits[1].append(col2.lo)
						splits[1].append(col2.hi)

				elif isinstance(c, Sym):
					col1 = Sym(2, c.pos, c.txt)
					col2 = Sym(2, c.pos, c.txt)

					for i in range(len(c.symList)):
						if i < cut:
							col1.addSym(c.symList[i])
						else:
							col2.addSym(c.symList[i])


				tbl1.cols.append(col1)
				tbl2.cols.append(col2)

			splits[0].append(tbl1)
			splits[1].append(tbl2)

			if yis == "Sym":
				splits[0].append(tbl1.cols[-1].mode)
				splits[1].append(tbl2.cols[-1].mode)
			else:

				splits[0].append(tbl1.cols[-1].mean)
				splits[1].append(tbl2.cols[-1].mean)

		return splits

	def showt(i, tree,pre= '',rnd=THE.tree.rnd):
		most = sorted(x.n for x in tree)[-1]
		for x  in tree:
			after =""
			s = x.txt + ' = ' + str(x.lo)
			if x.n == most:
				after,most = "*", None
			if x.lo != x.hi:
				s += ' .. ' + str(x.hi)
			if not x.kids and x.n != 0:
				print(pre + s,after,
				":", x.middle,
				'('+str(x.n) +')')
			else:
				if x.kids:
					print(pre + s,after)
					i.showt(x.kids,pre + '|   ')

	def tree(i, lst, y, yis, lvl=0):


		if len(lst.rows) >= THE.tree.minObs*2:
			lo, cut, col = 10**32, None, None
			for col1 in (lst.cols[0:-1]):
				x = lst.cols.index(col1)
				# x = lambda row: row.cells[col1.pos]
				d = Div2(lst, x=x, y=y, yis=yis)
				cut1, lo1 = d.cut, d.best
				if cut1:
					if lo1 < lo:
						l, cut, lo, col = d.l, cut1, lo1, col1
				

			if cut:
				if cut != l:
					return [o(lo   = lo,
						hi   = hi,
						n    = len(kids.rows),
						txt  = col.txt,
						kids = i.tree(kids,y,yis,lvl+1),
						middle = middle
						) for lo,hi,kids, middle in i.split(lst, l-1, cut-1, col.txt, yis)]

					return i.makeList(lst, yis)
		else:

			return None


	