import os
import time
import yaml
import cv2
import imageio
from threading import Thread

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
session_dir = os.path.join('/', 'shared', f"rec-{int(time.time())}")
os.makedirs(session_dir)

# Create GIF subdirectory
gif_dir = os.path.join(session_dir, 'gif')
os.makedirs(gif_dir)

# Set up variables for recording frames
frame_count = 0
start_time = time.time()

snap_delay = config['streams']['snap-delay']
gif_length = config['gif']['length']

# Set up variables for creating GIFs
gif_count = 0
gif_start_time = time.time()
gif_frames = []

def delete_jpgs(gif_count, frame_count):
    # Delete JPEG files used to create the current GIF
    for i in range(gif_count, frame_count):
        if i in gif_frames:
            os.remove(os.path.join(session_dir, f'{i}.jpg'))

while True:
    ret, frame = cap.read()

    # Write frame to file
    frame_path = os.path.join(session_dir, f'{frame_count}.jpg')
    cv2.imwrite(frame_path, frame)

    if time.time() - start_time >= snap_delay:
        frame_count += 1
        start_time = time.time()

        # Convert frame to RGB and add to GIF frames list
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gif_frames.append(frame_count - 1)

        # Check if it's time to create a new GIF
        if time.time() - gif_start_time >= gif_length:
            gif_start_time = time.time()

            # Create GIF from frames
            gif_path = os.path.join(gif_dir, f'{gif_count}-{frame_count-1}.gif')
            imageio.mimsave(gif_path, [cv2.cvtColor(cv2.imread(os.path.join(session_dir, f'{i}.jpg')), cv2.COLOR_BGR2RGB) for i in gif_frames], fps=config['gif']['fps'])

            # Delete JPEG files used to create the current GIF in a separate thread
            t = Thread(target=delete_jpgs, args=(gif_count, frame_count))
            t.start()

            # Reset GIF frames list and increment GIF count
            gif_count = frame_count
            gif_frames = []

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Delete any remaining JPEG files in gif_frames directory
delete_jpgs(gif_count, frame_count)

cap.release()
cv2.destroyAllWindows()
