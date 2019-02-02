# ProPresenter-Application-Bridge
Unofficial implementation of ProPresenter Stage Display XML Stream. Based on ProPresenter Stage Display for Python by Anthony Eden which can be found here: https://github.com/anthonyeden/ProPresenter-Stage-Display-Python/

Currently this only includes a basic UI for editing connection settings and seeing messages, as well as a Midi Show Control Output. 
This was written out of a neccessity to easily automate lighting cues from ProPresenter using a lighting software that only supported Midi Show Control and not Midi Notes.
You can write your own output code and implement it by simply changing the updateSlideNotesCurrent method in main.py

# Dependencies required:
1. Python 3.7 (Will possibly work in other versions, but was written and tested in 3.7) Will not work in python2
2. pyqt5 - https://pypi.org/project/PyQt5/
3. python-rtmidi - https://pypi.org/project/python-rtmidi/

# How it Works
The program connects to a socket provided by ProPresenter and listens for the Stage Display XML feed that is sent periodically or whenever there is new data for the stage display. This Program then parses the XML string for its individual components. Currently it only takes the Current Slide Notes field and processes what is in it. If it contains the proper syntax, it will be sent to midiProcess.py, where the command sent from the slide notes field is converted to Midi Show Control and sent out via a user set midi port.

# How to write Midi Show Control Commands in ProPresenter
1. Open the song you want to add commands to in the editor
2. On the Slide Properties tab, find the Slide Notes field
3. Enter the command you want to send in all caps. Currently supported MSC Commands are: GO, PAUSE, RESUME, ALL_OFF, GO_OFF, OPEN, and CLOSE.
4. Place a ':' after the command, leaving no spaces in between.
5. Write your data numbers. For most lighting consoles, only the GO Command needs both a Cue Number and A Cuelist number. All other commands only need a Cuelist Number to work. the ALL_OFF Command is the exception. On Onyx (Formerly Martin M-PC), the All_OFF command doesn't need anything after the ':'
6. To write GO Commands, and other commands needing more than one number, write the cue number, followed by a '-', and then write your Cuelist number. (The '-' is converted to a 00 in hex. Most lighting consoles use this to delimit between the numbers.
7. If you need to write more then one command, seperate the commands by a comma.

Example: "GO:12.3-4,OPEN:4" will send two commands,
  1. Go Cue Number 12.3 in Cuelist Number 4
  2. Open Cuelist Number 4

