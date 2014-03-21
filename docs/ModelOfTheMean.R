#!/usr/bin/Rscript


## read in the data
data <- read.csv("linreg-data.csv",header=TRUE,sep=',')
attach(data)
print(names(data))
print(lm(y~1))
print(mean(y))

## plot it
pdf("linreg-data.pdf",height=6,width=6)
hist(y,col='grey',main="distribution of y")
dev.off()

sink("model.txt")
cat("model{
    # priors
   }
",fill=TRUE)
sink()
