CSE3CAP - Capstone Project

Project Title: Gesture Based Image Manipulation (GBIM) Software

Team members:

Jason Styles
Hao Do Nguyen
Liam Bentley
Patrick Mika

----------------------

NOTE FOR FUTURE PATRICK - GIVE PEOPLE AN IMPORT OPTION TO SELECT / REFUSE PADDING
DEMO FOR JASON

## PUT UI AND MODULE CALL LOGIC IN HERE ##
from sys import maxsize
from turtle import window_height
import MPRecognition
import FrameLoop
import Functions
import os
import Style
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

        # Set up the image and place in frame
        #self.uiHelpImage = CTk.CTkLabel(master=self.uiHelpImageFrame, bg_color="transparent", text = "")
        #self.uiHelpImage.grid(column=0, row=0)
        
        self.uiHelpImage = None

        # Set up the help label and place it in frame
        self.uiHelpMessage = CTk.CTkLabel(master=self.uiHelpFrame, text="Help Window", justify="left", wraplength=200, font=uiFont)
        self.uiHelpMessage.grid(column=0, row=1,sticky=CTk.N)
        
        # Set up exit label to hold exit image
        self.uiHelpExit = CTk.CTkLabel(master=self.uiHelpFrame, bg_color="transparent", text="")
        self.uiHelpExit.grid(column=1, row=1,sticky=CTk.S)

        # Load the exit image
        ImageLoader(self.uiHelpExit, "Ui_Images\Exit.jpg",(100,100))

        # Set the window to be at the front of everything 
        self.attributes("-topmost", True)

    # This function sets the title of the help window
    def set_title(self, title):
        self.title(title)

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
        help_image_path = Gesture.gesture_image(enumGesture)
        # Load the image into the label        
        #ImageLoader(self.uiHelpImage, help_image_path,(320,220))
        self.uiHelpImage = GIFLabel(master=self.uiHelpImageFrame,image_path=help_image_path,isHelp=True,bg_color="transparent", text = "")
        self.uiHelpImage.grid(column=0, row=0)
        #label = GIFLabel(app, "any.gif")
        #label.pack()

class GIFLabel(CTk.CTkLabel):
    def __init__(self, master, image_path,isHelp, **kwargs):
        self.isHelp = isHelp
        self.animateJob = None
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Open the image file
        self.gif_image = Image.open(os.path.join(current_dir, image_path))
        # set the size of the label to the same as the GIF image
        #kwargs.setdefault("width", self.gif_image.width)
        #kwargs.setdefault("height", self.gif_image.height)
        #set to what we want
        kwargs.setdefault("width", 320)
        kwargs.setdefault("height", 220)
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
            self._frames.append(CTk.CTkImage(self.gif_image.copy(), size=(320, 220)))
        
        # start animation
        if(isHelp):
            self._animate()
        else:
            self.configure(image=self._frames[0])

    def _animate(self, idx=0):
        print("ENTER")
        self.configure(image=self._frames[idx])
        self.animateJob = self.after(self._duration, self._animate, (idx+1)%len(self._frames))
        
    def _killAnimate(self):
        print("LEAVE")
        self.after_cancel(self.animateJob)
        self.animateJob = None
        self.configure(image=self._frames[0])

        
        
