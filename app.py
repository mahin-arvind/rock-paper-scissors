#Step 1 - Importing libraries
import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, request, Response
from game import da_game

#Step 2 - Declaring the ‘MediaPipe’ objects and the finger and thumb coordinates
app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(da_game(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=='__main__':
    app.run(debug=True)
    