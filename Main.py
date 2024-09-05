## PUT UI AND MODULE CALL LOGIC IN HERE ##
import MPRecognition
import FrameLoop
import Functions
import os
import Style
from Gestures import Gesture
import customtkinter as CTk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog




## Instead of using a different class to create the UI, it will be easier (both logistically and layout-wise) to just write the UI in here.
## Get rid of all the testing stuff when you're ready to put the UI down. This was just a test to see if I could get things passing properly between class modules.
class HelpWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("375x400")
        uiFont = CTk.CTkFont(family='Inter', size=14) 
        #self.maxsize(max_width, max_height)
        self.configure(bg_color=Style.workspaceBackground,fg_color= Style.workspaceBackground)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.uiHelpFrame = CTk.CTkFrame(master=self,fg_color=Style.popupBackground, border_color = Style.windowBorder)
        self.uiHelpFrame.grid(row=0, column=0, ipadx=10, ipady=10, sticky=CTk.E+ CTk.W +CTk.N + CTk.S)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.uiHelpFrame.rowconfigure(0, weight=1)
        self.uiHelpFrame.rowconfigure(1, weight=1)
        self.uiHelpFrame.columnconfigure(0, weight=2)
        self.uiHelpFrame.columnconfigure(1, weight=1)

        self.uiHelpImageFrame = CTk.CTkFrame(master=self.uiHelpFrame, fg_color=Style.workspaceBackground, border_color = Style.windowBorder, border_width= 3)
        self.uiHelpImageFrame.grid(row=0, column=0, columnspan = 2, sticky=CTk.E+ CTk.W +CTk.N + CTk.S, padx = 20, pady = 20)
        self.uiHelpImageFrame.rowconfigure(0, weight=1)
        self.uiHelpImageFrame.columnconfigure(0, weight=1)

        self.uiHelpImage = CTk.CTkLabel(master=self.uiHelpImageFrame, bg_color="transparent", text = "")
        self.uiHelpImage.grid(column=0, row=0)
        
        self.uiHelpMessage = CTk.CTkLabel(master=self.uiHelpFrame, text="Help Window", justify="left", wraplength=200, font=uiFont)
        self.uiHelpMessage.grid(column=0, row=1,sticky=CTk.N)
        
        self.uiHelpExit = CTk.CTkLabel(master=self.uiHelpFrame, bg_color="transparent", text="")
        self.uiHelpExit.grid(column=1, row=1,sticky=CTk.S)

        image = Image.open(os.path.join(self.current_dir, "Ui_Images", "Exit.jpg"))
        #resize the image
        tk_image = CTk.CTkImage(image, size= (100,100))
        # Set the image on the label
        self.uiHelpExit.configure(image=tk_image)
        # Keep a reference to the image to prevent garbage collection
        self.uiHelpExit.image = tk_image       
        self.attributes("-topmost", True)
    def set_title(self, title):
        self.title(title)

    def set_help_text(self,gesture):
        enumGesture = Gesture.string_to_enum(gesture)
        help = Gesture.gesture_help(enumGesture)
        self.uiHelpMessage.configure(text=help)

    def set_help_image(self,gesture):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        enumGesture = Gesture.string_to_enum(gesture)
        help_image_path = Gesture.gesture_image(enumGesture)
        # Open the image file
        helpimage = Image.open(os.path.join(self.current_dir, "Ui_Images", help_image_path))
        #resize the image
        tk_help_image = CTk.CTkImage(helpimage, size= (320,220))
        # Set the image on the label
        self.uiHelpImage.configure(image=tk_help_image)
        # Keep a reference to the image to prevent garbage collection
        self.uiHelpImage.image = tk_help_image



