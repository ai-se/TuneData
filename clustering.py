'''
This is to clustering tuning data based on testing data.
'''
from __future__ import division, print_function
import pdb
import numpy as np
# from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn import decomposition
import pandas as pd


def get_data(src, name, data_start=3):
    '''
    :param src: src of a data set, e.g.: "./data/ant/ant-1.3.csv"
    :param name: the role of this data set in the experiment,  e.g.:"tune"
    :return: df, a pandas.DataFrame
    '''
    data_df = pd.read_csv(src, header=0)
    data_df = data_df.iloc[:, data_start:]  # get rid of version column
    data_df["name"] = np.array([name] * len(data_df))
    return data_df


def get_xy(data_df, normalize=True, class_col=20):
    '''
    :param df: DataFrame containing data
    :param normalize: a flag, indicate whether normalize the data  or not.
    :param class_col: indicate which column is the label column.
    :return:[X,Y], [independent variables, dependent variables]
    '''
    data_y = np.asarray(data_df.ix[:, class_col].as_matrix())
    data_df = data_df.iloc[:, :class_col]  # get all independent variables
    if normalize:
        data_df = (data_df - data_df.min()) / (data_df.max() - data_df.min())
    data_x = data_df.as_matrix()
    return [data_x, data_y]


def cluster_data(tune_path=None, test_path=None):
    '''
    :param tune_path: src of a tuning data set
    :param test_path: src of a testing data set
    :return: tuning data after clustering, in the form of [indep val,
    depen val]
    '''
    if not tune_path:
        tune_path = "./data/ant/ant-1.4.csv"
    if not test_path:
        test_path = "./data/ant/ant-1.5.csv"
    df_tune = get_data(tune_path, "tune")
    df_test = get_data(test_path, "test")
    tune_x, tune_y = get_xy(df_tune, normalize=True)
    test_x, test_y = get_xy(df_test, normalize=True)
    big_x = np.concatenate((tune_x, test_x))
    # big_Y = np.concatenate((tune_y, test_y))
    big_df = df_tune.append(df_test)
    big_db = DBSCAN().fit(big_x)
    df_cls = big_df[big_db.labels_ != -1]  # labels_ ==1 means outliers
    _tune_x, _tune_y = get_xy(df_cls[df_cls['name'] == 'tune'],
                              normalize=False)
    # print(len(_tune_x))
    return [_tune_x, _tune_y]


def near_data(tune_path=None, test_path=None):
    '''
    :param tune_path: src of a tuning data set
    :param test_path: src of a testing data set
    :return: tuning data after clustering, in the form of [indep val,
    depen val]
    '''
    if not tune_path:
        tune_path = "./data/ant/ant-1.4.csv"
    if not test_path:
        test_path = "./data/ant/ant-1.5.csv"
    df_tune = get_data(tune_path, "tune")
    df_test = get_data(test_path, "test")
    tune_x, tune_y = get_xy(df_tune, normalize=True)
    test_x, test_y = get_xy(df_test, normalize=True)
    nbrs = NearestNeighbors(n_neighbors=2).fit(tune_x)
    distance, indices = nbrs.kneighbors(test_x)
    indices = np.hstack(indices)
    unique_index = np.unique(indices)
    normal_tune_x, normal_tune_y = get_xy(df_tune,
                                          normalize=False)  # get the
    # original data, without normalization.
    _tune_x, _tune_y = normal_tune_x[unique_index], normal_tune_y[unique_index]
    # print(len(_tune_x))
    return [_tune_x, _tune_y]


def kmean_data(tune_path=None, test_path=None, cluster=5):
    '''
    :param tune_path: src of a tuning data set
    :param test_path: src of a testing data set
    :return: tuning data after clustering, in the form of [indep val,
    depen val]
    '''

    def find_min(a):
        return a.min()

    if not tune_path:
        tune_path = "./data/ant/ant-1.4.csv"
    if not test_path:
        test_path = "./data/ant/ant-1.5.csv"
    df_tune = get_data(tune_path, "tune")
    df_test = get_data(test_path, "test")
    tune_x, tune_y = get_xy(df_tune, normalize=True)
    test_x, test_y = get_xy(df_test, normalize=True)
    kmean = KMeans(n_clusters=cluster).fit(
        test_x)  ## use testing data to do clustering
    avg_distance = kmean.inertia_ / float(len(test_x))
    tune_distance = kmean.transform(tune_x)
    min_distance = np.apply_along_axis(find_min, 1, tune_distance)
    pick_index = min_distance < avg_distance * 2  # find tuning data whose
    # all distance to cluster center is less than avg_distance
    normal_tune_x, normal_tune_y = get_xy(df_tune, normalize=False)
    _tune_x, _tune_y = normal_tune_x[pick_index], normal_tune_y[pick_index]
    return [_tune_x, _tune_y]


def pca_analysis(data_path=None, name="tune", n_comp=3):
    if not data_path:
        data_path = "./data/ant/ant-1.4.csv"
    raw_data = get_data(data_path, name)
    data_x, data_y = get_xy(raw_data, normalize=True)
    pca = decomposition.PCA(n_components=n_comp)
    pca.fit(data_x)
    transformed_data = pca.transform(data_x)
    return [transformed_data, data_y]


if __name__ == "__main__":
    # near_data()
    # cluster_data()
    # kmean_data()
    pca_analysis()
