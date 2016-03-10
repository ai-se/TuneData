__author__ = 'WeiFu'
import pdb
import sys, os
# sys.path.append("/Users/WeiFu/Github/Research/version1.0")

def test_arithmeticMean():
  os.chdir('../')
  import  settings
  import tuner_JADE
  import start2
  global  The
  The.data.train = "./data/ant/ant-1.3.csv"
  The.data.tune = "./data/ant/ant-1.4.csv"
  The.data.predict = "./data/ant/ant-1.5.csv"
  model = start2.CART('./data/ant/ant-1.3.csv', './data/ant/ant-1.4.csv', './data/ant/ant-1.5.csv')
  DE_tester = tuner_JADE.CartDE(model)
  assert tuner_JADE.arithmeticMean([1, 1, 1, 1, 1]) == 1
