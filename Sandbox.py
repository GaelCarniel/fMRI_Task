from psychopy import visual, core, event
import random

from  function_Task1 import *


# Create a window
win = visual.Window(units='pix', fullscr=True, color='black');

#start_screen = visual.ImageStim(win=win,image="IMG/background.png",size=win.size,pos=(0,0));
global_obj = init(win); #Dictionnary that contains heavy objects

print(global_obj["game"]);


win.close()
core.quit()





### Backup updt

def update_belief(win,prior_belief,sampled,table,ref_table,trial,slider):
    '''This functions show the last panel (aggregated belief) and offer the possibility for the player to update his belief'''

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
                if len(grouped_belief[i]) == 1:
                    ghost = grouped_belief[i][0]; # There is only one element but [0] is necessary to ensure the good format  
                    belief = table[ghost][trial];
                    
                    #Load the correct image stim and replace the ghost tick
                    ghost_face = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief], slider.pos[1]-0.15*win.size[1])); 
                    ghost_tick.pos = (tick_positions[belief], slider.pos[1]);
                    #Draw
                    ghost_tick.draw();
                    ghost_face.draw();
                elif len(grouped_belief[i]) == 2:
                    offset = 1;
                    ghost_l = grouped_belief[i][0];
                    belief = table[ghost_l][trial];
                    
                    #Load the correct image stim and replace the ghost tick
                    ghost_face_l = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost_l]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]-0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                    ghost_tick.pos = (tick_positions[belief]-0.0065*win.size[0], slider.pos[1]);
                    #Draw
                    ghost_tick.draw();
                    ghost_face_l.draw();


                    ghost_r = grouped_belief[i][1];
                    belief = table[ghost_r][trial];
                    
                    #Load the correct image stim and replace the ghost tick
                    ghost_face_r = visual.ImageStim(win=win,image=f"IMG/{ref_table[ghost_r]}", size=(0.17*win.size[1],0.17*win.size[1]) ,pos=(tick_positions[belief]+0.09*win.size[1], slider.pos[1]-0.15*offset*win.size[1])); 
                    ghost_tick.pos = (tick_positions[belief]+0.0065*win.size[0], slider.pos[1]);
                    #Draw
                    ghost_tick.draw();
                    ghost_face_r.draw();
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