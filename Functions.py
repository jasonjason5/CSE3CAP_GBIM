from PIL import ImageTk, Image, ImageOps, ImageTk, ImageEnhance
import math
import numpy as np
from tkinter import filedialog, messagebox
from operator import add
import mouse
import pyautogui
from PIL import ImageEnhance
import mouse

class editFunctions:
    def __init__(self):
       
        ## Application Componentry References 

        self.image: Image = None
        self.canvas = None
        self.canvas_image = None

        self.screenDimensions = pyautogui.size()
       
       ## Image properties References
        
        self.start_width = None
        self.start_height = None
        self.start_pos = None
        self.start_rot = 0

        self.update_image = None
        self.update_width = None
        self.update_height = None
        self.update_rot = None
        self.start_results = None

        self.penHold = None
        self.penFrameCounter = 0

        ## Crop Properties References

        self.cropStage = "move"

        self.cropImage = None
        self.cropOverlay = None
        self.cropBounds = None
        
        self.cropDim = [0,0]

        self.cropBox_Sheight = None
        self.cropBox_Swidth = None
        self.cropBox_Uheight = None
        self.cropBox_Uwidth = None

        ## History References

        self.historyDoAdd = ["cropexit","rotate","brightness","contrast","resize"]
        self.imageHistory = []
        self.canRedo = False

    ## INPUT: image, the variable containing the canvas, the canvas object
    ## FUNCTION: Initialises all required references within the Function object. Enables the object to be instatiateed without references.
    def setRefs(self, image, canvas_image, canvas): 
        self.image = ImageTk.getimage(image)
        self.canvas = canvas
        self.canvas_image = canvas_image
        
        self.start_width = self.image.width
        self.start_height = self.image.height
        self.start_pos = canvas.coords(self.canvas_image)
        
        self.update_image = self.image 
        self.update_width = self.start_width
        self.update_height = self.start_height
        self.update_rot = self.start_rot
        
        self.imageHistory.insert(0,self.image)

    ## INPUT: Landmark results, Index
    ## OUTPUT: Specific landmark coordinates
    def _get_landmark(self, results, index):
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark[index]
        return None

    ## INPUT: Landmark Results
    ## FUNCTION: Calculates distance between initial point of gesture and current point of gesture,
    ## applies proportional distance as scaling operation to image. Updates references.
    def resize(self, results):

        if self.start_results is None:
            self.start_results = results

        start_point = self._get_landmark(self.start_results, 8)
        current_point = self._get_landmark(results, 8)

        if start_point and current_point:
            distance = math.sqrt((start_point.x - current_point.x) ** 2 + (start_point.y - current_point.y) ** 2)
            scaler = distance + 1

            if (current_point.x < start_point.x and current_point.y < start_point.y) or \
               (current_point.x < start_point.x and current_point.y > start_point.y):
                scaler = 1 / scaler

            resize_width = self.start_width * scaler
            resize_height = self.start_height * scaler

            self.update_width = resize_width
            self.update_height = resize_height

            resized_image = self.image.resize((math.floor(resize_width), math.floor(resize_height)), Image.Resampling.LANCZOS)
            resized_out = ImageTk.PhotoImage(resized_image)
            
            self.update_image = resized_image
            
            self.canvas.itemconfig(self.canvas_image, image=resized_out)
            self.canvas.imgref = resized_out

    ## INPUT: Landmark Results
    ## FUNCTION: Applies landmark coordinates to image coordinates. Moves image.
    def translate(self, results):
        if not self.start_results:
            self.start_results = results

        current_point = self._get_landmark(results, 8)
        cWidth = self.canvas.winfo_reqwidth()
        cHeight = self.canvas.winfo_reqheight()
        
        anchorOffsetX = self.start_height / 2 # Offsetting central anchor of image
        anchorOffsetY = self.start_width / 2

        print(self.canvas.coords(self.canvas_image))
        if current_point:
            self.canvas.moveto(self.canvas_image, current_point.x * cWidth - anchorOffsetX, current_point.y * cHeight - anchorOffsetY) 

    ## INPUT: Array of 15 degree increments, current rotation 
    ## OUTPUT: Rotation value snapped to the nearest increment
    def snap(self,array,value):
        snapped = (np.abs(array-value)).argmin()
        print(snapped)
        return array[snapped]

    ## INPUT: Results
    ## FUNCTION: Rotates the image based on the relative rotation of two landmarks. Updates references
    def rotate(self, results):

        if self.start_results is None:
            self.start_results = results

        start_point = self._get_landmark(self.start_results, 8)
        current_point = self._get_landmark(results, 5)
        pivot_point = self._get_landmark(results, 8)

        if start_point and current_point and pivot_point:
                
            rot_vec = np.subtract([current_point.x, current_point.y], [pivot_point.x, pivot_point.y])
            rotation = math.atan2(rot_vec[1], rot_vec[0])

            out_rot = -(math.degrees(rotation) - 90)
            array = np.array([-210,-180,-150,-120,-90,-75,-60,-45,-30,-15,0,15,30,45,60,75,90,120,150,180,210]) ## Snaps to 15/30 degree increments
            out_rot = self.snap(array,out_rot)


            self.update_rot = out_rot

            rotated_image = self.image.rotate(self.start_rot + out_rot)
            rez_rot_image = rotated_image.resize((math.floor(self.start_width),math.floor(self.start_height))) ## Avoids the rotated image becoming massive for some reason 
            rotated_out = ImageTk.PhotoImage(rez_rot_image)
            
            
            self.update_image = rez_rot_image
            
            self.canvas.itemconfig(self.canvas_image, image=rotated_out)
            self.canvas.imgref = rotated_out
            self.canvas.imgref = rotated_out

    ## INPUT: Nil
    ## FUNCTION: Creates crop overlay image, updates crop-specific references. 
    def createCropBounds(self):
        self.cropImage = Image.new(mode="RGBA", color=(153,153,153,127),size=(math.floor(self.start_width / 2),math.floor(self.start_height / 2) ))
        self.cropOverlay = ImageTk.PhotoImage(self.cropImage)

        canvasCentre = (int(self.canvas.winfo_width()/2),int(self.canvas.winfo_height()/2) - 75) # Hardcoded value to get the crop box overlay roughly in centre

        self.cropBounds = self.canvas.create_image(canvasCentre[0],canvasCentre[1], image = self.cropOverlay, anchor="center") #Creates a new image on the canvas
        
        sWidth, sHeight = self.cropImage.size

        self.cropBox_Swidth = sWidth
        self.cropBox_Sheight = sHeight
        self.cropDim[0] = sWidth
        self.cropDim[1] = sHeight

        self.cropStage == "scale" 

    ## INPUT: Nil
    ## FUNCTION: Applies the crop. Locates crop window position and image position, subtracts difference in pixels
    def applyCrop(self):

        ## All the coordinates need to be adjusted by the image dimensions due to the center anchor placement of the canvas objects    

        cropBoxCoordsTL = self.canvas.coords(self.cropBounds)
        cropBoxCoordsTL[0] -= self.cropDim[0] / 2
        cropBoxCoordsTL[1] -= self.cropDim[1] / 2
        
        imageCoordsTL = self.canvas.coords(self.canvas_image)
        imageCoordsTL[0] -= self.start_width / 2
        imageCoordsTL[1] -= self.start_height / 2
        cropBoxCoordsBR = list(map(add,cropBoxCoordsTL, self.cropDim))
        BRimSize = (self.start_width,self.start_height)
        imageCoordsBR = list(map(add,imageCoordsTL,BRimSize))

        
        print(cropBoxCoordsTL,cropBoxCoordsBR,imageCoordsTL,imageCoordsBR)
        
        LCrop = -imageCoordsTL[0] + cropBoxCoordsTL[0] 
        TCrop = -imageCoordsTL[1] + cropBoxCoordsTL[1]
        RCrop = imageCoordsBR[0] - cropBoxCoordsBR[0]
        BCrop = imageCoordsBR[1] - cropBoxCoordsBR[1]
        
        crop = (LCrop,TCrop,RCrop,BCrop)
        print(crop)

        if(RCrop < 0 or TCrop < 0 or LCrop < 0 or BCrop < 0):#I.E The crop box is bigger than the image 
            messagebox.showerror("Crop Error","Potential crop is larger than image dimensions. Try a smaller crop.")
            print("POTENTIAL CROP IS LARGER THAN IMAGE")
            return
           
        update_image = ImageOps.crop(self.image,crop)
        update_width,update_height = update_image.size
           
        self.update_image = update_image
        self.update_height = update_height
        self.update_width = update_width

        canvasOut = ImageTk.PhotoImage(update_image)
        self.canvas.itemconfig(self.canvas_image,image=canvasOut)
        self.canvas.imgref = canvasOut
          
    ## INPUT: exit boolean
    ## FUNCTION: Destroys crop overlay, empties references. Checks to see if crop should be applied before exiting.
    def destroyCropBounds(self,exit):
        if(self.cropBounds):
            if not exit:
                self.applyCrop()
            self.canvas.delete(self.cropBounds)
           
            self.cropOverlay = None
            self.cropImage = None
            self.canvas.image = self.image
           
            self.cropStage = "none"
            self.cropBounds = None
            
            self.cropDim = [0,0]
            
            self.cropBox_Sheight = None
            self.cropBox_Swidth = None
            self.cropBox_Uheight = None
            self.cropBox_Uwidth = None
    
    ## INPUT: Nil
    ## FUNCTION: Resets crop stage
    def resetCropStage(self):
        self.cropStage = "none"
        
    ## INPUT: Landmark Results
    ## FUNCTION: Two steop crop process - positioning and resizing. Updates references for crop operations.
    def crop(self, results):
        
        if(self.cropStage == "move"):
            
            if not self.start_results:
                self.start_results = results

            current_point = self._get_landmark(results, 8)
            cWidth = self.canvas.winfo_reqwidth()
            cHeight = self.canvas.winfo_reqheight()
        
            if current_point:
                self.canvas.moveto(self.cropBounds, current_point.x * cWidth, current_point.y * cHeight) #
                
        elif(self.cropStage == "scale"):
            

            if self.start_results is None:
                self.start_results = results

            start_point = self._get_landmark(self.start_results, 8)
            current_point = self._get_landmark(results, 8)

            if start_point and current_point:

                distance = math.sqrt((start_point.x - current_point.x) ** 2 + (start_point.y - current_point.y) ** 2)
                scaler = distance + 1

                if (current_point.x < start_point.x and current_point.y < start_point.y) or \
                   (current_point.x < start_point.x and current_point.y > start_point.y):
                    scaler = 1 / scaler

                resize_width = self.cropBox_Swidth * scaler
                resize_height = self.cropBox_Sheight * scaler

                self.cropBox_Uwidth = resize_width
                self.cropBox_Uheight = resize_height

                resized_image = self.cropImage.resize((math.floor(resize_width), math.floor(resize_height)), Image.Resampling.LANCZOS)
                resized_out = ImageTk.PhotoImage(resized_image)
            
                self.cropDim[0] = resized_image.width
                self.cropDim[1] = resized_image.height
                print(self.cropDim)

                self.canvas.itemconfig(self.cropBounds, image=resized_out)
                self.canvas.image = resized_out 

    ## INPUT: Landmark Results
    ## FUNCTION: Moves mouse proportionally based on landmark coordinates
    def pointer(self,results):


        if self.start_results is None:
            self.start_results = results

        indexMouse = self._get_landmark(results, 8)
        fingPosx = indexMouse.x
        fingPosy = indexMouse.y

        relX = fingPosx * self.screenDimensions[0]
        relY = fingPosy * self.screenDimensions[1]
        self.penHold = (relX,relY)

        if(self.penHold[0] - 10 <= relX <= self.penHold[0] + 10 and self.penHold[1] - 10 <= relY <= self.penHold[1] + 10):
            self.penFrameCounter += 1
        if(self.penFrameCounter > 45):
            mouse.click(button = "left")
            self.penFrameCounter = 0

    
        mouse.move(relX,relY)
       
    ## INPUT: B/C Value
    ## OUTPUT: Clamped value
    def clamp(self, value):
        if(value < 0):
            return 0
        elif(value > 5):
            return 5
        else:
            return value

    ## INPUT: Landmark Results
    ## FUNCTION: Increases / Decreases image brightness based on landmark position
    def brightness(self, results):
        if self.start_results is None:
            self.start_results = results

        # Get start and current positions for the pinky finger (landmark index 20)
        start_point = self._get_landmark(self.start_results, 20)
        current_point = self._get_landmark(results, 20)

        if start_point and current_point:
            delta_y = start_point.y  -  current_point.y
            brightness_factor = 1 + (delta_y * 1.5)
            clampedBF = self.clamp(brightness_factor)
            # Apply brightness adjustment using ImageEnhance.Brightness
            enhancer = ImageEnhance.Brightness(self.image)
            brightened_image = enhancer.enhance(clampedBF)
            brightened_out = ImageTk.PhotoImage(brightened_image)

            # Update the canvas and image with the new brightened image
            self.update_image = brightened_image
            self.canvas.itemconfig(self.canvas_image, image=brightened_out)
            self.canvas.imgref = brightened_out
    
    ## INPUT: Landmark Results
    ## FUNCTION: Increases / Decreases image contrast based on landmark position   
    def contrast(self, results):
        if self.start_results is None:
            self.start_results = results

        # Get start and current positions for the pinky finger (landmark index 20)
        start_point = self._get_landmark(self.start_results, 20)
        current_point = self._get_landmark(results, 20)

        if start_point and current_point:
            delta_y = current_point.x - start_point.x
            contrast_factor = 1 + (delta_y * 1.5)
            clampedCF = self.clamp(contrast_factor)
            # Apply Contrast adjustment using ImageEnhance.Contrast
            enhancer = ImageEnhance.Contrast(self.image)
            contrasted_image = enhancer.enhance(clampedCF)
            contrasted_out = ImageTk.PhotoImage(contrasted_image)

            # Update the canvas and image with the new brightened image
            self.update_image = contrasted_image
            self.canvas.itemconfig(self.canvas_image, image=contrasted_out)
            self.canvas.imgref = contrasted_out
            
    ## INPUT: Nil
    ## FUNCTION: Saves Image
    def save_file(self):
        saveFilePath = filedialog.asksaveasfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
            title="Save Image File")
        if saveFilePath:
            self.image.save(saveFilePath)

    ## Undo and redo usurp set_start as a function, and perform the resetting of variables by themselves to ensure continuity

    ## INPUT: Nil
    ## FUNCTION: Updates references with image stored in history
    def undo(self): 
        if(len(self.imageHistory) > 1):
            self.start_results = None
            self.image = self.imageHistory[0]
            tkUndo = ImageTk.PhotoImage(self.imageHistory[0])
            
            self.start_width = self.image.width
            self.start_height = self.image.height
            self.start_pos = self.canvas.coords(self.canvas_image)
            self.start_rot = 0
            
            self.canvas.itemconfig(self.canvas_image,image=tkUndo)
            self.canvas.imgref = tkUndo

            self.canRedo = True ## I have undone. I can now redo to a undo an undo.
        
    ## INPUT: Nil
    ## FUNCTION: Updates references with iamge stored in history
    def redo(self):
        if(self.canRedo == True):

            self.start_results = None
            self.image = self.imageHistory[1]
            tkRedo = ImageTk.PhotoImage(self.imageHistory[1])

            self.start_width = self.image.width
            self.start_height = self.image.height
            self.start_pos = self.canvas.coords(self.canvas_image)
            self.start_rot = 0
            
            self.canvas.itemconfig(self.canvas_image,image=tkRedo)
            self.canvas.imgref = tkRedo
            
            self.canRedo = False

    ## INPUT: edit performed
    ## FUNCTION: Conditionally adds a copy of the image to array for undo/redo. Shifts crop state, resets/updates value.
    ## Handles all end-of-gesture processes in preparation for the enxt gesture
    def set_start(self,edit):

        if(edit in self.historyDoAdd):
            if(len(self.imageHistory) == 2):
                self.imageHistory.pop(0)
            self.imageHistory.insert(1,self.update_image)
           
        self.start_results = None  # Resetting start position of gesture coordinates
       
        if(self.cropStage == "move"):
            self.cropStage = "scale"
        elif(self.cropStage == "scale"):
            self.cropStage = "move"
        else:
            self.cropStage = "none"
        
        #Update Values
        self.image = self.update_image
        self.start_width = self.update_width
        self.start_height = self.update_height
        self.start_rot = 0
        self.penHold = None
        self.penFrameCounter = 0
        
    def return_image(self):
        return self.image
        