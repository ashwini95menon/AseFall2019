from abc import ABC, abstractmethod

class Col():

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