import cv2
import time
import os
import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from paths import image_proc_dir, img_checkpoint_dir, input_image_dir, img_proc_dir
sys.path.append(img_proc_dir)
from identifier import ImageClassifier
from speak import speak
from tqdm import tqdm
# Replace 'your_rtsp_url' with your actual RTSP URL
rtsp_url = 'rtsp://192.168.1.10:554/user=admin&password=&channel=1&stream=1.sdp?'

# Create a VideoCapture object
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream has been opened successfully
if not cap.isOpened():
    print("Error opening video stream")

frame_rate = 0.5  # frame rate in Hz (1 frame every 2 seconds)
prev = 0  # to store time of previous frame capture
classifier = ImageClassifier(os.path.join(img_checkpoint_dir, 'tree_classifier.pkl'))

while cap.isOpened():
    time_elapsed = time.time() - prev
    ret, frame = cap.read()
    if ret and time_elapsed > 1./frame_rate:
        prev = time.time()

        # Save frame as JPEG file
        cv2.imwrite(os.path.join(input_image_dir,'frame-{}.jpg'.format(int(prev))), frame)
        category = classifier.identify(os.path.join(image_proc_dir, 'frame-{}.jpg'.format(int(prev))))
        print(category)
    elif not ret:
        break

# When everything done, release the video capture object
cap.release()