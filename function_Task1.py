import numpy as np
import pandas as pd
from psychopy import visual, event, core, data
import collections #Manage dictionnaries easier
from PIL import Image #Apply filter on images


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

    with open('Input/reference.json', 'r') as file:
        json_string = file.read();
    ref_table = eval(json_string);
    
    with open('Input/reference_bis.json', 'r') as file:
        json_string = file.read();
    ref_table_bis = eval(json_string);
    
    with open('Input/reference_intruders.json', 'r') as file:
        json_string = file.read();
    ref_table_intruder = eval(json_string);

    refs = [ref_table,ref_table_bis];
    s = [0,1];
    np.random.shuffle(s); #Select which one of the set will be bis #Select which one of the set will be bis

    dictionary = {"slider":slider,"game":game_schedule,"ref":refs[s[0]],"ref_bis":refs[s[1]],"intruders":ref_table_intruder}; 
    return dictionary


def gabor_task(win,angles,tstim,tvoid,slider,clock,max_resp_time=5,sf = 0.05,size=600,contrast=1.0):
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
    start = clock.getTime();


    ### Perception task response
    ticks = slider.ticks; #Get ticks from the slider object
    
    question = visual.TextStim(win, text="Were these two patches aligned?",color="white", height=.08*win_height,wrapWidth=.8*win.size[0],pos=(0, 0.4*win_height));
    no_text = visual.TextStim(win, text="No", color="white", height=0.08*win.size[1],pos=(-0.4*win.size[0],0));
    yes_text = visual.TextStim(win, text="Yes", color="white", height=0.08*win.size[1],pos=(+0.4*win.size[0],0));
    
    slider.markerPos = np.random.randint(0, len(ticks));
    slider.marker.opacity = 0; #Invisible marker here

#    question.draw();
    slider.draw();
    no_text.draw(); 
    yes_text.draw(); 
    win.flip();

    keys = event.waitKeys(keyList=['a','z','e','r','escape']);
    print(keys);
    stop = clock.getTime();

    if 'escape' in keys:
        return 'escape'
    elif 'a' in keys:
        return 0, stop-start
    elif 'z' in keys:
        return 1, stop-start
    elif 'e' in keys:
        return 2, stop-start
    elif 'r' in keys:
        return 3, stop-start
    win.flip();
    slider.marker.opacity = 1;



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

def gabor_angles_alt_version(true_state,g_delta,len_slider,sd=2):
    '''Define gabor angle with different difficulty:'''
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


