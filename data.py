import sys
import pdb
from os import listdir
from table import *
from os.path import isfile, join
import collections

class removequote():
  def __init__(i, filename = ""):
    i.filename = filename
  def removeq(i):
    f = open(i.filename)
    result = ""
    while True:
      line = f.readline()
      if "[" in line:
        for word in line:
          if "\'"in word:
            result += word[1:-2]
          else:
            result +=word
        for _ in range(10):
          f.readline()
      if not line:
        break

    print result



class extractarg():
  def mainloop(i):
    f = open(i.filename)
    where = False
    cart = False
    rf = False

    while True:
      line = f.readline()
      if not line:
        break
      if "Dataset:" in line:
        i.result += i.head(line)
        where = True
        cart = False
        rf = False
        continue
      if "Naive_Where" in line:
        cart = True
        where = False
        rf = False
      if "Naive_Cart" in line:
        cart = False
        where = False
        rf = True

      if where and line[:line.find(":")].split()[0] in i.wherelst:
        i.wherelst[line[:line.find(":")].split()[0]] +=line[line.find(":"):].split()
      if cart and line[:line.find(":")].split()[0] in i.cartlst:
        i.cartlst[line[:line.find(":")].split()[0]] +=line[line.find(":"):].split()
      if rf and line[:line.find(":")].split()[0] != [] and line[:line.find(":")].split()[0] in i.rflst:
        i.rflst[line[:line.find(":")].split()[0]] +=line[line.find(":"):].split()

    f.close()
    f = open(i.filename+'latex', 'w')
    f.write(i.result+'\n')
    f.close()
    print i.result
  def head(i,line):
    return line[9:line.find("\n")]


class model():
  def __init__(i,funname="", filename=""):
    i.funname = funname
    i.filename = filename
    i.result = ""
    i.tail = ""
  def mainloop(i):
    f = open(i.filename)
    while True:
      line = f.readline()
      if "Dataset:" in line:
        i.result += i.head(line)
      if "*prec*" in line:
        i.result +=i.sub(f)+i.tail
      if not line:
        break
    print i.improve
    f.close()
    f = open(i.filename+'latexBars', 'w')
    f.write(i.result+'\n')
    f.close()
    print i.result
  def sub(i, f):
    f.readline()
    f.readline()
    while True:
      line = f.readline()
      if "Y-Def" in line:
        i.result += str(i.operation(line))
      if "Def" not in line:
        break
  def head(i,line):
    return line[9:line.find("\n")]
    # return i.result


class G(model):
  '''
   generate the latex for ALL G value
  '''
  def __init__(i,funname="", filename=""):
    i.funname = funname
    i.filename = filename
    i.result = ""
    i.tail = "```\n"
  def head(i,line):
    return "***"+line[9:line.find("\n")]+"***\n"
  def operation(i,line):
    return str(line)

class IQR(model):
  '''
   generate the latex for G value with mean, IQR
  '''
  def __init__(i,funname="", filename="./result/0216/myresult10"):
    i.funname = funname
    i.filename = filename
    i.result = ""
    i.tail = ""
  def head(i,line):
    return "\\rowcolor[gray]{.9}"+line[9:line.find("\n")]
  def operation(i,line):
    return " & "+line[6:20].strip().replace("_","\_") +" & "+line[30:37].strip() \
           +" & "+line[40:47].strip()+" & \quart"+"{"+str(float(line[88:92].strip())*100) \
           +"}{"+str(line[40:47].strip())+"}{"+str(float(line[95:99].strip())*100)+"}"+"\\\\" +"\n"

