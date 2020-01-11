""" Num.py """

import sys
import random
from Col import Col 

class Num(Col):

	def __init__(self, oid, pos, txt, mean, sd, m2):
		self.oid = oid
		self.pos = pos
		self.txt = txt
		self.lo = 10 ** 32
		self.hi = -1 * self.lo
		self.mean = mean
		self.sd = sd
		self.m2 = m2
		self.count = 0
		self.numList = []

	def addToNum(self, num):
		self.lo = self.lo if self.lo < num else num
		self.hi = self.hi if self.hi > num else num
		self.numList.append(num)

	def removeFromNum(self):
		oldVal = self.numList[-1]
		del self.numList[-1]
		return oldVal

	def updateMeanAndSdAdd(self, newVal):

		self.count += 1
		delta = newVal - self.mean
		self.mean += delta / self.count
		delta2 = newVal - self.mean
		self.m2 += delta * delta2

		if self.m2 <= 0:
			self.sd = 0
		elif self.count < 2:
			self.sd = 0
		else:
			self.sd = (self.m2/(self.count - 1)) ** 0.5

	def updateMeanAndSdRemove(self, oldVal):

		if self.count < 2:
			self.sd = 0
			return

		self.count -= 1

		delta = oldVal - self.mean
		self.mean -= delta / self.count
		self.m2 -= delta * (oldVal - self.mean)

		if self.m2 < 0 or self.count < 2:
			self.sd = 0
		else:
			self.sd = (self.m2/self.count - 1) ** 0.5

	def NumLike(self, x):

		var = self.sd ** 2
		denom = (3.14159 * 2 * var) ** 0.5
		first_num = x - self.mean
		total = first_num / (self.sd + 0.01)
		squared = total ** 2
		squared = - squared / 2
		num = 2.71828 ** squared
		return num/(denom + 10 ** -64)