def sampling_player(win,pl,pr,table,ref_table,trial,conf_label=["High","Low","Low","High"],training = False):
    '''Display the panel for sampling selection (no randomisation here)'''
    player_list = list(ref_table.keys());
    
    image_P_left = ref_table[player_list[pl]];
    image_P_right = ref_table[player_list[pr]];

    box_left = visual.Rect(win,width = 0.3*win.size[0],height = 0.4*win.size[1],fillColor="#c8c8c8",lineColor = "#808080",lineWidth=5,pos=(-0.2*win.size[0],0.1*win.size[1]));
    box_right = visual.Rect(win,width = 0.3*win.size[0],height = 0.4*win.size[1],fillColor="#c8c8c8",lineColor = "#808080",lineWidth=5,pos=(0.2*win.size[0],0.1*win.size[1]));
    if training: #Images will be in black and white
        p_left_colour = Image.open(f"IMG/{image_P_left}");
        p_left_grey = p_left_colour.convert('L');
        p_left = visual.ImageStim(win=win,image=p_left_grey, size=(0.27*win.size[1],0.27*win.size[1]) ,pos=(-0.2*win.size[0],0.15*win.size[1])); 
        p_right_colour = Image.open(f"IMG/{image_P_right}");
        p_right_grey = p_right_colour.convert('L');
        p_right= visual.ImageStim(win=win,image=p_right_grey, size=(0.27*win.size[1],0.27*win.size[1]) ,pos=(0.2*win.size[0],0.15*win.size[1])); 
    else:
        p_left = visual.ImageStim(win=win,image=f"IMG/{image_P_left}", size=(0.27*win.size[1],0.27*win.size[1]) ,pos=(-0.2*win.size[0],0.15*win.size[1])); 
        p_right= visual.ImageStim(win=win,image=f"IMG/{image_P_right}", size=(0.27*win.size[1],0.27*win.size[1]) ,pos=(0.2*win.size[0],0.15*win.size[1])); 

    #text_left = visual.TextStim(win=win,text=f"Confidence: {conf_label[table[player_list[pl]][trial]]}", bold= True, pos=(-0.2*win.size[0],-0.05*win.size[1]), height = 0.05*win.size[1], wrapWidth = .5*win.size[0])
    #text_right= visual.TextStim(win=win,text=f"Confidence: {conf_label[table[player_list[pr]][trial]]}", bold= True, pos=(0.2*win.size[0],-0.05*win.size[1]), height = 0.05*win.size[1], wrapWidth = .5*win.size[0])
    
    circle_low = visual.Circle(win, radius = 0.03*win.size[1],lineWidth=0.01*win.size[1],lineColor='white',color=None);
    circle_high = visual.Circle(win, radius = 0.03*win.size[1],lineWidth=0.01*win.size[1],lineColor='white');
    
    print(conf_label[table[player_list[pl]][trial]]);
    print(conf_label[table[player_list[pr]][trial]]);
    if conf_label[table[player_list[pl]][trial]] == "High":
        text_left = visual.Circle(win, radius = 0.03*win.size[1],lineWidth=0.01*win.size[1],lineColor='#5c5c5c',color='#5c5c5c',pos=(-0.2*win.size[0],-0.05*win.size[1]));
    else:
        text_left = visual.Circle(win, radius = 0.03*win.size[1],lineWidth=0.01*win.size[1],lineColor='#5c5c5c',color=None,pos=(-0.2*win.size[0],-0.05*win.size[1]));
    if conf_label[table[player_list[pr]][trial]] == "High":
        text_right = visual.Circle(win, radius = 0.03*win.size[1],lineWidth=0.01*win.size[1],lineColor='#5c5c5c',color='#5c5c5c',pos = (0.2*win.size[0],-0.05*win.size[1]));
    else:
        text_right = visual.Circle(win, radius = 0.03*win.size[1],lineWidth=0.01*win.size[1],lineColor='#5c5c5c',color=None,pos = (0.2*win.size[0],-0.05*win.size[1]));
    
    
    
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
#        box_lchoice.draw();
#        text_lchoice.draw();
        box_right.draw();
        p_right.draw();
        text_right.draw();
#        box_rchoice.draw();
#        text_rchoice.draw();
#        box_nochoice.draw();
#        text_nochoice.draw();
        win.flip();

        keys = event.waitKeys(keyList=['escape','a','z','e','r']);
        
        if 'escape' in keys:
            return 'escape'
        elif 'a' in keys:
            print("left");
#            feedback_objects["lchoice"].draw();
            box_left.draw();
            p_left.draw();
            text_left.draw();
#            box_lchoice.draw();
#            text_lchoice.draw();
            box_right.draw();
            p_right.draw();
            text_right.draw();
#            box_rchoice.draw();
#            text_rchoice.draw();
#            box_nochoice.draw();
#            text_nochoice.draw();
            win.flip();
            core.wait(0.15);
            return player_list[pl]
        elif 'r' in keys:
            print("right");
#            feedback_objects["rchoice"].draw();
            box_left.draw();
            p_left.draw();
            text_left.draw();
#            box_lchoice.draw();
#            text_lchoice.draw();
            box_right.draw();
            p_right.draw();
            text_right.draw();
#            box_rchoice.draw();
#            text_rchoice.draw();
#            box_nochoice.draw();
#            text_nochoice.draw();
            win.flip();
            core.wait(0.15);
            return player_list[pr]
        elif 'z' in keys or 'e' in keys:
