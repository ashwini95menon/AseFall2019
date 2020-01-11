"""Sym.py"""

import operator

from Col import Col 
from math import log

class Sym(Col):

	def __init__(self, oid, pos, txt):
		self.oid = oid
		self.pos = pos
		self.txt = txt
		self.mode = ""
		self.most = 0
		self.cnt = {}
		self.count = 0
		self.symList = []

	def addSym(self, v):
		self.count += 1
		self.symList.append(v)
		if v not in self.cnt:
			self.cnt[v] = 0
		self.cnt[v] += 1

		temp = self.cnt[v]
		if temp > self.most:
			self.most = temp
			self.mode = v

	def removeSym(self, v):
		self.count -= 1
		self.cnt[v] -= 1
		if self.cnt[v] == 0:
			del self.cnt[v]
		if self.cnt:
			self.mode = max(self.cnt.items(), key=operator.itemgetter(1))[0]
			self.most = self.cnt[self.mode]
			self.symList.remove(v)
 
	def symEnt(self):
		e = 0.0
		for k in self.cnt:
			p = self.cnt[k] / self.count
			e -= p * log(p, 2)
		return e

	def SymLike(self, x, prior, m):

		f = self.cnt[x] if x in self.cnt else 0

		return (f + m * prior) / (self.count + m)

	def variety(self):
		return self.symEnt()

	def xpect(self, other):
		n = self.count + other.count;
		return self.count / n * self.variety() + other.count / n * other.variety();
