import numpy as np
import cv2 


def empty(a):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('Trackbars') 
cv2.resizeWindow('Trackbars', 640, 240)

cv2.createTrackbar('H minimum', 'Trackbars', 0, 179, empty) #red
cv2.createTrackbar('H maximum', 'Trackbars', 18, 179, empty)
cv2.createTrackbar('S minimum', 'Trackbars', 124, 255, empty)
cv2.createTrackbar('S maximum', 'Trackbars', 225, 255, empty)
cv2.createTrackbar('V minimum', 'Trackbars', 117, 255, empty)
cv2.createTrackbar('V maximum', 'Trackbars', 201, 255, empty)

while True:
    _, frame = cap.read()
    
    hMin = cv2.getTrackbarPos('H minimum', 'Trackbars')
    hMax = cv2.getTrackbarPos('H maximum', 'Trackbars')
    sMin = cv2.getTrackbarPos('S minimum', 'Trackbars')
    sMax = cv2.getTrackbarPos('S maximum', 'Trackbars')
    vMin = cv2.getTrackbarPos('V minimum', 'Trackbars')
    vMax = cv2.getTrackbarPos('V maximum', 'Trackbars')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax]) 

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (9,9), 0)
    
    mask = cv2.inRange(hsv, lower ,upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow("Result", result)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break