#            feedback_objects["nochoice"].draw();
            box_left.draw();
            p_left.draw();
            text_left.draw();
#            box_lchoice.draw();
#            text_lchoice.draw();
            box_right.draw();
            p_right.draw();
            text_right.draw();
#            box_rchoice.draw();
#            text_rchoice.draw();
#            box_nochoice.draw();
#            text_nochoice.draw();
            win.flip();
            core.wait(0.15);
            return "stop"

 
def sampling_players(win,table,ref_table,trial,maxSample=3,conf_label=["High","Low","Low","High"],training = False):
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
        new_sampled =sampling_player(win,order[leftright[0]],order[leftright[1]],table,ref_table,trial,conf_label=conf_label,training=training); 
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


def update_belief(win,prior_belief,sampled,table,ref_table,trial,slider,presentation_time=2,training=False):
    '''This functions show the last panel (aggregated belief) and offer the possibility for the player to update his belief'''

    question = visual.TextStim(win, text="\nWere these two patches aligned?",color="white", height=.07*win.size[1],wrapWidth=.95*win.size[0],pos=(0, 0.35*win.size[1]));
    no_text = visual.TextStim(win, text="No", color="white", height=0.08*win.size[1],pos=(-0.4*win.size[0],0));
    yes_text = visual.TextStim(win, text="Yes", color="white", height=0.08*win.size[1],pos=(+0.4*win.size[0],0));
    
    # Compute the position of the ghost' ticks
    ticks = slider.ticks;
    slider_length = slider.size[0];  # The width of the slider in pixels
    tick_positions = [slider.pos[0] - slider_length / 2 + i * (slider_length / (len(ticks) - 1)) for i in range(len(ticks))];
    
#    ghost_tick = visual.Rect(win, width=.015*slider_length, height=.065*slider_length, pos=(tick_positions[0], slider.pos[1]), fillColor='grey', lineColor='grey')
    triangle_vertices = np.array([[0, -0.5], [0.5, 0.5], [-0.5, 0.5]])*0.05*win.size[1];
    ghost_tick = visual.ShapeStim(win, vertices=triangle_vertices, fillColor='grey');
 

    slider.markerPos = prior_belief; #Original position of the marker
    
    marker = visual.Circle(win, radius=36, pos=(tick_positions[slider.getMarkerPos()], slider.pos[1]), fillColor='green', lineColor='green')#Start with a grey marker 




    beliefs = np.array(table[sampled].iloc[trial]);
    #Creation of a dictionnary to display players' belief
    grouped_belief = collections.defaultdict(list);
    data = table[sampled].iloc[trial];
    for key, value in data.items():
        grouped_belief[value].append(key) # I need to use a defaultdict to avoid problem of missing keys

    first_time=True;
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
                        if training:
                            img_colour = Image.open(f"IMG/{ref_table[ghost_l]}");
                            img_grey_l = img_colour.convert('L');
                            ghost_face_l = visual.ImageStim(win=win,image=img_grey_l, size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]-0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                        else:
                            ghost_face_l = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost_l]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]-0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                        ghost_tick.pos = (tick_positions[belief], slider.pos[1]+double*0.05*win.size[1]);
                        #Draw
                        ghost_tick.draw();
                        ghost_face_l.draw();

                        ##Right
                        ghost_r = grouped_belief[i][1+people_shawn];
                        belief = table[ghost_r][trial];
                        
                        #Load the correct image stim and replace the ghost tick
                        if training:
                            img_colour = Image.open(f"IMG/{ref_table[ghost_r]}");
                            img_grey_r = img_colour.convert('L');
                            ghost_face_r = visual.ImageStim(win=win,image=img_grey_r, size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]+0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                        else:
                            ghost_face_r = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost_r]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]+0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                        ghost_tick.pos = (tick_positions[belief], slider.pos[1]+2*(double)*0.05*win.size[1]);
                        #Draw
                        ghost_tick.draw();
                        ghost_face_r.draw();
                        
                        offset += 1.2; people_shawn+=2;
                if single > 0: #Draw the last one below
                    ghost = grouped_belief[i][0+people_shawn]; # There is only one element but [0] is necessary to ensure the good format  
                    belief = table[ghost][trial];
                    
                    #Load the correct image stim and replace the ghost tick
                    if training:
                        img_colour = Image.open(f"IMG/{ref_table[ghost]}");
                        img_grey = img_colour.convert('L');
                        ghost_face = visual.ImageStim(win=win,image=img_grey, size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief], slider.pos[1]-0.15*offset*win.size[1])); 
                    else:
                        ghost_face = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief], slider.pos[1]-0.15*offset*win.size[1])); 
                    ghost_tick.pos = ghost_tick.pos = (tick_positions[belief], slider.pos[1]+(2*double+single)*0.05*win.size[1]);
                    #Draw
                    ghost_tick.draw();
                    ghost_face.draw();

        
        if first_time:
