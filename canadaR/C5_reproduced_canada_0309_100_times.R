library(caret)
library("pROC")
library(C50)
difference <- function(x.1,x.2,...){
  x.1p <- do.call("paste", x.1)
  x.2p <- do.call("paste", x.2)
  x.1[! x.1p %in% x.2p, ]
}
randomSample = function(df,n) { 
  return (df[sample(nrow(df), n, replace=TRUE),])
}


SB<-function(datasets,result){
  datasets$bug[datasets$bug >0] <-1
  datasets$bug[datasets$bug == 0] <-0
  datasets$bug <- factor(datasets$bug, labels = c("N","Y"))
  # train_data<-randomSample(datasets,nrow(datasets))
  train_data <- datasets
  trainX <-train_data[,1:length(train_data)-1]
  trainY <-train_data$bug
  # test_data<-difference(datasets, train_data)
  # colnames(test_data)<-names(train_data)
  
  ########## Tuning Process #################
  fitControl <- trainControl(method = "boot", number = 100, classProbs = TRUE, summaryFunction = twoClassSummary)
  Grid <-  expand.grid(  .trials = c(1, 10, 20, 30, 40),
                         .winnow = c(FALSE, TRUE),
                         .model = c("tree","rules"))
  
  defaultGrid <- expand.grid(
                      .trials = c(1),
                      .winnow = c(FALSE),
                      .model = c("rules"))
  set.seed(1234)
  tuned <- train(trainX, trainY,
                method = "C5.0",
                trControl = fitControl,
                tuneGrid = Grid,
                metric = "ROC")
  
  set.seed(1234)
  default <- train(trainX, trainY,
                   method = "C5.0",
                   trControl = fitControl,
                   tuneGrid = defaultGrid,
                   metric = "ROC")
  
  # tuned_auc <- max(tuned$results$ROC)
  # default_auc <- max(default$results$ROC)
  result <- rbind(result,c(tuned=max(tuned$results$ROC), default=max(default$results$ROC)))
  return (result)
  # ########## repeats 100 times #################
  # improve <-c()
  # for( i in 1:10){
  #   train_data<-randomSample(datasets,nrow(datasets))
  #   trainX <-train_data[,1:length(train_data)-1]
  #   trainY <-train_data$bug
  #   test_data<-difference(datasets, train_data)
  #   colnames(test_data)<-names(train_data)
  #   
  #   # ########## TUNED MODEl #################
  #   # tuned_model <- C5.0(trainX, trainY, trails = Fit2$bestTune$trials, winnow = Fit2$bestTune$winnow, model = Fit2$bestTune$model)
  #   # tuned_predicted <-predict(tuned_model, newdata = test_data, type = "prob")
  #   # tuned_roc <-roc(predictor = data.frame(tuned_predicted)$Y, response = test_data$bug, levels = rev(levels(test_data$bug)))
  #   # tuned_auc <-auc(tuned_roc)
  # 
  #   ########## Default MODEl #################
  #   Default_model<- C5.0(trainX, trainY,trails=1, rules=TRUE)
  #   Default_predicted <- predict(Default_model, test_data, type = "prob")
  #   Default_roc <-roc(predictor = data.frame(Default_predicted)$Y, response = test_data$bug, levels = rev(levels(test_data$bug)))
  #   Default_auc <-auc(Default_roc)
  #   improve[i]<- (tuned_auc - Default_auc)
  # }
  # 
  # return (median(improve))  ### return median values
  
}




setwd("/Users/WeiFu/Github/Caret/dataR")
set.seed(1)
#### data ####
jm1 <- read.csv("./NASA/JM1.csv", sep= ",")
pc5 <- read.csv("./NASA/PC5.csv", sep= ",")
prop1 <- read.csv("./Proprietary/Prop-1.csv", sep = ",")
prop2 <- read.csv("./Proprietary/Prop-2.csv", sep = ",")
prop3 <- read.csv("./Proprietary/Prop-3.csv", sep = ",")
prop4 <- read.csv("./Proprietary/Prop-4.csv", sep = ",")
prop5 <- read.csv("./Proprietary/Prop-5.csv", sep = ",")
camel <-read.csv("./apache/camel-1.2.csv", sep = ",")
xalan25 <-read.csv("./apache/xalan-2.5.csv", sep= ",")
xalan26 <- read.csv("./apache/xalan-2.6.csv", sep = ",")
platform2 <- read.csv("./eclipse/platform2.0.csv", sep = ",")
platform21 <- read.csv("./eclipse/platform2.1.csv", sep = ",")
platfrom3 <- read.csv("./eclipse/platform3.0.csv", sep = ",")
debug34 <- read.csv("./eclipse/Debug3.4.csv", sep = ",")
swt34 <- read.csv("./eclipse/SWT3.4.csv", sep = ",")
jdt <- read.csv("./eclipse/JDT.csv", sep = ",")
jdt$X <-NULL
mylyn <- read.csv("./eclipse/mylyn.csv", sep = ",")
mylyn$X <-NULL
pde <- read.csv("./eclipse/PDE.csv", sep = ",")
pde$X <-NULL

mydata <- list(jm1, pc5, prop1, prop2, prop3, prop4, prop5, camel, xalan25, xalan26,
               platform2, platform21, platfrom3, debug34, swt34, jdt, mylyn, pde)
name <- c("jm1", "pc5", "prop1", "prop2", "prop3", "prop4", "prop5", "camel", "xalan25", "xalan26", "platform2", "platform21", "platfrom3", "debug34", "swt34", "jdt", "mylyn", "pde")


######grid #######

##### main ####
results_data <-NULL

for(i in 1:length(mydata)){
  print(name[i])
  print(Sys.time())
  results_data <- SB(mydata[[i]],results_data)
}

final <- data.frame(results_data,name,results_data[,1]-results_data[,2])
names(final) <- c("tuned","default","data_set","improvement")
boxplot(final$improvement, ylim=c(0,0.5) )
