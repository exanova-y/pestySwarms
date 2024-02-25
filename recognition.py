import cv2 # the OpenCV library
import numpy as np
import socket
import time
import re
class PA3400:
    # Network interface with Precise Automation PF3400 SCARA arm
    # Requires "Tcp_cmd_server" to be running on arm to accept TCP connections
    # and accept Guidance Programming Language (GPL) commands

    def __init__(self, address):
        self.host = address['host']
        self.port = address['port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Home position joint angles
        self.homej = [750, 0, 180, -180]
        self.curpos = []

        # Maximum speed limit %
        self.rapid = 20

    def connect(self):
        # Attempt to open TCP stream with robot
        try:
            self.sock.connect((self.host, self.port))
            print('Success')
        except socket.error as msg:
            print('Socket Error: ', msg)

    def enable(self):
        # Enable high power, attach robot 1 (local addr)
        self.sendcmd('mode 0')
        self.sendcmd('hp 1')
        time.sleep(4)
        self.sendcmd('attach 1')
        time.sleep(1)
        self.sendcmd('home')
        time.sleep(5)

    def disable(self):
        # Disable robot high power
        self.sendcmd('hp 0')

    def disconnect(self):
        # Close TCP stream with robot
        self.sock.close()

    def movej(self, pos):
        # Move robot to specified joint positions
        # pos = [H, A1, A2, A3, A4]
        # movej <profile#> <height> <angle2> <angle3> <angle4>
        cmd = 'movej 1 ' + ' '.join(str(n) for n in pos)
        self.sendcmd(cmd)

    def movec(self, pos):
        # Move robot to specified cartesian position, computing all joint
        # inverse kinematics.
        # pos = [X, Y, Z, Y, P, R]
        #
        # movec <profile#> <X> <Y> <Z> <Yaw> <pitch> <roll> [<handedness>]
        self.curpos = pos
        cmd = 'movec 1 ' + ' '.join(str(n) for n in pos)
        self.sendcmd(cmd)

    def movea(self, pos1, pos2):
        # Move robot to specified cartesian position, computing all joint
        # inverse kinematics.
        # pos = [X, Y, Z, Y, P, R]
        #
        # movec <profile#> <X> <Y> <Z> <Yaw> <pitch> <roll> [<handedness>]
        self.curpos = pos
        cmd = 'movea 1 ' + ' '.join(str(n) for n in pos1) + ' '.join(str(n) for n in pos2)
        self.sendcmd(cmd)

    def gohome(self):
        self.movej(self.homej)

    def sendcmd(self, cmd):
        # Attempt to send command on socket
        #
        # TODO add error handling
        cmd += '\n'
        self.sock.send(cmd.encode())
        print('Send command: ' + cmd)
        ack = self.sock.recv(1024)
        print(ack.decode())

    def parsegc(self, line):
        # Attempt to convert gcode block to PA command
        #

        blocks = line.split()

        if not len(blocks):
            return None
        # cmd = blocks[0]
        #

        # Extract letter coordinates
        blockchars = ['G','M','F','X','Y','Z','I','J','K']
        blockvals = dict.fromkeys(blockchars, 0)

        for letter in blockvals:
            block = re.search('(?<!\((?:(?!\))[\s\S\r])*?)' + letter + '-?\d*\.?\d*', line.upper())
            if block:
                if letter in ['G', 'M']:
                    blockvals[letter] = int(block.group()[1:])
                else:
                    blockvals[letter] = float(block.group()[1:])

        xyz = [blockvals['X'], blockvals['Y'], blockvals['Z']]
        ijk = [blockvals['I'], blockvals['J'], blockvals['K']]
        ypr = [90, -180, 1] # HACK
        g = blockvals['G']

        # bail if it's not a G command
        if not re.search('(?<!\((?:(?!\))[\s\S\r])*?)' + 'G' + '-?\d*\.?\d*', line.upper()):
            return None

        if g is 0:
            self.maxSpeed = 100
            pos = xyz + ypr
            self.movec(pos)

        elif g is 1:
            self.maxSpeed = 10
            pos = xyz + ijk
            self.movec(pos)

        elif g is 2:
            self.maxSpeed = 10

            # Convert center point arc to 3 point arc
            end = numpy.array(tuple(xyz))
            cur = numpy.array(tuple(self.curpos[:3]))
            cen = cur + numpy.array(tuple(ijk))
            midchord = cur + ((end - cur ) / 2)
            midarc = cen + ((midchord - cen) * numpy.linalg.norm(cur - cen) / numpy.linalg.norm(midchord - cen))

            pos1 = midarc + ypr
            pos2 = xyz + ypr
            self.movea(pos1, pos2)


        elif g is 3:
            self.maxSpeed = 10
            end = numpy.array(tuple(xyz))
            cur = numpy.array(tuple(self.curpos[:3]))
            cen = cur + numpy.array(tuple(ijk))
            midchord = cur + ((end - cur ) / 2)
            midarc = cen + ((midchord - cen) * numpy.linalg.norm(cur - cen) / numpy.linalg.norm(midchord - cen))
            pos1 = midarc + ypr
            pos2 = xyz + ypr
            self.movea(pos1, pos2)

        else:
            return

    @property
    def maxSpeed(self):
        return self.rapid

    @maxSpeed.setter
    def maxSpeed(self, speed):
        self.sendcmd('mspeed ' + str(speed))
        self.rapid = speed





cap = cv2.VideoCapture(0)  # Use the first webcam. can experiment with 0, 1, 2 etc.

robot = PA3400({'host': '10.10.10.40', 'port':10100 })

robot.connect()
robot.enable()

robot.maxSpeed = 100


pos = [-200, 90, 0, 0, 0]
robot.movej(pos)

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
            print("Centroid: ({centroid_x}, {centroid_y})")  # Print coordinates

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

