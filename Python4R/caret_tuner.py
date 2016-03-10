from __future__ import division
import random, pdb
from caret_run import writefile
from sklearn.cross_validation import StratifiedKFold
# from base import *
from newabcd import sk_abcd
import numpy as np


class deBase(object):
    def __init__(self, predictor, data_lst, file_name, tuned_objective=0):
        global The
        self.tobetuned = predictor.tunelst
        self.limit_max = predictor.tune_max
        self.limit_min = predictor.tune_min
        self.data_src = data_lst
        self.predictor = predictor
        self.np = 10
        self.fa = 0.75
        self.cr = 0.3
        self.repeats = 50
        self.life = 5
        self.obj = tuned_objective  # assume 5 is auc
        self.file_name = file_name
        self.evaluation = 0
        self.scores = {}
        self.frontier = [self.generate() for _ in xrange(self.np)]
        self.evaluate()
        self.bestconf, self.bestscore = self.best()

    def generate(self):
        candidates = []
        # pdb.set_trace()
        for n, item in enumerate(self.limit_min):
            if isinstance(item, float):
                candidates.append(round(
                    np.random.uniform(self.limit_min[n], self.limit_max[n], 1),
                    5))
            elif isinstance(item, bool):
                candidates.append(random.random() <= 0.5)
            elif isinstance(item, str):
                candidates.append(
                    self.limit_min[n] if random.random() <= 0.5 else
                    self.limit_max[n])
            elif isinstance(item, int):
                candidates.append(
                    int(random.uniform(self.limit_min[n], self.limit_max[n])))
            else:
                raise ValueError("type of limits are wrong!")
        # pdb.set_trace()
        return self.treat(candidates)

    def evaluate(self):
        for n, arglst in enumerate(self.frontier):
            # clf = self.assign(arglst)
            self.scores[n] = self.predictor.call_model(1, self.data_src,
                                                       arglst)

    def assign(self, tunedvalue):
        param_dict = {}
        for key, val in zip(self.tobetuned, tunedvalue):
            param_dict[key] = val
        param_dict["random_state"] = 1
        clf = self.predictor.default(param_dict).fit(self.train_X,
                                                     self.train_Y)
        return clf

    def best(self):
        sortlst = sorted(self.scores.items(), key=lambda x: x[1])
        bestconf = self.frontier[
            sortlst[-1][0]]  # [(0, [100, 73, 9, 42]), (1, [75, 41, 12, 66])]
        bestscore = sortlst[-1][1]
        return bestconf, bestscore

    def callModel(self, arglst):
        scores = self.predictor.call_model(1, self.data_src, arglst)
        return scores

    def treat(self, lst):
        """
        some parameters may have constraints, for example:
        when generating a parameter list, p[4]should be greater than p[5]
        You should implement this function in subclass
        """
        # return NotImplementedError("treat error")
        return lst

    def trim(self, n, x):
        if isinstance(self.limit_min[n], float):
            return max(self.limit_min[n], min(round(x, 2), self.limit_max[n]))
        elif isinstance(self.limit_max[n], int):
            return max(self.limit_min[n], min(int(x), self.limit_max[n]))
        else:
            raise ValueError("wrong type here in parameters")

    def gen3(self, n, f):
        seen = [n]

        def gen1(seen):
            while 1:
                k = random.randint(0, self.np - 1)
                if k not in seen:
                    seen += [k]
                    break
            return self.frontier[k]

        a = gen1(seen)
        b = gen1(seen)
        c = gen1(seen)
        return a, b, c

    def update(self, index, old):
        newf = []
        a, b, c = self.gen3(index, old)
        for k in xrange(len(old)):
            if isinstance(self.limit_min[k], bool):
                newf.append(
                    old[k] if self.cr < random.random() else not old[k])
            elif isinstance(self.limit_min[k], str):
                newf.append(
                    old[k] if self.cr < random.random() else random.choice(
                        [self.limit_max[k],
                        self.limit_min[k]]))  # random select one
            else:
                newf.append(
                    old[k] if self.cr < random.random() else self.trim(k, (
                        a[k] + self.fa * (b[k] - c[k]))))
        return self.treat(newf)

    def writeResults(self):
        # for p in self.tobetuned:
        #     temp = 0
        #     # exec ("temp =" + p)
        #     writefile(self.file_name, p + ": " + str(temp))
        writefile(self.file_name, "evaluation: " + str(
            self.evaluation) + "\n bestconf: " + str(self.bestconf))

    def DE(self):
        changed = False
        def isBetter(new, old):
            return new < old if self.obj == 1 else new > old

        for k in xrange(self.repeats):
            if self.life <= 0:
                break
            nextgeneration = []
            for index, f in enumerate(self.frontier):
                new = self.update(index, f)
                # clf = self.assign(new)
                newscore = self.callModel(new)
                self.evaluation += 1
                if isBetter(newscore, self.scores[index]):
                    nextgeneration.append(new)
                    self.scores[index] = newscore
                else:
                    nextgeneration.append(f)
            self.frontier = nextgeneration[:]
            newbestconf, newbestscore = self.best()
            if isBetter(newbestscore, self.bestscore):
                # print "newbestscore %s:" % str(newbestscore)
                # print "bestconf %s :" % str(newbestconf)
                self.bestscore = newbestscore
                self.bestconf = newbestconf[:]
                changed = True
            if not changed:
                self.life -= 1
            changed = False
        self.writeResults()
        print "final bestescore %s: " + str(self.bestscore)
        print "final bestconf %s: " + str(self.bestconf)
        print "DONE !!!!"
        # clf = self.assign(self.bestconf)
        return self.bestconf


class WhereDE(deBase):
    def __init__(self, predictor):
        super(WhereDE, i).__init__(predictor)

    def treat(self, lst):
        """
        The.where.depthmin < depthMax
        """

        def ig(l): return int(
            random.uniform(self.limit_min[l], self.limit_max[l]))

        if lst[-1] and lst[4] <= lst[5]:
            lst[4] = ig(4)
            lst[5] = ig(5)
            lst = self.treat(lst)
        return lst


class CartDE(deBase):
    def __init__(self, predictor):
        super(CartDE, self).__init__(predictor)

    def treat(self, lst):
        return lst


class RfDE(deBase):
    def __init__(self, predictor):
        super(RfDE, self).__init__(predictor)

    def treat(self, lst):
        return lst


def DE_tuner(predictor, data_lst, file_name):
    tuner = deBase(predictor, data_lst, file_name)

    clf = tuner.DE()
    return clf


if __name__ == "__main__":
    Where().DE()
