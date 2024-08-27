## PUT RECOGNITION LOGIC IN HERE ##
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
import numpy as np


class MPRecognizer:
    
    def __init__(self,model_data,lmdata):
        
        self.model_path = 'gesture_recognizer.task'
        self.model_data = model_data
        self.runningMode = mp.tasks.vision.RunningMode
        self.options = vision.GestureRecognizerOptions(base_options=python.BaseOptions(model_asset_buffer = self.model_data)) # Model Data can't be passed directly for some reason
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        
        self.lmdata = lmdata # Landmark data for cleanup
        self.buffer = [None]*5 # there may not be a need for this, we can just pass one buffer back and forth instead of both the FL and MPR having their own.
 
    
    def recognizeGesture(self,frame):
        
        processingFrame = mp.Image(image_format = mp.ImageFormat.SRGB,data = np.asarray(frame))
        recognitionResult = self.recognizer.recognize(processingFrame)
        
        try:
            detectedGesture = recognitionResult.gestures[0][0]
            for detectedGesture in recognitionResult.gestures:
                gestureID = [category.category_name for category in detectedGesture]

                self.buffer.pop(4)
                self.buffer.insert(0,gestureID[0])
               
                self.gestureCleanup(self.lmdata)
            
            return self.buffer
        
        except IndexError as e:
            return # We always seem to end up in here for no reason? It doesnt particularly affect the program in any way I just don't know why it's happening.
    
        
    def gestureCleanup(self,landmark_data):
    ## In order to clean up some of the recognition before we spit the buffer out to FL, we call this function. Plan is to mix recognition alongside
    ## A series of hardcoded, landmark based conditions - E.g it gets confused between help/open currently. we can fix that by manually going in
    ## when it detects help and goind "No, there's only one hand, so it's obviously not help - its open". Apply that across the whole spectrum

        return
        