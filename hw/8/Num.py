import sys
import random
from Col import Col 
from   lib   import THE,Pretty,same,first,last,ordered

class Num(Col):

    def __init__(self, oid, pos, txt, mean, sd, m2, weight=1):
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
        self.weight = weight

    def addToNum(self, num):
        self.lo = self.lo if self.lo < num else num
        self.hi = self.hi if self.hi > num else num
        self.numList.append(num)
        self.updateMeanAndSdAdd(num)

    def removeLastNum(self):
        oldVal = self.numList[-1]
        del self.numList[-1]
        self.updateMeanAndSdRemove(oldVal)

    def removeFirstNum(self):
        oldVal = self.numList[0]
        del self.numList[0]
        self.updateMeanAndSdRemove(oldVal)

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
            self.sd = (self.m2/(self.count - 1)) ** 0.5

    def NumLike(self, x):

        var = self.sd ** 2
        denom = (3.14159 * 2 * var) ** 0.5
        first_num = x - self.mean
        total = first_num / (self.sd + 0.01)
        squared = total ** 2
        squared = - squared / 2
        num = 2.71828 ** squared
        return num/(denom + 10 ** -64)

    def variety(self):
        return self.sd

    def xpect(self, other):
        n = self.count + other.count + 0.0001
        return self.count/n * self.sd + other.count/n * other.sd;

    def dist(self, val1, val2):
        "Calculate distance between 2 rows"
        norm = lambda z: (z - self.lo) / (self.hi - self.lo + 10 ** -32)
        if val1 == THE.char.skip:
            if val2 == THE.char.skip: return 1
            val2 = norm(val2)
            val1 = 0 if val2 > 0.5 else 1
        else:
            val1 = norm(val1)
            if val2 == THE.char.skip:
                val2 = 0 if val1 > 0.5 else 1
            else:
                val2 = norm(val2)
        return abs(val1 - val2)

    def norm(self, value):

        return (value - self.lo ) / (self.hi - self.lo + 0.00001)

