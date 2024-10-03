from psychopy import visual, core, event
import numpy as np

# Create a window
win = visual.Window(units='pix', fullscr=True, color='black');

# Parameters for the circle
R = 0.8  # Diameter of the circle (normalized units)
r = R / 2  # Radius of the circle

n_points = 12  # Number of points
theta_step = 2 * np.pi / n_points  # Angular step between points

D = 0.25*win.size[1];

# Create and draw 12 points equidistant on the circle
for i in range(n_points):
    theta_i = i * theta_step  # Angle for the ith point
    x = np.cos(theta_i)  # X-coordinate
    y = np.sin(theta_i)  # Y-coordinate
    
    x = x*D
    y = y*D;

    # Create a small dot at each (x, y) position
    dot = visual.Circle(win, radius=0.02*win.size[1], pos=(x, y), fillColor='white')
    dot.draw()

# Flip to display all dots on the circle
win.flip()

# Pause for a while to see the result
event.waitKeys();

# Close the window
win.close()
