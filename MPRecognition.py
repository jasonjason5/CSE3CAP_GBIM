## PUT RECOGNITION LOGIC IN HERE ##
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
import numpy as np


class MPRecognizer:
    
    def __init__(self,modelData):
        
        self.runningMode = mp.tasks.vision.RunningMode
        self.options = vision.GestureRecognizerOptions(base_options=python.BaseOptions(model_asset_buffer = modelData)) # Model Data can't be passed directly for some reason
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        
        self.buffer = [None]*5 # This can (and should) be tweaked in order to get better results
        
    
    def recognizeGesture(self,frame):
        
        processingFrame = mp.Image(image_format = mp.ImageFormat.SRGB,data = np.asarray(frame))
        recognitionResult = self.recognizer.recognize(processingFrame)
        
        try:
            detectedGesture = recognitionResult.gestures[0][0]
            for detectedGesture in recognitionResult.gestures:
                gestureID = [category.category_name for category in detectedGesture]
                self.buffer.pop(4)
                self.buffer.insert(0,gestureID[0])
        except IndexError as e:
            print("INDEX ERROR - OUT OF RANGE")
    
    def getBuffer(self): ## get the buffer to read from it as to which gesture is currently being done. Will be called by FrameLoop.callFunction()
        return self.buffer
        
            
        