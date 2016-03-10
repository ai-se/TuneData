
#######

suppressMessages(library(caret))
suppressMessages(library("pROC"))
suppressMessages(library(C50))
suppressMessages(library("ada"))
difference <- function(x.1,x.2,...){
  x.1p <- do.call("paste", x.1)
  x.2p <- do.call("paste", x.2)
  x.1[! x.1p %in% x.2p, ]
}
randomSample = function(df,n) { 
  return (df[sample(nrow(df), n, replace=TRUE),])
}


naive<-function(datasets,param_trails, param_winnow, param_rules){
  datasets$bug[datasets$bug >0] <-1
  datasets$bug[datasets$bug == 0] <-0
  datasets$bug <- factor(datasets$bug, labels = c("N","Y"))
    
  ########## repeats 100 times #################
#   keep <-c()
#   for( i in 1:10){
    train_data<-randomSample(datasets,nrow(datasets))
    trainX <-train_data[,1:length(train_data)-1]
    trainY <-train_data$bug
    test_data<-difference(datasets, train_data)
    colnames(test_data)<-names(train_data)

    ########## Default MODEl #################
    C50_control <- C5.0Control(winnow = param_winnow)
    Default_model<- C5.0(trainX, trainY,trails=trails, rules=param_rules, control = C50_control)
    Default_predicted <- predict(Default_model, test_data, type = "prob")
    Default_roc <-roc(predictor = data.frame(Default_predicted)$Y, response = test_data$bug, levels = rev(levels(test_data$bug)))
    Default_auc <-auc(Default_roc)
    return (Default_auc)
#   }
#   cat(keep)
#    return (keep)  ### return median values
}


############## tuining ###################

tune <- function(datasets,param_trails, param_winnow, param_rules){
  datasets$bug[datasets$bug >0] <-1
  datasets$bug[datasets$bug == 0] <-0
  datasets$bug <- factor(datasets$bug, labels = c("N","Y"))
  train_data<-randomSample(datasets,nrow(datasets))
  ##### train and tune #####
  keep <-c()
  for( i in 1:10){
    new_train_data <- randomSample(train_data, nrow(datasets)) 
    new_tune_data <- difference(train_data, new_train_data)
    colnames(new_tune_data) <- names(new_train_data)
    #   test_data<-difference(datasets, train_data)
    #   colnames(test_data)<-names(train_data)
#     control2 <- rpart.control(cp=nums)
#     tune_model<- rpart(new_train_data$bug ~ ., data = new_train_data, control=control2)
#     tune_predicted <- predict(tune_model, new_tune_data)
    new_trainX <-new_train_data[,1:length(new_train_data)-1]
    new_trainY <-new_train_data$bug
    C50_control <- C5.0Control(winnow = param_winnow)
    tune_model<- C5.0(new_trainX, new_trainY,trails=param_trails, rules=param_rules, control = C50_control)
    tune_predicted <- predict(tune_model, new_tune_data, type = "prob")
    frame_tune_predicted <- data.frame(tune_predicted)
    names(frame_tune_predicted)<-c('N','Y')
    tune_roc <-roc(predictor = frame_tune_predicted$Y, response = new_tune_data$bug, levels = rev(levels(new_tune_data$bug)))
    tune_auc <-auc(tune_roc)
    keep[i] <- tune_auc
  }
  return (median(keep))  ### return median values
}


set.seed(1)
options(warn=-1)
setwd("/Users/WeiFu/Github/Caret/dataR")
# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)
tuning = myArgs[1] # tunig flag: 0=naive, 1=tuning
data_src = myArgs[2] # data set_src
param_trails = as.numeric(myArgs[3]) # parameters
param_winnow = ifelse(myArgs[4] %in% c("False"), FALSE, TRUE)
param_rules = ifelse(myArgs[5] %in% c("rules"), TRUE, FALSE)

results_data <-c()
#  data_src <-"./apache/camel-1.2.csv"
#  tuning <- 1
# param_trails = 1
# param_winnow = FALSE
# param_rules = TRUE
if (tuning == 0){
  data_set <- read.csv(data_src, sep= ",")
  data_set$X <-NULL  # for JDE, mylyn, and PDE data
  for (i in 1:10){
    results_data[i] <- naive(data_set, param_trails, param_winnow, param_rules)
  }

}else{
  data_set <- read.csv(data_src, sep= ",")
  data_set$X <-NULL  # for JDE, mylyn, and PDE data
  results_data[1] <- tune(data_set, param_trails, param_winnow, param_rules)
}
cat(results_data)

