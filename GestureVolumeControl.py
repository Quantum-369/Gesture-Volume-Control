import math

import cv2
import time
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###width and height
wcam,hcam=640,480

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime=0

detector = htm.Handdetector()

#### code pasted from github
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None) # 0 leads to volum 100\
minvol = volrange[0]
maxvol = volrange[1]
vol=0
volbar=400
while True:
    ret, frame = cap.read()
    # detect hands
    frame = detector.findhands(frame)
    #call findposition method for land mark list
    lmlist=detector.findposition(frame,draw=False)
    # print only if lmlist is not zero
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8]) # since we are controlling our volume with two points i.e index point and thumb point


        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        # get centre of the line
        cx,cy =(x1+x2)//2,(y1+y2)//2
        # drawing circles over the points
        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        # find the length of the line
        length = math.hypot(x2-x1,y2-y1)

        # Hand range is between 20 to 280
        # volume range -65 to 0
        vol = np.interp(length,[20,300],[minvol,maxvol])
        volbar=np.interp(length,[20,300],[400,150])
        print(int(length),int(vol))
        # passing the vol to volume.setmaster volume
        volume.SetMasterVolumeLevel(vol, None)

        # we will draw the volume bar on side of the frame
        cv2.rectangle(frame,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(frame,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)


        # draw line between two points
        cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(frame,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    cv2.imshow("FRAME",frame)
    if ord('v') == cv2.waitKey(1) & 0xFF:  # escape key waiting
        break
cap.release()
cv2.destroyAllWindows()