class Once(model):
  '''
  FOR ONLY ONE VALUE, USE BARS TO SHOW THE PERCENTAGE
  '''
  def __init__(i,funname="", filename=""):
    i.funname = funname
    i.filename = filename
    i.result = ""
    i.tail = "\n"
    i.dic = {}
    i.namelst = ['Naive\\_WHERE', 'Tuned\\_WHERE', 'Naive\\_Cart','Tuned\\_Cart', 'Naive\\_RFst', 'Tuned\\_RFst']
    i.improve ={}
  def sub(i,f):
    f.readline()
    f.readline()
    # f.readline()
    i.dic = {}
    while True:
      line = f.readline()
      # pdb.set_trace()
      if "Y-Def" in line:
        i.dic[line[6:20].strip().replace("_","\_")] = float(line[30:37].strip())
        # pdb.set_trace()
      if "Def" not in line:
        break
    # pdb.set_trace()
    imin = i.min()
    imax = i.max()
    return i.operation(imin, imax)
  def min(i):
    return min(i.dic.itervalues())
  def max(i):
    return max(i.dic.itervalues())
  def head(i,line):
    return line[9:line.find("\n")]
  def operation(i,imin, imax):
    # pdb.set_trace()
    out = ""
    maxitem = max(i.dic, key = i.dic.get) # get the key of the max value
    maxvalue = i.dic[maxitem]
    for method in i.namelst:
      exp = " & "+str(int(i.dic[method])) +" & "
      if i.dic[method] == maxvalue:
        exp = " & {\\bf "+str(int(i.dic[method])) +"} & "
      out += exp +" "
      # if (i.dic[method]-imin)/(imax-imin) <=0.2:
      #   out += exp +"       "
      # elif (i.dic[method]-imin)/(imax-imin) <=0.4:
      #   out += exp +"{\\rone}"
      # elif (i.dic[method]-imin)/(imax-imin) <=0.6:
      #   out += exp +"{\\rtwo}"
      # elif (i.dic[method]-imin)/(imax-imin) <=0.8:
      #   out += exp +"{\\rthree}"
      # elif (i.dic[method]-imin)/(imax-imin) <=1:
      #   out += exp +"{\\rfour}"
    i.improve["1"] =sorted(i.improve.get("1",[])+[i.dic['Tuned\\_WHERE'] - i.dic['Naive\\_WHERE']])
    i.improve["2"] =sorted(i.improve.get("2",[])+[i.dic['Tuned\\_Cart'] - i.dic['Naive\\_Cart']])
    i.improve["3"] =(i.improve.get("3",[])+[i.dic['Tuned\\_RFst'] - i.dic['Naive\\_RFst']])
    return out+"\\\\"

class Parameters(model):
  '''
  GET THE TUNED PARAMETERS FOR DIFFERENT MODELS
  '''
  def __init__(i,filename=""):
    i.filename = filename
    i.result = ""
    i.tail = "\n"
    i.dataset = []
    i.parameters = {}
    i.wherelst = {"infoPrune":[],"threshold":[],"treeMin":[],"treePrune":[], "depthMax":[], "depthMin":[],"min_Size":[],"wherePrune":[]}
    i.cartlst = {"max_feature":[], "max_depth":[], "min_samples_split":[], "min_samples_leaf":[],"threshold":[]}
    i.rflst = {"max_feature":[], "max_depth":[], "min_samples_split":[], "min_samples_leaf":[],"threshold":[],"max_leaf_nodes":[], "n_estimators":[]}
  def keep(i):
    f = open(i.filename, "r")
    # pdb.set_trace()
    include = ['infoPrune',"threshold","min_sample_size","treePrune", "depthMax", "depthMin","min_Size","wherePrune","wriggle",\
               "max_feature", "min_samples_split", "min_samples_leaf","threshold",\
               "max_leaf_nodes", "n_estimators"]
    exclude = ['time','Time', 'bestscore','Evalutions','evaluation','Def']
    while True:
      line = f.readline()
      if "Dataset:" in line:
        i.dataset.append(i.head(line))
      # if ":" in line and not any([s not in line for s in include]):
      # print "******"+line
      if ":" in line and "-Def" not in line and "Running Time" not in line and "DataSet" not in line and\
       "Dataset" not in line and "time" not in line  and "bestscore" not in line and "evaluation" not in line and "Evaluations" not in line :
        # print line
        i.parameters[i.dataset[-1]]= i.parameters.get(i.dataset[-1],[]) +[line[line.find(":")+1:-1]]
      if not line :
        break
    # pdb.set_trace()

