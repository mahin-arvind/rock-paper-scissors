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

outcomes = ["ROCK", "SCISSOR", "PAPER"]
computer = "READY"

#Functions
def generate_multiLandMarks(image):
     #Step 3 - Converting the input image to ‘RGB’ image

    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    return multiLandMarks

def hand_list(multiLandMarks):
    """
    Returns hand list if multiLandMarks is not empty    

    """
    if multiLandMarks is None: return "Value Invalid"

    
    handList = []

    for handLms in multiLandMarks:

        mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
        for idx, lm in enumerate(handLms.landmark):

            #Step 5 - Changing the hand points coordinates into image pixels
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            handList.append((cx, cy))

    return handList

def hand_interpret(finger_Coord, thumb_Coord):
    """
    Counts the number of fingers to return interpreted move as:
    ROCK, PAPER, SCISSOR or INVALID

    Uses finger_Coord and thumb_Coord
    """


    upCount = 0
    for coordinate in finger_Coord:
        if handList[coordinate[0]][1] < handList[coordinate[1]][1]:
            upCount += 1
    if handList[thumb_Coord[0]][0] > handList[thumb_Coord[1]][0]:
        upCount += 1

    interpret = {
                    0: "ROCK",
                    1: "INVALID",
                    2: "SCISSOR",
                    3: "INVALID",
                    4: "INVALID",
                    5: "PAPER",
                }
            
    return interpret[upCount]

def display(move,image,computer):
    """
    Displays the move in the image
    """
    if (computer == "ROCK" and move == "PAPER") or (computer == "PAPER" and move == "SCISSOR") or (computer == "SCISSOR" and move == "ROCK"):
        cv2.putText(image, str(move) + "|" + computer + "| WIN", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
    elif move == "INVALID":
        cv2.putText(image, "INVALID", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
    elif move == computer:
        cv2.putText(image, str(move) + "|" + computer + "| DRAW", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
    else:
            cv2.putText(image, str(move) + "|" + computer + "| LOSE", (10,150), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 6)
        



while True:
    success, image = cap.read()

    multiLandMarks = generate_multiLandMarks(image)

    if multiLandMarks == None:
        computer = np.random.choice(outcomes)

    if multiLandMarks:

        handList =  hand_list(multiLandMarks)
        move = hand_interpret(finger_Coord, thumb_Coord )
        display(move,image,computer) 

    cv2.imshow("Counting number of fingers", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break