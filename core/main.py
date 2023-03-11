import os
import time
import yaml
import cv2

with open('/config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

if config['streams']['usb']:
    # Check for available USB cameras
    found_camera = False
    for i in range(4):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            found_camera = True
            break
    if not found_camera:
        raise ValueError('No available USB cameras')

else:
    # Load RTSP stream
    cap = cv2.VideoCapture(config['streams']['rtsp'])

# Create session directory
session_dir = os.path.join('/', 'shared', str(int(time.time())))
os.makedirs(session_dir)

# Set up variables for recording video
fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()

    # Write frame to file
    frame_path = os.path.join(session_dir, f'{frame_count}.jpg')
    cv2.imwrite(frame_path, frame)

    if time.time() - start_time >= 3.0:
        frame_count += 1
        start_time = time.time()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
