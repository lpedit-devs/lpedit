#!/usr/bin/Rscript
library(stats)
library(methods)

## declare variables
method = 'try1'
species = 'scerevisiae'
experiment = 'source-compare'
value = 'f1score'
assumptionsValid = TRUE

# load csv files
fileName <- paste(paste(experiment,species,method,value,sep='_'),'.csv',sep='')
filePath <- paste("./anovas/",fileName,sep="")
simulation <- read.table(filePath, header=T, sep=",")
attach(simulation)
print(names(simulation))

## test for normality (null distn is that data are normal)
normalityGO <- shapiro.test(score[dsource=="go"])
normalityGOPval <- normalityGO[[2]]
normalityPubs <- shapiro.test(score[dsource=="pubs"])
normalityPubsPval <- normalityPubs[[2]]
normalityGOPubs <- shapiro.test(score[dsource=="go-pubs"])
normalityGOPubsPval <- normalityGOPubs[[2]]

if(normalityGOPval < 0.05){
  print(paste('GO NOT Gaussian distributed',round(normalityGOPval,4),sep=' - '))
  assumptionsValid <- FALSE
}

if(normalityPubsPval < 0.05){
  print(paste('Pubs NOT Gaussian distributed',round(normalityPubsPval,4),sep=' - '))
  assumptionsValid <- FALSE
}

if(normalityPubsPval < 0.05){
  print(paste('GO-Pubs NOT Gaussian distributed',round(normalityGOPubsPval,4),sep=' - '))
  assumptionsValid <- FALSE
}

## test for equality of variance (null distn is that data are normal)
varianceTest <- bartlett.test(score~dsource)
varianceTestPval <- varianceTest[[3]]

if(varianceTest <-  0.05){
  print(paste('equality of variance does NOT hold among the groups',round(varianceTestPval,4),sep=' - '))
  assumptionsValid <- FALSE
}
