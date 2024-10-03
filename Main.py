## PUT UI AND MODULE CALL LOGIC IN HERE ##
#from symbol import varargslist
from sys import maxsize
from turtle import window_height

from cv2 import text
import MPRecognition
import FrameLoop
import Functions
import os
import Style
import time
from Gestures import Gesture
import customtkinter as CTk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import W, Canvas, filedialog
import math
from collections import deque

 ## TEST MATERIAL ##
model_path = 'gesture_recognizer.task'
with open(model_path,'rb') as file:
    model_data = file.read()

# Class for the Help Window.
class HelpWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window settings
        self.geometry("375x400")
        # Move the font elsewhere?
        uiFont = CTk.CTkFont(family='Inter', size=14) 
        self.configure(bg_color=Style.workspaceBackground,fg_color= Style.workspaceBackground)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        # Set up the frame to hold everthing in the window
        self.uiHelpFrame = CTk.CTkFrame(master=self,fg_color=Style.popupBackground, border_color = Style.windowBorder)
        self.uiHelpFrame.grid(row=0, column=0, ipadx=10, ipady=10, sticky=CTk.E+ CTk.W +CTk.N + CTk.S)

        # Configure the grid for the window
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Configure the grid for the frame
        self.uiHelpFrame.rowconfigure(0, weight=1)
        self.uiHelpFrame.rowconfigure(1, weight=1)
        self.uiHelpFrame.columnconfigure(0, weight=2)
        self.uiHelpFrame.columnconfigure(1, weight=1)

        # Set up the help image frame (to keep it centered and north)
        self.uiHelpImageFrame = CTk.CTkFrame(master=self.uiHelpFrame, fg_color=Style.workspaceBackground, border_color = Style.windowBorder, border_width= 3)
        self.uiHelpImageFrame.grid(row=0, column=0, columnspan = 2, sticky=CTk.E+ CTk.W +CTk.N + CTk.S, padx = 20, pady = 20)
        
        self.uiHelpImageFrame.rowconfigure(0, weight=1)
        self.uiHelpImageFrame.columnconfigure(0, weight=1) 
        
        #set help image to none     
        self.uiHelpImage = None

        # Set up the help label and place it in frame
        self.uiHelpMessage = CTk.CTkLabel(master=self.uiHelpFrame, text="Help Window", justify="left", wraplength=200, font=uiFont,text_color = Style.whiteText)
        self.uiHelpMessage.grid(column=0, row=1,sticky=CTk.N)
        
        # Set up exit image
       # self.uiHelpExit = ImageLabel(master=self.uiHelpFrame,image_path='Ui_Images\Exit.jpg',image_size=(100,100), bg_color="transparent", text="")
       # self.uiHelpExit.grid(column=1, row=1,sticky=CTk.S)

        # Set the window to be at the front of everything 
        self.attributes("-topmost", True)

    # This function sets the title of the help window
    def set_title(self, title):
        # Get the Gesture Enum object from the string value, and return the value of the gesture
        enumGesture = Gesture.string_to_enum(title).value
        # Append help at the end of the string
        message = enumGesture + " Command: Help"
        # set the title of the help window
        self.title(message)

    # This function sets the help text for the specified gesture
    def set_help_text(self,gesture):
        # Get the Gesture Enum object from the string value
        enumGesture = Gesture.string_to_enum(gesture)
        # Get the help message for the specific Gesture
        help = Gesture.gesture_help(enumGesture)
        # Set the help message to the value above
        self.uiHelpMessage.configure(text=help)

    # This function sets the help image for the specified gesture
    def set_help_image(self,gesture):
        # Get the Gesture Enum object from the string value
        enumGesture = Gesture.string_to_enum(gesture)
        # Get the image name for the specific Gesture
        help_image_path = Gesture.gesture_help_image(enumGesture)
        # Load the GIF into the label        
        self.uiHelpImage = GIFLabel(master=self.uiHelpImageFrame,root= self ,image_path=help_image_path,is_Help=True ,bg_color="transparent", text = "")
        self.uiHelpImage.grid(column=0, row=0)

