#Step 1 - Importing libraries
import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, request
from game import rock_paper_scissor, generate_multiLandMarks

#Step 2 - Declaring the ‘MediaPipe’ objects and the finger and thumb coordinates
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



##APP

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def start_page():
    print("Start")
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    multiLandMarks = generate_multiLandMarks(image, hands)

    if multiLandMarks == None:
        computer = np.random.choice(outcomes)
    rock_paper_scissor(image, mp_Hands, hands, mpDraw, multiLandMarks, computer)



if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)