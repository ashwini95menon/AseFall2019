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

    def same(self,j, conf=0.95, small=0.38):
        return self.tTestSame(j,conf) or self.hedges(j, small)
    def tTestSame(self,j,conf=0.95):
        nom   = abs(self.mean - j.mean)
        s1,s2 = self.variety(), j.variety()
        denom = ((s1/self.count + s2/j.count)**0.5) if s1+s2 else 1
        df    = min(self.count - 1, j.count - 1)
        return  criticalValue(df, conf) >= nom/denom

# The above needs a magic threshold )(on the last line) for sayng enough is enough

    def criticalValue(df,conf=0.95,
      xs= [             1,    2,     5,    10,    15,    20,    25,   30,     60,  100],
      ys= {0.9:  [ 3.078, 1.886, 1.476, 1.372, 1.341, 1.325, 1.316, 1.31,  1.296, 1.29],
           0.95: [ 6.314, 2.92,  2.015, 1.812, 1.753, 1.725, 1.708, 1.697, 1.671, 1.66],
           0.99: [31.821, 6.965, 3.365, 2.764, 2.602, 2.528, 2.485, 2.457, 2.39,  2.364]}):
      return interpolate(df, xs, ys[conf])

    def interpolate(x,xs,ys):
      if x <= xs[0] : return ys[0]
      if x >= xs[-1]: return ys[-1]
      x0, y0 = xs[0], ys[0]
      for x1,y1 in zip(xs,ys):
        if x < x0 or x > xs[-1] or x0 <= x < x1:
          break
        x0, y0 = x1, y1
      gap = (x - x0)/(x1 - x0)
      return y0 + gap*(y1 - y0)



    def hedges(self,j,small=0.38):

        num   = (self.count - 1)*self.variety()**2 + (j.count - 1)*j.variety()**2
        denom = (self.count- 1) + (self.count - 1)
        sp    = ( num / denom )**0.5
        delta = abs(self.mean - j.mean) / sp
        c     = 1 - 3.0 / (4*(self.count + j.count - 2) - 1)
        return delta * c < small