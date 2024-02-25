import cv2 # the OpenCV library
import numpy as np

cap = cv2.VideoCapture(0)  # Use the first webcam. can experiment with 0, 1, 2 etc.

robot = PA3400{'host': '192.168.0.168', 'port': 22}

robot.connect()
robot.enable()

robot.maxSpeed = 30
pos = [-200, -155, 244, 179.99, 90, -180, 2]
robot.movec(pos)

while True: # continuously capture frames from the webcam
    _, frame = cap.read() 
    # convert from OpenCV's BGR space to HSV
    # HSV can separate each colour in the H value and more understandable to humans
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 


    # Right now, we use three heuristics for recognizing circles:
    # 1: colour bound
    # 2: circularity ratio of a circle
    # 3: area > 500 pixels on screen
    lower_orange = np.array([10, 120, 100]) # lowest HSV, respectively
    upper_orange = np.array([25, 255, 255]) # highest HSV
    mask = cv2.inRange(hsv, lower_orange, upper_orange) 
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours: # for all the identified counter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        # the orange is always a circle. We check for circularity
        # area/perimeter = (pi*r**2)/(2*pi*r)**2 = 1/4pi 
        # meaning, 4*pi*area/perimeter^2 ~= 1

        circularity_ratio = 10 # initialize ratio to an impossibly large value
        if perimeter != 0: # avoid division by 0
            circularity_ratio = (4*np.pi*area)/(perimeter**2)  
        # print(f"Area: {area}, circularity ratio (close to 1 is good): {circularity_ratio}")
        centroid_x = 0

        if area > 300 and circularity_ratio > 0.7:
            # (0, 0) is the top left corner of the image
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # a bounding rectangle
            centroid_x = x + w//2
            centroid_y = y + h//2
            print(f"Centroid: ({centroid_x}, {centroid_y})")  # Print coordinates

        if 0 < centroid_x <= 200:
            print("1")

        elif 200 < centroid_x <= 400:
            print("2")
        elif 400 < centroid_x <= 600:
            print("3")
        elif 600 < centroid_x <= 800:
            print("4")
        elif 800 < centroid_x <= 1000:
            print("5")
        elif 1000 < centroid_x <= 1200:
            print("6")
        elif 1200 < centroid_x <= 1400:
            print("7")
        elif 1400 < centroid_x <= 1600:
            print("8")
        elif 1600 < centroid_x <= 1800:
            print("9")
        elif 1800 < centroid_x <= 2000:
            print("10")

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'): # to quit the program, press 'q' key
        break

cap.release()
cv2.destroyAllWindows()

