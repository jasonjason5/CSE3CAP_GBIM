## PUT UI AND MODULE CALL LOGIC IN HERE ##
import MPRecognition
import FrameLoop
import Functions
import Style
import customtkinter as CTk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog




## Instead of using a different class to create the UI, it will be easier (both logistically and layout-wise) to just write the UI in here.
## Get rid of all the testing stuff when you're ready to put the UI down. This was just a test to see if I could get things passing properly between class modules.

class ImageLoader:
    def __init__(self, label, image_path, ui_type):
        self.label = label
        self.image_path = image_path
        self.ui_type = ui_type
        self.load_image()

    def load_image(self):
        # Open the image file
        image = Image.open(self.image_path)
        #resize the image
        if self.ui_type == "Preimport":
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
        if self.ui_type == "Help":
            image = image.resize((100, 100), Image.Resampling.LANCZOS) 
        if self.ui_type == "Or":
            image = image.resize((50, 20), Image.Resampling.LANCZOS)  
        self.tk_image = ImageTk.PhotoImage(image)
        # Set the image on the label
        self.label.config(image=self.tk_image)
        # Keep a reference to the image to prevent garbage collection
        self.label.image = self.tk_image


def LoadImages():
    ImageLoader(uiPreimportOpenFileLbl,'C:/Users/Latrobe/Project/CSE3CAP_GBIM/Ui_Images/Openfile.jpg',"Preimport")
    ImageLoader(uiPreimportOpenConfirmLbl ,'C:/Users/Latrobe/Project/CSE3CAP_GBIM/Ui_Images/Confirm.jpg',"Preimport")
    ImageLoader(uiPreimportOpenOrLbl,'C:/Users/Latrobe/Project/CSE3CAP_GBIM/Ui_Images/Or.jpg',"Help")
    ImageLoader(uiHelpLbl,'C:/Users/Latrobe/Project/CSE3CAP_GBIM/Ui_Images/Help.jpg',"Help")
    ImageLoader(uiHelpOrLbl,'C:/Users/Latrobe/Project/CSE3CAP_GBIM/Ui_Images/HelpOr.jpg',"Or")
   
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

uiRoot = CTk.CTk()
uiRoot.title("Gesture Based Image Manipulation")
uiRoot.geometry("1280x720")
uiRoot.minsize(min_width, min_height)
#uiRoot.maxsize(max_width, max_height)
uiRoot.configure(bg_color=Style.workspaceBackground,fg_color= Style.workspaceBackground)
uiRoot.rowconfigure(0, weight = 3)
uiRoot.rowconfigure(1, weight = 1)
uiRoot.columnconfigure(0, weight = 1)
uiRoot.columnconfigure(1, weight = 1)
uiRoot.columnconfigure(2, weight = 1)

uiRenderFrame = tk.Canvas(master=uiRoot, bg= Style.workspaceBackground, bd=0,highlightthickness=0, relief='ridge')
uiRenderFrame.grid(column=1, row=0)



uiMasterFrame =CTk.CTkFrame(master=uiRoot, fg_color= Style.workspaceBackground, bg_color= Style.workspaceBackground)
uiMasterFrame.grid(column=0, columnspan= 3,row=1)
uiMasterFrame.columnconfigure(0, weight = 1)
uiMasterFrame.columnconfigure(1, weight = 1)
uiMasterFrame.columnconfigure(2, weight = 1)
uiMasterFrame.columnconfigure(3, weight = 1)
uiMasterFrame.rowconfigure(0, weight = 1)
uiMasterFrame.rowconfigure(1, weight = 2)


uiDetectedGestureFrame =CTk.CTkFrame(master=uiMasterFrame)
uiDetectedGestureFrame.grid(column=2, row=0, sticky=CTk.S)
uiDetectedGestureText = CTk.CTkLabel(master=uiDetectedGestureFrame, fg_color=Style.gestures,text_color=Style.blackText,text="Current Edit Gesture: ", corner_radius= 100)
uiDetectedGestureText.grid(column=0, row=0)
uiDetectedGesture = CTk.CTkLabel(master=uiDetectedGestureFrame, fg_color=Style.gestures,text_color=Style.blackText,text="Gesture",corner_radius= 100)
uiDetectedGesture.grid(column=1, row=0 )

