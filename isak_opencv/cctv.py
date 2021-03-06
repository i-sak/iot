# import the necessary packages

from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
import requests # for http

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

# url cctv 값 보내기
# http://122.43.56.49:8080/insertCctv
cctv_url = "http://192.168.219.111:8080/insertCctv"

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# face 인식
#cascade = cv2.CascadeClassifier("../../data/haarcascades/haarcascade_frontalface_alt.xml")
cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

# eye 인식
#nested = cv2.CascadeClassifier("../../data/haarcascades/haarcascade_eye.xml")
nested = cv2.CascadeClassifier("haarcascade_eye.xml")

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    img = frame.array

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # face  인식
    rects = detect(gray, cascade)
    vis = img.copy()
    draw_rects(vis, rects, (0, 255, 0))

    # http post
    if len(rects) > 0 :
        print('사람인식')

        cv2.imshow('capFrame', img) # 윈도우 프레임에 보임
        cv2.imwrite('temp.jpg', img) # image 저장하기

        params = {'time':time.strftime('%Y%m%d%H%M%S')}
        files = {'image' : open('temp.jpg', 'rb')}

        try:
            requests.post(url=cctv_url, data=params, files=files, timeout=10)
        except requests.exceptions.Timeout:
            print('http post Timeout')
            pass

        time.sleep(2)


    # eye 인식
    if not nested.empty():
        for x1, y1, x2, y2 in rects :
            roi = gray[y1:y2, x1:x2]
            vis_roi = vis[y1:y2, x1:x2]
            subrects = detect(roi.copy(), nested)
            draw_rects(vis_roi, subrects, (255, 0, 0))

    # show the frame
    cv2.imshow("Frame", vis)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
