from email.mime import image
from PIL import ImageTk, Image, ImageOps
import math
import numpy as np
import time
from tkinter import messagebox
from operator import add
import mouse
import pyautogui
from PIL import ImageEnhance



class editFunctions:
    def __init__(self, image: ImageTk, canvas_image, canvas, positioner):
       
        ## Application Componentry References 

        self.image: Image = ImageTk.getimage(image)
        self.canvas = canvas
        self.canvas_image = canvas_image
        self.positioner = positioner
        self.screenDimensions = pyautogui.size()
        ## Image properties References
        
        self.start_width = self.image.width
        self.start_height = self.image.height
        self.start_pos = canvas.coords(self.canvas_image)
        self.start_rot = 0

        self.update_image = self.image 
        self.update_width = self.start_width
        self.update_height = self.start_height
        self.update_rot = self.start_rot
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
        self.imageHistory.insert(0,self.image)
        self.canRedo = False

    def _get_landmark(self, results, index):
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark[index]
        return None

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

    def translate(self, results):
        if not self.start_results:
            self.start_results = results

        current_point = self._get_landmark(results, 8)
        cWidth = self.canvas.winfo_reqwidth()
        cHeight = self.canvas.winfo_reqheight()

        print(self.canvas.coords(self.canvas_image))
        if current_point:
            self.canvas.moveto(self.canvas_image, current_point.x * cWidth, current_point.y * cHeight) ## This will need to be adjusted based on canvas size. we need to pass canvas size into functiosn

    def snap(self,array,value):
        snapped = (np.abs(array-value)).argmin()
        print(snapped)
        return array[snapped]

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


    def createCropBounds(self):
        self.cropImage = Image.new(mode="RGBA", color=(153,153,153,127),size=(math.floor(self.start_width / 2),math.floor(self.start_height / 2) ))
        self.cropOverlay = ImageTk.PhotoImage(self.cropImage)

        canvasCentre = (int(self.canvas.winfo_width()/2),int(self.canvas.winfo_height()/2) - 150) # Hardcoded value to get the crop box overlay roughly in centre

        self.cropBounds = self.canvas.create_image(canvasCentre[0],canvasCentre[1], image = self.cropOverlay, anchor="center") #Creates a new image on the canvas
        
        sWidth, sHeight = self.cropImage.size

        self.cropBox_Swidth = sWidth
        self.cropBox_Sheight = sHeight
        self.cropDim[0] = sWidth
        self.cropDim[1] = sHeight

        self.cropStage == "scale"
        

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


    def resetCropStage(self):
        self.cropStage = "none"
        
    def crop(self, results):
        ## Create a two step crop process: Step one, position the image under the crop box, step two, resize the crop box.
        
        if(self.cropStage == "move"):
            
            if not self.start_results:
                self.start_results = results

            current_point = self._get_landmark(results, 8)
            cWidth = self.canvas.winfo_reqwidth()
            cHeight = self.canvas.winfo_reqheight()
        
            if current_point:
                self.canvas.moveto(self.canvas_image, current_point.x * cWidth, current_point.y * cHeight) #
                
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

    def pointer(self,results):


        if self.start_results is None:
            self.start_results = results


        indexMouse = self._get_landmark(results, 8)
        fingPosx = indexMouse.x
        fingPosy = indexMouse.y
        
       # print(fingPosx,fingPosy)
        print(self.screenDimensions)
        relX = fingPosx * self.screenDimensions[0]
        relY = fingPosy * self.screenDimensions[1]
        self.penHold = (relX,relY)

        if(self.penHold[0] - 10 <= relX <= self.penHold[0] + 10 and self.penHold[1] - 10 <= relY <= self.penHold[1] + 10):
            self.penFrameCounter += 1
        if(self.penFrameCounter > 60):
            mouse.click(button = "left")
            self.penFrameCounter = 0

    
        mouse.move(relX,relY)
       
    def contrast(self,results):
        return
    def save_file(self):
        self.image.save("SavedImage.png")

    ## Undo and redo usurp set_start as a function, and perform the resetting of variables by themselves to ensure continuity

    def undo(self): ## This could definitely be expanded out to 2-step/ 3-step undo but its fine as is right now.
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

    def set_start(self,edit):

        if(edit in self.historyDoAdd):
            if(len(self.imageHistory) == 2):
                self.imageHistory.pop(0)
            self.imageHistory.insert(1,self.update_image)
           
        self.start_results = None  # Resetting start position of gesture coordinates
       
        ## When we finish with the crop box resizing, we make it into here
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
        