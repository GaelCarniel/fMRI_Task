rm(list=ls())

time = 10 #Has to be even 

gen_gamestate <- function(time,seed=12345){
  set.seed(seed)
  true_state = sample(rep(0:1,time/2),time) #Shuffling without replacing so half/half
  slider_ticks = 0:3 #Be careful if you change this you have to change a lot of things sorry but this is not modulable
  competence = seq(1/6,1,1/6) #Competence of the six players
  
  trustfullness = sample(competence) 
  # plot(competence,trustfullness,main="This shouldn't be correlated")
  
  mat = matrix(NA,time,6)
  mat_simple = matrix(NA,time,6)
  for (i in 1:time){
    for (p in 1:6){
      rn = runif(1);rn2 = runif(1)
      if(rn<competence[p]){
        mat_simple[i,p]=true_state[i]
        if(rn2<trustfullness[p]){
          mat[i,p] = ifelse(true_state[i],3,0) #Here I am true and reliable so very confident 0 or 3 depending on the true state
        } else{
          mat[i,p] = ifelse(true_state[i],sample(2:3,1),sample(1:0,1))  #Here I am right but unreliable so random confidence right answer
        }
      }else{
        #THIS VERSION IF YOU FAIL COMPETENCE YOU ARE WRONG 
        #mat_simple[i,p]=(true_state[i]+1)%%2 #oposite of true_state
        #THIS VERSION IF YOU FAIL COMPETENCE YOU ARE RANDOM 
        #Proba to be really wrong when wrong 2/3
        
        #THIS VERSION IF YOU FAIL COMPETENCE YOU ARE CLOSE TO RANDOM
        p_list = list(c(2/3,1/3),c(1/3,2/3)) #True 2/3 to say no | False 2/3 to say Yes It could be .5 for pure randomness
        proba = p_list[[ifelse(true_state[i],1,2)]]
        mat_simple[i,p]=sample(0:1,1,prob = proba) #random
        if(rn2<trustfullness[p]){
          mat[i,p] = ifelse(mat_simple[i,p],1,2) #Here I am wrong and reliable so not very confident 1 or 2 depending on the true state
        } else{
          mat[i,p] = ifelse(mat_simple[i,p],sample(1:0,1),sample(2:3,1)) #Here I am wrong and unreliable so random confidence
        }
      }
    }
  }
  
  tab = cbind(mat,true_state)
  tab = as.data.frame(tab)
  names(tab) = c(paste0("P",1:6),"Stim")
  
  return(tab)
}

#Experiment set
tab = gen_gamestate(time)
write.csv(tab,"Game_Schedule.csv",row.names = F)

#Training set
tab = gen_gamestate(time,seed = 987654321)
write.csv(tab,"Game_Schedule_Training.csv",row.names = F)
