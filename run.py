from __future__ import print_function, division
import pdb
import pandas as pd
import numpy as np
from sklearn.metrics import scorer
import sklearn.grid_search as grid_search
from os import getcwd
from os import listdir
from os.path import join, isfile
from time import strftime
import time
# from mpi4py import MPI
from newlearner import *
from newtuner import *
from sk import rdivDemo
from sk import ksDemo
from clustering import cluster_data
from clustering import near_data
from clustering import kmean_data


def create_file(objective):
    home_path = getcwd()
    file_name = (home_path + '/result/' + strftime(
        "%Y-%m-%d %H:%M:%S") + '_' + objective)
    f = open(file_name, 'w').close()
    return file_name


def writefile(file_name, s):
    global The
    f = open(file_name, 'a')
    f.write(s + '\n')
    f.close()


def save_score(learner, new_score, score_lst):
    NDef = learner + ": N-Def"
    YDef = learner + ": Y-Def"
    for j, s in enumerate(score_lst):
        # s[NDef] = s.get(NDef, []) + [(float(score[0][j] / 100))]
        s[YDef] = s.get(YDef, []) + [(float(new_score[1][j] / 100))]
        # [YDef] will void to use myrdiv.
    return score_lst


def getScoring(goal):
    scoring = None
    if goal.lower() == "pd":
        scoring = 'recall'
    elif goal.lower() == "pf":
        raise ValueError("this goal is not implemented by scikit-learn!")
    elif goal.lower() == "precision":
        scoring = 'precision'
    elif goal.lower() == "f1":
        scoring = 'f1'
    elif goal.lower() == "auc":
        scoring = 'roc_auc'
    else:
        raise ValueError("this goal is not implemented by scikit-learn!")
    return scoring


def load_data(path, num_dataset=3, data_start=3, class_col=20, cluster=False):
    def cov(data):
        # lst = ["Defective" if i > 0  else "Non-Defective" for i in data]
        return data

    def build(src):
        df = pd.read_csv(src, header=0)
        df = df.iloc[:, data_start:]  # get rid of version,id, names
        train_Y = np.asarray(df.ix[:, class_col].as_matrix())
        train_X = df.iloc[:, :class_col].as_matrix()  # numpy array with numeric
        return [train_X, train_Y]

    # folders = [f for f in listdir(path) if not isfile(join(path, f))] ### this is for local machine
    # for folder in folders[:1]: ### this is for  local machine
    #     nextpath = join(path, folder) ### this is for local machine
    for nextpath in [path]:  ### this is for HPC
        folder = nextpath[nextpath.rindex("/") + 1:]  ### this is for HPC
        # folder_name = nextpath[nextpath.rindex("/") + 1:]
        data = [join(nextpath, f) for f in listdir(nextpath) if
                isfile(join(nextpath, f)) and ".DS" not in f]
        count = 0
        for i in range(len(data)):
            X = []
            try:
                for j in xrange(num_dataset):
                    X.append(build(data[i + j]))
            except IndexError, e:
                break
            X.append(cluster_data(data[i+1], data[i + 2]))  ##  put the clustered tuning data at the end of this list
            X.append(near_data(data[i+1], data[i + 2]))  ##  put the nearest tuning data at the end of this list
            X.append(kmean_data(data[i+1], data[i + 2]))  ## Kmeans, clustering data
            yield (folder + "V" + str(count), X)
            count += 1


