from psychopy import visual, core, event
import numpy as np

# Create a window
win = visual.Window(units='pix', fullscr=True, color='black');

def init(win,size=600,contrast=1.0,sf = 0.05):
    ### Instantiate gabor object I think it's quick enough not to be in init()
    gabor = visual.GratingStim(win=win,
        tex="sin",            # sine wave grating
        mask="gauss",         # Gaussian mask
        sf=sf,              # spatial frequency
        ori=0,               # orientation in degrees
        size=size,             # size of the Gabor patch
        contrast=contrast);         # contrast of the Gabor patch
    ### Instantiate slider object 
    slider = visual.Slider(win, 
        ticks=ticks,  # The range is from 0 to 3
        labels=lbl,  # Empty labels for each tick
        granularity=1,  # Discrete steps
        style=['rating'],  # Style of the slider
        size=(0.6*win.size[0], 0.05*win.size[1]),  # Size of the slider
        pos=(0, 0));  # Position at the center
    slider.marker.color = 'green';

def gabor_angles(state,delta):
    '''Define gabor angle with a given difficulty:'''
    angle1 = np.random.randint(0,361);
    if state==1:
        return [angle1,angle1],delta
    else:
        sign = np.random.choice([-1,1]);
        angle2 = (angle1 + sign*delta)%360;
        return [angle1,angle2],delta

def dif_sequence():
    #Create a difficulty sequence series of deltas
    #Create a series of boolean for true false gabors
    
def display_gabors(win,angles,tstim,tvoid,max_resp_time=5):
    gabor.ori = angle[0];
    gabor.draw();
    win.flip();
    core.wait(t_stim);

    win.flip();
    core.wait(t_void);

    gabor.ori = angle[1];
    gabor.draw();
    win.flip();
    core.wait(t_stim);
    if angles[0]==angles[1]:
        return "aligned"
    else:
        return "not-aligned"

def question(win,slider,state,maxWait=1):
    slider.markerColor = None;
    slider.draw();
    win.flip();
    even.waitKeys(maxWait=maxWait,keyList=['a','r']);
    if keys not None:
        if ('a' in keys and state == 'aligned') or ('r' in keys and state =='not-aligned'):
            return True
        else:
            return False
    else:
        fixation_cross();
        even.waitKeys(keyList=['a','r']);
        if ('a' in keys and state == 'aligned') or ('r' in keys and state =='not-aligned'):
            return True
        else:
            return False


def fixation_cross(win):
    fixation = visual.TextStim(win, text='+', color='white', height=0.3*win.size[1]);
    fixation.draw();
    win.flip();

init(win);
while True:
    event.waitKeys();
    
    break

# Close the window
win.close();
core.quit();