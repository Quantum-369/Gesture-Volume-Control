import cv2
import mediapipe as mp
import time

class Handdetector():
    ## intiliazations of objects
    def __init__(self,mode=False,maxhands=2,modelC=1,min_detect_confidence=0.8,min_track_confidence=0.8):
        self.mode=mode
        self.maxhands=maxhands
        self.modelC=modelC
        self.min_detect_confidence=min_detect_confidence
        self.min_track_confidence = min_track_confidence
        self.mpHands= mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxhands,self.modelC,self.min_detect_confidence,self.min_track_confidence)
        self.mpDraw = mp.solutions.drawing_utils
    # create findhands module
    def findhands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ## process the image using process fucntion
        self.results = self.hands.process(imgRGB)
        # if === true then for every point in of landmarks draw connections and return img
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                     self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
        return img
 # findpositions
    def findposition(self,img,handno =0,draw=True):

        lmlist =[] # landmark list
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):  # print id and landmark values
                # print(id,lm)
                h, w, c = img.shape  # height width and channels of frame
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return lmlist


def main():
    cap = cv2.VideoCapture(0)
    ptime = 0  # previous time
    ctime = 0  # currenttime

    detector = Handdetector()

    while True:

        ret, img = cap.read()
        img = detector.findhands(img)

        lmlist = detector.findposition(img)
        # if len(lmlist) !=0:
        #     print(lmlist[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        # write time on screen


        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(0, 255, 0), 3)

        cv2.imshow("Frames",img)
        if ord('v') == cv2.waitKey(1) & 0xFF:  # escape key waiting
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()