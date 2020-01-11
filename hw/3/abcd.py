"""abcd.py"""

class Abcd():

	def __init__(self, rx, data):
		self.known = {}
		self.a = {}
		self.b = {}
		self.c = {}
		self.d = {}
		self.rx = "rx" if rx == "" else rx
		self.data = "data" if data == "" else data
		self.yes = 0
		self.no = 0
		self.count = 0

	def abcd1(self, want, got):
		self.count += 1
		if not want in self.known:
			self.known[want] = 1
			self.a[want] = self.yes + self.no
		else:
			self.known[want] += 1

		if not got in self.known:
			self.known[got] = 1
			self.a[got] = self.yes + self.no
		else:
			self.known[got] += 1

		if want == got:
			self.yes +=	1
		else:
			self.no += 1

		for i in self.known:
			if i == want:
				if want == got:
					if i in self.d:
						self.d[i] += 1
					else: 
						self.d[i] = 1
				else:
					if i in self.b:
						self.b[i] += 1
					else:
						self.b[i] = 1
			else:
				if i == got:
					if i in self.c:
						self.c[i] += 1
					else:
						self.c[i] = 1
				else:
					if i in self.a:
						self.a[i] += 1
					else:
						self.a[i] = 1

	def abcdReport(self):

		q = "%4s"
		p = " %.2f"
		r = "%5s"
		s = " |"
		ds = "----"

		print(r % "db", s, r % "rx", s, r % "num", s, r % "a", s, r % "b", s, r % "c", s, r % "d", s, q % "acc", s, q % "pre", s, q % "pd", s, q % "pf", s, q % "f", s, q % "g", s, q % "class")
		print(r % ds, s, r % ds, s, r % ds, s, r % ds, s, r % ds, s, r % ds, s, r % ds, s, q % ds, s, q % ds, s, q % ds, s, q % ds, s, q % ds, s, q % ds, s, q % ds, s, q % ds)

		for x in self.known:
			# print("cc", x)
			pd = pf = pn = prec = g = f = acc = 0

			a = self.a[x] if x in self.a else 0
			b = self.b[x] if x in self.b else 0
			c = self.c[x] if x in self.c else 0
			d = self.d[x] if x in self.d else 0

			if b + d > 0:
				pd = d / (b + d)

			if a + c > 0:
				pf = c / (a + c)
				pn = (b + d) / (a + c)

			if c + d > 0:
				prec = d / (c + d)

			if 1 - pf + pd > 0:
				g = 2 * (1 - pf) * pd / (1 - pf + pd) 

			if prec + pd > 0:
  				f = 2 * prec * pd / (prec + pd) 

			if self.yes + self.no > 0:
				acc  = self.yes / (self.yes + self.no) 

			print(r % self.data, s, r % self.rx, s, r % self.count, s, r % a, s, r % b, s, r % c, s, r % d, s, p % acc, s, p % prec, s, p % pd, s, p % pf, s, p % f, s, p % g, s, q % x)


abcd = Abcd("rx", "data")

for i in range(6):
	abcd.abcd1("yes", "yes")

for i in range(2):
	abcd.abcd1("no", "no")

for i in range(5):
	abcd.abcd1("maybe", "maybe")

abcd.abcd1("maybe", "no")

abcd.abcdReport()





