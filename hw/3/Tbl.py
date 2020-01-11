"""Tbl.py"""

import re

class Tbl():

	def __init__(self, oid):
		self.oid = oid
		self.rows = []
		self.cols = []
		self.syms = []

	def read(self, file):
		return self.__fromString(file)


	def __compiler(self, x):
		"return something that can compile strings of type x"
		try: 
			if x == '?':
				return str(x)
			int(x); 
			return  int(x)
		except:
			try: float(x); return  float(x)
			except ValueError: 
				return str(x)

	def __string(self, s):
		"read lines from a string"
		for line in s.splitlines(): 
			yield line

	def __rows(self, src, sep = ",", doomed = r'([\n\t\r ]|#.*)'):
		"convert lines into lists, killing whitespace and comments"
		for line in src:
			line = line.strip()
			line = re.sub(doomed, '', line)
			if line:
				yield line.split(sep)

	def __cells(self, src):
		"convert strings into their right types"
		drop_col = []
		length = 0
		for n,cells in enumerate(src):
			# print(n, cells)
			if n == 0:
				# for col in range(len(cells)):
				# 	if cells[col][0] == "?":
				# 		drop_col.append(col)
				# for i in drop_col:
				# 	del cells[i]
				length = len(cells)
				yield cells
			else:
				rows = [self.__compiler(cell) for cell in cells]
				for i in drop_col:
					del rows[i]
				if len(rows) < length:
					yield "Skippimg line " + str((n + 1))
				else:
					yield rows 

	def __fromString(self, s):
		"putting it all together"
		for lst in self.__cells(self.__rows(self.__string(s))):
			yield lst

