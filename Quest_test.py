from psychopy import visual, core, event, data, gui
import numpy as np


def staircase_quest(win, n_trials = 50, tstim=.8, tvoid=.2, intertrial=.5, initial_delta = 10, min_delta = 0.1, max_delta = 45, quest_thresh = 0.75,gabor_size=600,sf = 0.05,contrast=1.0):
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
        
        print(f"Orientation Gabor {same_orientation}:");
        print(gabor1.ori);
        print(gabor2.ori);

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

        print(f"Trial {trial} delta = {delta} ({same_orientation})");
    return quest.mean()


def fixation_cross(win):
    fixation = visual.TextStim(win, text='+', color='white', height=0.3*win.size[1]);
    fixation.draw();
    win.flip();

win = visual.Window(units='pix', fullscr=True, color='black');
print(staircase_quest(win,n_trials=25));

win.close()
core.quit()
