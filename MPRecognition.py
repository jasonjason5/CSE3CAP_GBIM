## PUT RECOGNITION LOGIC IN HERE ##
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PIL import Image
import numpy as np
import math
import statistics
from google.protobuf.json_format import MessageToDict

gesture = "none" # This is literally the only value that needs to be returned god bless.

class MPRecognizer:
    
    def __init__(self,model_data):
        
        self.model_path = 'gesture_recognizer.task'
        self.model_data = model_data
        
        self.runningMode = mp.tasks.vision.RunningMode
        self.options = vision.GestureRecognizerOptions(base_options=python.BaseOptions(model_asset_buffer = self.model_data)) # Model Data can't be passed directly for some reason
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        
        self.confidence = 0.6 # Lower the value, the more inaccurate it becomes. We can dial this in with different buffer lengths as well - at the cost of responsiveness
        self.buffer = ["none"]*5
        
        ## Having these here stops redefinition everytime cleanup is called
        self.pinkyXYZ = [None]*3
        self.ringXYZ = [None]*3
        self.middleXYZ = [None]*3
        self.foreXYZ = [None]*3
        self.thumbXYZ = [None]*3
        self.rootXYZ = [None]*3

    def clear_Buffer(self):
        self.buffer = ["none"] * 5

    def recognizeGesture(self,frame,lmdata):
        
        processingFrame = mp.Image(image_format = mp.ImageFormat.SRGB,data = np.asarray(frame))
        recognitionResult = self.recognizer.recognize(processingFrame)
        
        try:
            detectedGesture = recognitionResult.gestures[0][0]
            for detectedGesture in recognitionResult.gestures:
                
                gestureID = [category.category_name for category in detectedGesture]
                self.buffer.pop(4)
                self.buffer.insert(0,gestureID[0])
                #print(self.buffer)
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
                
        self.pinkyXYZ[0] = h1.landmark[20].x; self.pinkyXYZ[1] = h1.landmark[20].y; self.pinkyXYZ[2] = h1.landmark[20].z
        self.ringXYZ[0] = h1.landmark[16].x; self.ringXYZ[1] = h1.landmark[16].y; self.ringXYZ[2] = h1.landmark[16].z
        self.middleXYZ[0] = h1.landmark[12].x; self.middleXYZ[1] = h1.landmark[12].y; self.middleXYZ[2] = h1.landmark[12].z
        self.foreXYZ[0] = h1.landmark[8].x; self.foreXYZ[1] = h1.landmark[8].y; self.foreXYZ[2] = h1.landmark[8].z;
        self.thumbXYZ[0] = h1.landmark[4].x; self.thumbXYZ[1] = h1.landmark[4].y; self.thumbXYZ[2] = h1.landmark[4].z;
        self.rootXYZ[0] = h1.landmark[0].x; self.rootXYZ[1] = h1.landmark[0].y; self.rootXYZ[2] = h1.landmark[0].z
                
        pinkyDistance = math.sqrt((self.pinkyXYZ[0] - self.rootXYZ[0])**2 + (self.pinkyXYZ[1] - self.rootXYZ[1])**2)
        ringDistance = math.sqrt((self.ringXYZ[0] - self.rootXYZ[0])**2 + (self.ringXYZ[1] - self.rootXYZ[1])**2)
        middleDistance = math.sqrt((self.middleXYZ[0] - self.rootXYZ[0])**2 + (self.middleXYZ[1] - self.rootXYZ[1])**2)        
        foreDistance = math.sqrt((self.foreXYZ[0] - self.rootXYZ[0])**2 + (self.foreXYZ[1] - self.rootXYZ[1])**2)
        thumbDistance = math.sqrt((self.thumbXYZ[0] - self.rootXYZ[0])**2 + (self.thumbXYZ[1] - self.rootXYZ[1])**2)
        
        thumbForeDistance = math.sqrt((self.thumbXYZ[0] - self.foreXYZ[0])**2 + (self.thumbXYZ[1] - self.foreXYZ[1])**2)
        
        return pinkyDistance,ringDistance,middleDistance, foreDistance,thumbDistance,thumbForeDistance ## This could possibly be returned as an array   
            
## An example of how this works: The method recognizeGesture() is called from FL. It is called 5 consecutive times over 5 input frames, filling the buffer of the module
## object in FL. Lets say the buffer gets filled [X,Y,X,Y,X] - 3 Xs, 2Ys. Mediapipe knows its either X or Y, but is unsure. Since X is present 3 times (i.e 60% of the buffer)
## X has surpassed the confidence value of 0.6. It gets passed into the cleanup. For this example, let's say that the gesture we actually gave was Y. The frame containing X
## Would then be checked against the values in cleanup - if we gave a thumbs up, perhaps pinky, ring, middle and fore distances from root (wrist) should be ~= 0.
## Since we actually gave Y, these values will be at a mismatch, and the gesture won't result in a false positive.
        
    def gestureCleanup(self,landmark_data):
        #gesture = "none"
        #print(self.buffer)
        global gesture 
        if(landmark_data.multi_hand_landmarks):
            ### SINGLE HANDED GESTURES ###
            if(len(landmark_data.multi_hand_landmarks) == 1):
               
                pinkyDistance,ringDistance,middleDistance,foreDistance,thumbDistance,thumbForeDistance = self.cleanupLandmarkValueGenerator(landmark_data)    
                #print(thumbForeDistance)
                # Could probably be a switch/case but it doesn't particularly matter
                #print(foreDistance)
                if(self.bufferWeighter('rotate') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25 and middleDistance < 0.25 and foreDistance > 0.45):
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
                elif(self.bufferWeighter('contrast') > self.confidence): # These two detect quite well and differentiate from one another when detected. Any hardcoding would have to deal with absolute coordinates not relative, but it seems unnecessary when its working as well as it is.
                        gesture= "contrast"
                elif(self.bufferWeighter('brightness') > self.confidence):
                        gesture= "brightness"
                elif(self.bufferWeighter('pointer') > self.confidence):
                    if(foreDistance > 0.2 and middleDistance < 0.25):
                        gesture= "pointer"
                elif(self.bufferWeighter('pen') > self.confidence):
                    if(foreDistance > 0.2 and middleDistance > 0.2):
                        gesture = "pen"    
                elif(self.bufferWeighter('undo') > self.confidence): ## THESE COULD USE SOME HARDCODE CHECKS
                    if(thumbForeDistance < 0.2):
                        gesture = "undo"
                elif(self.bufferWeighter('redo') > self.confidence): ## THESE COULD USE SOME HARDCODE CHECKS
                    gesture = "redo"


                elif(self.buffer[0] == 'close' and (self.buffer[4] == 'help' or self.buffer[3] == 'help' or self.buffer[2] == 'help')): # Definitely a better way to do this check
                     gesture = "save file"
                elif(self.buffer[0] == 'help' and (self.buffer[4] == 'close' or self.buffer[3] == 'close' or self.buffer[2] == 'close')): # Definitely a better way to do this check
                     gesture = "open file"
                    
                elif(self.bufferWeighter('help') > self.confidence):
                    gesture = "open hand"
                elif(self.bufferWeighter('close') > self.confidence):
                    gesture = "closed hand"   
                else:
                    gesture = "none"
           
            ### MULTI HANDDED GESTURES ###
            elif(len(landmark_data.multi_hand_landmarks) == 2):
                if(self.bufferWeighter('help') > self.confidence):
                    gesture = "help"
       
        return gesture