#            question.draw();
            smoke_screen =  visual.Rect(win,width=win.size[0],height=win.size[1],fillColor='black',opacity=.5);
            marker.draw();
            smoke_screen.draw();
            win.flip();
            core.wait(presentation_time);
            first_time= False;
        else:
#            question.draw();
            marker.draw();
            win.flip();
            keys = event.waitKeys(keyList=['a','z','e','r','escape']);
            print(keys);

            if 'escape' in keys:
                return 'escape'
            elif 'a' in keys:
                return 0
            elif 'z' in keys:
                return 1
            elif 'e' in keys:
                return 2
            elif 'r' in keys:
                return 3

    return 'error' #Should never happen





def feedback(win,updt, angles, time = 3, ticks = [0,1,2,3]):
    '''Give feedback about the updated belief'''
    g_yes = angles[0]==angles[1]; #true state
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
        image_feedback = visual.ImageStim(win=win,image="IMG/Right.png", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,0.1*win.size[1]));
    else:
        personal_feedback = visual.TextStim(win, text="You are wrong!", color='white', height=0.1*win.size[1], pos=(0, 0.25*win.size[1]),wrapWidth=win.size[0]*0.8);
        image_feedback = visual.ImageStim(win=win,image="IMG/Wrong.png", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=(0,0.1*win.size[1]));
        
    if g_yes:
        global_feedback = visual.TextStim(win, text="The patches were aligned", color='white', height=0.1*win.size[1], pos=(0, -0.25*win.size[1]),wrapWidth=win.size[0]*0.8);
        image_global_feedback = visual.ImageStim(win=win,image="IMG/aligned.png", size=(0.15*win.size[1],0.25*win.size[1]) ,pos=(0,-0.2*win.size[1]));

    else:
        global_feedback = visual.TextStim(win, text="The patches weren't aligned", color='white', height=0.1*win.size[1], pos=(0, -0.25*win.size[1]),wrapWidth=win.size[0]*0.8);
        image_global_feedback = visual.ImageStim(win=win,image="IMG/not_aligned.png", size=(0.15*win.size[1],0.25*win.size[1]) ,pos=(0,-0.2*win.size[1]));
#    personal_feedback.draw();
#    global_feedback.draw();
    image_feedback.draw();
    image_global_feedback.draw();
    win.flip();
    core.wait(time);

    return 0


def quick_replay(win,sampled,ref_table,ref_intruders,clock,transition_time=1.8,training = False,intruder_p = 1/18):
    '''This shows quickly all the participants you have to click on "y" if you saw him "n" otherwise as quickly as you can'''
    #Get ready screen
