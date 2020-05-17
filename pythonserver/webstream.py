# Webstreaming camera. A lot of inspiration from here: https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import cv2
import io
import numpy as np
import imutils

#Setting up page to show web-cam
PAGE="""\
<html>
<body style="background: url(stream.mjpg) no-repeat center center fixed; -webkit-background-size: cover; -moz-background-size: cover; -o-background-size: cover; background-size: cover;">
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    output = None
    min_area = 100

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                past_frame = None
                while True:
                    with StreamingHandler.output.condition:
                        StreamingHandler.output.condition.wait()
                        frame = StreamingHandler.output.frame
                        
                        #Used for motion detections.
                        if frame is not None: 
                            past_frame = self.handle_new_frame(frame, past_frame, self.min_area)
                        else:
                            print("No more frame")
                        
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
            
    #Function for motion detection
    def handle_new_frame(self, frame, past_frame, min_area):
        #Creating a frame
        data = np.fromstring(frame, dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        (h, w) = frame.shape[:2]
        r = 500 / float(w)
        dim = (500, int(h * r))
        frame = cv2.resize(frame, dim, cv2.INTER_AREA) # We resize the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # We apply a black & white filter
        gray = cv2.GaussianBlur(gray, (21, 21), 0) # Then we blur the picture

        # if the first frame is None, initialize it because there is no frame for comparing the current one with a previous one
        if past_frame is None:
            past_frame = gray
            return past_frame

        # check if past_frame and current have the same sizes
        (h_past_frame, w_past_frame) = past_frame.shape[:2]
        (h_current_frame, w_current_frame) = gray.shape[:2]
        if h_past_frame != h_current_frame or w_past_frame != w_current_frame: # This shouldnt occur but this is error handling
            print('Past frame and current frame do not have the same sizes {0} {1} {2} {3}'.format(h_past_frame, w_past_frame, h_current_frame, w_current_frame))
            return

        # compute the absolute difference between the current frame and first frame
        frame_detla = cv2.absdiff(past_frame, gray)
        # then apply a threshold to remove camera motion and other false positives (like light changes)
        thresh = cv2.threshold(frame_detla, 50, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue
            #print("Motion detected!")
        
            # Filename 
            filename = '/home/pi/waterpump/savedImage.jpg'
            cv2.imwrite(filename, frame)

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    def __init__(self, address, handler, output):
        handler.output = output
        super().__init__(address, handler)


#Function called from main.py
def webstream_start(s):
    try:
        camera = picamera.PiCamera(resolution='640x480', framerate=30)
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
    except Exception as e:
        picamera.PiCamera().close()
        webstream_start(s)
        
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler,output)
        server.serve_forever()
    finally:
        camera.stop_recording()
        