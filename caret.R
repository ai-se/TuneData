library(caret)
library("pROC")
difference <- function(x.1,x.2,...){
  x.1p <- do.call("paste", x.1)
  x.2p <- do.call("paste", x.2)
  x.1[! x.1p %in% x.2p, ]
}
randomSample = function(df,n) { 
  return (df[sample(nrow(df), n, replace=TRUE),])
}




SB<-function(XX){
  data <-read.csv("camel-1.2.csv", sep = ",")
  data <- data[,4:length(data)]
  data$X..bug[data$X..bug >0] <-1
  train_data<-randomSample(data,608)
  test_data<-difference(data, train_data)
  colnames(test_data)<-names(train_data)
  

  
  
  fitControl <- trainControl(method = "boot",classProbs = TRUE)
  
  gbmGrid <-  expand.grid(interaction.depth = c(1,2,3, 4,5),
                          n.trees = c(50,100,150,200,250),
                          shrinkage = 0.1,
                          n.minobsinnode = 10)
  
  
  gbmFit2 <- train(data$X..bug ~ ., data = train_data,
                   method = "gbm",
                   trControl = fitControl,
                   verbose = FALSE,
                   ## Now specify the exact models 
                   ## to evaluate:
                   tuneGrid = gbmGrid)
  prob <-predict(gbmFit2, newdata = test_data)
  out <-roc(test_data$X..bug,prob)
  result <-auc(out)
  
  
  # Default_model <-gbm(data$X..bug ~., data = test_data)
  train_X <-train_data[,1:length(train_data)-1]
  train_Y <-train_data$X..bug
  Default_model<- gbm.fit(train_X, train_Y, verbose = FALSE)
  Default_predicted <- predict(Default_model, test_data, n.trees=100)
  Default_out <-roc(test_data$X..bug,prob)
  Default_result <-auc(Default_out)
  
  return (result-Default_result)
}
# y <-SB(1)
set.seed(825)
yy <-sapply(1:100, SB)

