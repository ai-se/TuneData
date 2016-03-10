from __future__ import division, print_function
# __author__ = 'WeiFu'

import matplotlib.pyplot as  plt
import numpy as np


def show(data_lst, goal_lst):
  '''
  plot improvements
  '''
  for i in xrange(len(data_lst)):
    data_dict = data_lst[i]
    goal = goal_lst[i]
    label = 'abcdefghigklmnopq'
    plt.subplot(2, 1, i + 1)
    count = 0
    color = ['r', 'g', 'b']
    for key, val in data_dict.iteritems():
      x_aix = np.linspace(0, 16, 17)
      combined = zip(val, label)
      y_sorted = sorted(combined, key=lambda x: x[0])
      # label_sorted = [i[-1] for i in y_sorted]
      val_sorted = [ij[0] for ij in y_sorted]
      plt.plot(x_aix, val_sorted, 'yo-', color=color[count], label=key)
      plt.legend(fontsize='small', loc=0)
      # for i,z in enumerate(x[:]):
      #   y = val_sorted[i]
      #   plt.annotate(label_sorted[i], xy = (z,y+5), textcoords = "data")
      count += 1
    if i == 0:
      plt.title("New training data sets V.S. Old training data sets")
    plt.ylabel(goal)
  plt.xlabel("datasets, sorted by improments")

  plt.show()


if __name__ == '__main__':
  pass
