from __future__ import division
import random, pdb
from run import writefile
from sklearn.cross_validation import StratifiedKFold
# from base import *
from newabcd import sk_abcd


class deBase(object):
    def __init__(self, predictor, tuned_objective, train_X, train_Y, test_X,
                 test_Y, file_name):
        global The
        self.tobetuned = predictor.tunelst
        self.limit_max = predictor.tune_max
        self.limit_min = predictor.tune_min
        self.predictor = predictor
        self.train_X = train_X
        self.train_Y = train_Y
        self.test_X = test_X
        self.test_Y = test_Y
        self.np = 10
        self.fa = 0.75
        self.cr = 0.3
        self.repeats = 50
        self.life = 5
        self.obj = tuned_objective
        self.file_name = file_name
        self.evaluation = 0
        self.scores = {}
        self.frontier = [self.generate() for _ in xrange(self.np)]
        self.evaluate()
        self.bestconf, self.bestscore = self.best()

    def generate(self):
        candidates = []
        for n, item in enumerate(self.limit_min):
            if isinstance(item, float):
                candidates.append(
                    round(random.uniform(self.limit_min[n], self.limit_max[n]),
                          2))
            elif isinstance(item, bool):
                candidates.append(random.random() <= 0.5)
            elif isinstance(item, list):
                pass
            elif isinstance(item, int):
                candidates.append(
                    int(random.uniform(self.limit_min[n], self.limit_max[n])))
            else:
                raise ValueError("type of limits are wrong!")
        # pdb.set_trace()
        return self.treat(candidates)

    def evaluate(self):
        for n, arglst in enumerate(self.frontier):
            clf = self.assign(arglst)
            self.scores[n] = self.callModel(clf)
            # main return [[pd,pf,prec,f,g],[pd,pf,prec,f,g]], which are
            # N-defective,Y-defecitve

    def assign(self, tunedvalue):
        param_dict = {}
        for key, val in zip(self.tobetuned, tunedvalue):
            param_dict[key] = val
        param_dict["random_state"] = 1
        clf = self.predictor.default(param_dict).fit(self.train_X,
                                                     self.train_Y)
        return clf

    def best(self):
        sortlst = []
        if self.obj == 1:  # this is for pf
            sortlst = sorted(self.scores.items(), key=lambda x: x[1][self.obj],
                             reverse=True)  # alist of turple
        else:
            sortlst = sorted(self.scores.items(),
                             key=lambda x: x[1][self.obj])  # alist of turple
        bestconf = self.frontier[
            sortlst[-1][0]]  # [(0, [100, 73, 9, 42]), (1, [75, 41, 12, 66])]
        bestscore = sortlst[-1][-1][self.obj]
        return bestconf, bestscore

    def callModel(self, clf):
        predict_result = clf.predict(self.test_X)
        predict_pro = clf.predict_proba(self.test_X)
        scores = sk_abcd(predict_result, self.test_Y, predict_pro[:, 1])
        return scores[-1]

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
            elif isinstance(self.limit_min[k], list):
                pass
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
        writefile(self.file_name, "evaluation: " + str(self.evaluation))

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
                clf = self.assign(new)
                newscore = self.callModel(clf)
                self.evaluation += 1
                if isBetter(newscore[self.obj], self.scores[index][self.obj]):
                    nextgeneration.append(new)
                    self.scores[index] = newscore[:]
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
        # print "final bestescore %s: " + str(self.bestscore)
        # print "final bestconf %s: " + str(self.bestconf)
        # print "DONE !!!!"
        clf = self.assign(self.bestconf)
        return clf


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


def DE_tuner(predictor, goal_index, train_X, train_Y, file_name):
    index_train_tune = [(train, test) for train, test in
                        StratifiedKFold(train_Y, n_folds=2, random_state=1)]
    # here n_folds is hard-coded to 2
    new_train_X = train_X[index_train_tune[0][0]]  # the first fold as train
    new_train_Y = train_Y[index_train_tune[0][0]]  # the first fold as train
    new_test_X = train_X[index_train_tune[0][1]]  # the second fold as test
    new_test_Y = train_Y[index_train_tune[0][1]]  # the second fold as test
    tuner = deBase(predictor, goal_index, new_train_X, new_train_Y, new_test_X,
                   new_test_Y, file_name)

    clf = tuner.DE()
    return clf


if __name__ == "__main__":
    Where().DE()
