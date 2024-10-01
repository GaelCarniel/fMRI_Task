from psychopy import visual, event, core

# Create the window
win = visual.Window(units='pix', fullscr=True, color='black');
print(win.size)
# Slider settings
ticks = [0, 1, 2, 3]  # Slider ticks from 0 to 3
lbl = ['', '', '', '']  # Empty labels
slider = visual.Slider(win, 
    ticks=ticks,
    labels=lbl,
    granularity=1,  # Discrete steps
    style=['rating'],  # Style of the slider
    size=(0.6*win.size[0], 0.05*win.size[1]),  # Size of the slider
    pos=(0, 0)
)

# Compute the position of the ghost' ticks
slider_length = slider.size[0]  # The width of the slider in pixels
tick_positions = [slider.pos[0] - slider_length / 2 + i * (slider_length / (len(ticks) - 1)) for i in range(len(ticks))]
print(slider_length);

# Define the grey bar (Rect) to mark the second tick
grey_bar = visual.Rect(win, width=.015*slider_length, height=.065*slider_length, pos=(tick_positions[2], slider.pos[1]), fillColor='grey', lineColor='grey')

# Main loop to display the slider and the grey bar
while True:
    # Draw slider
    slider.draw()
    
    # Draw the grey bar at the second tick
    grey_bar.draw()
    
    # Flip the window to display the content
    win.flip()

    # Break if any key is pressed
    if len(event.getKeys()) > 0:
        break

# Close the window
win.close()
core.quit()
