"""
Divide numbers.
"""

import math
from   lib   import THE,Pretty,same,first,last,ordered
from   copy  import deepcopy as kopy
from Num import Num
from Sym import Sym

class Div2(Pretty):
  """
  Recursively divide a list of numns by finding splits
  that minimizing the expected value of the standard
  deviation (after the splits).
  """

  def makeList(i, data, yis):
    data = sorted(data,key=lambda x: (x[0]))
    x_lst = Num(1, 1, "x", 0, 0, 0)
    if yis == "Num":
      y_lst = Num(2, 2, "y", 0, 0, 0)
    else:
      y_lst = Sym(2, 2, "y")
    for i in data:
      x_lst.addToNum(i[0])
      if yis == "Num":
        y_lst.addToNum(i[1])
      else:
        y_lst.addSym(i[1])

    return x_lst, y_lst

  def printSplits(i):
    if i.yis == "Num":
      print("\nOutput for part 1:")
      for k in range(len(i.xranges)):
        numx = i.xranges[k]
        numy = i.yranges[k]
        print(str(k+1) + " x.n\t" + str(numx.count) + " | x.lo " + str(round(numx.lo,4)) + " | x.hi " + str(round(numx.hi,4)) + " | y.lo " + str(round(numy.lo,4)) + " | y.hi " + str(round(numy.hi,4)))
    else:
      print("\nOutput for part 2:")
      for k in range(len(i.xranges)):
        numx = i.xranges[k]
        numy = i.yranges[k]
        print(str(k+1) + " x.n\t" + str(numx.count) + " | x.lo " + str(round(numx.lo,4)) + " | x.hi " + str(round(numx.hi,4)) + " | y.mode " + str(numy.mode) + " | y.ent " + str(round(numy.variety(),4)))


  def __init__(i,lst, x = "first", y = "last", yis="Num"):
    i.yis    = yis
    i.x_lst, i.y_lst = i.makeList(lst, yis)
    i.b4     = i.y_lst
    i._lst   = sorted(lst,key=lambda x: (x[0]))
    i.gain   = 0                             # where we will be, once done
    i.step   = int(i.y_lst.count**THE.div.min) # each split need >= 'step' items
    i.stop   = last(i.x_lst.numList)          # top list value
    i.start  = first(i.x_lst.numList)         # bottom list value
    i.xranges = []                            # the generted ranges
    i.yranges = []
    i.epsilon= i.y_lst.variety() * THE.div.cohen     # bins must be seperated >= epsilon
    i.__divide(1, len(i._lst), i.x_lst, i.y_lst, 1)
    i.gain   /= len(i._lst)
    i.printSplits()

  def __divide(i, lo, hi, xr, yr, rank):
    "Find a split between lo and hi, then recurse on each split."
    b4       = kopy(xr)
    y_old = kopy(yr)
    xl        = Num(1, 1, "x", 0, 0, 0)
    if i.yis == "Num":
      yl = Num(2, 2, "y", 0, 0, 0)
    else:
      yl = Sym(2, 2, "y")

    i.epsilon = b4.variety() * THE.div.cohen
    best      = yr.variety()
    cut       = None

    i.stop  = last(b4.numList)              
    i.start = first(b4.numList) 

    for j in range(lo,hi):

      xl.addToNum(i._lst[j][0])
      xr.removeFirstNum()
      if i.yis == "Num":
        yl.addToNum(i._lst[j][1])
        yr.removeFirstNum()
      else:
        yl.addSym(i._lst[j][1])
        yr.removeSym(i._lst[j][1])
    
      if xl.count >= i.step:
        if xr.count >= i.step:
          now   = i._lst[j-1][0]
          after = i._lst[j][0] 
          if now == after: continue
          if abs(xr.mean - xl.mean) >= i.epsilon:
            if after - i.start >= i.epsilon:
              if i.stop - now >= i.epsilon: 
                xpect = yl.xpect(yr)
                if xpect*THE.div.trivial < best:
                  best, cut = xpect, j

    if cut:
      ls, rs = i._lst[lo:cut], i._lst[cut:hi] 
      xl_newr , yl_newr = i.makeList(ls, i.yis)
      xr_newr , yr_newr = i.makeList(rs, i.yis)
      rank   = i.__divide(lo, cut, xl_newr , yl_newr, rank) + 1
      rank   = i.__divide(cut ,hi, xr_newr , yr_newr, rank)
    else:
      i.gain   += b4.count * b4.variety()
      i.xranges += [ b4 ]
      i.yranges += [ y_old ]

    return rank