class features(model):
  def __init__(i, funname ="", filename = ""):
    i.funname = funname
    i.filename = filename
    i.result = ""
    i.tail = "\n"
    i.featuresbefore = {"wmc":[],"dit":[],"noc":[],"cbo":[],
                  "rfc":[],"lcom":[],"ca":[],"ce":[],
                  "npm":[],"lcom3":[],"loc":[],"dam":[],
                  "moa":[],"mfa":[],"cam":[],"ic":[],
                  "cbm":[],"amc":[],"max_cc":[],"avg_cc":[]}
    i.featuresafter = {"wmc":[],"dit":[],"noc":[],"cbo":[],
                  "rfc":[],"lcom":[],"ca":[],"ce":[],
                  "npm":[],"lcom3":[],"loc":[],"dam":[],
                  "moa":[],"mfa":[],"cam":[],"ic":[],
                  "cbm":[],"amc":[],"max_cc":[],"avg_cc":[]}
    i.dataset = []

  def keep(i):
    f = open(i.filename,"r")
    count = -1
    while True:
      line = f.readline()
      if "Dataset:" in line:
        i.dataset.append(i.head(line))
        count += 1
      if "Evaluations" in line:
        line = f.readline()
        if line =="[]\n":
          continue
        else:
          ll = line.split(",")
          for val in ll:
            a =val[val.find("\'")+1:-1] if val[-1] =="\'" else val[val.find("\'")+1:-3]
            i.featuresafter[a].append(count)
      if "Tuned_Where Running Time" in line:
        line = f.readline()
        if line =="[]\n":
          continue
        else:
          ll = line.split(",")
          for val in ll:
            a =val[val.find("\'")+1:-1] if val[-1] =="\'" else val[val.find("\'")+1:-3]
            i.featuresbefore[a].append(count)
      if not line:
        break
    print i.featuresafter
    print i.featuresbefore


class time(model):
  def __init__(i, filename=""):
    i.filename = filename
    i.dataset = []
    i.elapsedtime = {}
  def keep(i):
    f = open(i.filename, "r")
    # pdb.set_trace()
    while True:
      line = f.readline()
      if "Dataset:" in line:
        i.dataset.append(i.head(line))
      if "Evaluations" in line or "evaluation" in line:
        i.elapsedtime[i.dataset[-1]]= i.elapsedtime.get(i.dataset[-1],[]) +[line[line.find(":")+1:-1]]
      if "Tuned_Where Running" in line:
        i.elapsedtime[i.dataset[-1]]= [i.elapsedtime.get(i.dataset[-1],[])[0]+" /"+line[line.find(":")+1:line.find(".")+3]]
      elif "Tuned_CART Running" in line:
        # pdb.set_trace()
        i.elapsedtime[i.dataset[-1]][2]= i.elapsedtime.get(i.dataset[-1],[])[2]+" /"+line[line.find(":")+1:line.find(".")+3]
      elif "Tuned_RF Running" in line :
        # pdb.set_trace()
        i.elapsedtime[i.dataset[-1]][4] = i.elapsedtime.get(i.dataset[-1],[])[4]+" /"+line[line.find(":")+1:line.find(".")+3]
      elif "Running Time" in line:
        i.elapsedtime[i.dataset[-1]]= i.elapsedtime.get(i.dataset[-1],[]) +[line[line.find(":")+1:line.find(".")+3]]
      if not line :
        break

def genFeatureLatex(filename):
  '''
  this function generates the latex scripts for feature selection tables
  '''
  def mulcol(num, style, name):
    return "\multicolumn{"+num+"}{"+style+"}{" +name+"}"
  def datasetName():
    return ("&").join([mulcol("2","c", i[:-2]) if "0" in i else mulcol("2","c", i) for i in extractFeatures.dataset])
  def readstar():
    command =""
    # pdb.set_trace()
    for (key, val) in extractFeatures.featuresbefore.iteritems():
      label = ["& " for _ in range(34)]
      command +=key.replace("_","\_") if "_" in key else key
      if extractFeatures.featuresbefore[key] !=[]:
        for i in extractFeatures.featuresbefore[key]:
          label[i*2] = "& $\star$"
      if extractFeatures.featuresafter[key] !=[]:
        for i in extractFeatures.featuresafter[key]:
          label[i*2+1] = "& $\circ$"
      command +=("").join(label)+"\\\\\n"
    print command
    return command

      

  extractFeatures = features("",filename)
  extractFeatures.keep()
  f = open(extractFeatures.filename+'latex', 'w')
  space = "  "
  texCommand = "\\begin{figure*}[!ht]\n"\
              "\\scriptsize\n"\
              "\\centering\n"\
              +space+"\\begin{tabular}{"+"c|c "*18+"}\n"\
              +space+"\\hline\\hline\n"\
              +space+"Features & "+datasetName()+"\n\\\\\\hline\n"\
              +space+readstar()+"\n"\
              +space+"\\end{tabular}\n"\
              "\\end{figure*}\n"
  f.write(texCommand+'\n')
  f.close()

