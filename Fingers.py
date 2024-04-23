import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 2, 1, 0.75, 0.5)
mpDraw = mp.solutions.drawing_utils

def findHands(frame):
    global results
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            #print(handLms.landmark)
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)


def findPosition(frame, handNo=0):

    lmList = []

    if results.multi_hand_landmarks:

        myHand = results.multi_hand_landmarks[handNo]

        for id, lm in enumerate(myHand.landmark):

            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

            if id==8:
                cv2.circle(frame, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

    return lmList

cap = cv2.VideoCapture(0)
tipIds = [4, 8, 12, 16, 20]

while True:

    success, frame = cap.read()
    findHands(frame)
    lmList = findPosition(frame)

    if len(lmList) != 0:

        fingers = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:

            fingers.append(1)

        else:

            fingers.append(0)

        for i in range(1, 5):

            if lmList[tipIds[i]][2] < lmList[tipIds[i] - 2][2]:

                fingers.append(1)

            else:

                fingers.append(0)

        totalFingers = fingers.count(1)

        if totalFingers == 0:
            h = '0'
            cv2.putText(frame, h, (100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if totalFingers == 1:
            h = '1'
            cv2.putText(frame, h, (100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if totalFingers == 2:
            h = '2'
            cv2.putText(frame, h, (100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if totalFingers == 3:
            h = '3'
            cv2.putText(frame, h, (100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if totalFingers == 4:
            h = '4'
            cv2.putText(frame, h, (100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if totalFingers == 5:
            h = '5'
            cv2.putText(frame, h, (100, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.rectangle(frame, (50, 200), (175, 270), (0, 255, 0), 2)
    cv2.imshow("Count", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break


