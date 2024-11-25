from  function_Task1 import *

##Inputs
g_delta = 8; #Initial delta (perception task)
training_delta = 15; #Constant delta only use in training
n_task = 60; #Duration of the task should be longuer than the generated stim
n_training_set = 5; #Number of training sets
sample_all=True

#Note 7 trial 3 min minimum

#GUI
dialog = gui.Dlg(title="Information");
dialog.addText('Participant ID:');
dialog.addField('Participant_ID');
pat_id = dialog.show()['Participant_ID'];

# Create a window
win = visual.Window(units='pix', fullscr=True, color='black',monitor='testMonitor');#Test monitor only here to suppress the remaining warning
win.mouseVisible=False;

global_obj = init(win); #Dictionnary that contains heavy objects

##Object in the global env
time = min(len(global_obj["game"]["Stim"]),n_task);#The first trial are read from the same stim (for now)
len_slider = len(global_obj["slider"].ticks);
#Saving dataframe
data_to_save = [];
events_to_save = [];
#events = pd.DataFrame(columns=["Phase","Trial","Time","Keys"]); #Later

#Initiate perception task
gabor_response = 2; #initial belief to launch the loop
right = 1; #Same to launch the loop

#Start screen
if dialog.OK:
    if start_screen(win) == 'escape':
        time = -1;
        print("Start cancelled");

clock = core.Clock();

#Prepare logs
logging.setDefaultClock(clock);
abs_time=core.getAbsTime();
log_filename = f"Output/Logs/{abs_time}_{pat_id}.txt";
print(log_filename);
logging.LogFile(log_filename, level=logging.INFO);  # Log to a file

logging.info(f'EXPERIMENT STARTED');

##PreTask finding delta
#logging.info(f'staircase_quest: begin, time: {clock.getTime()}');
#delta_star = staircase_quest(win,n_trials=25); We don't do that now it is not important for our task yet
#logging.info(f'staircase_quest: end, time: {clock.getTime()}');
##Training set
t_trial = 0;
if t_trial<n_training_set and dialog.OK:
    write_text(win,"Training phase");
    print("Training...");
    logging.info(f'TRAINING SET: begin, time: {clock.getTime()}');
while t_trial<n_training_set and dialog.OK:
    logging.info(f'Training trial {t_trial}: begin, time: {clock.getTime()}');
    angles, delta_to_be_ignored = gabor_angles(gabor_response,right,global_obj["game_training"]["Stim"][t_trial],training_delta,len_slider);  #First automation might be more complex later
    print(f"Gabor angle {angles} delta: {g_delta}");
    gabor_response, g_rt = gabor_task(win,angles,.8,.2,global_obj["slider"],clock);
    print(f"Belief: {gabor_response}, RT: {g_rt}");

    #Response processing
    if gabor_response is not None:
        if gabor_response == 'escape':
            break
        else:
            right = check_gabor_response(gabor_response,global_obj["game_training"]["Stim"][t_trial]); #Check gabor response, will be used to update difficulty update the difficulty

    #Sampling phase
    sampled = sampling_players(win,global_obj["game_training"],global_obj["ref_bis"],t_trial,training = True,sample_all=sample_all);
    if 'escape' in sampled:
        break
    print(sampled);

    print("Update phase");
    updt = update_belief(win,gabor_response,sampled,global_obj["game_training"],global_obj["ref_bis"],t_trial,global_obj["slider"],training = True);
    if updt == 'escape':
        break
    print(f"Belief updated: {updt}");
    
    #Feedback
    right_updt = feedback(win,updt,angles);

    fixation_cross(win);
    core.wait(2);

    #Replay
    acc, rt, replay_order, replay_images = quick_replay(win,sampled,global_obj['ref_bis'],global_obj['intruders'],clock,training=True,intruder_p=0);#No intruder they do not know who they are playing with
    print("Replay:\n");
    print(f"accuracy:{acc}\nrt{rt}");

    #Save
    data_to_save.append(['Training',t_trial,training_delta,angles,gabor_response,g_rt,right,updt,right_updt,acc,rt,replay_order,replay_images,sampled]);

    logging.info(f'Training trial {t_trial}: begin, time: {clock.getTime()}');
    t_trial+=1;
    print(f"\nTraining trial {t_trial}");

logging.info(f'TRAINING SET: end, time: {clock.getTime()}');

##Presentation of other players
if dialog.OK:
    print(f"Begining show others : {clock.getTime()}");
    logging.info(f'Player presentation: begin, time: {clock.getTime()}');
    out = presentation_off_others(win,global_obj["ref"]);
    logging.info(f'Player presentation: end, time: {clock.getTime()}');
    if out == 'escape':
        time=0;
    print(f"End show others : {clock.getTime()}");

##Task
trial = 0;
print(f"Trial {trial}");
if dialog.OK:
    write_text(win,"Begining of the task");
    print(f"Begining task : {clock.getTime()}");
    logging.info(f'Trial {trial}: begin, time: {clock.getTime()}');
while trial < time and dialog.OK:
    #Perception task
    angles, ng_delta = gabor_angles(gabor_response,right,global_obj["game"]["Stim"][trial],g_delta,len_slider);  #First automation might be more complex later
    print(f"Gabor angle {angles} delta: {g_delta}");
    gabor_response, g_rt = gabor_task(win,angles,.8,.2,global_obj["slider"],clock);
    print(f"Belief: {gabor_response}, RT: {g_rt}");
    
    #Response processing
    if gabor_response is not None:
        if gabor_response == 'escape':
            break
        else:
            right = check_gabor_response(gabor_response,global_obj["game"]["Stim"][trial]); #Check gabor response, will be used to update difficulty update the difficulty
            print(f"Accuracy (one shot) {right}");
    
    #Sampling phase
    sampled = sampling_players(win,global_obj["game"],global_obj["ref"],trial,sample_all=sample_all);
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
    right_updt = feedback(win,updt,angles);
    
    fixation_cross(win);
    core.wait(2);

    #Replay
    acc, rt, replay_order, replay_images = quick_replay(win,sampled,global_obj['ref'],global_obj['intruders'],clock);
    print("Replay:\n");
    print(f"accuracy:{acc}\nrt{rt}");

    #Save
    data_to_save.append(['Experiment',trial,g_delta,angles,gabor_response,g_rt,right,updt,right_updt,acc,rt,replay_order,replay_images,sampled]);
    g_delta = ng_delta;

    if trial == 20:
        logging.info(f"Pause start");
        pause(win);
        logging.info(f"Pause end")


    trial += 1;
    print(f"\nTrial {trial}");

logging.info(f'Trial {trial}: end, time: {clock.getTime()}');
#Create csv
abs_time=core.getAbsTime();
save_df = pd.DataFrame(data_to_save,columns=["Phase", "Trial","Delta","Gabor_Angles","Belief_alone","Gabor_RT","Gabor_Acc","Updated_belief","Gabor_Acc_Updated","Replay_Acc","Replay_RT","Replay_Order","Replay_Images","Sampled"]);
save_df.to_csv(f"Output/{abs_time}_{pat_id}.csv");#Adding the time to make sure it is unique

finish_screen(win);

#Save the logs
logging.info(f"EXPERIMENT ENDED, time: {clock.getTime()}")
logging.flush()  # Save the logs

#Save the logs
#call_the_experimenter(win; #A function that ask to call the experimenter only unlockable with a series of keys press (password) to code

win.close();
core.quit();