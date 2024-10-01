from  function_Task1 import *

# Create a window
win = visual.Window(units='pix', fullscr=True, color='black');

global_obj = init(win); #Dictionnary that contains heavy objects

##Object in the global env
time = len(global_obj["game"]["Stim"]);
#Initiate perception task
g_delta = 10; #5 #initial delta (perception task)
gabor_response = 2; #initial belief to launch the loop
right = 1; #Same to launch the loop

#Start screen
if start_screen(win) == 'escape':
    time = -1;
    print("Start cancelled");

clock = core.Clock();

trial = 0;
print(f"Trial {trial}");
len_slider = len(global_obj["slider"].ticks);

while trial<time:
    #Perception task
    angles, g_delta = gabor_angles(gabor_response,right,global_obj["game"]["Stim"][trial],g_delta,len_slider);  #First automation might be more complex later
    print(f"Gabor angle {angles} delta: {g_delta}");
    gabor_response = gabor_task(win,angles,.8,.2,global_obj["slider"]);
    print(f"Belief: {gabor_response}");

    #Response processing
    if gabor_response is not None:
        if gabor_response == 'escape':
            break
        else:
            right = check_gabor_response(gabor_response,global_obj["game"]["Stim"][trial]); #Check gabor response and update the difficulty
            print(f"Accuracy (one shot) {right}");

    #Sampling phase
    sampled = sampling_players(win,global_obj["game"],global_obj["ref"],trial);
    if 'escape' in sampled:
        break
    print(sampled);

    # Belief sampled:
    if show_belief(win,sampled,global_obj["game"],global_obj["ref"],trial,global_obj["slider"]) != 0:
        break

    print("Update phase");
    updt = update_belief(win,gabor_response,sampled,global_obj["game"],global_obj["ref"],trial,global_obj["slider"]);
    if updt == 'escape':
        break
    print(f"Belief updated: {updt}");
    
    #Feedback
    print(global_obj["game"]["Stim"]);
    feedback(win,updt,angles);

    #Replay
    acc, rt = quick_replay(win,sampled,global_obj["ref"],clock);
    print("Replay:\n");
    print(f"accuracy:{acc}\nrt{rt}");
    break

    trial += 1;
    print(f"\nTrial {trial}");


win.close();
core.quit();