from psychopy import visual, event, core
from PIL import Image

# Load and convert the image to grayscale using PIL
img_colour = Image.open('IMG/Avatar7.png')
img_grey = img_colour.convert('L')

# Create a PsychoPy window
win = visual.Window([800, 800])

# Load the grayscale image into PsychoPy and set opacity to darken it slightly
image = visual.ImageStim(win, image=img_grey, opacity=1,size=(.5,.5))

# Draw and display the image
image.draw()
win.flip()

# Wait for a keypress before closing
event.waitKeys()

# Close the window
win.close()
core.quit()
