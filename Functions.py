from re import T
from PIL import ImageTk, Image
import math
import numpy as np
import time


class editFunctions:
    def __init__(self, image: ImageTk, canvas_image, canvas):
        self.image: Image = ImageTk.getimage(image)
        self.canvas = canvas
        self.canvas_image = canvas_image

        self.start_width = self.image.width
        self.start_height = self.image.height
        self.start_pos = canvas.coords(self.canvas_image)
        self.start_rot = 0

        self.update_image = self.image # We need to actually update the image reference with the modifications, otherwise the modifications will not reflect in the saved file that operates from this reference
        self.update_width = self.start_width
        self.update_height = self.start_height
        self.update_rot = self.start_rot
        self.start_results = None
        self.rotation_start_time = None
        self.is_locked = False
        

        self.historyDoAdd = ["crop","rotate","brightness","contrast","resize"]
        self.imageHistory = []
        self.imageHistory.insert(0,self.image)

    def _get_landmark(self, results, index):
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0].landmark[index]
        return None

    def resize(self, results):
        if self.is_locked:
            return

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
        if self.is_locked:
            return

        if not self.start_results:
            self.start_results = results

        current_point = self._get_landmark(results, 8)

        if current_point:
            self.canvas.moveto(self.canvas_image, current_point.x * 1280, current_point.y * 720) ## This will need to be adjusted based on canvas size. we need to pass canvas size into functiosn

    def rotate(self, results):
        if self.is_locked:
            return

        if self.start_results is None:
            self.start_results = results

        start_point = self._get_landmark(self.start_results, 8)
        current_point = self._get_landmark(results, 5)
        pivot_point = self._get_landmark(results, 8)

        if start_point and current_point and pivot_point:
            rot_vec = np.subtract([current_point.x, current_point.y], [pivot_point.x, pivot_point.y])
            rotation = math.atan2(rot_vec[1], rot_vec[0])

            out_rot = -(math.degrees(rotation) - 90)
            self.update_rot = self.start_rot + out_rot

            rotated_image = self.image.rotate(self.start_rot + out_rot)
            rez_rot_image = rotated_image.resize((math.floor(self.start_width),math.floor(self.start_height))) ## Avoids the rotated image becoming massive for some reason 
            rotated_out = ImageTk.PhotoImage(rez_rot_image)
            
            
            self.update_image = rez_rot_image
            
            self.canvas.itemconfig(self.canvas_image, image=rotated_out)
            self.canvas.imgref = rotated_out
            
            # Check if the landmark has been held for 5 seconds
            if self.rotation_start_time is not None and time.time() - self.rotation_start_time >= 5:
                self.is_locked = True
            elif self.rotation_start_time is None:
                self.rotation_start_time = time.time() ## This needs to be changed a bit so that it rotates on the canvas not the image itself

    def crop(self, results):
        print("cropping")
        return

    def pen(self,results):
        return
    def brightness(self, results):
        return
    def contrast(self,results):
        return
    
    def save_file(self):
        self.image.save("SavedImage.png")
        


    def undo(self): ## THERE ARE SOME SLIGH ISSUES HERE THAT I CANNOT RESOLVE RIGHT NOW
        if(len(self.imageHistory) > 1):
            self.start_results = None
            self.image = self.imageHistory[1]
            tkUndo = ImageTk.PhotoImage(self.imageHistory[1])


            self.start_width = self.image.width
            self.start_height = self.image.height
            self.start_pos = self.canvas.coords(self.canvas_image)
            self.start_rot = 0
            


            self.canvas.itemconfig(self.canvas_image,image=tkUndo)
            self.canvas.imgref = tkUndo

            self.rotation_start_time = None
            self.is_locked = False
        
    def set_start(self,edit):
        print(self.imageHistory)
        if(edit in self.historyDoAdd):
            if(len(self.imageHistory) == 2):
                self.imageHistory.pop(1)
            self.imageHistory.insert(0,self.image)
           
        #print(self.imageHistory)

        self.start_results = None  # Resetting start position of gesture coordinates
        self.image = self.update_image
        self.start_width = self.update_width
        self.start_height = self.update_height
        self.start_rot = self.update_rot
        self.rotation_start_time = None  # Reset rotation start time
        self.is_locked = False