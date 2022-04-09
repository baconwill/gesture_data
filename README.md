
# Project Title



Hey everyone! This program uses MediaPipe and your camera to get tracking data of your hand poses for ASL recognition.

Quick Disclamer:
--
    The number frames recorded (often refered to as variable 'frame_count') is hardcoded at 10 
    and isn't in the adjustable settings. If you would like to modify this for your own use, 
    I don't care, please do what you want, however I request that any data sent to me 
    have 'frame_count' set to 10.


Setup:
------
	
	0. clone the repository (or just download project)

	1. If you don't have python installed please do that (my version=3.9.7)

	2. Install mediapipe for python - https://google.github.io/mediapipe/getting_started/python.html 

	3. I'm pretty sure the rest of the packages are either already installed or can be gotten 
       easily with pip or homebrew but if not just tell me and I'll do something



Running:
-------

	1. Look up a video of the ASL letter you want to sign (some have movement)

	2. Open config.settings in a text editor and change the parameters how you want:

	  - parent_directory: the directory that houses all the dat

	  - gesture: label of the sign you want to do and also the name of the subdirectory for 
        that letter

	  - number_of_vids: number of videos you want to record in this session 
		(Note: Its often better to do a higher frequency of shorter sessions so you 
        get a little break)

	  - video_source: the number of the capture device on your computer, usually its 0 but play
        around with it especially if you have an external webcam

	  - setup_check: boolean value (True or False) that, when set to True, won't save any 
        data captured and is useful for making sure you're setup is working properly
		(Note: recommended to start with this set to True and change when you're ready to record)

	3. If you did steps 1 and 2 I'm assuming you know where the repository is located. 
       Please enter the repository.
	   In your terminal type: cd EXAMPLE_PATH/gesture_data
	   (Note: syntax may be different on windows, type cd EXAMPLE_PATH\gesture_data)

	4. When you're ready (and in the right directory) type: 
       'python data_collection.py' (without the quotation marks) to start


After:
------
    Please just send me the data folder, it's small and I promise you 
    it's easier if I deal with it on my end.

    Preferred: baconwil@gmail.com

    but send it how you want :)
	





