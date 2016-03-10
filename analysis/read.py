from __future__ import division, print_function


# __author__ = 'WeiFu'
# import pdb


class Read(object):
  '''
  analysis is to read the results from experiments
  and then put them into proper data structure.
  '''

  def __init__(self, path=""):
    '''
    initialization
    '''
    self.path = path
    self.result = {}


  def readbasic(self, row):
    '''
    read all those basic parameter values
    '''

    def tofloat(astring):
      '''
      try to convert string to Float if possible
      '''
      try:
        return float(astring)
      except ValueError:
        return astring

    item = [ii.strip() for ii in row.split(":")]
    self.result[item[0]] = self.result.get(item[0], []) + [tofloat(item[1])]

  def readthreshold(self, row, content, i):
    '''
    read threshold values for WHERE, CART, RF
    '''
    item = [ii.strip() for ii in row.split(":")]
    if 'where' in content[i + 1]:
      self.result["Where threshold"] = \
        self.result.get("Where threshold", []) + [float(item[1])]
    elif 'cart' in content[i - 1]:
      self.result["CART threshold"] = \
        self.result.get("CART threshold", []) + [float(item[1])]
    elif 'rf' in content[i - 1]:
      self.result["RF threshold"] = \
        self.result.get("RF threshold", []) + [float(item[1])]

  def readevaluation(self, row, content, i):
    '''
    read Evaluations for WHERE, CART, RF
    '''
    item = [ii.strip() for ii in row.split(":")]
    if 'where' in content[i - 1]:
      self.result['Tuned_Where Evaluation'] = \
        self.result.get('Tuned_Where Evaluation', []) + [item[1]]
    elif 'CART' in content[1 + i]:
      self.result['Tuned_CART Evaluation'] = \
        self.result.get('Tuned_CART Evaluation', []) + [item[1]]
    elif 'RF' in content[1 + i]:
      self.result['Tuned_RF Evaluation'] = \
        self.result.get('Tuned_RF Evaluation', []) + [item[1]]

  def readfeatures(self, row, class_name="Tuned Features"):
    '''
    read Features selected by Naive_Where and Tuned_Where
    '''
    item = [ii.strip() for ii in row.rstrip("]").lstrip("[").split("'")
            if ii and "," not in ii]
    if not len(item):
      item = None
    self.result[class_name] = self.result.get(class_name, []) + [item]

  def readgoal(self, row):
    '''
    read performance values for pd, pf, prec, f, g
    '''
    line = [ii.strip() for ii in row.split(",")]
    method = line[1][:line[1].find(':')]  ## Tuned_WHere
    score = float(line[2])
    self.result[method] = self.result.get(method, []) + [score]

  def read(self):
    '''
    the main function to read files
    '''

    if not self.path:
      raise EOFError("No file path provided!")
    content = open(self.path, "r").read().splitlines()
    goal = None
    for i, row in enumerate(content):
      if row:
        if ':' in row and '|' not in row and 'evaluation' \
          not in row and 'option' not in row and 'Def' not in row:
          self.readbasic(row)
        elif 'option.threshold' in row:
          self.readthreshold(row, content, i)
        elif 'evaluation' in row:
          self.readevaluation(row, content, i)
        elif "[" in row and "Tuned_Where Running" in content[i + 1]:
          # features chose by tuner where
          self.readfeatures(row, "Tuned Features")
        elif "[" in row and "Naive_Where Running" in content[i + 1]:
          # features chose by untuned where
          self.readfeatures(row, "Naive Features")
        elif "*****" in row:

          goal = row.strip('*')
        elif "Y-Def" in row and goal == self.result['Tuning objective'][0]:
          self.readgoal(row)
    return self.result





if __name__ == '__main__':
  JADE_prec = Read('../result/1028/myresult2015-10-28 03:50:19prec').read()
  DE_prec =  Read('../result/0906/np=10_f_precision/myresult2015-09-06 18:44:48prec').read()
  import pdb
  pdb.set_trace()
  print("hhhh")
