from __future__ import division, print_function
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import pandas as pd
import pdb


def data(path="./data/ant", num_dataset=3, class_col=23):
    def cov(data):
        # lst = ["Defective" if i > 0  else "Non-Defective" for i in data]
        return data

    def build(src):
        df = pd.read_csv(src, header=0)
        train_Y = np.asarray(cov(df.ix[:, class_col].as_matrix()))
        df = df._get_numeric_data()  # get numeric data
        df = df.iloc[:, 1:21]  # get rid of version column
        df = df / df.max()  # normalization!
        train_X = df.as_matrix()  # numpy array with numeric
        return [train_X, train_Y, df]

    return build(path)


def get_data(src, name):
    df = pd.read_csv(src, header=0)
    df = df._get_numeric_data()
    df = df.iloc[:, 1:]  # get rid of version column
    df["name"] = np.array([name] * len(df))
    return df


def get_X_Y(df, normalize=True, class_col=20):
    Y = np.asarray(df.ix[:, class_col].as_matrix())
    df = df._get_numeric_data()
    df = df.iloc[:, :class_col]  # get all independent variables
    if normalize:
        df = (df - df.min()) / (df.max() - df.min())
    X = df.as_matrix()
    return [X, Y]


def cluster_data(tune_path="./data/ant/ant-1.3.csv", test_path="./data/ant/ant-1.4.csv"):
    df_tune = get_data(tune_path, "tune")
    df_test = get_data(test_path, "test")
    tune_X, tune_Y = get_X_Y(df_tune, normalize=True)
    test_X, test_Y = get_X_Y(df_test, normalize=True)
    big_X = np.concatenate((tune_X, test_X))
    big_Y = np.concatenate((tune_Y, test_Y))
    big_df = df_tune.append(df_test)
    big_db = DBSCAN(algorithm="kd_tree").fit(big_X)
    df_clusters = big_df[big_db.labels_ != -1]  # labels_ ==1 means outliers
    actual_tune_X, actual_tune_Y = get_X_Y(df_clusters[df_clusters['name'] == 'tune'], normalize=False)
    # actual_test_X, actual_test_Y = get_X_Y(df_clusters[df_clusters['name'] == 'test'], normalize=False)
    return[actual_tune_X,actual_tune_Y]


if __name__ == "__main__":
    cluster_data()
