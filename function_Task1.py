import numpy as np
import pandas as pd
from psychopy import visual, event, core
import collections


def init(win, ticks=[0,1,2,3]):
    '''Instantiate the bigger objects so I do not have to do it in the middle of the experiment'''
    lbl= [''] * len(ticks);
    slider = visual.Slider(win, 
        ticks=ticks,  # The range is from 0 to 3
        labels=lbl,  # Empty labels for each tick
        granularity=1,  # Discrete steps
        style=['rating'],  # Style of the slider
        size=(0.6*win.size[0], 0.05*win.size[1]),  # Size of the slider
        pos=(0, 0));  # Position at the center
    slider.marker.color = 'green';

        
    ### Read inputs
    game_schedule = pd.read_csv("Input/Game_Schedule.csv");
    #with open('Input/reference.json', 'r') as json_file:
    #    ref_table = json.load(json_file); #Sadly cannot do that because I would've to pip install json but on pavlovia it might not be possible
    with open('Input/reference.json', 'r') as file:
        json_string = file.read()
    ref_table = eval(json_string)

    dictionary = {"slider":slider,"game":game_schedule,"ref":ref_table};
    return dictionary


def gabor_task(win,angles,tstim,tvoid,slider,max_resp_time=5,sf = .05,size=400,contrast=1.0):
    '''Gabor task with predefined parameters'''

    if np.isscalar(angles):
        angles = [angles,angles];
    if np.isscalar(sf):
        sf = [sf,sf];

    win_height = win.size[1]

    ### Instantiate gabor object I think it's quick enough not to be in init()
    gabor = visual.GratingStim(win=win,
        tex="sin",            # sine wave grating
        mask="gauss",         # Gaussian mask
        sf=sf,              # spatial frequency
        ori=angles[0],               # orientation in degrees
        size=size,             # size of the Gabor patch
        contrast=contrast);         # contrast of the Gabor patch

    #Display gabor patches
    gabor.draw();
    win.flip();
    core.wait(tstim);
    
    win.flip();
    core.wait(tvoid);
    
    gabor.ori=angles[1];
    gabor.draw();
    win.flip();
    core.wait(tstim);


    ### Perception task response
    ticks = slider.ticks; #Get ticks from the slider object
    
    question = visual.TextStim(win, text="Were these two patches aligned?",color="white", height=.08*win_height,wrapWidth=.8*win.size[0],pos=(0, 0.4*win_height));
    no_text = visual.TextStim(win, text="No", color="white", height=0.08*win.size[1],pos=(-0.4*win.size[0],0));
    yes_text = visual.TextStim(win, text="Yes", color="white", height=0.08*win.size[1],pos=(+0.4*win.size[0],0));
    
    slider.markerPos = np.random.randint(0, len(ticks));

    while True:
        question.draw();
        slider.draw();
        no_text.draw(); 
        yes_text.draw(); 
        win.flip();

        keys = event.waitKeys(keyList=['y','n','escape','return']);
        print(keys);
        
        if 'escape' in keys:
            return 'escape'
        elif 'return' in keys:
            return slider.markerPos
        elif 'y' in keys and slider.markerPos < max(ticks):
            slider.markerPos += 1;
        elif 'n' in keys and slider.markerPos > min(ticks):
            slider.markerPos -= 1;
    win.flip();

    return slider.markerPos

