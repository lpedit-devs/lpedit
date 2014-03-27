#!/usr/bin/Rscript


## read in the data
data <- read.csv("snakes.csv",header=TRUE,sep=',')
attach(data)
print(names(data))

## use factors where 
pop <- as.factor(pop)
region <- as.factor(region)
hab <- as.factor(hab)


## plot it
pdf("snakes-hist.pdf",height=6,width=6)
hist(mass,col='grey',main="distribution of y")
dev.off()

## specify the model
cat("model{
    # priors

    mu ~ dunif(0,5000)             # populaiton mean
    sigma ~ dunif(0,100)           # populaiton sd
    tau <- 1 / sigma * sigma       # Precision = 1 / variance


    # likelihood
    for(i in 1:N){
        mass[i] ~ dnorm(mu,tau)
     }
    }
",fill=TRUE,file="model-of-the-mean.txt")

# bundle data
jagsData <- list(mass=mass,N=length(mass))

# inits function
inits <- function(){list(mu=rnorm(1,600),
                          sigma=runif(1,1,30))}

# Parameters to estimate
params <- c("mu","sigma")

## parameters for MCMC sampling
nc <- 3       # Number of Chains
ni <- 5000    # Number of draws from posterior (for each chain)
nb <- 200     # Number of draws to discard as burn in
nt <- 2       # Thinning rate

## run it
library(R2jags)
jagsfit <- jags(jagsData,inits=inits,parameters.to.save=params,
                  model.file="model-of-the-mean.txt",n.thin=nt,
                  n.chains=nc,n.burnin=nb,n.iter=ni)

## plot the chains
jagsfit.mcmc <- as.mcmc(jagsfit)

png("model-of-the-mean-chains.png")
xyplot(jagsfit.mcmc)
dev.off()

png("model-of-the-mean-densities.png")
densityplot(jagsfit.mcmc)
dev.off()

## print results
print(jagsfit['BUGSoutput'])
print(lm(mass~1))
print(mean(mass))
