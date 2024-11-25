rm(list=ls())
tab= read.csv("C:/Users/gcarniel/Documents/Psycopy/fMRITask1/Input/Game_Schedule.csv")


par(mfrow=c(2,3))
for (i in 1:6){
  hist(tab[,i],breaks = seq(-.5,3.5),main=paste("Belief:",names(tab)[i]))
}


for (i in 1:6){
  c = hist(ifelse(tab[,7],tab[,i],abs(tab[,i]-3)),breaks = seq(-.5,3.5),plot=F)$counts
  barplot(c,names.arg = c("Wrong","Bit wrong","Bit right","Right"),main = paste("Accuracy",names(tab)[i]))
}


