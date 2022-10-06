import cv2
import mediapipe as mp
import numpy as np



#Functions
def generate_multiLandMarks(image, hands):
     #Step 3 - Converting the input image to ‘RGB’ image

    RGB_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(RGB_image)
    multiLandMarks = results.multi_hand_landmarks

    return multiLandMarks

def hand_list(image,multiLandMarks, mpDraw, mp_Hands):
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

def hand_interpret(finger_Coord, thumb_Coord, handList):
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
        

def rock_paper_scissor(image, mp_Hands, hands, mpDraw, multiLandMarks, computer):
    """
    Game
    
    :param image: takes image as input and returns the image with RPS game
   
    """

    finger_Coord = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_Coord = (4,2)

    #GAME DEETS

    if multiLandMarks:

        handList =  hand_list(image,multiLandMarks, mpDraw, mp_Hands)
        move = hand_interpret(finger_Coord, thumb_Coord, handList)
        display(move,image,computer) 


cap = cv2.VideoCapture(0)
mp_Hands = mp.solutions.hands
hands = mp_Hands.Hands()
mpDraw = mp.solutions.drawing_utils
outcomes = ["ROCK","PAPER","SCISSOR"]

while True:
    success, image = cap.read()

    multiLandMarks = generate_multiLandMarks(image, hands)

    if multiLandMarks == None:
        computer = np.random.choice(outcomes)
    rock_paper_scissor(image, mp_Hands, hands, mpDraw, multiLandMarks, computer)


    cv2.imshow("Counting number of fingers", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

