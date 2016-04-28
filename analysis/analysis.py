from __future__ import division, print_function
# __author__ = 'WeiFu'
from read import Read as result
import pdb
from plots import *
from combine_HPC import *

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

  def tell_neg(self, data, goal):

    print("=" * 10, goal, "=" * 10)
    for key, val in data.iteritems():
      first, second, third = int(len(val) * 0.25), int(len(val) * 0.5), int(len(val) * 0.75)
      sorted_data = sorted(val)
      count = 0
      for i in xrange(len(sorted_data)):
        if sorted_data[i] <= 0:
          count += 1
      print(key + ' IQR:', str(sorted_data[first]), ',', str(sorted_data[second]), ',', str(sorted_data[third]))
      print(' ' * len(key) + ' num<0:', count)

  def csv(self, name):
    naive_learner = ['Naive_Where', 'Naive_CART', 'Naive_RF']
    tuned_learner = ['Tuned_Where', 'Tuned_CART', 'Tuned_RF']

    oldresult = result(self.old_path).read()
    newresult = result(self.new_path).read()
    res = "Name," + ",".join(newresult["Dataset"]) + '\n'
    for j, aresult in enumerate([oldresult, newresult]):
      for one in naive_learner:
        if j == 0:
          res += "Old_" + str(one) + "," + ",".join([str(i) for i in aresult[one]]) + '\n'
        else:
          res += "New_" + str(one) + "," + ",".join([str(i) for i in aresult[one]]) + '\n'
    f = open("RX4_" + name + '.csv', "w")
    f.write(res)

  def csv_rx4(self, name):
    naive_learner = ['Naive_Where', 'Naive_CART', 'Naive_RF']
    tuned_learner = ['Tuned_Where', 'Tuned_CART', 'Tuned_RF']

    # oldresult = result(self.old_path).read()
    newresult = result(self.new_path).read()
    res = "Name," + ",".join(newresult["Dataset"]) + '\n'
    for j, aresult in enumerate([newresult]):
      for naive, tuned in zip(naive_learner, tuned_learner):
        res += "RX4_" + str(naive) + "," + ",".join([str(i) for i in aresult[naive]]) + '\n'
        res += "RX4_" + str(tuned) + "," + ",".join([str(i) for i in aresult[tuned]]) + '\n'
    f = open("RX4_" + name + '.csv', "w")
    f.write(res)


def tune_over_naive(path):
  '''
  :param path: the path of experiment results, e.g: "allf"
  :return: a list of results for each learner with respect to Naive, Tuned, Grid.
  '''
  result_dict = result(path).read()
  # pdb.set_trace()
  out = []
  # if "f" in path:
  #   result_dict["Grid_CART"] = [0,52,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  #   result_dict["Grid_RF"] = [0,0,11,33,0,46,18,36,0,0,0,0,0,0,56,0,0]
  # else:
  #   result_dict["Grid_CART"] = [85,85,19,93,0,0,100,0,67,60,0,60,0,0,66,0,0]
  #   result_dict["Grid_RF"] = [59,40,0,0,0,0,0,0,46,0,100,100,100,75,0,0,25]
  # for learner in ["CART", "RF"]:
  for learner in ["CART","RF"]:
    res = {}
    naive = None
    for task in ["Naive_", "Tuned_", "Grid_"]:
      name = task + learner
      if task == "Naive_":
        naive = name
      res[name] = np.array(result_dict[name])
    sorted_index = np.argsort(res[naive])
    res_sorted = {}
    for key, val in res.iteritems():
      res_sorted[key] = val[sorted_index]
    # print(str(res))
    out.append(res_sorted)
  return out


def show_plots(data_lst, goal_lst=["F", "F"]):
  '''
  :param data_lst: lists of dictionary type of resuts to be ploted.
  :param goal_lst: lists of ylabel associalted with each dictionary data
  :return: None
  '''
  for kk in xrange(len(data_lst)):
    data_dict = data_lst[kk]
    goal = goal_lst[kk]
    plt.subplot(2, 1, kk + 1)
    color = {'Grid': 'r', 'Naive': 'g', 'Tuned': 'b'}
    find_y_max = 0
    for order in ['Naive', 'Grid', 'Tuned']:
      key = [i for i in data_dict.keys() if order in i][0]
      val = data_dict[key]
      this_label = key
      if order == "Naive":
        this_label =key.replace(order,"Untuned")
      if order == "Tuned":
        this_label = key.replace(order, "DE")
      x_aix = np.linspace(1, 17, 17)
      # pdb.set_trace()
      find_y_max = max(find_y_max,max(val))
      if order =="Grid": ### only plot siginificant better GridSearch
        plt.plot(x_aix, val, 'yo', color=color[key[:key.index("_")]], label=this_label)
      else:
        plt.plot(x_aix, val, 'yo-', color=color[key[:key.index("_")]], label=this_label)
      plt.legend(fontsize='xx-small', loc=4)
    if kk == 0:
      # plt.title("Tuning Goal is "+goal_lst[0], y=1.1)
      pass
    plt.ylabel(goal.upper(),fontsize="x-small",position=(2,0.5))
    plt.ylim((0,find_y_max+3))
    plt.xlim(1,17)
  plt.xlabel("Data sets, sorted by results using default tunings.", fontsize="small")
  plt.gcf().set_size_inches(w=4, h=4, forward=True)
  plt.savefig(goal_lst[0]+'.png', pad_inches=0)
  plt.tight_layout()
  plt.show()


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
  # prec_newsrc = "../result/1103TuningAsTraining/myresult2015-11-03 09:22:16prec"
  # f_newsrc = "../result/1103TuningAsTraining/myresult2015-11-03 20:24:47f"
  # prec_oldsrc = prec_newsrc
  # f_oldsrc = f_newsrc
  # PREC = Compare(prec_oldsrc, prec_newsrc)
  # F = Compare(f_oldsrc, f_newsrc)

  ###### plots ######
  # PREC.tell_neg(PREC.tell(),"PREC")
  # F.tell_neg(F.tell(),"F")
  # show([PREC.tell(),F.tell()],['PREC Improvements','F Improvements'])

  #  generate csv file of results
  # PREC.csv_rx4("PREC")
  # F.csv_rx4("F")

  ################## plot Naive, Grid, Tuned plots over different data sets ##################
  goal_results_dict = combine("../result/20160321")
  for goal, src in goal_results_dict.iteritems():
    result_lst = tune_over_naive(src)
    show_plots(result_lst,[goal,goal])
