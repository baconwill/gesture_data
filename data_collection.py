import cv2
import numpy as np
import mediapipe as mp
from matplotlib import pyplot as plt
import os
import configparser



mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils


# function to draw mediapipe landmarks on capture frame
def draw_hand_landmarks(image, result):
	if result.multi_hand_landmarks:
		for handslms in result.multi_hand_landmarks:
			mp_drawing.draw_landmarks(image, handslms, mp_hands.HAND_CONNECTIONS,mp_drawing.DrawingSpec(color=(255,255,255), thickness=1,circle_radius=1),mp_drawing.DrawingSpec(color=(255,51,255), thickness=1,circle_radius=1))


# # get gesture classes from file
# def getClasses(gesture_file):
# 	f = open('gesture.names', 'r')
# 	classNames = f.read().split('\n')
# 	f.close()
# 	return classNames


# tells you if it is a left or right hand
def get_label(index, hand, results):
	label = None
	for idx, classification in enumerate(results.multi_handedness):
		if classification.classification[0].index == index:
			label = classification.classification[0].label
	return label


# turns the result from the landmark detector into a numpy array of:
# -------  (2 hands)x(21 landmarks)x(cartesian triplet)  ----------
# with a final shape of:
# ---------------------- (2 hands)x(63 points)  -------------------

# NOTE: hand order will always be LEFT then RIGHT in the array
#                                 ----      -----

def extract_keypoints(result):
	if result.multi_hand_landmarks:
		if len(result.multi_hand_landmarks) == 1:
			hand = result.multi_hand_landmarks[0]
			hand_label = get_label(1, hand, result)
			if hand_label == 'Left':
				left_hand = np.array([[res.x, res.y, res.z] for res in hand.landmark]).flatten() 
				right_hand = np.zeros(21*3)
			else:
				right_hand = np.array([[res.x, res.y, res.z] for res in hand.landmark]).flatten() 
				left_hand = np.zeros(21*3)
		else:
			hand1 = result.multi_hand_landmarks[0]
			hand2 = result.multi_hand_landmarks[1]
			hand_label = get_label(1, hand1, result)
			if hand_label == 'Left':
				left_hand = np.array([[res.x, res.y, res.z] for res in hand1.landmark]).flatten() 
				right_hand = np.array([[res.x, res.y, res.z] for res in hand2.landmark]).flatten() 
			else:
				right_hand = np.array([[res.x, res.y, res.z] for res in hand1.landmark]).flatten() 
				left_hand = np.array([[res.x, res.y, res.z] for res in hand2.landmark]).flatten() 
	else:
		left_hand = np.zeros(21*3)
		right_hand = np.zeros(21*3)
	landmark = np.concatenate([left_hand,right_hand])
	return landmark


# get mediapipe results from the captured frame
def mediapipe_detection(image, model):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image.flags.writeable = False
	results = model.process(image)
	image.flags.writeable = True
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	return image, results


# allows you to start capturing and labeling data from the right
# label number if there is already data in that letter
# ex: 50 videos in A (A0-A49), new captured data will automatically be
# labeled starting at A50
def get_starting_val(gesture_dir):
	vals = [i for i in os.listdir(gesture_dir) if  i != '.DS_Store']
	return len(vals)


def removeFolder(folder_dir):
	content = os.listdir(folder_dir)
	# destroy content of folder recursively
	for item in content:
		item_dir = os.path.join(folder_dir,item)
		if os.path.isdir(item_dir):
			# if it's a folder recurse through
			removeFolder(item_dir)
		else:
			# otherwise destroy and keep on chuggin'
			os.remove(item_dir)
	# destroy current folder and return
	os.rmdir(folder_dir)
	return


def captureVideo(video_dir, gesture, video_count,frame_count,video_source,setup_check):
	print("capturing video...")
	cap = cv2.VideoCapture(video_source)
	frame_num = 0
	while cap.isOpened():
		ret,frame = cap.read()
		if ret and (frame_num < frame_count):
			image, results = mediapipe_detection(frame, hands)
			draw_hand_landmarks(image,results)
			cv2.imshow('OpenCV Feed', image)
			if not setup_check:
				keypoints = extract_keypoints(results)
				frame_path = os.path.join(video_dir,"{}{}_f{}".format(gesture, video_count, frame_num))
				np.save(frame_path, keypoints)
			frame_num += 1
			# cv2.waitKey(15)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			print("frame hit")
			break
	cap.release()
	cv2.destroyAllWindows()




def captureData(gesture_dir, gesture, video_count,video_source,setup_check):
	video_dir = os.path.join(gesture_dir, gesture + str(video_count))
	if (not os.path.exists(video_dir)) and (not setup_check):
		os.mkdir(video_dir)
	print("capturing video #{}".format(video_count))
	captureVideo(video_dir, gesture, video_count,10,video_source,setup_check)



def runCaptureLoop(parent_dir, gesture, number_of_vids,video_source,setup_check):
	gesture_dir = os.path.join(parent_dir, gesture)
	if not os.path.exists(gesture_dir):
		os.mkdir(gesture_dir)
	start_val = get_starting_val(gesture_dir)
	for i in range(start_val, start_val +number_of_vids):
		captureData(gesture_dir, gesture, i, video_source,setup_check)


def getDataConfig():
	parser = configparser.ConfigParser()
	parser.read('config.settings')
	pd = parser.get('data_collection', 'parent_directory')
	g = parser.get('data_collection', 'gesture')
	nv = int(parser.get('data_collection', 'number_of_vids'))
	vs = int(parser.get('data_collection', 'video_source'))
	sc = parser.getboolean('data_collection','setup_check')
	return pd,g,nv,vs,sc


parent_directory, gesture, number_of_vids,video_source,setup_check = getDataConfig()

# if main folder doesn't exist then make it
if not os.path.exists(parent_directory):
	print("making data folder...")
	os.mkdir(parent_directory)


runCaptureLoop(parent_directory, gesture, number_of_vids, video_source, setup_check)
