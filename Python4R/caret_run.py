from __future__ import division, print_function
import sys
import pdb
from os.path import join, isfile
from os import listdir
from caret_learner import *
from caret_tuner import *
from os import getenv
from time import strftime
import time
from sk import *


def create_file(objective):
    home_path = getenv("HOME")
    file_name = (home_path + '/Github/Caret/result/' + strftime(
        "%Y-%m-%d %H:%M:%S") + objective)
    f = open(file_name, 'w').close()
    return file_name


def writefile(file_name, s):
    global The
    f = open(file_name, 'a')
    f.write(s + '\n')
    f.close()


def printResult(dataname, score_dict, file_name):
    def myrdiv(d):
        stat = []
        for key, val in d.iteritems():
            val.insert(0, key)
            stat.append(val)
        return stat
    print("\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20)
    writefile(file_name, "\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20)
    obj = ["auc"]
    for j, k in enumerate(obj):
        express = "\n" + "*" * 10 + " " + k + " " + "*" * 10
        print(express)
        writefile(file_name, express)
        rdivDemo(file_name, myrdiv(score_dict))

    writefile(file_name,
              "End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
    print("\n")


def run(path="../dataR/"):
    results_over_learner = {}
    file_name = create_file("auc")
    folders = [f for f in listdir(path) if not isfile(join(path, f))]
    for folder in folders[:]:
        nextpath = join(path, folder)
        data = [join(nextpath, f) for f in listdir(nextpath) if
                isfile(join(nextpath, f)) and ".DS" not in f]
        for d in data[:]:
            auc = {}
            data_name = d[d.rindex("/") + 1:d.rindex(".")]
            # pdb.set_trace()
            for l in [CART, C50, avnnet]:
                result_each_learner = {}
                for rig in ["Tune","Naive"]:
                    random.seed(1)
                    writefile(file_name, "-" * 30 + "\n")
                    begin_time = time.time()
                    name = rig + l.__name__
                    if rig == "Naive":
                        model = l()
                        X = model.call_model(0, [d], model.default)
                        auc[name] = X[:]
                        result_each_learner[rig] = X[:]
                    else:
                        model = l()
                        tuned_param = DE_tuner(model, [d], file_name)
                        X = model.call_model(0, [d], tuned_param)
                        auc[name] = X[:]
                        result_each_learner[rig] = X[:]
                    run_time = name + " Running Time: " + str(
                        round(time.time() - begin_time, 3))
                    print(run_time)
                    writefile(file_name, run_time)
                if len(result_each_learner.keys()) == 2:
                    results_over_learner[l.__name__] = results_over_learner.get(
                        l.__name__, []) + [np.median(result_each_learner["Tune"]) - np.median(
                        result_each_learner["Naive"])]
            printResult(data_name, auc, file_name)
    printResult("Final",results_over_learner,file_name)


if __name__ == "__main__":
    run()
