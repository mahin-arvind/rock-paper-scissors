#Step 1 - Importing libraries
import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, request

#Step 2 - Declaring the ‘MediaPipe’ objects and the finger and thumb coordinates
cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
thumb_Coord = (4,2)

#GAME DEETS
interpret = {
    0: "ROCK",
    1: "INVALID",
    2: "SCISSOR",
    3: "INVALID",
    4: "INVALID",
    5: "PAPER",
    }
outcomes = ["ROCK", "SCISSOR", "PAPER"]
computer = "READY"


#Step 3 - Converting the input image to ‘RGB’ image
while True:
    success, image = cap.read()
    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    #Step 4 -Drawing the landmarks present in the hands
    if multiLandMarks == None:
        computer = np.random.choice(outcomes)

    if multiLandMarks:

        handList = []

        for handLms in multiLandMarks:

            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            for idx, lm in enumerate(handLms.landmark):

                #Step 5 - Changing the hand points coordinates into image pixels
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                handList.append((cx, cy))

        #Step 6 - Circling the hand points
        for point in handList:
            cv2.circle(image, point, 10, (255, 255, 0), cv2.FILLED)

        #Step 7 - Checling whether a finger is open or closed
        upCount = 0
        for coordinate in finger_Coord:
            if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
                upCount += 1
        if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
            upCount += 1
        
        #Step 8 - Display output
        if (computer == "ROCK" and interpret[upCount] == "PAPER") or (computer == "PAPER" and interpret[upCount] == "SCISSOR") or (computer == "SCISSOR" and interpret[upCount] == "ROCK"):
            cv2.putText(image, str(interpret[upCount]) + "|" + computer + "| WIN", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
        elif interpret[upCount] == "INVALID":
            cv2.putText(image, "INVALID", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
        elif interpret[upCount] == computer:
            cv2.putText(image, str(interpret[upCount]) + "|" + computer + "| DRAW", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
        else:
                cv2.putText(image, str(interpret[upCount]) + "|" + computer + "| LOSE", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
              

    cv2.imshow("Counting number of fingers", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break