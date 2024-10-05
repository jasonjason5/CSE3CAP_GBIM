import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import math

gesture = "none"

class MPRecognizer:
    
    def __init__(self,model_data):
        

        ## MediaPipe Recognition References ##

        self.model_path = 'gesture_recognizer.task'
        self.model_data = model_data
        
        self.runningMode = mp.tasks.vision.RunningMode
        self.options = vision.GestureRecognizerOptions(base_options=python.BaseOptions(model_asset_buffer = self.model_data))
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)
        
        ## Confidence value corresponding to proportion of identical gestures in buffer.
        self.confidence = 0.49 
        ## Buffer for storing gestures detected for the last 8 frames.
        self.buffer = ["none"]*8
        
        ## Specific landmark value variables initialised 
        self.pinkyXYZ = [None]*3
        self.ringXYZ = [None]*3
        self.middleXYZ = [None]*3
        self.foreXYZ = [None]*3
        self.thumbXYZ = [None]*3
        self.rootXYZ = [None]*3

    def clear_Buffer(self):
        self.buffer = ["none"] * 8


    ## INPUT: Image frame, mediapipe model data
    ## OUTPUT: Recognised gesture
    def recognizeGesture(self,frame,lmdata):
        print(self.buffer)
        
        processingFrame = mp.Image(image_format = mp.ImageFormat.SRGB,data = np.asarray(frame))
        recognitionResult = self.recognizer.recognize(processingFrame)
        
        try:
            detectedGesture = recognitionResult.gestures[0][0]
            for detectedGesture in recognitionResult.gestures:
                ## Inserting gesture into the buffer
                gestureID = [category.category_name for category in detectedGesture]
                self.buffer.pop(7)
                self.buffer.insert(0,gestureID[0])
                ## Call for cleanup
                outGesture = self.gestureCleanup(lmdata)
            
            return outGesture
        
        except IndexError as e:
            return 
            
    ## INPUT: specific gesture
    ## OUTPUT: Proportion of buffer identical to specific gesture as float
    def bufferWeighter(self,gesture):
        weight = 0
        for value in self.buffer:
            if value == gesture:
                weight += 1
        return weight / len(self.buffer)

    ## INPUT: Landmark Data
    ## OUTPUT: Updates references. Returns distance from finger-tip landmarks to wrist landmark for hard-coded value checks
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
        
        return pinkyDistance,ringDistance,middleDistance, foreDistance,thumbDistance,thumbForeDistance  
       
    ## INPUT: Landmark Data
    ## OUTPUT: Detected Gesture
    def gestureCleanup(self,landmark_data):

        global gesture 
        
        if(landmark_data.multi_hand_landmarks):
            ### SINGLE HANDED GESTURES ###
            if(len(landmark_data.multi_hand_landmarks) == 1):
               
                pinkyDistance,ringDistance,middleDistance,foreDistance,thumbDistance,thumbForeDistance = self.cleanupLandmarkValueGenerator(landmark_data)    

                ## Example Cleanup: If the x/8 buffer slots are filled with the same gesture, we check hardcoded values from the generator.
                ## If both checks are passed, we can confidently return the detected gesture.
                if(self.bufferWeighter('rotate') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25 and middleDistance < 0.25 and foreDistance > 0.45):
                        gesture = "rotate"
                
                elif(self.bufferWeighter('resize') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25 and middleDistance > 0.25): 
                        gesture = "resize"
                
                elif(self.bufferWeighter('crop') > self.confidence):
                    if(pinkyDistance < 0.25 and ringDistance < 0.25):
                        gesture = "crop"
                
                elif(self.bufferWeighter('translate') > self.confidence):
                    if(pinkyDistance < 0.2 and thumbDistance < 0.3):
                        gesture = "translate"
               
                elif(self.bufferWeighter('contrast') > self.confidence or self.bufferWeighter('help') > self.confidence):
                    if(self.pinkyXYZ[2] - 0.01 < self.thumbXYZ[2] <  self.pinkyXYZ[2] + 0.01): 
                        gesture = "open hand" 
                    elif(self.bufferWeighter('contrast') > self.confidence / 2):
                        gesture= "contrast"
               
                elif(self.bufferWeighter('brightness') > self.confidence):
                        gesture= "brightness"
                
                elif(self.bufferWeighter('pointer') > self.confidence):
                    if(foreDistance > 0.2 and middleDistance < 0.25):
                        gesture= "pointer"
                
                elif(self.bufferWeighter('pen') > self.confidence):
                    if(foreDistance > 0.2 and middleDistance > 0.2):
                        gesture = "pen"    
                
                elif(self.bufferWeighter('undo') > self.confidence): 
                    if(thumbForeDistance < 0.2):
                        gesture = "undo"
                
                elif(self.bufferWeighter('redo') > self.confidence): 
                    gesture = "redo"

                elif(self.buffer[0] == 'close' and (self.buffer[7] == 'help' or self.buffer[6] == 'help' or self.buffer[5] == 'help')): 
                     gesture = "save file"
               
                elif(self.buffer[0] == 'help' and (self.buffer[7] == 'close' or self.buffer[6] == 'close' or self.buffer[5] == 'close')):
                     gesture = "open file"
               
                elif(self.bufferWeighter('close') > self.confidence):
                    gesture = "closed hand"   
                else:
                    gesture = "none"
           
            ### MULTI HANDDED GESTURES ###
            elif(len(landmark_data.multi_hand_landmarks) == 2):
                if(self.bufferWeighter('help') > self.confidence):
                    gesture = "help"
       
        return gesture
