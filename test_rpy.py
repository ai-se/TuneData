from __future__ import division, print_function
import sys
import pdb
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpkg
from rpy2.robjects.vectors import StrVector
import pandas.rpy
from rpy2.robjects import globalenv




# def install_pkg():
#     packnames = ('caret', 'C50','rpart','pROC')
#     packnames_to_install = [x for x in packnames if not rpkg.isinstalled(x)]
#     if len(packnames_to_install) > 0:
#         # import R's utility package
#         utils = rpkg.importr('utils')
#         # select a mirror for R packages
#         utils.chooseCRANmirror(ind=1)  # select the first mirror in the list
#         utils.install_packages(StrVector(packnames_to_install))
#
# def run():
#     install_pkg()
#
#     robjects.r('''
#     library(caret)
#     library(rpart)
#     library("pROC")
#     library(C50)
#     library("ada")
#     difference <- function(x.1,x.2,...){
#         x.1p <- do.call("paste", x.1)
#         x.2p <- do.call("paste", x.2)
#         x.1[! x.1p %in% x.2p, ]
#     }
#
#     randomSample = function(df,n) {
#         return (df[sample(nrow(df), n, replace=TRUE),])
#     }
#
#     SB <- function(){
#         setwd("/Users/WeiFu/Github/Caret/dataR")
#         jm1 <- read.csv("./NASA/JM1.csv", sep= ",")
#         datasets <- jm1
#         train_data<-randomSample(datasets,nrow(datasets))
#         trainX <-train_data[,1:length(train_data)-1]
#         trainY <-train_data$bug
#         test_data<-difference(datasets, train_data)
#         colnames(test_data)<-names(train_data)
#
#         control2 <- rpart.control(cp=0.01)
#         Default_model<- rpart(train_data$bug ~ ., data = train_data, control=control2)
#         Default_predicted <- predict(Default_model, test_data)
#         frame_default_predicted <- data.frame(Default_predicted)
#         names(frame_default_predicted)<-c('N','Y')
#         Default_roc <-roc(predictor = frame_default_predicted$Y, response = test_data$bug, levels = rev(levels(test_data$bug)))
#         Default_auc <-auc(Default_roc)
#         improve<- (tuned_auc - Default_auc)
#         return (improve)
#     }
#
#     ''')
#     r_f = robjects.globalenv['SB']
#     pdb.set_trace()
#     r_f()
#     print(r_f.r_repr())
#
# if __name__ == "__main__":
#     run()

import pandas.rpy.common as com
import rpy2
import pdb
import rpy2.robjects as ro
from rpy2.robjects import Formula
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector, BoolVector, StrVector

caretr = importr("caret")
rpartr = importr("rpart")
base = importr("base")
stats = importr("stats")

data_train = ro.DataFrame.from_csvfile("./dataR/NASA/JM1.csv", sep=',')

'''
Default_model<- rpart(train_data$bug ~ ., data = train_data, control=control2)
    Default_predicted <- predict(Default_model, test_data, type = "prob")
    frame_default_predicted <- data.frame(Default_predicted)
    names(frame_default_predicted)<-c('N','Y')
    Default_roc <-roc(predictor = frame_default_predicted$Y, response = test_data$bug, levels = rev(levels(test_data$bug)))
    Default_auc <-auc(Default_roc)
    improve[i]<- (tuned_auc - Default_auc)
'''

ctrl = rpartr.rpart_control(cp=0.01)
formula = Formula("bug ~ .")
model = rpartr.rpart(formula, data = data_train, control=ctrl)
t = {"type":"prob"}

pdb.set_trace()
args = (('newdata',data_train),('type', 'prob'))
rpartr.predict_rpart.rcall(model, args)
predicted = rpartr.predict_rpart(model, newdata= data_train, **t)

pdb.set_trace()

n = FloatVector((0.0001,0.001,0.01,0.1,0.5))
Grid = base.expand_grid(cp=n)
pdb.set_trace()
param2 = {'method' : 'rf', 'trControl' : ctrl}
rf_for = Formula("bug ~ .")
rfmod = caretr.train(rf_for, data = data_train, method = 'rpart', trControl = ctrl,tuneGrid = Grid,
                   metric = "ROC")
print(rfmod)