from __future__ import division, print_function
import sys
import pdb
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from scikitlearners2 import *


class RF(object):
    def __init__(self):
        self.clf = self.default()
        self.tunelst = ["min_samples_split", "min_samples_leaf",
                        "max_leaf_nodes", "n_estimators", "max_features"]
        self.tune_min = [1, 2, 10, 50, 0.01]
        self.tune_max = [20, 20, 50, 150, 1]
        self.default_value = [2, 1, None, 100, "auto", 0.5]

    def default(self, params=None):
        if not params:
            return RandomForestClassifier(random_state=1)
        else:
            return RandomForestClassifier(**params)

    def tuned_parameters(self):
        return [{'n_estimators': [50, 151], 'max_features': [0.01, 1.0],
                 'min_samples_split': [1, 21], 'min_samples_leaf': [2, 21],
                 'max_leaf_nodes': [10, 51]}]

    def grid_parameters(self, randomly=True):
        if randomly:
            return [{'n_estimators': random.sample(range(50, 151), 3),
                 'max_features': random.sample(np.arange(0.01, 1.0, 0.1), 3),
                 'min_samples_split': random.sample(range(1, 21), 3),
                 'min_samples_leaf': random.sample(range(2, 21), 3),
                 'max_leaf_nodes': random.sample(range(10, 51), 3)}]
        else:
            return [{'n_estimators': [50,100, 150],
                 'max_features': [0.01, 0.33, 0.99],
                 'min_samples_split': [1, 10,21],
                 'min_samples_leaf': [2, 12,21],
                 'max_leaf_nodes': [10, 30,50]}]

            # # exhuastive grid search
            # return [{'n_estimators': np.arange(50,150,10),
            #      'max_features': np.arange(0.01, 1.01,0.1),
            #      'min_samples_split': np.arange(1,21,2),
            #      'min_samples_leaf': np.arange(2,21,2),
            #      'max_leaf_nodes': np.arange(10, 50,4)}]



class CART(object):
    def __init__(self):
        self.clf = self.default()
        self.tunelst = ["max_features", "max_depth", "min_samples_split",
                        "min_samples_leaf"]
        self.tune_min = [0.01, 1, 2, 1]
        self.tune_max = [1, 50, 20, 20]

    def default(self, params=None):
        if not params:
            return DecisionTreeClassifier(random_state=1)
        else:
            return DecisionTreeClassifier(**params)

    def tuned_parameters(self):
        return [{'max_features': [0.01, 1.0], 'max_depth': [1, 50],
                 'min_samples_split': [1, 20], 'min_samples_leaf': [2, 21]}]

    def grid_parameters(self,randomly=True):
        if randomly:
            return [{'max_features': random.sample(np.arange(0.01, 1, 0.1), 3),
                 'max_depth': random.sample(range(1, 51), 3),
                 'min_samples_split': random.sample(range(1, 20), 3),
                 'min_samples_leaf': random.sample(range(2, 20), 3)}]
        else:
            return [{'max_features': [0.01, 0.33,0.99],
                 'max_depth': [1, 25,50],
                 'min_samples_split': [1, 11,20],
                 'min_samples_leaf': [2, 11,20]}]
            # return [{'max_features': np.arange(0.01, 1, 0.1),
            #      'max_depth': np.arange(1,51,5),
            #      'min_samples_split': np.arange(1,21,2),
            #      'min_samples_leaf': np.arange(2,21,2)}]