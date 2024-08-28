## PUT RECOGNITION LOGIC IN HERE ##
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
import numpy as np
import math
import statistics
from google.protobuf.json_format import MessageToDict

class MPRecognizer:
    
    def __init__(self,model_data):
        
        self.model_path = 'gesture_recognizer.task'
        self.model_data = model_data
        
        self.runningMode = mp.tasks.vision.RunningMode
        self.options = vision.GestureRecognizerOptions(base_options=python.BaseOptions(model_asset_buffer = self.model_data)) # Model Data can't be passed directly for some reason
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        
        self.confidence = 0.4 # Lower the value, the more inaccurate it becomes. We can dial this in with different buffer lengths as well - at the cost of responsiveness
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
                print(self.buffer)
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
        foreXYZ[0] = h1.landmark[8].x; foreXYZ[1] = h1.landmark[8].y; foreXYZ[2] = h1.landmark[8].z;
        thumbXYZ[0] = h1.landmark[4].x; thumbXYZ[1] = h1.landmark[4].y; thumbXYZ[2] = h1.landmark[4].z;
        rootXYZ[0] = h1.landmark[0].x; rootXYZ[1] = h1.landmark[0].y; rootXYZ[2] = h1.landmark[0].z
                
        pinkyDistance = math.sqrt((pinkyXYZ[0] - rootXYZ[0])**2 + (pinkyXYZ[1] - rootXYZ[1])**2)
        ringDistance = math.sqrt((ringXYZ[0] - rootXYZ[0])**2 + (ringXYZ[1] - rootXYZ[1])**2)
        middleDistance = math.sqrt((middleXYZ[0] - rootXYZ[0])**2 + (middleXYZ[1] - rootXYZ[1])**2)        
        foreDistance = math.sqrt((foreXYZ[0] - rootXYZ[0])**2 + (foreXYZ[1] - rootXYZ[1])**2)
        thumbDistance = math.sqrt((thumbXYZ[0] - rootXYZ[0])**2 + (thumbXYZ[1] - rootXYZ[1])**2)
        
        return pinkyDistance,ringDistance,middleDistance, foreDistance,thumbDistance ## This could possibly be returned as an array   
            
## An example of how this works: The method recognizeGesture() is called from FL. It is called 5 consecutive times over 5 input frames, filling the buffer of the module
## object in FL. Lets say the buffer gets filled [X,Y,X,Y,X] - 3 Xs, 2Ys. Mediapipe knows its either X or Y, but is unsure. Since X is present 3 times (i.e 60% of the buffer)
## X has surpassed the confidence value of 0.6. It gets passed into the cleanup. For this example, let's say that the gesture we actually gave was Y. The frame containing X
## Would then be checked against the values in cleanup - if we gave a thumbs up, perhaps pinky, ring, middle and fore distances from root (wrist) should be ~= 0.
## Since we actually gave Y, these values will be at a mismatch, and the gesture won't result in a false positive.
        
    def gestureCleanup(self,landmark_data):
        gesture = "none"
        if(landmark_data.multi_hand_landmarks):
            ### SINGLE HANDED GESTURES ###
            if(len(landmark_data.multi_hand_landmarks) == 1):
               
                pinkyDistance,ringDistance,middleDistance,foreDistance,thumbDistance = self.cleanupLandmarkValueGenerator(landmark_data)    
                print(pinkyDistance,ringDistance,middleDistance)
                # Could probably be a switch/case but it doesn't particularly matter
                
                if(self.bufferWeighter('rotate') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25 and middleDistance < 0.25):
                        gesture = "rotate"
                elif(self.bufferWeighter('resize') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25 and middleDistance > 0.25): # This is the prime example of the work this does. This makes rotate and resize distinct by comparing middleDistance
                        gesture = "resize"
                elif(self.bufferWeighter('crop') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25):
                        gesture = "crop"
                elif(self.bufferWeighter('translate') > self.confidence):
                    if(pinkyDistance < 0.2 and thumbDistance < 0.3):
                        gesture = "translate"
               
                    
           
            ### MULTI HANDDED GESTURES ###
        return gesture