def printResult(dataname, which_is_better, lst, file_name, goal_index):
    def count_better(dicts):
        temp = {}
        learner_name = set(
            [i[i.index("_") + 1:i.index(":")] for i in dicts.keys()])
        for key, val in dicts.iteritems():
            if "Y-Def" in key and ("Tuned_" in key or "Grid_" in key):
                temp[key] = np.median(val)
        for each in learner_name:
            tune = "Tuned_" + each + ": Y-Def"
            grid = "Grid_" + each + ": Y-Def"
            if temp[tune] >= temp[grid]:
                which_is_better[tune] = which_is_better.get(tune, 0) + 1
            else:
                which_is_better[grid] = which_is_better.get(grid, 0) + 1

    def myrdiv(d):
        stat = []
        for key, val in d.iteritems():
            val.insert(0, key)
            stat.append(val)
        return stat

    print("\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20)
    obj = ["pd", "pf", "prec", "f", "g"]
    for j, k in enumerate(obj):
        express = "\n" + "*" * 10 + " " + k + " " + "*" * 10
        print(express)
        writefile(file_name, express)
        # pdb.set_trace()
        # if j == goal_index:
        #     count_better(lst[j])
        rdivDemo(file_name, myrdiv(lst[j]))
    out_better = (
        "\n In terms of " + str(goal_index) + " : the times of better "
                                              "tuners are" + str(
            which_is_better))
    print(out_better)
    writefile(file_name, out_better)
    writefile(file_name,
              "End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
    print("\n")


def start(src, goal, randomly=False, processor=10, repeats=20):
    tuning_goal = ["pd", "pf", "prec", "f", "g", "auc"]
    if goal not in tuning_goal:
        raise ValueError("Tuning goal %s is not supported! only "
                         "these  %s are supported" % (
                             goal, tuple(tuning_goal)))
    # file_name = create_file(goal)
    nextpath = [src][0]  ### this is for HPC
    file_name = create_file(nextpath[nextpath.rindex("/") + 1:] + "_" + goal)  ### this is for HPC
    which_is_better = {}
    for data_tpl in load_data(src):
        pd, pf, prec, F, g = {}, {}, {}, {}, {}
        score_lst = [pd, pf, prec, F, g]
        data_name, data_lst = data_tpl  # data_lst include 3 consective data
        #  sets
        train_data_X = np.concatenate((data_lst[0][0], data_lst[1][0]), axis=0)
        train_data_Y = np.concatenate((data_lst[0][1], data_lst[1][1]), axis=0)
        new_train_data_X = data_lst[0][0]
        new_train_data_Y = data_lst[0][1]
        new_tuning_data_X = data_lst[1][0]
        new_tuning_data_Y = data_lst[1][1]
        test_data_X = data_lst[2][0]
        test_data_Y = data_lst[2][1]
        title = ("GriSearch: " + str(
            randomly) + "\n" + "Tuning objective: " + goal + "\nBegin time: "
                                                             "" + strftime(
            "%Y-%m-%d %H:%M:%S"))  # pdb.set_trace()
        writefile(file_name, title)
        writefile(file_name, "Dataset: " + data_name)
        for predictor in [RF, CART]:
            # for task in ["Naive_","Tuned_",  "Cluster_", "Nbrs_","Kmeans_"]:  # "Naive_", "Tuned_",
            for task in ["Naive_","Tuned_", "Nbrs_","Kmeans_","Cluster_"]:  # "Naive_", "Tuned_",
                random.seed(1)
                writefile(file_name, "-" * 30 + "\n")
                begin_time = time.time()
                name = task + predictor.__name__
                if task == "Naive_":
                    for _ in xrange(repeats):
                        clf = predictor().default()
                        clf.fit(train_data_X, train_data_Y)
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        0.5)
                        save_score(name, score, score_lst)
                if task == "NaiveTest_":
                    for _ in xrange(repeats):
                        clf = predictor().default()
                        clf.fit(test_data_X, test_data_Y)
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        0.5)
                        save_score(name, score, score_lst)
                elif task == "Grid_":
                    new_predictor = predictor()
                    score_fun = getScoring(goal)
                    for _ in xrange(repeats):
                        clf = new_predictor.default()
                        clf = grid_search.GridSearchCV(clf,
                                                       new_predictor.grid_parameters(
                                                           randomly), cv=2,
                                                       scoring=score_fun,
                                                       refit=True)
                        clf.fit(train_data_X, train_data_Y)
                        # best_params = clf.best_params_
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        0.5)
                        save_score(name, score, score_lst)
                elif task == "Tuned_":
                    new_predictor = predictor()
                    for _ in xrange(repeats):
                        clf, threshold = DE_tuner(new_predictor,
                                                  goal_index=tuning_goal.index(
                                                      goal),
                                                  new_train_X=new_train_data_X,
                                                  new_train_Y=new_train_data_Y,
                                                  new_test_X=new_tuning_data_X,
                                                  new_test_Y=new_tuning_data_Y,
                                                  file_name=file_name)
                        # pdb.set_trace()
                        clf = clf.fit(new_train_data_X, new_train_data_Y)
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        threshold=threshold)
                        save_score(name, score, score_lst)
                elif task == "Cluster_":
                    new_predictor = predictor()
                    cluster_tuning_data_X = data_lst[3][0]
                    cluster_tuning_data_Y = data_lst[3][1]
                    for _ in xrange(repeats):
                        clf, threshold = DE_tuner(new_predictor,
                                                  goal_index=tuning_goal.index(
                                                      goal),
                                                  new_train_X=new_train_data_X,
                                                  new_train_Y=new_train_data_Y,
                                                  new_test_X=cluster_tuning_data_X,
                                                  new_test_Y=cluster_tuning_data_Y,
                                                  file_name=file_name)
                        # pdb.set_trace()
                        clf = clf.fit(new_train_data_X, new_train_data_Y)
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        threshold=threshold)
                        save_score(name, score, score_lst)
                elif task == "Nbrs_":
                    new_predictor = predictor()
                    Nbrs_tuning_data_X = data_lst[4][0]
                    Nbrs_tuning_data_Y = data_lst[4][1]
                    for _ in xrange(repeats):
                        clf, threshold = DE_tuner(new_predictor,
                                                  goal_index=tuning_goal.index(
                                                      goal),
                                                  new_train_X=new_train_data_X,
                                                  new_train_Y=new_train_data_Y,
                                                  new_test_X=Nbrs_tuning_data_X,
                                                  new_test_Y=Nbrs_tuning_data_Y,
                                                  file_name=file_name)
                        # pdb.set_trace()
                        clf = clf.fit(new_train_data_X, new_train_data_Y)
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        threshold=threshold)
                        save_score(name, score, score_lst)
                elif task == "Kmeans_":
                    new_predictor = predictor()
                    Kmean_tuning_data_X = data_lst[5][0]
                    Kmean_tuning_data_Y = data_lst[5][1]
                    for _ in xrange(repeats):
                        clf, threshold = DE_tuner(new_predictor,
                                                  goal_index=tuning_goal.index(
                                                      goal),
                                                  new_train_X=new_train_data_X,
                                                  new_train_Y=new_train_data_Y,
                                                  new_test_X=Kmean_tuning_data_X,
                                                  new_test_Y=Kmean_tuning_data_Y,
                                                  file_name=file_name)
                        # pdb.set_trace()
                        clf = clf.fit(new_train_data_X, new_train_data_Y)
                        predict_result = clf.predict(test_data_X)
                        score = sk_abcd(predict_result, test_data_Y,
                                        threshold=threshold)
                        save_score(name, score, score_lst)
                run_time = name + " Running Time: " + str(
                    round(time.time() - begin_time, 3) / repeats)
                print(run_time)
                writefile(file_name, run_time)
        printResult(data_name, which_is_better, score_lst, file_name,
                    tuning_goal.index(goal))


def run(goal, randomly):
    if randomly.lower() == "true":
        start(src="/share3/wfu/Caret/", goal=goal, randomly=True)
    else:
        start(src="/share3/wfu/Caret/", goal=goal, randomly=False)


def atom(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x


def cmd(com="./data/ant"):
    "Convert command line to a function call."

    # # pdb.set_trace()
    # if len(sys.argv) < 2: return start("./data/ant", True)

    def strp(x): return isinstance(x, basestring)

    def wrap(x): return "'%s'" % x if strp(x) else str(x)

    words = map(wrap, map(atom, sys.argv[2:]))
    return sys.argv[1] + '(' + ','.join(words) + ')'


if __name__ == "__main__":
    if len(sys.argv) < 2:
        start("./data/ant", "prec")
    else:
        eval(cmd())
        # for i in ["precision", "f1", "auc"]:
        #     for j in [True, False]:
        #         start(goal=i, randomly=j)