def check_gabor_response(gabor_response,true_state,ticks=[0,1,2,3]):
    '''Check if the first answer is correct'''
    len_slider = len(ticks);
    mid = ticks[len_slider//2];#By default 2
    if (true_state == 1 and gabor_response >= mid) or (true_state ==0 and gabor_response < mid):#He was right
        return 1
    else:
        return 0

def gabor_angles(past_belief,right_before,true_state,delta,len_slider,jump=2):
    '''Define gabor angle with adaptative difficulty: (First automation might be more complex later)'''
    mid = len_slider//2;
    angle1 = np.random.randint(0,361);
    
    #Difficulty update
    if right_before == 1:#He was right
        if past_belief not in [mid,mid+1]: #If he is confident enough
            if delta>3:
                delta -= jump;
    else:
        delta += jump;

    if true_state==1:
        return [angle1,angle1],delta
    else:
        sign = np.random.choice([-1,1]);
        angle2 = (angle1 + sign*delta)%360;
        return [angle1,angle2],delta


def sampling_player(win,pl,pr,table,ref_table,trial,conf_label=["High","Low","Low","High"]):
    '''Display the panel for sampling selection (no randomisation here)'''
    player_list = list(ref_table.keys());
    
    image_P_left = ref_table[player_list[pl]];
    image_P_right = ref_table[player_list[pr]];

    box_left = visual.Rect(win,width = 0.3*win.size[0],height = 0.4*win.size[1],fillColor="#c8c8c8",lineColor = "#808080",lineWidth=5,pos=(-0.2*win.size[0],0.1*win.size[1]));
    box_right = visual.Rect(win,width = 0.3*win.size[0],height = 0.4*win.size[1],fillColor="#c8c8c8",lineColor = "#808080",lineWidth=5,pos=(0.2*win.size[0],0.1*win.size[1]));
    p_left = visual.ImageStim(win=win,image=f"IMG/{image_P_left}", size=(0.27*win.size[1],0.27*win.size[1]) ,pos=(-0.2*win.size[0],0.15*win.size[1])); 
    p_right= visual.ImageStim(win=win,image=f"IMG/{image_P_right}", size=(0.27*win.size[1],0.27*win.size[1]) ,pos=(0.2*win.size[0],0.15*win.size[1])); 
    
    text_left = visual.TextStim(win=win,text=f"Confidence: {conf_label[table[player_list[pl]][trial]]}", bold= True, pos=(-0.2*win.size[0],-0.05*win.size[1]), height = 0.05*win.size[1], wrapWidth = .5*win.size[0])
    text_right= visual.TextStim(win=win,text=f"Confidence: {conf_label[table[player_list[pr]][trial]]}", bold= True, pos=(0.2*win.size[0],-0.05*win.size[1]), height = 0.05*win.size[1], wrapWidth = .5*win.size[0])
    
    box_lchoice = visual.Rect(win,width = 0.1*win.size[0],height = 0.08*win.size[1],fillColor="grey",lineColor = "darkgrey",lineWidth=5,pos=(-0.2*win.size[0],-0.2*win.size[1]));
    text_lchoice = visual.TextStim(win=win,text = "Select",height=0.05*win.size[1],pos=(-0.2*win.size[0],-0.2*win.size[1]));
    box_rchoice = visual.Rect(win,width = 0.1*win.size[0],height = 0.08*win.size[1],fillColor="grey",lineColor = "darkgrey",lineWidth=5,pos=(0.2*win.size[0],-0.2*win.size[1]));
    text_rchoice = visual.TextStim(win=win,text = "Select",height=0.05*win.size[1],pos=(0.2*win.size[0],-0.2*win.size[1]));
    box_nochoice = visual.Rect(win,width = 0.1*win.size[0],height = 0.08*win.size[1],fillColor="grey",lineColor = "darkgrey",lineWidth=5,pos=(0,-0.35*win.size[1]));
    text_nochoice = visual.TextStim(win=win,text = "Stop",height=0.05*win.size[1],pos=(0,-0.35*win.size[1]));
    
    feedback_objects = {
        "lchoice": visual.Rect(win, width=0.12*win.size[0], height=0.1*win.size[1], fillColor="white", lineColor="white", lineWidth=5, pos=(-0.2*win.size[0], -0.2*win.size[1])),
        "rchoice": visual.Rect(win, width=0.12*win.size[0], height=0.1*win.size[1], fillColor="white", lineColor="white", lineWidth=5, pos=(0.2*win.size[0], -0.2*win.size[1])),
        "nochoice": visual.Rect(win, width=0.12*win.size[0], height=0.1*win.size[1], fillColor="white", lineColor="white", lineWidth=5, pos=(0, -0.35*win.size[1]))
    } 


    while True:
        box_left.draw();
        p_left.draw();
        text_left.draw();
        box_lchoice.draw();
        text_lchoice.draw();
        box_right.draw();
        p_right.draw();
        text_right.draw();
        box_rchoice.draw();
        text_rchoice.draw();
        box_nochoice.draw();
        text_nochoice.draw();
        win.flip();

        keys = event.waitKeys(keyList=['escape','return','y','n','h']);
        
        if 'escape' in keys:
            return 'escape'
        elif 'return' in keys:
            return 'return'
        elif 'y' in keys:
            print("left");
            feedback_objects["lchoice"].draw();
            box_left.draw();
            p_left.draw();
            text_left.draw();
            box_lchoice.draw();
            text_lchoice.draw();
            box_right.draw();
            p_right.draw();
            text_right.draw();
            box_rchoice.draw();
            text_rchoice.draw();
            box_nochoice.draw();
            text_nochoice.draw();
            win.flip();
            core.wait(0.15);
            return player_list[pl]
        elif 'n' in keys:
            print("right");
            feedback_objects["rchoice"].draw();
            box_left.draw();
            p_left.draw();
            text_left.draw();
            box_lchoice.draw();
            text_lchoice.draw();
            box_right.draw();
            p_right.draw();
            text_right.draw();
            box_rchoice.draw();
            text_rchoice.draw();
            box_nochoice.draw();
            text_nochoice.draw();
            win.flip();
            core.wait(0.15);
            return player_list[pr]
        elif 'h' in keys:
            feedback_objects["nochoice"].draw();
            box_left.draw();
            p_left.draw();
            text_left.draw();
            box_lchoice.draw();
            text_lchoice.draw();
            box_right.draw();
            p_right.draw();
            text_right.draw();
            box_rchoice.draw();
            text_rchoice.draw();
            box_nochoice.draw();
            text_nochoice.draw();
            win.flip();
            core.wait(0.15);
            return "stop"


def sampling_players(win,table,ref_table,trial,maxSample=3,conf_label=["High","Low","Low","High"]):
    '''Select the players to show and call the function to plot them, return the list of sampled players
    Be careful this function have to be adapted MANUALLY to the confidence array [0,1,2,3]'''
    ###Version 1 sorted by confidence
    player_list = list(ref_table.keys());
    arr = np.array(table.iloc[trial,:-1]);

    high_conf = np.where((arr==0) | (arr==3));
    low_conf = np.where((arr==1) | (arr==2));
    order = np.concatenate((np.array(high_conf).flat,np.array(low_conf).flat));#Flat ensure it is one dimensional thank you python for being so weird
    
    leftright = [0,1]; #Who's gonna be left
    chosen = [];
    s = 0;
    while s<maxSample and len(order)>1:  #While we still can sample
        np.random.shuffle(leftright);
        new_sampled =sampling_player(win,order[leftright[0]],order[leftright[1]],table,ref_table,trial,conf_label=conf_label); 
        chosen.append(new_sampled);

        if 'escape' in chosen:
            return 'escape'
        elif 'stop' in chosen:
            chosen.remove('stop');
            print("Sampling stopped");
            return chosen 
        else:
            selected_index = np.where(np.array(player_list)==new_sampled);
            order = order[order!=selected_index[0]];  #Delete the indexes that correspond to the selected player 

        s+=1;

    return chosen



def show_belief(win,sampled,table,ref_table,trial,slider,showing_time=1):
    '''Only show the belief of the participant on a slider axis'''
    no_text = visual.TextStim(win, text="No", color="white", height=0.08*win.size[1],pos=(-0.4*win.size[0],0));
    yes_text = visual.TextStim(win, text="Yes", color="white", height=0.08*win.size[1],pos=(+0.4*win.size[0],0));
    
    # Compute the position of the ghost' ticks
    ticks = slider.ticks;
    slider_length = slider.size[0];  # The width of the slider in pixels
    tick_positions = [slider.pos[0] - slider_length / 2 + i * (slider_length / (len(ticks) - 1)) for i in range(len(ticks))];
    
    ghost_tick = visual.Rect(win, width=.015*slider_length, height=.065*slider_length, pos=(tick_positions[0], slider.pos[1]), fillColor='grey', lineColor='grey');
    slider.marker.opacity = 0; #Invisible marker here

    for i in range(len(sampled)):
        ghost = sampled[i];
        belief = table[ghost][trial];
        #Load the correct image stim
        ghost_face = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief], slider.pos[1]-0.15*win.size[1])); 


        ghost_tick.pos = (tick_positions[belief], slider.pos[1]);
        slider.draw();
        ghost_tick.draw();
        ghost_face.draw();
        no_text.draw(); 
        yes_text.draw(); 
        win.flip();
        core.wait(showing_time);
    slider.marker.opacity = 1; #Restore the opacity of the slider marker
    return 0