class ImageLoader:
    def __init__(self, label, image_path, ui_size):
        self.label = label
        self.image_path = image_path
        self.ui_size = ui_size
        self.load_image()

    def load_image(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Open the image file
        image = Image.open(os.path.join(current_dir, "Ui_Images", self.image_path))
        #resize the image
        self.tk_image = CTk.CTkImage(image, size= (self.ui_size))
        # Set the image on the label
        self.label.configure(image=self.tk_image)
        # Keep a reference to the image to prevent garbage collection
        self.label.image = self.tk_image

class ActionHistory(CTk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)    
        self.label_list = []

    def add_item(self, item, image=None):
        label = CTk.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        self.label_list.append(label)

    def remove_item(self, item):
        for label in zip(self.label_list):
            if item == label.cget("text"):
                label.destroy()
                self.label_list.remove(label)
                return
            
class App(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def LoadImages():   
            ImageLoader(uiPreimportOpenFileLbl,'Openfile.jpg',(150,150))
            ImageLoader(uiPreimportOpenConfirmLbl ,'Confirm.jpg',(150,150))
            ImageLoader(uiPreimportOpenOrLbl,'Or.jpg',(60,100))
            ImageLoader(uiHelpLbl,'Help.jpg',(100,100))
            ImageLoader(uiHelpOrLbl,'HelpOr.jpg',(50,20))
        
        def killStartFrame():
            uiStartFrame.destroy()
            uiMasterFrame.grid(column=0, row=1,ipadx=1280, sticky=CTk.S)
            uiRenderFrame.grid(column=0,columnspan= 3, row=0, ipadx=1280, ipady=100)
            LoadImages()

        def startCamera():
            killStartFrame()
            looper.updateFrame()

                # Minimum size of window
        min_width = 320
        min_height = 320
        #max size of window
        #max_width = 1920
        #max_height = 1080
        self.toplevel_window = None
        self.title("Gesture Based Image Manipulation")
        self.geometry("1280x720")
        self.minsize(min_width, min_height)
        uiFont = CTk.CTkFont(family='Inter', size=24) 
        #self.maxsize(max_width, max_height)
        self.configure(bg_color=Style.workspaceBackground,fg_color= Style.workspaceBackground)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        uiRenderFrame = tk.Canvas(master=self, bg= Style.workspaceBackground, bd=0,highlightthickness=0, relief='ridge')
        uiRenderFrame.grid(column=1, row=0)



        uiMasterFrame = CTk.CTkFrame(master=self, fg_color= Style.workspaceBackground, bg_color= Style.workspaceBackground)
        uiMasterFrame.grid(column=0, columnspan= 3,row=1)
        uiMasterFrame.columnconfigure(0, weight = 4)
        uiMasterFrame.columnconfigure(1, weight = 4)
        uiMasterFrame.columnconfigure(2, weight = 4)
        uiMasterFrame.columnconfigure(3, weight = 1)
        uiMasterFrame.rowconfigure(0, weight = 1)
        uiMasterFrame.rowconfigure(1, weight = 2)


        uiDetectedGestureFrame =CTk.CTkFrame(master=uiMasterFrame)
        uiDetectedGestureFrame.grid(column=2, row=0, sticky=CTk.S)
        uiDetectedGestureText = CTk.CTkLabel(master=uiDetectedGestureFrame, fg_color=Style.gestures,text_color=Style.blackText,text="Current Edit Gesture: ", corner_radius= 50, font=uiFont)
        uiDetectedGestureText.grid(column=0, row=0)
        uiDetectedGesture = CTk.CTkLabel(master=uiDetectedGestureFrame, fg_color=Style.gestures,text_color=Style.blackText,text="Gesture",corner_radius= 50, font=uiFont)
        uiDetectedGesture.grid(column=1, row=0 )

        # menu frame, holds the gesture help, open file, action history, gesture function list
        uiMenuFrame = CTk.CTkFrame(master=uiMasterFrame, fg_color=Style.popupBackground, border_width= 3, border_color= Style.windowBorder) 
        uiMenuFrame.grid(column=0, columnspan= 3, row=1, sticky=CTk.E + CTk.W, ipadx=30, ipady=30)


        ## Static UI ##

        ## Splash Start UI ##

        uiStartFrame = CTk.CTkFrame(master=self, height=100,width=500, fg_color=Style.popupBackground, border_color = Style.windowBorder)
        uiStartFrame.place(relx=0.5,rely=0.5,anchor='center')

        uiStartWelcome = CTk.CTkLabel(master=uiStartFrame,fg_color=Style.popupBackground, text_color=Style.whiteText,text="Welcome to [Application Name]!", font=uiFont)
        uiStartWelcome.place(relx=0.5,rely=0.3,anchor='center')

        uiStartButton = CTk.CTkButton(master=uiStartFrame,text="Start Device Camera", fg_color=Style.gestures, text_color=Style.blackText, command = startCamera)
        uiStartButton.place(relx=0.5,rely=0.7,anchor='center')

        ## Splash Start UI ##



        ## Pre import UI ##

        uiPreimportFrame = CTk.CTkFrame(master=uiMenuFrame, fg_color="transparent",bg_color="transparent")
        uiPreimportFrame.pack(side=CTk.LEFT, expand=False)

        uiPreimportOpenFileLbl = CTk.CTkLabel(master=uiPreimportFrame, bg_color="transparent", text = "")
        uiPreimportOpenFileLbl.grid(column=0, row=0,padx=20, pady=20)

        uiPreimportOpenConfirmLbl = CTk.CTkLabel(master=uiPreimportFrame, bg_color= "transparent",text = "")
        uiPreimportOpenConfirmLbl.grid(column=1, row=0, padx=20, pady=20)

        uiPreimportOpenOrLbl = CTk.CTkLabel(master=uiPreimportFrame, bg_color= "transparent",text = "")
        uiPreimportOpenOrLbl.grid(column=2, row=0,padx=20, pady=20)

        ## Pre import UI ##

        def open_image():
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
                title="Select an Image File"
            )
            
            if file_path:
                img = Image.open(file_path)

                canvas_width = uiRenderFrame.winfo_width()
                canvas_height = uiRenderFrame.winfo_height()

                img = img.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                
                uiRenderFrame.delete("all")
                uiRenderFrame.create_image(0, 0, anchor=tk.NW, image=img_tk)
                uiRenderFrame.image = img_tk
                #show detected gesture
                uiPreimportFrame.pack_forget()
                uiDetectedGestureFrame.grid(column=2, row=0, sticky=CTk.S)
                uiHistoryFrame.pack(side=CTk.LEFT, expand=False)
                


        uiPreimportOpenFileBtn = CTk.CTkButton(master=uiPreimportFrame, fg_color=Style.gestures, text_color=Style.blackText, text="Open File", font=uiFont, command=open_image,corner_radius=20, width= 60, height= 30)
        uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.W)


        # Action history Gui

        uiHistoryFrame = CTk.CTkFrame(master=uiMenuFrame, fg_color=Style.popupBackground, width=100, height=100)
        uiHistoryFrame.pack(side=CTk.LEFT, expand=False)

        uiActionHistory = ActionHistory(master=uiHistoryFrame, width=200, height=5,label_text="Action History", corner_radius=0, fg_color=Style.popupBackground,border_width= 3, border_color= Style.windowBorder)
        uiActionHistory.grid(row=0, column=0, padx=5, pady=5)
        
        # add test item to the Action history
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image = CTk.CTkImage(Image.open(os.path.join(current_dir, "Ui_Images", "HelpOr.jpg")))
        uiActionHistory.add_item(item = "test", image=image)

        # Function list

        # uiFunctionFrame = CTk.CTk


        ## Help UI #
        uiHelpFrame = CTk.CTkFrame(master=uiMenuFrame, fg_color="transparent")
        uiHelpFrame.pack(side=CTk.RIGHT, expand=False,)

        uiHelpLbl = CTk.CTkLabel(master=uiHelpFrame,bg_color= "transparent",text = "")
        uiHelpLbl.grid(column=0, row=0, padx=5, pady=5)

        uiHelpOrLbl = CTk.CTkLabel(master=uiHelpFrame, bg_color= "transparent",text = "")
        uiHelpOrLbl.grid(column=0, row=1 ,padx=5, pady=5)

        uiHelpBtn = CTk.CTkButton(master=uiHelpFrame ,fg_color=Style.gestures,text_color=Style.blackText,text="Help", font=uiFont, corner_radius=20, width= 60, height= 30, command=lambda:self.open_help(uiDetectedGesture.cget("text")))
        uiHelpBtn.grid(column=0, row=2)

        # Help UI #

        ## Camera UI ##
        uiDeviceCameraFrame = CTk.CTkFrame(master=uiMasterFrame,fg_color=Style.popupBackground)
        uiDeviceCameraFrame.grid(column=3, row=0, rowspan= 2)
        uiDeviceCamera = CTk.CTkLabel(master=uiDeviceCameraFrame ,bg_color= Style.workspaceBackground, text="")
        uiDeviceCamera.grid(column=0, row=0)
        #uiDeviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

        #Hide frames
        uiMasterFrame.grid_forget()
        uiRenderFrame.grid_forget()
        uiDetectedGestureFrame.grid_forget()
        uiHistoryFrame.pack_forget()
        
        
    
        ## TEST MATERIAL ##
        model_path = 'gesture_recognizer.task'
        with open(model_path,'rb') as file:
            model_data = file.read()

        looper = FrameLoop.GestureVision(self,uiDeviceCamera,uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget
        # functions = Functions.editFunctions(reference to image, reference to canvas etc.)
    def open_help(self ,affirmation):
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
    

