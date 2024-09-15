import cv2
from cv2.cuda import setBufferPoolConfig
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
import customtkinter as CTk
from PIL import ImageTk
import _tkinter as tk
import MPRecognition
import numpy as np
import math
from threading import Thread
import time


class GestureVision:
    
    def __init__(self,root,window,affirmation,model_data): ## Initialises all MP and CV variables and objects to be operated on
        
        self.frameCapture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.mpHands = mp.solutions.hands
        self.mpDrawing = mp.solutions.drawing_utils
        self.mpHandObject = self.mpHands.Hands()
        
        ##MPRecognition REFERENCES
        
        self.model_data = model_data
        self.recognizer = MPRecognition.MPRecognizer(self.model_data)
        self.gesture = None
        ## UI REFERENCES ##
       
        self.root = root 
        self.window = window
        self.affirmation = affirmation
        
        ## Optimisations ##
        self.runProcessing = 0
        self.start_time = None
        self.end_time = None
        
        ## Editing ##
        self.opened = False # For making sure you cant open an image on an open image
        self.prevEdit = "none"
        self.cropMode = False
        self.boolBuffer = ["none"]*5
        self.editor = None
        self.history = None
        self.historyDoAdd = ["translate","crop","rotate","brightness","contrast","resize"]
        
    def updateFrame(self):
        success, frame = self.frameCapture.read()
        if success:
            #self.end_timer()
            frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) ## OpenCV takes images in BGR format, this converts them into the proper RGB format for display and processing
            results = self.mpHandObject.process(frameRGB)
            
            gestureFrame = Image.fromarray(frameRGB)

            if(results.multi_hand_landmarks):
              
                if(self.runProcessing == 0):
                    gThread = Thread(target = self.recognizer.recognizeGesture,args = [gestureFrame,results])
                    gThread.daemon = True
                    gThread.start()
                    self.runProcessing += 1
                    
                elif(self.runProcessing < 3):
                    self.runProcessing += 1
                    
                else:
                    self.runProcessing = 0
                    
            else:
                MPRecognition.gesture = "none"



            if(self.cropMode == False): ## Crop mode indicator
                self.affirmation.configure(text = MPRecognition.gesture)
            else:
                self.affirmation.configure(text = "crop")


            if(self.history):
                if(self.history.check_top().cget("text") != MPRecognition.gesture and MPRecognition.gesture in self.historyDoAdd): ## adds the appropriate gestures to the history
                    self.history.add_item(item = MPRecognition.gesture)
                



            self.callFunction(MPRecognition.gesture,results)
            
            resizedFrame = gestureFrame.resize((320,240),Image.Resampling.LANCZOS)
            displayFrame = CTk.CTkImage(resizedFrame, size= (320,240))
       
            ## return it to the tkinter widget in which we want to display it
       
            self.window.image = displayFrame
            self.window.configure(image=displayFrame)
            self.root.after(1,self.updateFrame)  
            
            # if after set to 1 takes about  0.07 seconds to loop - UI Choppy
            # if after set to 100 takes about 0.1 seconds to loop - UI much more reponsive
            # The above is likely varied on the PC running it 
            
           # print(self.prevEdit)
            
        else:
            return
        
      

    def setEditor(self,editor):
        self.editor = editor

    def setHistory(self,history):
        self.history = history
        

    def drawLandmarks(self): ## Draws hand landmarks. Good debugging tool but unnecessary to do all the time. Could add as boolean option
        return
    
    def callFunction(self,gesture,results): ## This method will be called to check which function to call based on the contents of the buffer
        
        if(gesture == "resize"):
            if(self.cropMode == True):
                self.editor.crop(results)
                self.prevEdit = "cropsize"
            
            elif(self.cropMode == False):
                self.editor.resize(results)
                self.prevEdit = "resize"
        
        elif(gesture == "crop"):
            
            if(self.cropMode == False and self.prevEdit != "cropexit"): #If you didnt just exit crop
                self.cropMode = True
                self.prevEdit = "cropenter"
            
            elif(self.cropMode == True and self.prevEdit != "cropenter"): # You were in crop mode but you didnt just literally enter into it. Will need to change how this behaves when gestures other than resize are given
                print("EXITING")
                self.cropMode = False
                self.prevEdit = "cropexit"


# There's definitely a more elegant way to handle dropping out of crop mode other than checking it each time, but for now this will suffice.

        elif(gesture == "rotate"):
            if(self.cropMode == False):
                self.editor.rotate(results)
                self.prevEdit = "rotate"
            else:
                print("EXITING")
                self.cropMode = False
        
        elif(gesture == "translate"):
            if(self.cropMode == False):
                self.editor.translate(results)
                self.prevEdit = "translate"
            else:
                print("EXITING")
                self.cropMode = False
            
            
            
            
            
            
            
        elif(gesture == "open file" and self.opened == False): # This can be done here as opposed to functions in order to avoid unnecessary passing of info
            self.opened == True
            MPRecognition.gesture = "none" # This forces the gesture out of recognition so that it doesnt repeatedly open windows
            self.recognizer.clear_Buffer()
            self.root.open_file()
            
        elif(gesture == "save file"):
            self.recognizer.clear_Buffer()
            self.editor.save_file()
           


        elif(gesture == "help"): # Ditto as above
            MPRecognition.gesture = "none" # This forces the gesture out of recognition so that it doesnt repeatedly open windows
            self.recognizer.clear_Buffer()
            self.root.open_help(self.prevEdit)
            
            
        elif(self.prevEdit != "none"):
            self.editor.set_start()
            if(gesture == "none"):
                self.prevEdit = "none"
            
    












   # def start_timer(self): ## Method to count how long a loop takes to run
     #   self.start_time = time.time()
     #   return 
    
    #def end_timer(self): ## Method to count how long a loop takes to run
    #    if self.start_time is None:
      #      return  
      #  self.end_time = time.time()
      #  elapsed_time = self.end_time - self.start_time
      #  print(f"Time taken for the loop to run: {elapsed_time} seconds")
      #  return 