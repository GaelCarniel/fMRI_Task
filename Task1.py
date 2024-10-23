from  function_Task1 import *

##Inputs
g_delta = 10; #Initial delta (perception task)
training_delta = 15; #Constant delta only use in training
n_task = 5; #Duration of the task should be longuer than the generated stim
n_training_set = 2; #Number of training sets

#Note 7 trial 3 min
#Be careful for now there is only one game stim so training and actual phase or exactly the same states


# Create a window
win = visual.Window(units='pix', fullscr=True, color='black');

global_obj = init(win); #Dictionnary that contains heavy objects

##Object in the global env
time = min(len(global_obj["game"]["Stim"]),n_task);
len_slider = len(global_obj["slider"].ticks);
#Initiate perception task
gabor_response = 2; #initial belief to launch the loop
right = 1; #Same to launch the loop

#Start screen
if start_screen(win) == 'escape':
    time = -1;
    print("Start cancelled");

clock = core.Clock();

##PreTask finding delta
#delta_star = staircase_quest(win,n_trials=25); We don't do that now it is not important for our task yet

##Training set
write_text(win,"Training phase");
print("Training...");
t_trial = 0;
while t_trial<n_training_set:
    angles, delta_to_be_ignored = gabor_angles(gabor_response,right,global_obj["game"]["Stim"][t_trial],training_delta,len_slider);  #First automation might be more complex later
    print(f"Gabor angle {angles} delta: {g_delta}");
    gabor_response, rt = gabor_task(win,angles,.8,.2,global_obj["slider"],clock);
    print(f"Belief: {gabor_response}, RT: {rt}");
    
    #Sampling phase
    sampled = sampling_players(win,global_obj["game"],global_obj["ref"],t_trial,training = True);
    if 'escape' in sampled:
        break
    print(sampled);

    print("Update phase");
    updt = update_belief(win,gabor_response,sampled,global_obj["game"],global_obj["ref"],t_trial,global_obj["slider"],training = True);
    if updt == 'escape':
        break
    print(f"Belief updated: {updt}");
    
    #Feedback
    feedback(win,updt,angles);

    fixation_cross(win);
    core.wait(2);

    #Replay
    acc, rt = quick_replay(win,sampled,global_obj,clock,training=True);
    print("Replay:\n");
    print(f"accuracy:{acc}\nrt{rt}");

    t_trial+=1;
    print(f"\nTraining trial {t_trial}");


##Task
trial = 0;
print(f"Trial {trial}");
write_text(win,"Begining of the task");
print(f"Begining task : {clock.getTime()}");
while trial<time:
    #Perception task
    angles, g_delta = gabor_angles(gabor_response,right,global_obj["game"]["Stim"][trial],g_delta,len_slider);  #First automation might be more complex later
    print(f"Gabor angle {angles} delta: {g_delta}");
    gabor_response, rt = gabor_task(win,angles,.8,.2,global_obj["slider"],clock);
    print(f"Belief: {gabor_response}, RT: {rt}");
    
    #Response processing
    if gabor_response is not None:
        if gabor_response == 'escape':
            break
        else:
            right = check_gabor_response(gabor_response,global_obj["game"]["Stim"][trial]); #Check gabor response, will be used to update difficulty update the difficulty
            print(f"Accuracy (one shot) {right}");
    
    #Sampling phase
    sampled = sampling_players(win,global_obj["game"],global_obj["ref"],trial);
    if 'escape' in sampled:
        break
    print(sampled);

#    # Belief sampled:  #We decided not to show them one by one 
#    if show_belief(win,sampled,global_obj["game"],global_obj["ref"],trial,global_obj["slider"]) != 0:
#        break

    print("Update phase");
    updt = update_belief(win,gabor_response,sampled,global_obj["game"],global_obj["ref"],trial,global_obj["slider"]);
    if updt == 'escape':
        break
    print(f"Belief updated: {updt}");


    #Feedback
    feedback(win,updt,angles);
    
    fixation_cross(win);
    core.wait(2);

    #Replay
    acc, rt = quick_replay(win,sampled,global_obj,clock);
    print("Replay:\n");
    print(f"accuracy:{acc}\nrt{rt}");


    trial += 1;
    print(f"\nTrial {trial}");



finish_screen(win);


win.close();
core.quit();