# menu frame, holds the gesture help, open file, action history, gesture function list
uiMenuFrame = CTk.CTkFrame(master=uiMasterFrame, fg_color=Style.popupBackground, border_width= 3, border_color= "black",) 
uiMenuFrame.grid(column=0, columnspan= 3, row=1, sticky=CTk.EW, ipadx=20, ipady=20)


## Static UI ##

## Splash Start UI ##

uiStartFrame = CTk.CTkFrame(master=uiRoot, height=100,width=500, fg_color=Style.popupBackground, border_color = "black")
uiStartFrame.place(relx=0.5,rely=0.5,anchor='center')

uiStartWelcome = CTk.CTkLabel(master=uiStartFrame,fg_color=Style.popupBackground, text_color=Style.whiteText,text="Welcome to [Application Name]!")
uiStartWelcome.place(relx=0.5,rely=0.3,anchor='center')

uiStartButton = CTk.CTkButton(master=uiStartFrame,text="Start Device Camera", fg_color=Style.gestures, text_color=Style.blackText, command = startCamera)
uiStartButton.place(relx=0.5,rely=0.7,anchor='center')

## Splash Start UI ##



## Pre import UI ##

uiPreimportFrame = CTk.CTkFrame(master=uiMenuFrame, fg_color="transparent")
uiPreimportFrame.pack(side=CTk.LEFT, expand=False)

uiPreimportOpenFileLbl = tk.Label(master=uiPreimportFrame, bg= Style.popupBackground)
uiPreimportOpenFileLbl.grid(column=0, row=0,ipadx=20, ipady=20)

uiPreimportOpenConfirmLbl = tk.Label(master=uiPreimportFrame, bg= Style.popupBackground)
uiPreimportOpenConfirmLbl.grid(column=1, row=0, ipadx=20, ipady=20)

uiPreimportOpenOrLbl = tk.Label(master=uiPreimportFrame, bg= Style.popupBackground)
uiPreimportOpenOrLbl.grid(column=2, row=0,ipadx=20, ipady=20)

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
        uiDetectedGestureFrame.grid(column=2, row=0, sticky=CTk.S)


uiPreimportOpenFileBtn = CTk.CTkButton(master=uiPreimportFrame, fg_color=Style.gestures, text_color=Style.blackText, text="Open File", command=open_image,corner_radius=20, width= 60, height= 30)
uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.W)


# Action history Gui

uiHistoryFrame = CTk.CTkFrame(master=uiMenuFrame, fg_color=Style.popupBackground)
uiHistoryFrame.pack(side=CTk.RIGHT, expand=False)



## Help UI #
uiHelpFrame = CTk.CTkFrame(master=uiMenuFrame, fg_color=Style.popupBackground)
uiHelpFrame.pack(side=CTk.RIGHT, expand=False)

uiHelpLbl = tk.Label(master=uiHelpFrame, borderwidth= 0,bg= Style.popupBackground)
uiHelpLbl.grid(column=0, row=0, ipadx=5, ipady=5)

uiHelpOrLbl = tk.Label(master=uiHelpFrame, borderwidth= 0, bg= Style.popupBackground)
uiHelpOrLbl.grid(column=0, row=1 ,ipadx=5, ipady=5)

uiHelpBtn = CTk.CTkButton(master=uiHelpFrame ,fg_color=Style.gestures,text_color=Style.blackText,text="Help", corner_radius=20, width= 60, height= 30)
uiHelpBtn.grid(column=0, row=2)

# Help UI #

## Camera UI ##

uiDeviceCamera = tk.Label(master=uiMasterFrame,bg= Style.workspaceBackground, fg= Style.workspaceBackground)
uiDeviceCamera.grid(column=3, row=0, rowspan= 2, sticky=tk.S)
#uiDeviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

uiMasterFrame.grid_forget()
uiRenderFrame.grid_forget()
uiDetectedGestureFrame.grid_forget()

## TEST MATERIAL ##
model_path = 'gesture_recognizer.task'
with open(model_path,'rb') as file:
    model_data = file.read()

looper = FrameLoop.GestureVision(uiRoot,uiDeviceCamera,uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget
# functions = Functions.editFunctions(reference to image, reference to canvas etc.)

## TEST MATERIAL ##

if __name__ == "__main__":
    uiRoot.mainloop()
    

