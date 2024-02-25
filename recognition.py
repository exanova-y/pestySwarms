import cv2 # the OpenCV library
import numpy as np

cap = cv2.VideoCapture(0)  # Use the first webcam

while True: # continuously capture frames from the webcam
    _, frame = cap.read() 
    # convert from OpenCV's BGR space to HSV
    # HSV can separate each colour in the H value and more understandable to humans
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 


    # use a colour bound with as a heuristic
    lower_orange = np.array([33, 48, 89]) # lowest HSV, respectively
    upper_orange = np.array([24, 74, 65]) # highest HSV
    mask = cv2.inRange(hsv, lower_orange, upper_orange) 
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours: # for all the identified counter
        area = cv2.contourArea(cnt)
        if area > 100:  # Min area of 500 pixels to reduce noise
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

