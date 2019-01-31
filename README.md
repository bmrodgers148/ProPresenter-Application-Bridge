# ProPresenter-Application-Bridge
Unofficial implementation of ProPresenter Stage Display XML Stream. Based on ProPresenter Stage Display for Python by Anthony Eden which can be found here: https://github.com/anthonyeden/ProPresenter-Stage-Display-Python/

Currently this only includes a basic UI for editing connection settings and seeing messages, as well as a Midi Show Control Output. 
This was written out of a neccessity to easily automate lighting cues from ProPresenter using a lighting software that only supported Midi Show Control and not Midi Notes.
You can write your own output code and implement it by simply changing the updateSlideNotesCurrent method in main.py

# Dependencies required:
1. Python 3.7 (Will possibly work in other versions, but was written and tested in 3.7) Will not work in python2
2. pyqt5 - https://pypi.org/project/PyQt5/
3. python-rtmidi - https://pypi.org/project/python-rtmidi/

# Known Bugs
1. Connection Status does not automatically update
2. config.json can sometimes be emptied by saveAndConnect method, required it to be rewritten before running the program again.
3. Automatic reconnection is broken.
