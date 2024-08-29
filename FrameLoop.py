## PUT OPENCV FRAME UPDATE LOGIC IN HERE ##

## Not too sure how python hands passing objects, whether they're copied and passed by value or passed by reference and can be edited from within the caller.
## Will need to investigate when things are up and running to see.

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
from PIL import ImageTk
import _tkinter as tk
import MPRecognition
import numpy as np
import math
import multiprocessing

class GestureVision:
    
    def __init__(self,root,window,affirmation,model_data): ## Initialises all MP and CV variables and objects to be operated on
        
        self.frameCapture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.mpHands = mp.solutions.hands
        self.mpDrawing = mp.solutions.drawing_utils
        self.mpHandObject = self.mpHands.Hands()
        
        ##MPRecognition REFERENCES
        
        self.model_data = model_data
        self.recognizer = MPRecognition.MPRecognizer(self.model_data)
        self.gesture = "none"

        ## UI REFERENCES ##
       
        self.root = root 
        self.window = window
        self.affirmation = affirmation
        
        ## Optimisations ##
        self.runProcessing = 0
        
    def updateFrame(self):
        success, frame = self.frameCapture.read()
        if success:
            frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) ## OpenCV takes images in BGR format, this converts them into the proper RGB format for display and processing
            results = self.mpHandObject.process(frameRGB)
            
            gestureFrame = Image.fromarray(frameRGB)
 
            ## MPObject will be a globally defined MPRecognizer object declared within the main ui loop
            if(self.runProcessing == 0):
                self.gesture = self.recognizer.recognizeGesture(gestureFrame,results)
                self.runProcessing += 1
            elif(self.runProcessing < 3):
                self.runProcessing += 1
            else:
                self.runProcessing = 0

            ##DEBUG##
            self.affirmation.config(text=self.gesture)
            ##DEBUG##
            
            resizedFrame = gestureFrame.resize((320,240),Image.Resampling.LANCZOS)
            displayFrame = ImageTk.PhotoImage(image = resizedFrame)
       
            ## return it to the tkinter widget in which we want to display it
       
            self.window.image = displayFrame
            self.window.config(image=displayFrame)
            self.root.after(1,self.updateFrame)
            
        else:
            return
        
      
    def drawLandmarks(self): ## Draws hand landmarks. Good debugging tool but unnecessary to do all the time. Could add as boolean option
        return
    
    def callFunction(self,gesture,results): ## This method will be called to check which function to call based on the contents of the buffer
        return
    
    def displayGesture(self): ## Method to display affirmative gesture feedback (Similar to what is currently under DEBUG)
        return
        
        