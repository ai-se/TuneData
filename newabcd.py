""" This is the module to claculate pd, pf, precision, f, g and auc(not yet)"""
from __future__ import division
# import sys
# from sklearn.metrics import roc_curve, auc, roc_auc_score
import pdb
import numpy as np


def sk_abcd(pred_lst, actual_lst, threshold):
    # n = lambda x: int(x)
    p = lambda x: int(x * 100)

    def isDef(x):
        return ["Defective" if i >= threshold else "Non-Defective" for i in x]

    def getLabel():
        label = []
        for i in actual_lst:
            if i not in label:
                label.append(i)
        return label

    # def get_auc(y_predict, predict_pro, y_actual):
    #     if y_predict.dtype == np.dtype("S13"):  ##  defective or non-defective
    #         fpr, tpr, thresholds = roc_curve(y_actual, predict_pro, pos_label="Defective")
    #     else:  # this is 0 or 1, no need to specify pros_label
    #         fpr, tpr, thresholds = roc_curve(y_actual, predict_pro)
    #     roc_auc = auc(fpr, tpr)
    #     return roc_auc

    def getABCD(label):
        """
        :param label: all labels in this data sets
        :return (A,B,C,D)true positive, false negative, false positive, true negative
        """
        for actual, predict in zip(actual_lst, pred_lst):
            for i in label:
                if actual == i:
                    if actual == predict:
                        D[i] = D.get(i, 0) + 1
                    else:
                        B[i] = B.get(i, 0) + 1
                else:
                    if predict == i:
                        C[i] = C.get(i, 0) + 1
                    else:
                        A[i] = A.get(i, 0) + 1
        return A, B, C, D

    def score(label):
        out = []
        for i in label:
            pd = pf = prec = f = g = 0
            a = A.get(i, 0)
            b = B.get(i, 0)
            c = C.get(i, 0)
            d = D.get(i, 0)
            if b + d: pd = d / (b + d)
            if a + c: pf = c / (a + c)
            if c + d: prec = d / (c + d)
            if prec + pd: f = 2 * pd * prec / (pd + prec)
            if pd + 1 - pf: g = 2 * pd * (1 - pf) / (1 - pf + pd)
            if pd + 1 - pf + prec: w = 3 * pd * (1 - pf) * prec / (
                1 - pf + pd + prec)
            if a + b + c + d: acc = (a + d) / (a + b + c + d)
            out += [[p(pd), p(pf), p(prec), p(f), p(g)]]
        return out

    A, B, C, D = {}, {}, {}, {}
    pred_lst = isDef(pred_lst)
    actual_lst = isDef(actual_lst)
    labels = getLabel()
    A, B, C, D = getABCD(labels)
    out = score(['Non-Defective', 'Defective'])
    # auc_score = int(get_auc(pred_lst, actual_lst) * 100)
    # out[0].append(auc_score)
    # out[1].append(auc_score)
    pdb.set_trace()
    return out
