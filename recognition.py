import cv2 # the OpenCV library
import numpy as np

cap = cv2.VideoCapture(0)  # Use the first webcam

while True: # continuously capture frames from the webcam
    _, frame = cap.read() 
    # convert from OpenCV's BGR space to HSV
    # HSV can separate each colour in the H value and more understandable to humans
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 


    # Right now, we use three heuristics for recognizing circles:
    # 1: colour bound
    # 2: circularity ratio of a circle
    # 3: area > 500 pixels on screen
    lower_orange = np.array([10, 130, 100]) # lowest HSV, respectively
    upper_orange = np.array([25, 255, 255]) # highest HSV
    mask = cv2.inRange(hsv, lower_orange, upper_orange) 
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours: # for all the identified counter
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)

        # the orange is always a circle. We check for circularity
        # area/perimeter = (pi*r**2)/(2*pi*r)**2 = 1/4pi ~= 0.079
        # roughly, the ratio should be < 0.1
        ratio = 1 # initialize ratio to 1
        if perimeter != 0:
            ratio = area/(perimeter**2)  
        print(f"Area: {area}, Area-perimeter ratio: {ratio}")
        
        if area > 500 and (ratio > 0.055 and ratio < 0.075): 
            # (0, 0) is the top left corner of the image
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # a bounding rectangle
            centroid_x = x + w//2
            centroid_y = y + h//2
            print(f"Centroid: ({centroid_x}, {centroid_y})")  # Print coordinates

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'): # to quit the program, press 'q' key
        break

cap.release()
cv2.destroyAllWindows()