def update_belief(win,prior_belief,sampled,table,ref_table,trial,slider):
    '''This functions show the last panel (aggregated belief) and offer the possibility for the player to update his belief'''

    question = visual.TextStim(win, text="\nWere these two patches aligned?",color="white", height=.07*win.size[1],wrapWidth=.95*win.size[0],pos=(0, 0.35*win.size[1]));
    no_text = visual.TextStim(win, text="No", color="white", height=0.08*win.size[1],pos=(-0.4*win.size[0],0));
    yes_text = visual.TextStim(win, text="Yes", color="white", height=0.08*win.size[1],pos=(+0.4*win.size[0],0));
    
    # Compute the position of the ghost' ticks
    ticks = slider.ticks;
    slider_length = slider.size[0];  # The width of the slider in pixels
    tick_positions = [slider.pos[0] - slider_length / 2 + i * (slider_length / (len(ticks) - 1)) for i in range(len(ticks))];
    
    ghost_tick = visual.Rect(win, width=.015*slider_length, height=.065*slider_length, pos=(tick_positions[0], slider.pos[1]), fillColor='grey', lineColor='grey')

    slider.markerPos = prior_belief; #Original position of the marker
    marker = visual.Circle(win, radius=36, pos=(tick_positions[slider.getMarkerPos()], slider.pos[1]), fillColor='green', lineColor='green')




    beliefs = np.array(table[sampled].iloc[trial]);
    #Creation of a dictionnary to display players' belief
    grouped_belief = collections.defaultdict(list);
    data = table[sampled].iloc[trial];
    for key, value in data.items():
        grouped_belief[value].append(key) # I need to use a defaultdict to avoid problem of missing keys


    while True:
        #Slider draws
        slider.draw();
        no_text.draw(); 
        yes_text.draw(); 
        for i in ticks:
            if len(grouped_belief[i])>0:
                question.text = "Here is what other participants answered:\n\nNow, were these two patches aligned?";
                offset = 1;people_shawn=0;
                double = len(grouped_belief[i])//2;
                single = len(grouped_belief[i])%2;
                if double > 0:
                    for doub in range(double):#Draw pairs if needed
                        ##Left
                        ghost_l = grouped_belief[i][0+people_shawn];
                        belief = table[ghost_l][trial];
                        #Load the correct image stim and replace the ghost tick
                        ghost_face_l = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost_l]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]-0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                        ghost_tick.pos = (tick_positions[belief]-0.01*win.size[0], slider.pos[1]);
                        #Draw
                        ghost_tick.draw();
                        ghost_face_l.draw();

                        ##Right
                        ghost_r = grouped_belief[i][1+people_shawn];
                        belief = table[ghost_r][trial];
                        
                        #Load the correct image stim and replace the ghost tick
                        ghost_face_r = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost_r]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]+0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                        ghost_tick.pos = (tick_positions[belief]+0.01*win.size[0], slider.pos[1]);
                        #Draw
                        ghost_tick.draw();
                        ghost_face_r.draw();
                        
                        offset += 1.2; people_shawn+=2;
                if single > 0: #Draw the last one below
                    ghost = grouped_belief[i][0+people_shawn]; # There is only one element but [0] is necessary to ensure the good format  
                    belief = table[ghost][trial];
                    
                    #Load the correct image stim and replace the ghost tick
                    ghost_face = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief], slider.pos[1]-0.15*offset*win.size[1])); 
                    ghost_tick.pos = (tick_positions[belief], slider.pos[1]);
                    #Draw
                    ghost_tick.draw();
                    ghost_face.draw();

        question.draw();
        marker.draw();
        win.flip();
        keys = event.waitKeys(keyList=['y','n','escape','return']);
        print(keys);
        
        if 'escape' in keys:
            return 'escape'
        elif 'return' in keys:
            return slider.markerPos
        elif 'y' in keys and slider.markerPos < max(ticks):
            slider.markerPos += 1;
            marker.pos = (tick_positions[slider.getMarkerPos()], slider.pos[1]);
        elif 'n' in keys and slider.markerPos > min(ticks):
            slider.markerPos -= 1;
            marker.pos = (tick_positions[slider.getMarkerPos()], slider.pos[1]);

    return 'error'





