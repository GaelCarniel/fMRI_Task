from psychopy import visual, core, event

# Create the window
win = visual.Window(
    units='pix', fullscr=True, color='black', monitor='testMonitor'
)

gabor = visual.GratingStim(win=win,
        tex="sin",            # sine wave grating
        mask="gauss",         # Gaussian mask
        sf=0.1,              # spatial frequency
        ori=0,               # orientation in degrees
        size=600,             # size of the Gabor patch
        contrast=0.2);         # contrast of the Gabor patch
gabor.draw()
win.flip()

event.waitKeys()

# Close the window and quit
win.close()
core.quit()

