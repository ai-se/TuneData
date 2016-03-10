from __future__ import division, print_function
from sklearn import grid_search
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from scikitlearners2 import *

def getParam(learner):
  params = None
  if learner.__class__.__name__.lower() == "cart":
    params = [{'max_features': random.sample(np.arange(0.01, 1,0.1),4 ),
               'max_depth': random.sample(range(1, 51), 3),
               'min_samples_split': random.sample(range(2, 20), 3),
               'min_samples_leaf': random.sample(range(2, 20), 3)}]
    clf = DecisionTreeRegressor
  elif learner.__class__.__name__.lower() == "rf":
    params = [{'n_estimators':random.sample(range(50,151),3),
              'max_features':random.sample(np.arange(0.01,1.0,0.1),3),
              'min_samples_split':random.sample(range(1,21),2),
              'min_samples_leaf':random.sample(range(2,21),3),
              'max_leaf_nodes':random.sample(range(10,51),2)}]
    clf = RandomForestRegressor

  return clf, params


def getScoring(goal):
  scoring = None
  if goal.lower() =="pd":
    scoring = 'recall'
  elif goal.lower() =="pf":
    raise ValueError("this goal is not implemented by scikit-learn!")
  elif goal.lower() =="prec":
    scoring = 'precision'
  elif goal.lower() == "f":
    scoring = 'f1'
  elif goal.lower() == "auc":
    scoring = 'roc_auc'
  else:
    raise ValueError("this goal is not implemented by scikit-learn!")
  return scoring

def getData(train_src):
  def conv(x):
    return [float(i) for i in x]
  # train_src = [learner.train,learner.tune] ### remember, here, used both train and tune
  traintable = csv2py(train_src)
  traindata_X = [conv(row.cells[:-1]) for row in traintable._rows]
  traindata_Y = [(row.cells[-1]) for row in traintable._rows]
  traindata_Y = [1 if i >0 else 0 for i in traindata_Y ]
  # pdb.set_trace()
  # from sklearn.preprocessing import LabelBinarizer
  #
  # lb = LabelBinarizer()
  # y_train = np.array([number[0] for number in lb.fit_transform(traindata_Y)])
  return traindata_X, traindata_Y


def predict(test_src,clf_fitted):
  def conv(x):
    return [float(i) for i in x]

  testdata, actual = buildtestdata1(test_src)
  predictdata_X = [conv(row.cells[:-1]) for row in testdata]
  predictdata_Y = [(row.cells[-1]) for row in testdata]
  array = clf_fitted.predict(predictdata_X)
  predictresult = [i for i in array]
  scores = N_Abcd(predictresult, actual)
  return scores


def gridSearch(learner, goal):
  clf_init, parameters = getParam(learner)
  score_fun = getScoring(goal)
  train_X, train_Y = getData([learner.train, learner.tune])
  clf = grid_search.GridSearchCV(clf_init(random_state=1), parameters, cv=2, scoring=score_fun, refit=True)
  clf.fit(train_X,train_Y)
  best_params = clf.best_params_
  best_params["random_state"] = 1
  clf_fitted = clf_init(**best_params)
  clf_fitted.fit(train_X,train_Y)
  scores = predict(learner.test,clf_fitted)
  # pdb.set_trace()
  return scores

