from __future__ import division, print_function
import sys
#__author__ = 'WeiFu'


"""
Anonymous containers, credits go to Dr. Menzies
"""
class o :
  def __init__(self, **d):
    self.has().update(**d)
  def has(self):
    return self.__dict__
  def update(self,**d):
    self.has().update(d)
    return self
  def __repr__(self):
    show = [ '%s :%s' %(k, self.has()[k])for k in sorted(self.has().keys()) if k[0] is not '_']
    txt = ' '.join(show)
    if len(txt) > 60:
      show = map(lambda x: '\t' +x + '\n', show)
    return '{' + ' '.join(show) + '}'


"""

Decorator to run code at load time, credits go to Dr.Menzies

"""
def run(f):
  print ('\n# ---|', f.__name__, '|------')
  if f.__doc__:
    print ("'''", f.__doc__,"\n'''")

  f()



"""

test case

"""

@run
def test_o():
  '''
  asdf  sdf   lskdk
  hello world
  '''
  tests = o(data = "sbse", x= [1,3,3,4], y = ["hello~~~~~~~~~~~~~","icse"])
  print(tests)

if __name__ == '__main__':
  pass