class GIFLabel(CTk.CTkLabel):
    def __init__(self, master, root, image_path, gif_width = 320, gif_height = 220, is_Help = True, is_Open = False, is_Help_Button = False, **kwargs):
        self.is_Help = is_Help
        self.is_Help_Button = is_Help_Button
        self.is_Open = is_Open
        self.animate_Job = None
        self.gif_width = gif_width
        self.gif_height = gif_height
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Open the image file
        self.gif_image = Image.open(os.path.join(current_dir, image_path))
        # set the size of the label to the same as the GIF image
        #kwargs.setdefault("width", self.gif_image.width)
        #kwargs.setdefault("height", self.gif_image.height)
        #set to what we want
        kwargs.setdefault("width", self.gif_width)
        kwargs.setdefault("height", self.gif_height)
        # don't show the text initially
        kwargs.setdefault("text", "")
        # delay for the after loop
        self._duration = kwargs.pop("duration", None) or self.gif_image.info["duration"]
        super().__init__(master, **kwargs)
        # load all the frames
        self._frames = []
        for i in range(self.gif_image.n_frames):
            self.gif_image.seek(i)
            #set to gif actual size
            #self._frames.append(CTk.CTkImage(self.gif_image.copy(), size=(self["width"], self["height"])))
            #set to what we want
            self._frames.append(CTk.CTkImage(self.gif_image.copy(), size=(self.gif_width, self.gif_height)))
        # start animation
        if(is_Help):
            self._animate()
            return
        if(is_Open):
            self.bind("<Button-1>", lambda event:root.importOptionsPopUp())
        elif(is_Help_Button):
            self.bind("<Button-1>", lambda event:root.open_help(root.uiActionHistory.get_last_gesture_text()))
        else:
            self.bind("<Button-1>", lambda event:root.open_help(Gesture.get_gesture_from_imagepath(Gesture, image_path)))
        self.bind("<Enter>", lambda event:self._animate())
        self.bind("<Leave>", lambda event:self._killAnimate())
        self.configure(image=self._frames[1])

    def _animate(self, idx=0):
        self.configure(image=self._frames[idx])
        self.animate_Job = self.after(self._duration, self._animate, (idx+1)%len(self._frames))
    
    def _killAnimate(self):
        self.after_cancel(self.animate_Job)
        self.animate_Job = None
        self.configure(image=self._frames[1])
        
