""" Num.py """

import sys
import random
from Col import Col 

class Num(Col):

	def __init__(self, mean, sd, m2):
		self.mean = mean
		self.sd = sd
		self.m2 = m2
		self.count = 0
		self.numList = []

	def addToNum(self, num):
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

		if self.m2 < 0 or self.count < 2:
			self.sd = 0
		else:
			self.sd = (self.m2/self.count - 1) ** 0.5

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

def main():

	output = ""

	n = Num(0, 0, 0)

	meanCache = []
	sdCache = []

	for x in range(100):
		newVal = random.randint(1,1000)
		n.addToNum(newVal)
		n.updateMeanAndSdAdd(newVal)
		if x % 10 == 9:
			meanCache.append(n.mean)
			sdCache.append(n.sd)

	i = 9

	meanCache1 = []
	sdCache1 = []

	for x in range(100, 0, -1):
		# print(x)
		if x % 10 == 0:

			meanCache1.append(n.mean)
			sdCache1.append(n.sd)

			if round(meanCache[i]) == round(n.mean) and round(sdCache[i]) == round(n.sd):
				output = output + "For i = " + str(x) + "\nCached mean = " + str(meanCache[i]) + " and new mean = " + str(n.mean) + "\n" 
				output = output + "Cached sd = " + str(sdCache[i]) + " and new sd = " + str(n.sd) + "\n"
				i -= 1

		oldVal = n.removeFromNum()
		n.updateMeanAndSdRemove(oldVal)

	file = open("output.txt", "w+")
	file.write(output)

main()

