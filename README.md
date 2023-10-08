# Python Bowling Scoreboard

This is a test project intended to mimic a bowling alley scoreboard system. The project is written in python and utilizes the TKinter import to create and modify a simple window and multiple UI elements.

Instructions for the given task can be found in Instructions.md

I've assumed a few things that were left ambiguous in the instructions. For one, I've locked all frame text entry for any frame in which a previous frame wasn't completed. This ensures the user doesn't accidentally put data into a frame farther ahead than they actually are in the game. In addition, I have enabled only the Entry areas that are valid to put data into (other than the right corner with a strike frame, since I wasn't sure what the preference was there, given that some scoreboards put the X in the top right and some in the top left). I also specifically left out an "EXIT" button in the main UI since the window already has one and I didn't want to add any UI you didn't specifically request, since I thought that might be presumptuous.

Run the program with "py Program.py"