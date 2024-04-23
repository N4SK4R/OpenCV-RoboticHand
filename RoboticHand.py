import cv2 as cv
import mediapipe as mp
import numpy
import serial
import time
import math

SerialObj=serial.Serial("COM7",9600)
time.sleep(1)

cap=cv.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 2, 1, 0.8, 0.5)
mpDraw = mp.solutions.drawing_utils

def findHands(frame):
    global results
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    frameRGB=cv.GaussianBlur(frameRGB,(9,9),0)
    results = hands.process(frameRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

def findPosition(frame, handNo=0):

    lmList = []

    if results.multi_hand_landmarks:

        myHand = results.multi_hand_landmarks[handNo]

        for id, lm in enumerate(myHand.landmark):

            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            
            if id==4 or id==20 or id==8 or id==12 or id==16:
                cv.circle(frame, (cx, cy), 10, (255, 255, 255), cv.FILLED)
            
    return lmList

while True:
    _,frame =cap.read()
    findHands(frame)
    lmLIST=findPosition(frame)
      
    if len(lmLIST) != 0:
        
        y_pinky=lmLIST[20][2]-lmLIST[0][2]
        x_pinky=lmLIST[20][1]-lmLIST[0][1]
        pinky_len=math.sqrt(y_pinky**2 +x_pinky**2)
        cv.line(frame, (lmLIST[20][1], lmLIST[20][2]),(lmLIST[0][1],lmLIST[0][2]),(255, 255, 255),3)
        pinky_angle=int(numpy.interp(pinky_len,[50,170],[120,0]))
         
        y_ring=lmLIST[16][2]-lmLIST[0][2]
        x_ring=lmLIST[16][1]-lmLIST[0][1]
        ring_len=math.sqrt(y_ring**2 +x_ring**2)
        cv.line(frame, (lmLIST[16][1], lmLIST[16][2]),(lmLIST[0][1],lmLIST[0][2]),(255, 255, 255),3)
        ring_angle=int(numpy.interp(ring_len,[130,300],[120,0])) 
         
        y_middle=lmLIST[12][2]-lmLIST[0][2]
        x_middle=lmLIST[12][1]-lmLIST[0][1]
        middle_len=math.sqrt(y_middle**2 +x_middle**2)
        cv.line(frame, (lmLIST[12][1], lmLIST[12][2]),(lmLIST[0][1],lmLIST[0][2]),(255, 255, 255),3)
        middle_angle=int(numpy.interp(middle_len,[150,300],[110,0]))
         
        y_index=lmLIST[8][2]-lmLIST[0][2]
        x_index=lmLIST[8][1]-lmLIST[0][1]
        index_len=math.sqrt(y_index**2 +x_index**2)
        cv.line(frame, (lmLIST[8][1], lmLIST[8][2]),(lmLIST[0][1],lmLIST[0][2]),(255, 255, 255),3)
        index_angle=int(numpy.interp(index_len,[130,300],[100,0]))
         
        y_thumb=lmLIST[4][2]-lmLIST[1][2]
        x_thumb=lmLIST[4][1]-lmLIST[1][1]
        thumb_len=math.sqrt(y_thumb**2 +x_thumb**2)
        cv.line(frame, (lmLIST[4][1], lmLIST[4][2]),(lmLIST[1][1],lmLIST[1][2]),(255, 255, 255),3)
        thumb_angle=int(numpy.interp(thumb_len,[60,140],[90,0]))
        
        SerialObj.write(("M"+str(middle_angle)+"R"+str(ring_angle)+"P"+str(pinky_angle)+"I"+str(index_angle)+"T"+str(thumb_angle)+"\n").encode())
    

    cv.imshow("Hand Operations",frame)
    
    if cv.waitKey(3) & 0xFF == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        SerialObj.close()
        break