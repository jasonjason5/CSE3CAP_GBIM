## PUT RECOGNITION LOGIC IN HERE ##
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
import numpy as np
import math
import statistics

class MPRecognizer:
    
    def __init__(self,model_data):
        
        self.model_path = 'gesture_recognizer.task'
        self.model_data = model_data
        
        self.runningMode = mp.tasks.vision.RunningMode
        self.options = vision.GestureRecognizerOptions(base_options=python.BaseOptions(model_asset_buffer = self.model_data)) # Model Data can't be passed directly for some reason
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        
        self.confidence = 0.6
        self.buffer = ["none"]*5
    
    def recognizeGesture(self,frame,lmdata):
        
        processingFrame = mp.Image(image_format = mp.ImageFormat.SRGB,data = np.asarray(frame))
        recognitionResult = self.recognizer.recognize(processingFrame)
        
        try:
            detectedGesture = recognitionResult.gestures[0][0]
            for detectedGesture in recognitionResult.gestures:
                
                gestureID = [category.category_name for category in detectedGesture]
                self.buffer.pop(4)
                self.buffer.insert(0,gestureID[0])
                outGesture = self.gestureCleanup(lmdata)
            
            return outGesture
        
        except IndexError as e:
            return # We always seem to end up in here for no reason? It doesnt particularly affect the program in any way I just don't know why it's happening.
            
## This bit calculates the confidence value
    def bufferWeighter(self,gesture):
        weight = 0
        for value in self.buffer:
            if value == gesture:
                weight += 1
        return weight / len(self.buffer)
    
## This next bit is basically a bunch of vector math to get the abs distance in xy coords from the tips of each fingers to the root of the hand (wrist). This way we can check
## specific distances - for instance, in the rotate gesture the pinky, ring and middle should be below 0.2 distance from the root - and then once we have that, we can 
## use that to double check the gesture detected with a 0.6 confidence (i.e the recognizer has filled 3/5 buffer slots with a consistent gesture)
## should make this whole thing rather robust I think.

    def cleanupLandmarkValueGenerator(self,landmark_data):
        h1 = landmark_data.multi_hand_landmarks[0]
        
        pinkyXYZ = [None]*3
        ringXYZ = [None]*3
        middleXYZ = [None]*3
        foreXYZ = [None]*3
        thumbXYZ = [None]*3
        rootXYZ = [None]*3
                
        pinkyXYZ[0] = h1.landmark[20].x; pinkyXYZ[1] = h1.landmark[20].y; pinkyXYZ[2] = h1.landmark[20].z
        ringXYZ[0] = h1.landmark[16].x; ringXYZ[1] = h1.landmark[16].y; ringXYZ[2] = h1.landmark[16].z
        middleXYZ[0] = h1.landmark[12].x; middleXYZ[1] = h1.landmark[12].y; middleXYZ[2] = h1.landmark[12].z
        rootXYZ[0] = h1.landmark[0].x; rootXYZ[1] = h1.landmark[0].y; rootXYZ[2] = h1.landmark[0].z
                
        pinkyDistance = math.sqrt((pinkyXYZ[0] - rootXYZ[0])**2 + (pinkyXYZ[1] - rootXYZ[1])**2)
        ringDistance = math.sqrt((middleXYZ[0] - rootXYZ[0])**2 + (middleXYZ[1] - rootXYZ[1])**2)
        middleDistance = math.sqrt((middleXYZ[0] - rootXYZ[0])**2 + (middleXYZ[1] - rootXYZ[1])**2)        
        
        return pinkyDistance,ringDistance,middleDistance   
            
## In order to clean up some of the recognition before we spit the buffer out to FL, we call this function. Plan is to mix recognition alongside
## A series of hardcoded, landmark based conditions - E.g it gets confused between help/open currently. we can fix that by manually going in
## when it detects help and goind "No, there's only one hand, so it's obviously not help - its open". Apply that across the whole spectrum
        
    def gestureCleanup(self,landmark_data):
        
        pinkyDistance,ringDistance,middleDistance = self.cleanupLandmarkValueGenerator(landmark_data)
        gesture = "none"
        if(self.bufferWeighter('rotate') > self.confidence):
                if(pinkyDistance < 0.2 and ringDistance < 0.2 and middleDistance < 0.2):
                    gesture = "rotate"
                    ## This is interesting because now we have the option of calling the function either from here, because now we know what function we're doing - or from Frameloop. Will probably do it from
                    ## Frameloop to avoid getting too deep in the callback sauce
        return gesture
            


