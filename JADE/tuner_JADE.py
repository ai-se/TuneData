from __future__ import division
import random, pdb
from main import *
from base import *
import collections
# from file import *
from scipy.stats import cauchy
from scikitlearners2 import *
from start2 import *


class DeBase(object):
  def __init__(i, model):
    global The
    i.tobetuned = model.tunelst
    i.limit_max = model.tune_max
    i.limit_min = model.tune_min
    i.np = Settings.de.np
    i.u_cr = 0.5 # initial mean of normal distribution
    i.u_f = 0.5 # initial mean of cauchy distribution
    i.genF()
    i.genCr()
    # i.fa = [min(max(0,cauchy(i.u_f, 0.1).rvs()),1) for _ in
    #         xrange(i.np)]  # generate i.np fa's for each candidate from cauchy(0.5, 1) as initialization
    # i.cr = [random.gauss(i.u_cr, 0.1) for _ in
    #         xrange(i.np)]  # generate i.np cr's for each candidate from cauchy(0.5, 1) as initialization
    i.S_f = []  # list to store successful f's
    i.S_cr = []  # list to store successful cr's
    i.repeats = Settings.de.repeats
    i.life = Settings.de.life
    i.obj = The.option.tunedobjective
    # i.obj = 3  ### This is for testing
    i.evaluation = 0
    i.scores = {}
    i.frontier = [i.generate() for _ in xrange(i.np)]
    i.evaluate()
    i.bestconf, i.bestscore = i.best()

  def generate(i):
    candidates = []
    for n, item in enumerate(i.limit_min):
      if isinstance(item, float):
        candidates.append(round(random.uniform(i.limit_min[n], i.limit_max[n]), 2))
      elif isinstance(item, bool):
        candidates.append(random.random() <= 0.5)
      elif isinstance(item, list):
        pass
      elif isinstance(item, int):
        candidates.append(int(random.uniform(i.limit_min[n], i.limit_max[n])))
      else:
        raise ValueError("type of limits are wrong!")
    # pdb.set_trace()
    return i.treat(candidates)

  def evaluate(i):
    for n, arglst in enumerate(i.frontier):
      i.assign(i.tobetuned, arglst)
      i.scores[n] = i.callModel()  # main return [[pd,pf,prec,f,g],[pd,pf,prec,f,g]], which are N-defective,Y-defecitve

  def assign(i, tobetuned, tunedvalue):
    for key, val in zip(tobetuned, tunedvalue):
      exec (key + "= " + str(val))
      # tobetuned[key] = val

  def best(i):
    sortlst = []
    if i.obj == 1:  # this is for pf
      sortlst = sorted(i.scores.items(), key=lambda x: x[1][i.obj], reverse=True)  # alist of turple
    else:
      sortlst = sorted(i.scores.items(), key=lambda x: x[1][i.obj])  # alist of turple
    bestconf = i.frontier[sortlst[-1][0]]  # [(0, [100, 73, 9, 42]), (1, [75, 41, 12, 66])]
    bestscore = sortlst[-1][-1][i.obj]
    return bestconf, bestscore

  def callModel(i):
    raise NotImplementedError("callMode error")

  def treat(i):
    """
    some parameters may have constraints, for example:
    when generating a parameter list, p[4]should be greater than p[5]
    You should implement this function in subclass
    """
    return NotImplementedError("treat error")

  def trim(i, n, x):
    if isinstance(i.limit_min[n], float):
      return max(i.limit_min[n], min(round(x, 2), i.limit_max[n]))
    elif isinstance(i.limit_max[n], int):
      return max(i.limit_min[n], min(int(x), i.limit_max[n]))
    else:
      raise ValueError("wrong type here in parameters")

  def gen3(i, n, f):
    seen = [n]

    def gen1(seen):
      while 1:
        k = random.randint(0, i.np - 1)
        if k not in seen:
          seen += [k]
          break
      return i.frontier[k]

    a = gen1(seen)
    b = gen1(seen)
    c = gen1(seen)
    return a, b, c

  def update(i, index, old):
    newf = []
    a, b, c = i.gen3(index, old)
    for k in xrange(len(old)):
      if isinstance(i.limit_min[k], bool):
        newf.append(old[k] if i.cr[index] < random.random() else not old[k])
      elif isinstance(i.limit_min[k], list):
        pass
      else:
        # mutation : current to the best p (5%), since np = 10, then 10*0.05 = 0.5 , we choose the beset one
        newf.append(old[k] if i.cr[index] < random.random() else i.trim(k, (old[k] +i.fa[index]*(i.bestconf[k] - old[k]) + i.fa[index] * (b[k] - c[k]))))
    return i.treat(newf)

  def updateMean1(i, old_val, mean_val):
    c = 0.1 ## this is set by JADE author
    return (1-c) * old_val + c * mean_val

  def lehmerMean(i, SF):
    """
    this to calculate Lehmer mean of SF
    """
    if not len(SF):
      return 0
    return float(sum([f**2 for f in SF]))/sum(SF)

  def arithmeticMean(i,Scr):
    if not len(Scr):
      return 0
    return float(sum(Scr))/len(Scr)

  def updateMean(i):
    i.u_cr = i.updateMean1(i.u_cr, i.arithmeticMean(i.S_cr))
    i.u_f = i.updateMean1(i.u_f, i.lehmerMean(i.S_f))
    # i.fa = [cauchy(i.u_f, 0.1).rvs() for _ in
    #         xrange(i.np)]  # generate i.np fa's for each candidate from cauchy(0.5, 1) as initialization
    # i.cr = [random.gauss(i.u_cr, 0.1) for _ in
    #         xrange(i.np)]  # generate i.np cr's for each candidate from cauchy(0.5, 1) as initialization

  def genCr(i):
    """
    Cr in [0,1]
    """
    lst = []
    while len(lst) < i.np:
      temp = random.gauss(i.u_cr, 0.1)
      lst.append(max(0,min(1,random.gauss(i.u_cr,0.1))))
    # generate i.np cr's for each candidate from cauchy(0.5, 1) as initialization
    i.cr = lst[:]
    return

  def genF(i):
    """
    F in (0,1]
    """
    lst = []
    while len(lst) < i.np:
      temp = cauchy(i.u_f, 0.1).rvs()
      if temp >= 1:
        lst.append(1)
      elif temp <= 0:
        continue
      else:
        lst.append(temp)
    i.fa = lst[:]
    return

  def writeResults(i):
    for p in i.tobetuned:
      temp = 0
      exec ("temp =" + p)
      writefile(p + ": " + str(temp))
    writefile("evaluation: " + str(i.evaluation))

  def DE(i):
    changed = False

    def isBetter(new, old):
      return new < old if i.obj == 1 else new > old

    for k in xrange(i.repeats):
      if i.life <= 0:
        break
      nextgeneration = []
      i.S_cr = []  ## clear before each generation
      i.S_f = []  ## clear before each generation
      for index, candidate in enumerate(i.frontier):
        new = i.update(index, candidate)
        i.assign(i.tobetuned, new)
        newscore = i.callModel()
        i.evaluation += 1
        if isBetter(newscore[i.obj], i.scores[index][i.obj]):
          nextgeneration.append(new)
          i.S_cr.append(i.cr[index]) ## add cr and fa if new candidate is better
          i.S_f.append(i.fa[index])
          i.scores[index] = newscore[:]
        else:
          nextgeneration.append(candidate)
      i.frontier = nextgeneration[:]
      newbestconf, newbestscore = i.best()
      if isBetter(newbestscore, i.bestscore):
        print "newbestscore %s:" % str(newbestscore)
        print "bestconf %s :" % str(newbestconf)
        i.bestscore = newbestscore
        i.bestconf = newbestconf[:]
        changed = True
      if not changed:
        i.life -= 1
      changed = False
      i.updateMean() # update the means of gaussian distrobitopm amd caushy distribution
      i.genCr() # generate the new Cr for next generation
      i.genF()  # generate the new F for next generation
    i.assign(i.tobetuned, i.bestconf)
    i.writeResults()
    print "final bestescore %s: " + str(i.bestscore)
    print "final bestconf %s: " + str(i.bestconf)
    print "DONE !!!!"


class WhereDE(DeBase):
  def __init__(i, model):
    super(WhereDE, i).__init__(model)

  def treat(i, lst):
    """
    The.where.depthmin < depthMax
    """

    def ig(l): return int(random.uniform(i.limit_min[l], i.limit_max[l]))

    if lst[-1] and lst[4] <= lst[5]:
      lst[4] = ig(4)
      lst[5] = ig(5)
      lst = i.treat(lst)
    return lst

  def callModel(i):
    return main()[-1]


class CartDE(DeBase):
  def __init__(i, model):
    super(CartDE, i).__init__(model)

  def treat(i, lst):
    return lst

  def callModel(i):
    return cart()[-1]


class RfDE(DeBase):
  def __init__(i, model):
    super(RfDE, i).__init__(model)

  def treat(i, lst):
    return lst

  def callModel(i):
    return rf()[-1]


if __name__ == "__main__":
  The.data.train = "./data/ant/ant-1.3.csv"
  The.data.tune = "./data/ant/ant-1.4.csv"
  The.data.predict = "./data/ant/ant-1.5.csv"
  CART('./data/ant/ant-1.3.csv','./data/ant/ant-1.4.csv','./data/ant/ant-1.5.csv').optimizer()
