import numpy as np
import pandas as pd
from psychopy import visual, event, core

def init(win, ticks=[0,1,2,3]):
    '''Instantiate the bigger objects so I do not have to do it in the middle of the experiment'''
    lbl= [''] * len(ticks);
    slider = visual.Slider(win, 
        ticks=ticks,  # The range is from 0 to 4
        labels=lbl,  # Empty labels for each tick
        granularity=1,  # Discrete steps
        style=['rating'],  # Style of the slider
        size=(0.6*win.size[0], 0.05*win.size[1]),  # Size of the slider
        pos=(0, 0));  # Position at the center
        
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
    
    question = visual.TextStim(win, text="Were these two patches aligned?",color="white", height=.05*win_height,wrapWidth=.8*win.size[0],pos=(0, 0.4*win_height));
    no_text = visual.TextStim(win, text="No", color="white", height=0.08*win.size[1],pos=(-0.4*win.size[0],0));
    yes_text = visual.TextStim(win, text="Yes", color="white", height=0.08*win.size[1],pos=(+0.4*win.size[0],0));
    
    slider.markerPos = np.random.randint(0, len(ticks));
    slider.marker.color = 'green';

    while True:
        slider.draw();
        no_text.draw(); 
        yes_text.draw(); 
        win.flip();

        keys = event.waitKeys(keyList=['y','n','escape','return']);
        
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

def check_gabor_response(gabor_response,true_state,len_slider):
    mid = len_slider//2;
    if (true_state == 1 and gabor_response > mid) or (true_state ==0 and gabor_response < mid + 1):#He was right
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
    player_list = list(ref_table.keys());
    
    image_P_left = ref_table[player_list[pl]];
    image_P_right = ref_table[player_list[pr]];

    box_left = visual.Rect(win,width = 0.3*win.size[0],height = 0.4*win.size[1],fillColor="#c8c8c8",lineColor = "#808080",lineWidth=5,pos=(-0.2*win.size[0],0.1*win.size[1]));
    box_right = visual.Rect(win,width = 0.3*win.size[0],height = 0.4*win.size[1],fillColor="#c8c8c8",lineColor = "#808080",lineWidth=5,pos=(0.2*win.size[0],0.1*win.size[1]));
    p_left = visual.ImageStim(win=win,image=f"IMG/{image_P_left}", size=(400,400) ,pos=(-0.2*win.size[0],0.15*win.size[1])); 
    p_right= visual.ImageStim(win=win,image=f"IMG/{image_P_right}", size=(400,400) ,pos=(0.2*win.size[0],0.15*win.size[1])); 
    
    text_left = visual.TextStim(win=win,text=f"Confidence: {conf_label[table[player_list[pl]][trial]]}", pos=(-0.2*win.size[0],-0.05*win.size[1]), height = 0.05*win.size[1], wrapWidth = .5*win.size[0])
    text_right= visual.TextStim(win=win,text=f"Confidence: {conf_label[table[player_list[pr]][trial]]}", pos=(0.2*win.size[0],-0.05*win.size[1]), height = 0.05*win.size[1], wrapWidth = .5*win.size[0])
    
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
            return "Stop"


def sampling_players(win,table,ref_table,trial,maxSample=3,conf_label=["High","Low","Low","High"]):
    '''Select the players to show and call the function to plot them, return the list of sampled players
    Be careful this function have to be adapted MANUALLY to the confidence array [0,1,2,3]'''
    ###Version 1 sorted by confidence
    player_list = list(ref_table.keys());
    arr = np.array(table.iloc[trial,:-1]);

    high_conf = np.where((arr==0) | (arr==3));
    low_conf = np.where((arr==1) | (arr==2));
    np.random.shuffle(high_conf);
    np.random.shuffle(low_conf);
    print(np.array(high_conf).flat);
    order = np.concatenate((np.array(high_conf).flat,np.array(low_conf).flat));#Flat ensure it is one dimensional thank you python for being so weird

    chosen = [];
    
    s = 0
    while s<maxSample and len(order)>1:  #While we still can sample
        if len(chosen) == 0:
            chosen.append(sampling_player(win,order[0],order[1],table,ref_table,trial,conf_label=conf_label));
            print(chosen);
        
        if "stop" in chosen:
            break 
        #else .pop the sampled one display the other one in the row 
        
    
    return 'escape'





