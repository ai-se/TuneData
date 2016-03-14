""" This is the module to claculate pd, pf, precision, f, g and auc(not yet)"""
from __future__ import division
import pdb


def sk_abcd(pred_lst, actual_lst, threshold):
    """
    :param pred_lst: array_like, the predicted results
           actual_lst: array_like, the actual labels
    :return out: list of list, [[pd, pf,prec,f,g],[pd,pf,prec,f,g]]
                 the firs list contains scores for non-defective data,
                 the second list contains scores for defective data
    """
    p = lambda x: int(x * 100)

    def isDef(x):
        return ["Defective" if i >= threshold else "Non-Defective" for i in x]

    def getABCD(labels):
        """
        :param label: all labels in this data sets
        :return (A,B,C,D)true negative, false negative, false positive, true positive
        """
        for actual, predict in zip(actual_lst, pred_lst):
            for i in labels:
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

    def score(labels):
        """
        :param label: list, all labels contained in the actual data
        :return out:list of list, [[pd, pf,prec,f,g],[pd,pf,prec,f,g]]
        """
        out = []
        for i in labels:
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
    labels = ['Non-Defective', 'Defective']
    A, B, C, D = getABCD(labels)
    out = score(labels)
    return out
