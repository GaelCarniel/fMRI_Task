from psychopy import visual, core, event, logging

# Define the password
password = "start"

# Create a window and display message
win = visual.Window(color="black", fullscr=True)
message = visual.TextStim(win, text="Congratulation for your work!\n\nPlease, wait for the experimenter", color="white", height=0.1*win.size[1])
message.draw()
win.flip()

# Initialize variables
input_text = ""  # This will hold the user’s input

# Loop until the correct password is entered
while True:
    keys = event.waitKeys()  # Wait for a key press

    for key in keys:
        if key == "return":  # Check if 'Enter' was pressed to submit password
            if input_text == password:
                # Correct password entered
                logging.data("Experimenter password entered correctly.")
                win.close()
                core.quit()
            else:
                # Incorrect password entered
                logging.data("Incorrect password attempt.")
                input_text = ""  # Clear the input text if password is wrong
                message.text = "Incorrect password. Try again."
                message.draw()
                win.flip()
        
        elif key == "backspace":  # Handle backspace to delete the last character
            input_text = input_text[:-1]
        
        elif key == "escape":  # Allow escape to quit for emergency exit
            win.close()
            core.quit()
        
        else:
            # Add the typed character to the input text
            input_text += key

# This code will close the window and end the experiment when the password is correct
# or quit if the 'escape' key is pressed.