# This class creates an image label.
class ImageLabel(CTk.CTkLabel):
    def __init__(self, master, root, image_path, image_size, is_gesture = False, **kwargs):
        self.image_path = image_path
        self.image_size = image_size
        self.is_gesture = is_gesture
        self.root = root
        super().__init__(master, **kwargs)
        self.load_image()

    def load_image(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Open the image file
        image = Image.open(os.path.join(current_dir, self.image_path))
        # Resize the image
        self.tk_image = CTk.CTkImage(image, size= (self.image_size))
        # Set the image on the label
        self.configure(image=self.tk_image)
        # Keep a reference to the image to prevent garbage collection
        self.image = self.tk_image
        #if the image is a gesture image, give it an on click event that opens the help for it
        if(self.is_gesture):
            self.bind("<Button-1>", lambda event:self.root.open_help(Gesture.get_gesture_from_imagepath(Gesture, self.image_path)))

class ActionHistory(CTk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs) 
        self.label_list = deque(maxlen = 3) ## Limiting to 5 History
        self.last_gesture = "none"
        self.colourCounter = 0
        self.nav_title = CTk.CTkLabel(self, text="Action History", fg_color=Style.gestures,text_color=Style.blackText, width= 150)
        self.nav_title.grid(row = 0, column = 0)
            
    def pop_item(self):
        self.label_list[2].destroy()
        self.label_list.pop()
        for label in self.label_list: # Shuffles everything back to allow for push to Queue
            gridRow = label.grid_info()['row']
            label.grid(row = gridRow + 1)
            
        return

    def add_item(self, item, image=None):
        self.last_gesture = item
        if(self.colourCounter > 0): # Makes nice alternating colours
            bgColour = Style.popupBackground
            self.colourCounter = 0
        else:
            bgColour = Style.workspaceBackground
            self.colourCounter += 1

        if(len(self.label_list) == 3):
            self.pop_item()

        label = CTk.CTkLabel(self, text=item,font=("Arial",20) ,image=image,height = 35, width=120 ,compound="left", justify = "center", anchor= "center", corner_radius= 50, fg_color = bgColour,text_color=Style.whiteText)
        label.grid(row= 4 - len(self.label_list), column=0) # 5 - len ensures we're adding it to the start
        self.label_list.appendleft(label) # from a list to FIFO
            
    def check_top(self): #Returns topmost element
        return self.label_list[0]
    
    def get_last_gesture_text(self):
        return self.last_gesture

class FunctionFrame(CTk.CTkFrame):
    def __init__(self, master, root, **kwargs):
        self.root = root  
        super().__init__(master, **kwargs) 
        self.label_list = []
        self.width = 0
        self.start_time = None
        self.end_time = None

    def add_item(self, gesture):
        img = Gesture.gesture_image(gesture)
        #text = Gesture(gesture).value
        label = ImageLabel(master=self,root= self.root,image_path=img,image_size=(60,60),is_gesture=True ,bg_color="transparent",text = "")
       # label = CTk.CTkLabel(self, text=item,font=("Arial",25) ,image=image,height = 50, width=400 ,compound="left", padx=5, anchor="w",bg_color = bgColour)
        if len(self.label_list) < 6:
            label.grid(row=0 ,column=len(self.label_list), padx=(5,5), pady=(5,5), sticky="nsew")
        else:
            label.grid(row=1 ,column=len(self.label_list) - 6, padx=(5,5), pady=(5,5), sticky="nsew")
        self.label_list.append(label) # from a list to FIFO
        self.width += 120
        self.configure(width = self.width)
        #self.grid_columnconfigure(0, weight=1)
        #self.pack_configure(side=CTk.LEFT, expand=True)
             
    
# Main App Class         
class App(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Minimum size of window
        min_width = 1280
        min_height = 900
        #max size of window
        max_width = 1920
        max_height = 1080
        self.toplevel_window = None
        self.title("Finger Print")
        self.geometry("1280x900")
        self.minsize(min_width, min_height)
        uiFont = CTk.CTkFont(family='Inter', size=24) 
        self.maxsize(max_width, max_height)
        self.configure(bg_color=Style.workspaceBackground,fg_color= Style.workspaceBackground)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        
        # frame for the rendering canvas - REMOVED - we've now got the canvas directly on the master frame instead of on an intermediary

        # frame that holds all of the bottom of the UI
        self.uiMasterFrame = CTk.CTkFrame(master=self, fg_color= Style.workspaceBackground, bg_color= Style.workspaceBackground)
        self.uiMasterFrame.grid(column=0, columnspan= 3,row=1 ,sticky=CTk.EW + CTk.S)
        self.uiMasterFrame.columnconfigure(0, weight = 3)
        self.uiMasterFrame.columnconfigure(1, weight = 3)
        self.uiMasterFrame.columnconfigure(2, weight = 3)
        self.uiMasterFrame.columnconfigure(3, minsize= Style.cameraWidth)
        self.uiMasterFrame.rowconfigure(0, weight = 1)
        self.uiMasterFrame.rowconfigure(1, weight = 4)

        # Detected gesture UI
        self.uiDetectedGestureFrame =CTk.CTkFrame(master=self.uiMasterFrame, fg_color= Style.workspaceBackground)
        self.uiDetectedGestureFrame.grid(column=0, columnspan = 3, row=0, sticky=CTk.E + CTk.W + CTk.S)
        self.uiDetectedGestureText = CTk.CTkLabel(master=self.uiDetectedGestureFrame, fg_color=Style.gestures,text_color=Style.blackText,text="Current Edit Gesture: ", corner_radius= 50, font=uiFont)
        self.uiDetectedGestureText.grid(column=0, row=0)
       
       # Removed detected gesture string, frameloop now operates directly on this widget. Fixed widget height / width to avoid changes when text updates
        self.uiDetectedGesture = CTk.CTkLabel(master=self.uiDetectedGestureFrame, height = 30, width=200, fg_color=Style.gestures,text_color=Style.blackText,text="Help",corner_radius= 50, font=uiFont)
        self.uiDetectedGesture.grid(column=1, row=0 )

        # menu frame, holds the gesture help, open file, action history, gesture function list
        self.uiMenuFrame = CTk.CTkFrame(master=self.uiMasterFrame, fg_color=Style.popupBackground, border_width= 3, border_color= Style.windowBorder,corner_radius=0) 
        self.uiMenuFrame.grid(column=0, columnspan= 3, row=1, sticky=CTk.E + CTk.W + CTk.S, ipadx=10, ipady=10)


        ## Static UI ##

        ## Splash Start UI ##

        self.uiStartFrame = CTk.CTkFrame(master=self, height=100,width=500, fg_color=Style.popupBackground, border_color = Style.windowBorder)
        self.uiStartFrame.place(relx=0.5,rely=0.5,anchor='center')

        self.uiStartWelcome = CTk.CTkLabel(master=self.uiStartFrame,fg_color=Style.popupBackground, text_color=Style.whiteText,text="Welcome to Finger Print!", font=uiFont)
        self.uiStartWelcome.place(relx=0.5,rely=0.3,anchor='center')

        self.uiStartButton = CTk.CTkButton(master=self.uiStartFrame,text="Start Device Camera", fg_color=Style.gestures, text_color=Style.blackText, command = self.startCamera)
        self.uiStartButton.place(relx=0.5,rely=0.7,anchor='center')

        ## Splash Start UI ##


        ## Pre import UI ##

        self.uiPreimportFrame = CTk.CTkFrame(master=self.uiMenuFrame, fg_color="transparent",bg_color="transparent")
        self.uiPreimportFrame.pack(side=CTk.LEFT, expand=False, pady = 10, padx = 10)

        self.uiPreimportOpenFileLbl = GIFLabel(master=self.uiPreimportFrame,root= self, image_path='Ui_Images\OpenUI.gif',gif_width=100,gif_height= 100,is_Help=False, is_Open = True, bg_color="transparent", text = "") ## Giffed
        self.uiPreimportOpenFileLbl.grid(column=0, row=0,padx=20, pady=20)

        self.uiPreimportBoilerPlate = CTk.CTkLabel(master=self.uiPreimportFrame, width = 200, height= 100, text_color=Style.whiteText,font=('Inter',16), text="Please ensure you are seated in a well lit room.\nHave your camera facing directly head on.\n\nWhen you are ready to begin: press the open file image or give the gesture!")
        self.uiPreimportBoilerPlate.grid(column=1,row=0,padx=20,pady=20)

        #self.uiPreimportOpenOrLbl = ImageLabel(master=self.uiPreimportFrame, root= self, image_path='Ui_Images\Or.jpg',image_size=(60,100), bg_color= "transparent",text = "")
        #self.uiPreimportOpenOrLbl.grid(column=2, row=0,padx=20, pady=20)

        #self.uiPreimportOpenFileBtn = CTk.CTkButton(master=self.uiPreimportFrame, fg_color=Style.gestures, text_color=Style.blackText, text="Open File", font=uiFont, command=self.importOptionsPopUp,corner_radius=20, width= 60, height= 30)
        #self.uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.W)


        ## Pre import UI ##

        # Action history Gui

        self.uiActionHistory = ActionHistory(master=self.uiMenuFrame, height=130, width = 150, corner_radius=0, fg_color=Style.popupBackground,border_width= 3, border_color= Style.windowBorder)
        
        # add test item to the Action history
        self.uiActionHistory.add_item(item = "openfile")

        # Function list
        self.uiFunctionList = FunctionFrame( master=self.uiMenuFrame, root=self,height= 130, corner_radius=0, fg_color=Style.popupBackground,border_width= 0, border_color= Style.windowBorder)


        gestures = Gesture.return_enums(Gesture)
        print(gestures)
        for gesture in gestures:
            self.uiFunctionList.add_item(gesture = gesture)
      

        ## Help UI #
        self.uiHelpFrame = CTk.CTkFrame(master=self.uiMenuFrame, fg_color="transparent")
        self.uiHelpFrame.pack(side=CTk.RIGHT, expand=False, pady = 10, padx = 10)

        self.uiHelpLbl = GIFLabel(master=self.uiHelpFrame,root= self,image_path='Ui_Images\HelpUI.gif' ,gif_width=100,gif_height= 100, is_Help=False , is_Help_Button= True,bg_color="transparent", text = "")
        self.uiHelpLbl.grid(column=0, row=0, padx=5, pady=5)

       # self.uiHelpOrLbl = ImageLabel(master=self.uiHelpFrame, root= self,image_path='Ui_Images\HelpOr.jpg',image_size=(25,10), bg_color= "transparent",text = "")
       # self.uiHelpOrLbl.grid(column=0, row=1 ,padx=5, pady=5)
        
       # self.uiHelpBtn = CTk.CTkButton(master=self.uiHelpFrame ,fg_color=Style.gestures,text_color=Style.blackText,text="Help", font=uiFont, corner_radius=20, width= 30, height= 15, command=lambda:self.open_help(self.uiActionHistory.get_last_gesture_text()))
       # self.uiHelpBtn.grid(column=0, row=2)

        # Help UI #

        ## Camera UI ##
        self.uiDeviceCameraFrame = CTk.CTkFrame(master=self.uiMasterFrame,fg_color=Style.popupBackground ,border_width= 3, border_color= Style.windowBorder, height=Style.cameraHeight, width=Style.cameraWidth,corner_radius=0)
        self.uiDeviceCameraFrame.grid(column=3, row=0, rowspan= 2, sticky= CTk.S)
        self.uiDeviceCamera = CTk.CTkLabel(master=self.uiDeviceCameraFrame ,bg_color= Style.workspaceBackground, text="")
        self.uiDeviceCamera.pack(side=CTk.RIGHT, expand=False, pady = 5, padx = 5)

        #Hide frames
        self.uiMasterFrame.grid_forget()
        self.uiDetectedGestureFrame.grid_forget()

        #start loop
        self.looper = FrameLoop.GestureVision(self,self.uiDeviceCamera,self.uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget
        self.editor = Functions.editFunctions()
        self.looper.setEditor(self.editor)
        self.looper.setHistory(self.uiActionHistory)

        
    def killStartFrame(self):
        self.uiStartFrame.destroy()
        self.uiMasterFrame.grid(column=0, row=1, columnspan= 3, sticky=CTk.EW + CTk.S)

        # remove the row span below to place the Canvas above the menu frame         
        #self.uiRenderFrame1.grid(column=0, row=0, columnspan= 3, sticky=tk.NSEW)

    def startCamera(self):
        self.killStartFrame()
        self.after(0, self.looper.updateFrame())

    def importOptionsPopUp(self):
        popup = tk.Toplevel()
        popup.geometry("300x100")
        popup.resizable(False,False)
        popup.title("Import Options")

        self.paddingBool = tk.BooleanVar()
        self.overlayBool = tk.BooleanVar()
        
        pCheckBox = tk.Checkbutton(popup, text= "Pad the image to avoid rotational clipping?",variable= self.paddingBool)
        pCheckBox.select()
        oCheckBox = tk.Checkbutton(popup, text= "Overlay CV2 landmarks on webcam?", variable= self.overlayBool)
        continueButton = tk.Button(popup, text= "Continue", command = self.open_image)
        
        pCheckBox.place(x=10,y=10)
        oCheckBox.place(x=10,y=30)
        continueButton.place(x=150,y=75,anchor='center')
        
    def open_image(self):
        global editor

        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
            title="Select an Image File"
        )
            
        if file_path:
            img = Image.open(file_path)

            UIoffset = self.uiMenuFrame.winfo_height() + 85 # 85 accounts for gesture detection
            rfHeight = self.winfo_height() - UIoffset
            relPos = 1 - (rfHeight / self.winfo_height())
            
            img = self.resizeImport(img,self.winfo_width(),rfHeight)
                
            img_tk = ImageTk.PhotoImage(img)
                
            self.uiRenderFrame = tk.Canvas(master=self, width=self.winfo_width(), height= rfHeight, bg= Style.workspaceBackground, bd=0, highlightthickness=0,) ## This will need to be changed along with some window dimensions but nothing that cant be changed in an afternoon.
            self.uiRenderFrame.delete("all")
            self.uiRenderFrame.place(x=0,y=0)
            
            self.bind("<Configure>", lambda event: self.handle_resize(event)) # This doesnt necessarily need to be in here but there's no real reason it can't be either

            editingImage = self.uiRenderFrame.create_image(self.winfo_width()/2,rfHeight/2,anchor='center',image=img_tk) ## Creates the reference to be passed to the looper
            self.uiRenderFrame.imgref = img_tk
               

            self.editor.setRefs(img_tk,editingImage,self.uiRenderFrame)
            self.looper.setActive() # Activates detection
            if(self.overlayBool.get() == True):
                self.looper.setOverlay()
            
            # remove the preimport menu
            self.uiPreimportFrame.pack_forget()
            # show the new menu items
            self.uiDetectedGestureFrame.grid(column=1, columnspan = 2, row=0, sticky=CTk.E + CTk.W + CTk.S)
            self.uiActionHistory.pack(side=CTk.LEFT, fill= CTk.BOTH ,expand=False , pady = 10, padx = 10)
            self.uiFunctionList.pack( expand=True, fill= CTk.BOTH, pady = 10, padx = 10)


    def resizeImport(self,img,canvas_width,canvas_height): 
        ## Resizes the image to better fit the current canvas size
        ## This also creates a padding box around the image to solve the scenario where rotation cuts sections of the image off.

        image_width, image_height = img.size
        resizerWidth = image_width/canvas_width
        resizerHeight = image_height/canvas_height

        if(resizerHeight > 1 or resizerWidth > 1):

            resizer = 1 / max(resizerHeight,resizerWidth)
        else:
            resizer = 1
           
        resOutWidth = math.floor(resizer*image_width)
        resOutHeight = math.floor(resizer*image_height)
        img = img.resize((resOutWidth, resOutHeight), Image.Resampling.LANCZOS)
        
        if(self.paddingBool.get() == True):
            padDim = math.ceil(math.sqrt(resOutHeight**2 + resOutWidth **2))
            padBox = Image.new(mode="RGBA",size = (padDim,padDim)) # color=(153,153,153,255) ## This fixes the rotation, problem, but any image output by this program will input back in with a larger padding onto of whatever was originally added
            # in saying that, this is sort of a problem that photoshop / photopea etc. also have. Like if you create a bigger canvas and then rotate your image, the output image will be the size of the canvas,
            # and then when you put that new image back in, its pulled in as one layer, it isnt as if you can separate out the original image from the padding. So its not a problem we have to solve.
        
            padBoxWidth, padBoxHeight = padBox.size

            offset = ((padBoxWidth - resOutWidth) // 2, (padBoxHeight - resOutHeight) // 2)
        
            padBox.paste(img,offset)
        else:
            padBox = img

        return padBox

    def handle_resize(self,event): # Correctly resizes the canvas based on root window size :)
            print(event)
            UIoffset = self.uiMenuFrame.winfo_height() + 35 # 35 accounts for little gesture readout's size
            rfHeight = self.winfo_height() - UIoffset
            newWidth = self.winfo_width()
            #print(f"Canvas (uiRenderFrame) resized: {newWidth}x{rfHeight}") 
            self.uiRenderFrame.config(width = newWidth, height =rfHeight )
      

    def open_file(self):
        self.importOptionsPopUp()

    def open_help(self, affirmation):
        if affirmation is None or affirmation == "none":
            print('working')
            affirmation = "help"          
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():      
            self.toplevel_window = HelpWindow(self)  # create window if its None or destroyed         
        else:
            self.toplevel_window.focus()  # if window exists focus it
        print("affirmation = " + affirmation)
        self.toplevel_window.set_help_text( gesture= affirmation)
        self.toplevel_window.set_help_image( gesture= affirmation)
        self.toplevel_window.set_title(title= affirmation)     
                 
## TEST MATERIAL ##

if __name__ == "__main__":
    app = App()
    app.mainloop()
    