# This class loads images into the label passed to it.
class ImageLoader:
    def __init__(self, label, image_path, ui_size):
        self.label = label
        self.image_path = image_path
        self.ui_size = ui_size
        self.load_image()

    def load_image(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Open the image file
        image = Image.open(os.path.join(current_dir, self.image_path))
        # Resize the image
        self.tk_image = CTk.CTkImage(image, size= (self.ui_size))
        # Set the image on the label
        self.label.configure(image=self.tk_image)
        # Keep a reference to the image to prevent garbage collection
        self.label.image = self.tk_image

class ActionHistory(CTk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)    
        self.label_list = deque(maxlen = 2) ## Limiting to 5 History
        self.colourCounter = 0
            
    def pop_item(self):
        self.label_list[1].destroy()
        self.label_list.pop()
        for label in self.label_list: # Shuffles everything back to allow for push to Queue
            gridRow = label.grid_info()['row']
            label.grid(row = gridRow + 1)
            
        return

    def add_item(self, item, image=None):
        if(self.colourCounter > 0):
            bgColour = Style.popupBackground
            self.colourCounter = 0
        else:
            bgColour = Style.workspaceBackground
            self.colourCounter += 1

        if(len(self.label_list) == 2):
            self.pop_item()

        label = CTk.CTkLabel(self, text=item,font=("Arial",25) ,image=image,height = 50, width=400 ,compound="left", padx=5, anchor="w",bg_color = bgColour)
        label.grid(row= 2 - len(self.label_list), column=0, pady=(0, 10), sticky="w") # 5 - len ensures we're adding it to the start
        self.label_list.appendleft(label) # from a list to FIFO
            
    def check_top(self): #Returns topmost element
        return self.label_list[0]
    
# Main App Class         
class App(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Minimum size of window
        min_width = 320
        min_height = 320
        #max size of window
        #max_width = 1920
        #max_height = 1080
        self.toplevel_window = None
        self.title("Gesture Based Image Manipulation")
        self.geometry("1280x900")
        self.minsize(min_width, min_height)
        uiFont = CTk.CTkFont(family='Inter', size=24) 
        #self.maxsize(max_width, max_height)
        self.configure(bg_color=Style.workspaceBackground,fg_color= Style.workspaceBackground)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        
        # frame for the rendering canvas
        self.uiRenderFrame1 = CTk.CTkFrame(master=self, fg_color= Style.workspaceBackground, bg_color= Style.workspaceBackground)
        
        # frame that holds all of the bottom of the UI
        self.uiMasterFrame = CTk.CTkFrame(master=self, fg_color= Style.workspaceBackground, bg_color= Style.workspaceBackground)
        self.uiMasterFrame.grid(column=0, columnspan= 3,row=1 ,sticky=CTk.EW + CTk.S)
        self.uiMasterFrame.columnconfigure(0, weight = 4)
        self.uiMasterFrame.columnconfigure(1, weight = 4)
        self.uiMasterFrame.columnconfigure(2, weight = 4)
        self.uiMasterFrame.columnconfigure(3, weight = 1)
        self.uiMasterFrame.rowconfigure(0, weight = 1)
        self.uiMasterFrame.rowconfigure(1, weight = 2)

        # Detected gesture UI
        self.uiDetectedGestureFrame =CTk.CTkFrame(master=self.uiMasterFrame)
        self.uiDetectedGestureFrame.grid(column=2, row=0, sticky=CTk.S)
        self.uiDetectedGestureText = CTk.CTkLabel(master=self.uiDetectedGestureFrame, fg_color=Style.gestures,text_color=Style.blackText,text="Current Edit Gesture: ", corner_radius= 50, font=uiFont)
        self.uiDetectedGestureText.grid(column=0, row=0)
        # Removed detected gesture string, frameloop now operates directly on this widget. Fixed widget height / width to avoid changes when text updates
        self.uiDetectedGesture = CTk.CTkLabel(master=self.uiDetectedGestureFrame, height = 30, width=200, fg_color=Style.gestures,text_color=Style.blackText,text="Gesture",corner_radius= 50, font=uiFont)
        self.uiDetectedGesture.grid(column=1, row=0 )

        # menu frame, holds the gesture help, open file, action history, gesture function list
        self.uiMenuFrame = CTk.CTkFrame(master=self.uiMasterFrame, fg_color=Style.popupBackground, border_width= 3, border_color= Style.windowBorder) 
        self.uiMenuFrame.grid(column=0, columnspan= 3, row=1, sticky=CTk.E + CTk.W, ipadx=30, ipady=30)


        ## Static UI ##

        ## Splash Start UI ##

        self.uiStartFrame = CTk.CTkFrame(master=self, height=100,width=500, fg_color=Style.popupBackground, border_color = Style.windowBorder)
        self.uiStartFrame.place(relx=0.5,rely=0.5,anchor='center')

        self.uiStartWelcome = CTk.CTkLabel(master=self.uiStartFrame,fg_color=Style.popupBackground, text_color=Style.whiteText,text="Welcome to [Application Name]!", font=uiFont)
        self.uiStartWelcome.place(relx=0.5,rely=0.3,anchor='center')

        self.uiStartButton = CTk.CTkButton(master=self.uiStartFrame,text="Start Device Camera", fg_color=Style.gestures, text_color=Style.blackText, command = self.startCamera)
        self.uiStartButton.place(relx=0.5,rely=0.7,anchor='center')

        ## Splash Start UI ##


        ## Pre import UI ##

        self.uiPreimportFrame = CTk.CTkFrame(master=self.uiMenuFrame, fg_color="transparent",bg_color="transparent")
        self.uiPreimportFrame.pack(side=CTk.LEFT, expand=False)

        self.uiPreimportOpenFileLbl = GIFLabel(master=self.uiPreimportFrame,image_path='Ui_Images\OpenUI.gif',isHelp=False ,bg_color="transparent", text = "") ## Giffed
        self.uiPreimportOpenFileLbl.grid(column=0, row=0,padx=20, pady=20)
        self.uiPreimportOpenFileLbl.bind("<Enter>", lambda event:self.uiPreimportOpenFileLbl._animate())
        self.uiPreimportOpenFileLbl.bind("<Leave>", lambda event:self.uiPreimportOpenFileLbl._killAnimate())
        
        self.uiPreimportOpenConfirmLbl = CTk.CTkLabel(master=self.uiPreimportFrame, bg_color= "transparent",text = "")
        self.uiPreimportOpenConfirmLbl.grid(column=1, row=0, padx=20, pady=20)

        self.uiPreimportOpenOrLbl = CTk.CTkLabel(master=self.uiPreimportFrame, bg_color= "transparent",text = "")
        self.uiPreimportOpenOrLbl.grid(column=2, row=0,padx=20, pady=20)

        ## Pre import UI ##

        # Action history Gui

        self.uiHistoryFrame = CTk.CTkFrame(master=self.uiMenuFrame, fg_color=Style.popupBackground, width=100, height=100)
        self.uiHistoryFrame.pack(side=CTk.LEFT, expand=False)

        self.uiActionHistory = ActionHistory(master=self.uiHistoryFrame, width=200, height=5,label_text="Action History", corner_radius=0, fg_color=Style.popupBackground,border_width= 3, border_color= Style.windowBorder)
        self.uiActionHistory.grid(row=0, column=0, padx=5, pady=5)
        
        # add test item to the Action history
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image = CTk.CTkImage(Image.open(os.path.join(current_dir, "Ui_Images", "HelpOr.jpg")))
        self.uiActionHistory.add_item(item = "open")

        # Function list

        # uiFunctionFrame = CTk.CTk


        ## Help UI #
        self.uiHelpFrame = CTk.CTkFrame(master=self.uiMenuFrame, fg_color="transparent")
        self.uiHelpFrame.pack(side=CTk.RIGHT, expand=False,)

        self.uiHelpLbl = CTk.CTkLabel(master=self.uiHelpFrame,bg_color= "transparent",text = "")
        self.uiHelpLbl.grid(column=0, row=0, padx=5, pady=5)

        self.uiHelpOrLbl = CTk.CTkLabel(master=self.uiHelpFrame, bg_color= "transparent",text = "")
        self.uiHelpOrLbl.grid(column=0, row=1 ,padx=5, pady=5)

        self.uiHelpBtn = CTk.CTkButton(master=self.uiHelpFrame ,fg_color=Style.gestures,text_color=Style.blackText,text="Help", font=uiFont, corner_radius=20, width= 60, height= 30, command=lambda:self.open_help(self.uiDetectedGesture.cget("text"))) ## Throws error if you do help first thing
        self.uiHelpBtn.grid(column=0, row=2)

        # Help UI #

        ## Camera UI ##
        self.uiDeviceCameraFrame = CTk.CTkFrame(master=self.uiMasterFrame,fg_color=Style.popupBackground)
        self.uiDeviceCameraFrame.grid(column=3, row=0, rowspan= 2)
        self.uiDeviceCamera = CTk.CTkLabel(master=self.uiDeviceCameraFrame ,bg_color= Style.workspaceBackground, text="")
        self.uiDeviceCamera.grid(column=0, row=0)
        #uiDeviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

        #Hide frames
        self.uiMasterFrame.grid_forget()
  
        self.uiDetectedGestureFrame.grid_forget()
        self.uiHistoryFrame.pack_forget()  
        
        self.uiPreimportOpenFileBtn = CTk.CTkButton(master=self.uiPreimportFrame, fg_color=Style.gestures, text_color=Style.blackText, text="Open File", font=uiFont, command=self.open_image,corner_radius=20, width= 60, height= 30)
        self.uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.W)

        self.looper = FrameLoop.GestureVision(self,self.uiDeviceCamera,self.uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget

    def LoadImages(self):   
        #ImageLoader(self.uiPreimportOpenFileLbl,'Ui_Images\OpenUI.gif',(175,150)) ## Giffed
        ImageLoader(self.uiPreimportOpenConfirmLbl ,'Ui_Images\Confirm.jpg',(150,150))
        ImageLoader(self.uiPreimportOpenOrLbl,'Ui_Images\Or.jpg',(60,100))
        ImageLoader(self.uiHelpLbl,'Ui_Images\HelpUI.gif',(117,100)) ## Giffed
        ImageLoader(self.uiHelpOrLbl,'Ui_Images\HelpOr.jpg',(50,20))
        
    def killStartFrame(self):
        self.uiStartFrame.destroy()
        self.uiMasterFrame.grid(column=0, row=1, columnspan= 3, sticky=CTk.EW + CTk.S)            
        self.uiRenderFrame1.grid(column=0, row=0, rowspan=2, columnspan= 3, sticky=tk.NSEW)
        self.LoadImages()

    def startCamera(self):
        self.killStartFrame()
        self.after(0, self.looper.updateFrame())

    def handle_gesture_changed(self,var, index, mode):
        # Your code to adjust canvas size goes here
            #print("Gesture (detectedGestureString.get()) Changed: " + detectedGestureString.get()) 
            return

    def open_image(self):
        global editor
            
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
            title="Select an Image File"
        )
            
        if file_path:
            img = Image.open(file_path)

            canvas_width = int((self.uiRenderFrame1.winfo_width()))
            canvas_height = int((self.uiRenderFrame1.winfo_height()))
            print("Height:" + str(self.winfo_height()) + "Width:" + str(self.winfo_width()))
            
            img = self.resizeImport(img,canvas_width,canvas_height)

                
            img_tk = ImageTk.PhotoImage(img)
                
            self.uiRenderFrame = tk.Canvas(master=self.uiRenderFrame1, width=canvas_width, height=canvas_height, bg= Style.workspaceBackground, bd=0,highlightthickness=0) ## This will need to be changed along with some window dimensions but nothing that cant be changed in an afternoon.
            self.uiRenderFrame.delete("all")
            self.uiRenderFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.uiRenderFrame.bind("<Configure>", self.handle_resize)
            ### Changing this for later
            
            editingImage = self.uiRenderFrame.create_image(canvas_width/2,canvas_height/2,anchor='center',image=img_tk) ## Creates the reference to be passed to the looper
            self.uiRenderFrame.imgref = img_tk
                
            #uiRenderFrame.grid(column=1, row=0, columnspan= 3, sticky=tk.W)
            #show detected gesture
            self.uiPreimportFrame.pack_forget()
            self.uiDetectedGestureFrame.grid(column=2, row=0, sticky=CTk.S)
            self.uiHistoryFrame.pack(side=CTk.LEFT, expand=False)

            ## Creates Function objects
            editor = Functions.editFunctions(img_tk,editingImage,self.uiRenderFrame)
            self.looper.setActive() # Activates detection
            self.looper.setEditor(editor)
            self.looper.setHistory(self.uiActionHistory)

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
        
        padDim = math.ceil(math.sqrt(resOutHeight**2 + resOutWidth **2))
        padBox = Image.new(mode="RGBA",size = (padDim,padDim)) # color=(153,153,153,255) ## This fixes the rotation, problem, but any image output by this program will input back in with a larger padding onto of whatever was originally added
        # in saying that, this is sort of a problem that photoshop / photopea etc. also have. Like if you create a bigger canvas and then rotate your image, the output image will be the size of the canvas,
        # and then when you put that new image back in, its pulled in as one layer, it isnt as if you can separate out the original image from the padding. So its not a problem we have to solve.
        
        padBoxWidth, padBoxHeight = padBox.size

        offset = ((padBoxWidth - resOutWidth) // 2, (padBoxHeight - resOutHeight) // 2)
        
        padBox.paste(img,offset)

        return padBox
    












    def handle_resize(self,event): ## This is showing an error since the reshuffle, potentially to do with passing in self
        # Your code to adjust canvas size goes here
            print(f"Canvas (uiRenderFrame) resized: {event.width}x{event.height}")  
        

    def open_file(self):
        self.open_image()

    def open_help(self, affirmation):
        if affirmation == "none":
            affirmation = "help"          
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():      
            self.toplevel_window = HelpWindow(self)  # create window if its None or destroyed
            self.toplevel_window.set_help_text( gesture= affirmation)
            self.toplevel_window.set_help_image( gesture= affirmation)
            affirmation = affirmation + ": Help"
            self.toplevel_window.set_title(title = affirmation)          
        else:
            self.toplevel_window.focus()  # if window exists focus it
            self.toplevel_window.set_help_text( gesture= affirmation)
            self.toplevel_window.set_help_image( gesture= affirmation)
            affirmation = affirmation + ": Help"
            self.toplevel_window.set_title(title= affirmation) 
                 
    
    def set_help_title(self, affirmation):
        self.toplevel_window.set_title(title=affirmation) 

## TEST MATERIAL ##

if __name__ == "__main__":
    app = App()
    app.mainloop()
    

