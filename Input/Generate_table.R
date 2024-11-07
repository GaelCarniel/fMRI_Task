rm(list=ls())

time = 100 #Has to be even 


halton_sequence_gen = function(i,b){#Non random
  #Generate Halton sequence of base b
  r=0;f=1
  while (i>0){
    f = f/b
    r = r +f*(i%%b)
    i = i%/%b
  }
  return(r)
}

halton_ngen = function(ngen,b,width=1,height=1){
  a=numeric(ngen)
  for (i in 1:ngen){
    a[i]=halton_sequence_gen(i,b)
  }
  return(cbind(a*width,((1:ngen)/ngen)*height))
}

gen_gamestate <- function(time,seed=12345,display_profiles=T){
  set.seed(seed)
  true_state = sample(rep(0:1,time/2),time) #Shuffling without replacing so half/half
  slider_ticks = 0:3 #Be careful if you change this you have to change a lot of things this is not modulable
  
  #Generating profiles
  coord = halton_ngen(6,3,0.7,1)
  coord[,1] = coord[,1]+0.25
  if (display_profiles){
    plot(coord,xlim=c(0,1),ylim=c(0,1),ylab="Trustfullness",xlab="Competence",main="Bots' Profile")
    # abline(h=c(0.2,0.8),col='grey')
    # abline(v=c(0.25,0.95),col='grey')
    abline(v =c(min(coord[,1]),max(coord[,1])),lty=3,col='grey')
    abline(h =c(min(coord[,2]),max(coord[,2])),lty=3,col='grey')
    
  }
  # Old
  # competence = seq(1/6,1,1/6) #Competence of the six players
  # trustfullness = sample(competence) 
  
  competence = coord[,1]
  trustfullness = coord[,2]

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
tab = gen_gamestate(time,seed = 9872)
write.csv(tab,"Game_Schedule_Training.csv",row.names = F)
