/* Simple regression model
*/
model in "line-reg-simple.bug"
data in "line-reg-simple-data.R"
compile, nchains(2)
parameters in "line-reg-simple-inits-1.R", chain(1)
parameters in "line-reg-simple-inits-2.R", chain(2)
initialize
update 1000
monitor set w0
monitor set w1
monitor set sigma 
monitor set beta 
update 20000 
coda *
