# install.packages("caret")
# devtools::install_github("klainfo/DefectData")
library(DefectData)
library(caret)

results <- NULL

grid.param <-  expand.grid(trials=c(1,10,20,30,40),model=c("tree","rules"),winnow=c(TRUE,FALSE))
default.param <-  expand.grid(trials=c(1),model=c("rules"),winnow=c(FALSE))

for(system in listData[listData$EPV > 10 & listData$DefectiveRatio < 50,]$system){
  print(system)
  print(Sys.time())
  Data <- loadData(system)
  data <- Data$data
  dep <- Data$dep
  indep <- Data$indep  
  
  transformLog  <- function(y){ y <- log1p(y)}
  indep.log <- apply(data[,indep], 2, function(x) { !(min(x) < 0)})
  indep.log <- names(indep.log[which(indep.log == TRUE)])
  data[,indep.log] <- data.frame(apply(data[,indep.log], 2, transformLog))
  data[,dep] <- as.factor(ifelse(data[,dep] == "TRUE","T","F"))
  
  ctrl <- trainControl(method = "boot", number = 100, classProbs = TRUE, summaryFunction=twoClassSummary)
  
  set.seed(1234)
  optimize <- caret::train(data[,indep], data[,dep],
                           method = "C5.0",
                           trControl = ctrl, 
                           tuneGrid = grid.param,
                           metric = "ROC")  
  
  set.seed(1234)
  default <- caret::train(data[,indep], data[,dep],
                          method = "C5.0",
                          trControl = ctrl, 
                          tuneGrid = default.param,
                          metric = "ROC")  
  
  results <- rbind(results, c(optimize=max(optimize$results$ROC), default=max(default$results$ROC)))
}

results <- data.frame(results)
results$system <- listData[listData$EPV > 10 & listData$DefectiveRatio < 50,]$system
# saveRDS(results, file="C5.0.rds")
results <- readRDS(file="C5.0.rds")
results$improvement <- results$optimize-results$default