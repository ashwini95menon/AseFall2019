from abc import ABC, abstractmethod

class Col():

	def __init__(self, oid, pos, txt):
		self.oid = oid
		self.pos = pos
		self.txt = txt

	@abstractmethod
	def updateMean():
		pass

	@abstractmethod
	def updateSd():
		pass

	@abstractmethod
	def addToNum():
		pass

	@abstractmethod
	def removeFromNum():
		pass