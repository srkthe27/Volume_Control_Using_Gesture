import time
import math
import numpy as np
import cv2 as cv
import mediapipe as mp
import hand_tracking_module as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

w_cam, h_cam = 640, 480
ptime = 0

device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

detector = htm.HandDetector(detectionCon=0.7)

cap = cv.VideoCapture(0)
cap.set(3,w_cam)
cap.set(4,h_cam)
vol = 0
vol_bar = 400
vol_percentage = 0

while True:
    isTrue,img = cap.read()
    
    img = detector.findHands(img)
    lm_list = detector.find_position(img,draw=False)

    if len(lm_list) !=0:
        # print(lm_list[4],lm_list[8])
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        c_x, c_y = (x1+x2)//2, (y1+y2)//2

        cv.circle(img,(x1,y1),15,(255,0,255),cv.FILLED)
        cv.circle(img,(x2,y2),15,(255,0,255),cv.FILLED)
        cv.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv.circle(img,(c_x,c_y),15,(255,0,255),cv.FILLED)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        # Hand range 50 - 300
        # Volume range -65.25 - 0.0
        vol = np.interp(length,[50,300],[min_vol,max_vol])
        vol_bar = np.interp(length,[50,300],[400,150])
        vol_percentage = np.interp(length,[50,300],[0,100])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv.circle(img,(c_x,c_y),15,(255,0,0),cv.FILLED)
    cv.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv.rectangle(img,(50,int(vol_bar)),(85,400),(0,255,0),cv.FILLED)
    cv.putText(img,f'{int(vol_percentage)} %',(40,450),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,245),2)

    if not isTrue:
        print("Videosource or webcam is  not found")
        break
    img = cv.flip(img,1)
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    cv.putText(img,f'FPS: {int(fps)}',(10,10),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,255),2)
    cv.imshow("Video",img)
    
    if cv.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv.destroyAllWindows()