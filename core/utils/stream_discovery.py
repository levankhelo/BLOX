import cv2
import yaml

def discover_stream():
    # Load configuration
    with open('/config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Check if USB camera is available
    if config.get('streams', {}).get('usb', False):
        found_camera = False
        for i in range(4):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                found_camera = True
                break
        if found_camera:
            return cap

    # Check if RTSP stream is available
    rtsp_config = config.get('streams', {}).get('rtsp', {})
    if rtsp_config.get('enabled', False):
        rtsp_address = rtsp_config.get('address', None)
        if rtsp_address:
            cap = cv2.VideoCapture(rtsp_address)
            if cap.isOpened():
                return cap

    # Try default camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        return cap

    # No available camera or stream
    raise ValueError('No available camera or stream')
