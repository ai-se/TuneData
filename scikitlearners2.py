from __future__ import division, print_function
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
# from main import *
from newabcd import sk_abcd
import pandas as pd
import numpy as np


def csv2py(f):
    if isinstance(f, list):
        tbl = [table(src) for src in f]  # tbl is a list of tables
        t = tbl[0]
        for i in range(1, len(tbl)):
            t._rows += tbl[i]._rows
        tbl = t
    else:
        tbl = table(f)
    return tbl


def N_Abcd(predicted, actual):
    predicted_txt = []
    # abcd = Abcd(db='Traing', rx='Testing')
    global The

    def isDef(x):
        return "Defective" if x > 0 else "Non-Defective"
        # use the.option.threshold for cart,
        # rf and where!!

    for data in predicted:
        predicted_txt += [
            isDef(data)]  # this is for defect prediction, binary classes
        # predicted_txt.append(data)  # for multiple classes, just use it
    score = sk_abcd(predicted_txt, actual)
    return score


def learn(clf):
    def conv(x):
        return [float(i) for i in x]

    predict_result, actual = None, None

    if not The.option.tuning:  # this is the non-tuning case.
        testdata, actual = buildtestdata1(The.data.predict)
        traintable = csv2py(The.data.train)
        traindata_X = [conv(row.cells[:-1]) for row in traintable._rows]
        traindata_Y = [(row.cells[-1]) for row in traintable._rows]
        traindata_Y = np.array([1 if i > 0 else 0 for i in traindata_Y])
        predictdata_Y = [(row.cells[-1]) for row in testdata]
        predictdata_X = [conv(row.cells[:-1]) for row in testdata]
        clf = clf.fit(traindata_X, traindata_Y)
        array = clf.predict(predictdata_X)
        predict_result = [i for i in array]
        # pdb.set_trace()

    else:  # this is for DE tuning, using the first fold of StratifiedKfold
        traintable = csv2py([The.data.train, The.data.predict])
        traindata_X = np.array(
            [conv(row.cells[:-1]) for row in traintable._rows])
        traindata_Y = np.array([(row.cells[-1]) for row in traintable._rows])
        traindata_Y = np.array([1 if i > 0 else 0 for i in traindata_Y])
        index_train_tune = [(train, test) for train, test in
                            StratifiedKFold(traindata_Y, n_folds=2,
                                            random_state=1)]
        # here n_folds is hard-coded to 2
        new_train_X = traindata_X[
            index_train_tune[0][0]]  # the first fold as train
        new_train_Y = traindata_Y[
            index_train_tune[0][0]]  # the first fold as train
        new_test_X = traindata_X[
            index_train_tune[0][1]]  # the second fold as test
        new_test_Y = traindata_Y[
            index_train_tune[0][1]]  # the second fold as test
        clf = clf.fit(new_train_X, new_train_Y)
        actual = []
        for i in new_test_Y:
            actual += ["Defective" if i > 0 else "Non-Defective"]
        array = clf.predict(new_test_X)
        predict_result = [i for i in array]

    scores = N_Abcd(predict_result, actual)
    return scores


def cart():
    clf = DecisionTreeRegressor(
        max_features=The.cart.max_features,
        max_depth=The.cart.max_depth,
        min_samples_split=The.cart.min_samples_split,
        min_samples_leaf=The.cart.min_samples_leaf,
        random_state=1)
    return learn(clf)


def rf():
    clf = RandomForestRegressor(
        n_estimators=The.rf.n_estimators,
        max_features=The.rf.max_features,
        min_samples_split=The.rf.min_samples_split,
        min_samples_leaf=The.rf.min_samples_leaf,
        max_leaf_nodes=The.rf.max_leaf_nodes,
        random_state=1)
    return learn(clf)


def rf_classifier():
    clf = RandomForestClassifier(
        n_estimators=The.rf.n_estimators,
        max_features=The.rf.max_features,
        min_samples_split=The.rf.min_samples_split,
        min_samples_leaf=The.rf.min_samples_leaf,
        max_leaf_nodes=The.rf.max_leaf_nodes,
        random_state=1)
    # pdb.set_trace()
    return learn(clf)


def bayes():
    clf = GaussianNB()
    return learn(clf)


def logistic():
    clf = linear_model.LogisticRegression()
    return learn(clf)


if __name__ == "__main__":
    eval(cmd())