def feedback(win,updt, angles, time = 3, ticks = [0,1,2,3]):
    '''Give feedback about the updated belief'''
    g_yes = angles[0]==angles[1]; #true state
    print("g_yes",g_yes);
    print("tick",ticks[len(ticks)//2]);
    print("updt",updt < ticks[len(ticks)//2]);
    print(updt);
    if updt < ticks[len(ticks)//2]: #Thinks it is false
        if g_yes:
            right=0;
        else:
            right=1;
    else: #Thinks it is true
        if g_yes:
            right=1;
        else:
            right=0;

    if right == 1:
        personal_feedback = visual.TextStim(win, text="You are right!", color='white', height=0.1*win.size[1], pos=(0, 0.25*win.size[1]),wrapWidth=win.size[0]*0.8);
        image_feedback = visual.ImageStim(win=win,image="IMG/Right.png", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,0));
    else:
        personal_feedback = visual.TextStim(win, text="You are wrong!", color='white', height=0.1*win.size[1], pos=(0, 0.25*win.size[1]),wrapWidth=win.size[0]*0.8);
        image_feedback = visual.ImageStim(win=win,image="IMG/Wrong.png", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,0));
        
    if g_yes:
        global_feedback = visual.TextStim(win, text="The patches were aligned", color='white', height=0.1*win.size[1], pos=(0, -0.25*win.size[1]),wrapWidth=win.size[0]*0.8);
    else:
        global_feedback = visual.TextStim(win, text="The patches weren't aligned", color='white', height=0.1*win.size[1], pos=(0, -0.25*win.size[1]),wrapWidth=win.size[0]*0.8);

    personal_feedback.draw();
    global_feedback.draw();
    image_feedback.draw()
    win.flip();
    core.wait(time);
    
    return 0



def start_screen(win):
    """
    Display the start panel
    """
    screen_size = win.size

    text = visual.TextStim(win, text="Welcome to this experiment!", color='#f5f5f5', height=80, pos=(0, 0.20*screen_size[1]),wrapWidth=screen_size[0]*0.8)
    text2 = visual.TextStim(win, text="Press 'space' if you are ready to start.", color='#f5f5f5', height=55, pos=(0, -0.2*screen_size[1]),wrapWidth=screen_size[0]*0.8)

    text.draw()
    text2.draw()
    win.flip()

    keys = event.waitKeys(keyList=['space', 'escape'])

    return keys