#    get_ready= visual.TextStim(win, text="Did you see their opinion this round \n\nGet Ready..",color="white", height=.08*win.size[1],wrapWidth=.8*win.size[0],pos=(0, 0));
#    get_ready.draw();
#    win.flip();

    #Task 
    player_list = list(ref_table.keys());
    indexes = np.arange(0,len(player_list));
    np.random.shuffle(indexes);
    key_pressed=[];acc=[];rt=[];intruder_appeared = False;
    for i in indexes:
        start = clock.getTime()
        if intruder_appeared:
            dice = 1;
        else:
            dice = np.random.uniform(0, 1);

        if dice < intruder_p:
            intruder = np.random.choice(list(ref_intruders.values()));
            if training:
                img_colour = Image.open(f"IMG/{intruder}")
                img_grey = img_colour.convert('L')
                avatar = visual.ImageStim(win=win,image=img_grey, size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,0)); 
            else:
                avatar = visual.ImageStim(win=win,image=f"IMG/{intruder}", size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,0)); 
            intruder_appeared = True;
        else:
            player = player_list[i];
            if training:
                img_colour = Image.open(f"IMG/{ref_table[player]}")
                img_grey = img_colour.convert('L')
                avatar = visual.ImageStim(win=win,image=img_grey, size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,0)); 

            else:
                avatar = visual.ImageStim(win=win,image=f"IMG/{ref_table[player]}", size=(0.35*win.size[1],0.35*win.size[1]) ,pos=(0,0)); 
        avatar.draw();
        win.flip();
        keys = event.waitKeys(maxWait=1,keyList=['escape','a','z','e','r']);
        if keys is not None:
            key_pressed.append(keys);
            end = clock.getTime();
            rt.append(end-start);
            if dice < intruder_p:
                if 'z' in keys or 'e' in keys:
                    acc.append('detected'); #The player detected the intruder
                else:
                    acc.append('undetected'); #The player didn't detect the intruder
            else:
                if 'escape' in keys:
                    return 'escape'
                elif 'r' in keys:
                    acc.append(player in sampled); #True would be if player has been sampled
                elif 'a' in keys:
                    acc.append(player not in sampled); #True would be if player has not been sampled
            win.flip();
            core.wait(.1);
        else:
            fixation_cross(win); 
            keys = event.waitKeys(keyList=['escape','a','z','e','r']);
            end = clock.getTime();
            rt.append(end-start);
            key_pressed.append(keys);
            if dice < intruder_p:
                if 'z' in keys or 'e' in keys:
                    acc.append('detected'); #The player detected the intruder
                else:
                    acc.append('undetected'); #The player didn't detect the intruder
            else:
                if ('r' in keys and player in sampled) or ('a' in keys and player not in sampled):
                    acc.append(True);
                else:
                    acc.append(False);
#        #Print section
#        if dice>intruder_p:
#            print(f'Player {player}');
#        print(f'Dice {dice}');
#        print(f'Avatar {avatar.image}');
#        print(f'Keys {keys}');
#        print(f'Acc {acc}');


    #Mark the end of a round
    next_round = visual.TextStim(win, text="Next round",color="white", height=.08*win.size[1],wrapWidth=.8*win.size[0],pos=(0, 0));
    next_round.draw();
    win.flip()
    core.wait(transition_time);

    return acc, rt


def fixation_cross(win):
    fixation = visual.TextStim(win, text='+', color='white', height=0.3*win.size[1]);
    fixation.draw();
    win.flip();

