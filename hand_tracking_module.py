import cv2 as cv
import mediapipe as mp
import time

class HandDetector:
    def __init__(self,mode = False,maxHands = 2,detectionCon = 0.5,trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
        static_image_mode=self.mode,
        max_num_hands=self.maxHands,
        min_detection_confidence=self.detectionCon,
        min_tracking_confidence=self.trackCon
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def findHands(self,frame,draw=True):
        imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        # Because MediaPipe works with RGB images
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame,handLms,self.mpHands.HAND_CONNECTIONS)
        return frame
    
    def find_position(self,frame,hand_no = 0,draw = True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(my_hand.landmark):
                    # print(id,lm)
                    h,w,c = frame.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    # print(id,cx,cy)
                    lm_list.append([id,cx,cy])
                    if draw:
                        cv.circle(frame,(cx,cy),5,(188,109,211),cv.FILLED)
        return lm_list

def main():
    ptime = 0
    ctime = 0
    cap = cv.VideoCapture(0)
    detecor = HandDetector()
    while True:
        isTrue, frame = cap.read()
        frame = cv.flip(frame,1)
        frame = detecor.findHands(frame)
        lm_list = detecor.find_position(frame)
        if len(lm_list) !=0:
            print(lm_list[4])

        if not isTrue:
            print("Failed to capture video")
            break
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(frame,f'FPS: {int(fps)}',(10,10),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,0,255),2)
        cv.imshow('Video', frame)

        if cv.waitKey(1) & 0xFF == ord('d'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()