def genTotalFeatures(filename):
  def readstar():
    # pd = "./result/0224/myresult2015-02-23 22:28:52pd"
    # pf = "./result/0224/myresult2015-02-25 09:52:06pf"
    prec = "./result/0324/myresult2015-03-23 22:58:35prec"
    f = "./result/0324/myresult2015-03-24 11:02:10f"
    # g = "./result/0224/myresult2015-02-26 00:32:46g"
    before, after = {}, {}
    # filenames = [pd, pf, prec, f, g]
    # keys = ["pd","pf","prec","f", "g"]
    filenames = [prec, f]
    keys = ["prec","f"]
    total ={}
    command = ""
    for key,name in zip(keys,filenames):
      temp = features("",name)
      temp.keep()
      before[key]=temp.featuresbefore
      after[key]=temp.featuresafter
    for feature in before["prec"].keys():
      # label = ["& " for _ in range(10)]
      # command +=feature.replace("_","\_") if "_" in feature else feature
      count = 0
      for i,key in enumerate(keys):
        count +=len(before[key][feature])+len(after[key][feature])
      total [feature] = count
    orderedfeature = sorted(total.iteritems(), key =lambda x:x[1] )

    for feature in orderedfeature:
      label = ["& " for _ in range(5)]
      command +=feature[0].replace("_","\_") if "_" in feature[0] else feature[0]
      for i,key in enumerate(keys):
        label[i*2] = "& " + str(len(before[key][feature[0]]))
        label[i*2+1] = "& " +str(len(after[key][feature[0]]))
      command +=("").join(label)+"& "+str(feature[1])+"\\\\\n"
    print orderedfeature
    print command
    return command

  f = open('./result/0324/latexTotalFeatureExpB', 'w')
  space = "  "
  texCommand = "\\begin{figure*}[!ht]\n"\
              "\\scriptsize\n"\
              "\\centering\n"\
              +space+"\\begin{tabular}{"+"c|c "*6+"|c}\n"\
              +space+"\\hline\\hline\n"\
              +space+"Features & \multicolumn{2}{c}{Pd} & \multicolumn{2}{c}{Pf} & \multicolumn{2}{c}{Precision} & \multicolumn{2}{c}{F} & \multicolumn{2}{c}{G} & SUM\n\\\\\\hline\n"\
              +space+readstar()+"\n"\
              +space+"\\end{tabular}\n"\
              "\\end{figure*}\n"
  f.write(texCommand+'\n')
  f.close()

def genTime():
  # def readstar():
  # pd = "./result/0224/myresult2015-02-23 22:28:52pd"
  # pf = "./result/0224/myresult2015-02-25 09:52:06pf"
  # prec = "./result/0224/myresult2015-02-24 11:05:28prec"
  # f = "./result/0224/myresult2015-02-24 16:13:22f"
  prec = "./result/0906/prec"
  f = "./result/0906/f"
  filenames = [ prec, f]
  keys = ["prec","F"]
  space = "  "
  objtime ={}
  for key,name in zip(keys,filenames):
    temp = time(name)
    temp.keep()
    objtime[key]=temp.elapsedtime # key is pd,pf, f, prec,g.....
  temp = time(filenames[0])
  temp.keep()
  texCommand = ""
  for key in keys:
    label = ""
    for data in temp.dataset:
      dataname = data[:-2] if "0" in data else data
      label += space*2 +dataname +" &"+(" &" ).join(objtime[key][data]) +"\\\\\n"

    texCommand +="%%%%time for "+ key +" %%%%%%\n"\
          "\\begin{figure*}[!ht]\n"\
          "\\scriptsize\n"\
          "\\centering\n"\
          +space+"\\begin{tabular}{l"+"|c "*6+"}\n"\
          +space*2+"\\hline\\hline\n"\
          +space*2+"Datasets & Tuned\_Where & Naive\_Where & Tuned\_CART & Naive\_CART & Tuned\_RanFst & Naive\_RanFst\\\\\n"\
          +space*2+"\\hline\n"\
          +label\
          +space+"\\end{tabular}\n"\
          +space+"\\caption{Evaluations/runtimes and runtimes for tuned and default learners(in sec), optimizing for "+key+"}\n"\
          "\\end{figure*}\n\n\n"
    print texCommand
  f = open('./result/0906/latexTime', 'w')
  f.write(texCommand+'\n')


