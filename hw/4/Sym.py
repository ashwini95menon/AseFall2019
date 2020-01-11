"""Sym.py"""

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

	def addSym(self, v):
		self.count += 1
		if v not in self.cnt:
			self.cnt[v] = 0
		self.cnt[v] += 1

		temp = self.cnt[v]
		if temp > self.most:
			self.most = temp
			self.mode = v

	def symEnt(self):
		e = 0.0
		for k in self.cnt:
			p = self.cnt[k] / self.count
			e -= p * log(p) / log(2)
		return e

	def SymLike(self, x, prior, m):

		f = self.cnt[x] if x in self.cnt else 0

		return (f + m * prior) / (self.count + m)
