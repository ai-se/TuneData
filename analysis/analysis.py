from __future__ import division, print_function
# __author__ = 'WeiFu'
from read import Read as result
import pdb
from plots import *


class Compare(object):
  '''
  this class is to compare the improvement of the new method
  over the old one.
  '''

  def __init__(self, old_path, new_path):
    self.improve = {}
    self.old_path = old_path
    self.new_path = new_path

  def calculate(self, learner):
    '''
    calculate the improvements for one learner
    '''
    res = []
    oldresult = result(self.old_path).read()
    newresult = result(self.new_path).read()
    for old, new in zip(oldresult[learner], newresult[learner]):
      try:
        res.append(new - old)
      except:
        continue
    return res

  def tell(self):
    '''
    tell improvements of three learners
    '''
    for learner in ['Naive_Where', 'Naive_CART', 'Naive_RF']:
      self.improve[learner] = self.calculate(learner)
    # pdb.set_trace()
    # print(self.improve)
    return self.improve
  def tell_neg(self,data, goal):

    print("="*10,goal,"="*10)
    for key, val in data.iteritems():
      first, second, third = int(len(val)*0.25), int(len(val)*0.5), int(len(val)*0.75)
      sorted_data = sorted(val)
      count = 0
      for i in xrange(len(sorted_data)):
        if sorted_data[i] <=0:
          count +=1
      print(key +' IQR:', str(sorted_data[first]),',', str(sorted_data[second]),',',str(sorted_data[third]))
      print(' '*len(key) + ' num<0:',count)

  def csv(self,name):
    naive_learner = ['Naive_Where', 'Naive_CART', 'Naive_RF']
    tuned_learner = ['Tuned_Where', 'Tuned_CART', 'Tuned_RF']

    oldresult = result(self.old_path).read()
    newresult = result(self.new_path).read()
    res = "Name," +",".join(newresult["Dataset"])+'\n'
    for j, aresult in enumerate([oldresult,newresult]):
      for one in naive_learner:
        if j == 0:
          res += "Old_"+str(one) +"," + ",".join([str(i) for i in aresult[one]]) + '\n'
        else:
          res += "New_"+str(one) +"," + ",".join([str(i) for i in aresult[one]]) + '\n'
    f = open("RX4_"+name+'.csv',"w")
    f.write(res)


  def csv_rx4(self,name):
    naive_learner = ['Naive_Where', 'Naive_CART', 'Naive_RF']
    tuned_learner = ['Tuned_Where', 'Tuned_CART', 'Tuned_RF']

    # oldresult = result(self.old_path).read()
    newresult = result(self.new_path).read()
    res = "Name," +",".join(newresult["Dataset"])+'\n'
    for j, aresult in enumerate([newresult]):
      for naive, tuned in zip(naive_learner,tuned_learner):
          res += "RX4_"+str(naive) +"," + ",".join([str(i) for i in aresult[naive]]) + '\n'
          res += "RX4_"+str(tuned) +"," + ",".join([str(i) for i in aresult[tuned]]) + '\n'
    f = open("RX4_"+name+'.csv',"w")
    f.write(res)





    #
    # out = ""
    # for key, val in data.iteritems():
    #   out += key + "," +",".join([str(i) for i in val]) + "\n"
    # print (goal, out)




if __name__ == "__main__":
  # prec_oldsrc = '../result/0906/np=10_f_precision/myresult2015-09-06 18:44:48prec'
  # prec_newsrc = '../result/1028/myresult2015-10-28 03:50:19prec'
  # f_oldsrc = "../result/0906/np=10_f_precision/myresult2015-09-06 21:56:38f"
  # f_newsrc ="../result/1028/myresult2015-10-28 05:32:42f"


  # ######### new and old baseline experiment RX2 and RX3
  # prec_oldsrc = "../result/0906/np=10_f_precision/myresult2015-09-06 18:44:48prec"
  # prec_newsrc = "../result/1101/myresult2015-11-01 10:22:15prec"
  # f_oldsrc = "../result/0906/np=10_f_precision/myresult2015-09-06 21:56:38f"
  # f_newsrc = "../result/1101/myresult2015-11-01 10:31:37f"

  ####### RX4 results
  prec_newsrc = "../result/1103TuningAsTraining/myresult2015-11-03 09:22:16prec"
  f_newsrc = "../result/1103TuningAsTraining/myresult2015-11-03 20:24:47f"
  prec_oldsrc = prec_newsrc
  f_oldsrc = f_newsrc
  PREC = Compare(prec_oldsrc, prec_newsrc)
  F = Compare(f_oldsrc, f_newsrc)

  ###### plots ######
  # PREC.tell_neg(PREC.tell(),"PREC")
  # F.tell_neg(F.tell(),"F")
  # show([PREC.tell(),F.tell()],['PREC Improvements','F Improvements'])

  #  generate csv file of results
  PREC.csv_rx4("PREC")
  F.csv_rx4("F")




