import cv2
import time

# Replace 'your_rtsp_url' with your actual RTSP URL
rtsp_url = 'your_rtsp_url'

# Create a VideoCapture object
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream has been opened successfully
if not cap.isOpened():
    print("Error opening video stream")

frame_rate = 0.5  # frame rate in Hz (1 frame every 2 seconds)
prev = 0  # to store time of previous frame capture

while cap.isOpened():
    time_elapsed = time.time() - prev
    ret, frame = cap.read()
    if ret and time_elapsed > 1./frame_rate:
        prev = time.time()

        # Save frame as JPEG file
        cv2.imwrite('frame-{}.jpg'.format(int(prev)), frame)
    elif not ret:
        break

# When everything done, release the video capture object
cap.release()