def genPara():
  # def readstar():
  # pd = "./result/0224/myresult2015-02-23 22:28:52pd"
  # pf = "./result/0224/myresult2015-02-25 09:52:06pf"
  # prec = "./result/0224/myresult2015-02-24 11:05:28prec"
  # f = "./result/0224/myresult2015-02-24 16:13:22f"
  # g = "./result/0224/myresult2015-02-26 00:32:46g"
  # filenames = [pd, pf, prec, f, g]
  # keys = ["pd","pf","prec","F", "G"]
  prec = "./result/0324/myresult2015-03-23 22:58:35prec"
  f = "./result/0324/myresult2015-03-24 11:02:10f"
  # prec = "./result/0322/myresult2015-03-22 17:05:50prec"
  # f = "./result/0322/myresult2015-03-22 21:09:34f"
  filenames = [ prec, f]
  keys = ["prec","F"]
  space = "  "
  objPara ={}
  paraName =["threshold", "infoPrune","min\_sample\_size", "min\_Size", "wriggle", "depthMin","depthMax", "wherePrune", "treePrune",\
            "threshold", "max\_feature", "min\_samples\_split", "min\_samples\_leaf", "max\_depth",\
            "threshold", "max\_feature","max\_leaf\_nodes", "min\_samples\_split", "min\_samples\_leaf", "n\_estimators"]
  default = ["0.5", "0.33", "4", "0.5", "0.2", "2","10","False", "True",\
             "0.5", "None","2","1","None",\
             "0.5", "None", "None", "2", "1", "100"]
  for key, name in zip(keys,filenames):
    temp = Parameters(name)
    temp.keep()
    objPara[key] = temp.parameters
  temp = Parameters(filenames[0])
  temp.keep()
  texCommand = ""
  for key in keys:
    label = ""
    Para ={}
    for k in xrange(20):
      for data in temp.dataset:
        dataname = data[:-2] if "0" in data else data
        Para[k] = Para.get(k,[])+[objPara[key][data][k]]
    content = ""
    for i, name in enumerate(paraName):
      if i==0:
        content +="\\multirow{8}{*}{\\begin{tabular}[c]{@{}c@{}}Where\\\\based\\\\ Learner\\end{tabular}}\n"
      if i ==9:
        content +="\\hline\n\\multirow{4}{*}{CART}\n"
      if i ==13:
        content +="\\hline\n\\multirow{6}{*}{\\begin{tabular}[c]{@{}c@{}}Random \\\\ Forests\\end{tabular}} \n"
      content += "& "+name+"& "+default[i]+"&"+ ("&").join(Para[i])+"\\\\ \\cline{2-20}\n"
    content +="\\hline"


    head = 	"\\begin{tabular}[c]{@{}c@{}}Learner \\\\ Name\end{tabular}&Parameters  & Default &" \
             +("&").join(temp.dataset)+"\\\\ \n \hline"
    texCommand +="%%%%parameters for "+ key +" %%%%%%\n"\
          "\\begin{figure*}[!ht]\n"\
          "\\resizebox{\\textwidth}{!}{\n"\
          "\\scriptsize\n"\
          "\\centering\n"\
          +space+"\\begin{tabular}{"+"|c "*20+"|}\n"\
          +space*2+"\\hline\n"\
          +space+head +"\n"\
          +content\
          +space+"\\end{tabular}\n}\n"\
          +space+"\\caption{Parameters tuned on different models over the objective of "+key+"}\n"\
          "\\end{figure*}\n\n\n"
    print texCommand
  f = open('./result/0324/latexParameters', 'w')
  f.write(texCommand+'\n')