def staircase_quest(win, n_trials = 50, tstim=.5, tvoid=.5, intertrial=.5, initial_delta = 10, min_delta = 0.1, max_delta = 45, quest_thresh = 0.75,gabor_size=600,sf = 0.05,contrast=1.0):
    quest = data.QuestHandler(startVal=initial_delta, startValSd=8, pThreshold=quest_thresh, gamma=0.5, nTrials=n_trials, minVal=min_delta, maxVal=max_delta);#gamma = by chance

    gabor1 = visual.GratingStim(win, tex="sin", mask="gauss", size=gabor_size, sf=sf, ori=0,contrast=contrast);
    gabor2 = visual.GratingStim(win, tex="sin", mask="gauss", size=gabor_size, sf=sf, ori=0,contrast=contrast);

    # Trial loop
    for trial in quest:
        delta = quest.next();
        delta = max(min(delta, max_delta), min_delta);

        # True or False gabor
        same_orientation = np.random.choice([True, False]);
        sign = np.random.choice([-1,1]);

        # Set orientations
        base_orientation = np.random.uniform(0, 180);
        gabor1.ori = base_orientation;
        gabor2.ori = base_orientation if same_orientation else base_orientation + delta*sign;

        # Show first Gabor patch
        gabor1.draw();
        win.flip();
        core.wait(tstim);  
        win.flip();
        core.wait(tvoid);  

        # Show second Gabor patch
        gabor2.draw();
        win.flip();
        core.wait(tstim);
        fixation_cross(win);
        win.flip();
        
        keys = event.waitKeys(keyList=['a', 'r', 'escape']);
        # Exit if the participant presses 'escape'
        if "escape" in keys:
            return 'escape'

        # Record response and whether it was correct
        if ('a' in keys and same_orientation) or ('r' in keys and not same_orientation):
            correct = 1;
        else:
            correct = 0;

        # Update QUEST with the correctness of the response
        quest.addResponse(correct);

        win.flip();
        core.wait(intertrial);  # Inter-trial interval

#        print(f"Trial {trial} delta = {delta} ({same_orientation})");
    return quest.mean()

def presentation_off_others(win, ref, time_limit=False , maxTime=10):
    '''Display the other 6 participant faces'''
    if len(ref) != 6:
        print("Be carful this function is only meant to display 6 participants");

    player_list = list(ref.keys());
    np.random.shuffle(player_list);
    for i in range(6):
        player = player_list[i];
        avatar = visual.ImageStim(win=win,image=f"IMG/{ref[player]}", size=(0.25*win.size[1],0.25*win.size[1]) ,pos=((0.3*(i%3)-0.3)*win.size[1],(0.3*(i//3)-(0.3/2))*win.size[1]));
        avatar.draw();
    win.flip()

    keys = 'nokeys';
    if time_limit:
        keys = event.waitKeys(maxWait=maxTime,keyList=['escape','a','z','e','r']);
    else:
        keys = event.waitKeys(keyList=['escape','a','z','e','r']);

    if 'escape' in keys:
        return 'escape'
    else:
        return 'go'


def start_screen(win):
    """
    Display the start panel
    """

    text = visual.TextStim(win, text="Welcome to this experiment!", color='#f5f5f5', height=0.1*win.size[1], pos=(0, 0.20*win.size[1]),wrapWidth=win.size[0]*0.8)
    text2 = visual.TextStim(win, text="Press 'space' if you are ready to start.", color='#f5f5f5', height=0.05*win.size[1], pos=(0, -0.2*win.size[1]),wrapWidth=win.size[0]*0.8)

    text.draw()
    text2.draw()
    win.flip()

    keys = event.waitKeys(keyList=['space', 'escape'])

    return keys

def write_text(win, text, display_time=1):
    """
    Display text 
    """
    text2print = visual.TextStim(win, text=text, color='#f5f5f5', height=0.1*win.size[1], pos=(0, 0.10*win.size[1]),wrapWidth=win.size[0]*0.8)

    text2print.draw()
    win.flip()
    core.wait(display_time);



def finish_screen(win):
    """
    Display the end panel
    """
    bg = visual.ImageStim(win=win,image="IMG/Fireworks.jpg",size = win.size,pos=(0,0));
    bg.draw();

    text = visual.TextStim(win, text="Thank you for participating!", color='white', height=0.12*win.size[1], pos=(0, -0.05*win.size[1]),wrapWidth=win.size[0]*0.95)
    text2 = visual.TextStim(win, text="Press any key to exit", color='white',height=0.08*win.size[1], pos=(0, -0.3*win.size[1]),wrapWidth=win.size[0]*0.8)
    text.draw()
    text2.draw()
    
    

    win.flip()
    
    event.waitKeys()
    return 0