def readBug(filen, path="./data"):
  '''
   read the last column of data file to compute defetive vs non-defective
  '''
  def makeTex(train, tune, test):
    def mulcol(num, style, name):
      # return "\multicolumn{"+num+"}{"+style+"}{" +name+"}"
      return name
    def datasetName():
      return ("&").join([mulcol("1","c", i[:-2]) if "0" in i else mulcol("1","c", i) for i in extractFeatures.dataset])
    def lstStat(num):
      # pdb.set_trace()
      return (" &").join(num)
    def divide(lst):
      return [lst[:(len(lst)/2+1)], lst[(len(lst)/2+1):]]
    extractFeatures = features("",filen)
    extractFeatures.keep()
    f = open(extractFeatures.filename+'DefNonDeflatex', 'w')
    space = "  "
    datasets = divide(datasetName())
    train = divide(train)
    tune = divide(tune)
    test = divide(test)
    texCommand =""
    for i in range(2):
      texCommand += "\\begin{figure*}[!ht]\n"\
                "\\scriptsize\n"\
                "\\centering\n"\
                +space+"\\begin{tabular}{"+"c "*10+"}\n"\
                +space+"\\hline\\hline\n"\
                +space+"Dataset &"+datasets[i]+"\n\\\\\\hline\n"\
                +space+"training &"+lstStat(train[i])+"\n\\\\"\
                +space+"tunning  &"+lstStat(tune[i])+"\n\\\\"\
                +space+"testing &"+lstStat(test[i])+"\n\\\\"\
                +space+"\\end{tabular}\n"\
                "\\end{figure*}\n"

    f.write(texCommand+'\n')
    f.close()



  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  # stat = collections.OrderedDict
  stats = {}
  train = []
  tune = []
  test = []
  for one in folders:
    nextpath = join(path, one)
    filename = [f for f in listdir(nextpath) if isfile(join(nextpath, f))]
    filepath = [join(nextpath, f)
            for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for dataname in filename:
      filepath = join(nextpath,dataname)
      defNum = 0
      nondefNum = 0
      tbl = table(filepath)
      for row in tbl._rows:
        if row.cells[-1]>=1:
          defNum+=1
        else:
          nondefNum+=1

      stats[dataname] = str(defNum)+"/"+ str(nondefNum +defNum)
      # stats.append([dataname,str(defNum)+"/"+ str(nondefNum)])
    for i in range(len(filename)):
      dataname = one +"V"+str(i)
      try:
        # pdb.set_trace()
        test += [stats[filename[i+2]]]
        tune += [stats[filename[i+1]]]
        train += [stats[filename[i]]]
      except IndexError, e:
        print one+" done!"
        break
  # pdb.set_trace()
  makeTex(train, tune, test)

  print stats

# def vivek(path):
#   def wheresub(f):
#     para = []
#     while True:
#       line = f.readline()
#       if ":" in line:
#         try:
#           para.append(float(line[line.find(":")+2:-1]))
#         except:
#           if line[line.find(":")+2:-1] == "True":
#             para.append(True)
#           else:
#             para.append(False)
#       if ":" not in line:
#         break
#     new=[] # change order according to vivek's code
#     # print para
#     new+=[para[1]]+[para[2]]+[para[0]]+[para[3]]+[para[6]]+[para[5]]+[para[4]]+[para[8]]+[para[7]]
#     return new
#   def cartsub(f):
#     para = []
#     while True:
#       line = f.readline()
#       if ":"  in line:
#         try:
#           para.append(float(line[line.find(":")+2:-1]))
#         except:
#           if line[line.find(":")+2:-1] == "True":
#             para.append(True)
#           else:
#             para.append(False)
#       if ":" not in line:
#         break
#     new=[] # change order according to vivek's code
#     new +=[para[3]]+[para[4]]+[para[2]]+[para[-1]]+[para[0]]
#     return new
#
#   def rfsub(f):
#     para = []
#     while True:
#       line = f.readline()
#       if ":"  in line:
#         try:
#           para.append(float(line[line.find(":")+2:-1]))
#         except:
#           if line[line.find(":")+2:-1] == "True":
#             para.append(True)
#           else:
#             para.append(False)
#       if ":" not in line:
#         break
#     new=[] # change order according to vivek's code
#     new +=[para[3]]+[para[4]]+[para[2]]+[para[-1]]+[para[1]]+[para[0]]
#     return new
#
#   f = open(path, "r")
#   while True:
#     line = f.readline()
#     if "WHERE" in line:
#       where =wheresub(f)
#       print where
#     if "CART" in line:
#       cart = cartsub(f)
#       print cart
#     if "RF" in line:
#       rf = rfsub(f)
#       print rf
#     if not line:
#       break








def main():
  # call=Once("",'./result/0324/myresult2015-03-23 22:58:35prec')
  # call.mainloop()
  # call = removequote("./result/0219/myresult2015-02-19 02:01:10")
  # call.removeq()
  # call = features("",'./result/0224/myresult2015-02-26 00:32:46g')
  # call.keep()
  # genFeatureLatex("./result/0224/myresult2015-02-23 22:28:52pd")
  # readBug("./result/0320/0320_prec_results")
  # genTotalFeatures("")
  ss = time("./result/0906/prec")
  ss.keep()
  genTime()
  # ss = Parameters("./result/0224/myresult2015-02-26 00:32:46g")
  # ss.keep()
  # genPara()
  # vivek("/Users/WeiFu/Github/Research/defect prediction/Vivekmyresult2015-03-18 02:52:12prec")
if __name__=="__main__":
  main()








