## PUT UI AND MODULE CALL LOGIC IN HERE ##
import MPRecognition
import FrameLoop
import Functions
import Style
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog




## Instead of using a different class to create the UI, it will be easier (both logistically and layout-wise) to just write the UI in here.
## Get rid of all the testing stuff when you're ready to put the UI down. This was just a test to see if I could get things passing properly between class modules.

def killStartFrame():
    uiStartFrame.destroy()
    uiMasterFrame.grid(column=0, row=1,ipadx=1280, sticky=tk.S)

def startCamera():
    killStartFrame()
    looper.updateFrame()


# Minimum size of window
min_width = 320
min_height = 320

#max size of window
#max_width = 1920
#max_height = 1080

uiRoot = tk.Tk()
uiRoot.title("Gesture Based Image Manipulation")
uiRoot.geometry("1280x720")
uiRoot.minsize(min_width, min_height)
#uiRoot.maxsize(max_width, max_height)
uiRoot.configure(background=Style.workspaceBackground)
uiRoot.rowconfigure(0, weight = 3)
uiRoot.rowconfigure(1, weight = 1)
uiRoot.rowconfigure(2, weight = 1)
uiRoot.columnconfigure(0, weight = 1)
uiRoot.columnconfigure(1, weight = 1)
uiRoot.columnconfigure(2, weight = 1)

uiRenderFrame = tk.Canvas(master=uiRoot, bg= Style.workspaceBackground)
uiRenderFrame.grid(column=0,columnspan= 3, row=0, ipadx=1280, ipady=100)


uiMasterFrame = tk.Frame(master=uiRoot, bg= Style.workspaceBackground)
uiMasterFrame.grid(column=0, columnspan= 3,row=2,ipadx=1280, sticky=tk.S)
uiMasterFrame.columnconfigure(0, weight = 1)
uiMasterFrame.columnconfigure(1, weight = 1)
uiMasterFrame.columnconfigure(2, weight = 1)
uiMasterFrame.columnconfigure(3, weight = 1)
uiMasterFrame.rowconfigure(0, weight = 1)
uiMasterFrame.rowconfigure(1, weight = 2)


uiDetectedGestureFrame =tk.Frame(master=uiMasterFrame, bg='black')
uiDetectedGestureFrame.grid(column=2, row=0, sticky=tk.S)
uiDetectedGesture = tk.Label(master=uiDetectedGestureFrame,bg='black',fg=Style.whiteText,text="Gesture")
uiDetectedGesture.grid(column=0, row=0, sticky=tk.SW, ipadx=400, ipady=40)

# menu frame, holds the gesture help, open file, action history, gesture function list
uiMenuFrame = tk.Frame(master=uiMasterFrame, bg=Style.popupBackground)
uiMenuFrame.grid(column=0, columnspan= 3, row=1, sticky=tk.EW)


## Static UI ##

## Splash Start UI ##

uiStartFrame = tk.Frame(master=uiRoot, height=100,width=500, bg=Style.popupBackground)
uiStartFrame.place(relx=0.5,rely=0.5,anchor='center')

uiStartWelcome = tk.Label(master=uiStartFrame,bg=Style.popupBackground, fg=Style.whiteText,text="Welcome to [Application Name]!")
uiStartWelcome.place(relx=0.5,rely=0.3,anchor='center')

uiStartButton = tk.Button(master=uiStartFrame,text="Start Device Camera", bg=Style.gestures, fg=Style.blackText, command = startCamera)
uiStartButton.place(relx=0.5,rely=0.7,anchor='center')

## Splash Start UI ##



## Pre import UI ##

uiPreimportFrame = tk.Frame(master=uiMenuFrame, bg=Style.popupBackground)
uiPreimportFrame.pack(side=tk.LEFT, expand=False)
uiPreimportOpenFileLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Open File")
uiPreimportOpenFileLbl.grid(column=0, row=0, sticky=tk.SW, ipadx=30, ipady=30)
uiPreimportOpenConfirmLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Confirm")
uiPreimportOpenConfirmLbl.grid(column=1, row=0, sticky=tk.SW, ipadx=30, ipady=30)
uiPreimportOpenOrLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="OR")
uiPreimportOpenOrLbl.grid(column=2, row=0, sticky=tk.SW, ipadx=30, ipady=30)
uiPreimportOpenFileBtn = tk.Button(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Open File")
uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.SW, ipadx=30, ipady=30)

## Pre import UI ##

def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")],
        title="Select an Image File"
    )
    
    if file_path:
        img = Image.open(file_path)
        img = img.resize((1280, 720), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)
        
        uiRenderFrame.delete("all")
        uiRenderFrame.create_image(0, 0, anchor=tk.NW, image=img_tk)
        uiRenderFrame.image = img_tk 

uiPreimportOpenFileBtn = tk.Button(master=uiPreimportFrame, bg=Style.gestures, fg=Style.blackText, text="Open File", command=open_image)
uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.SW, ipadx=30, ipady=30)

## Help UI #
uiHelpFrame = tk.Frame(master=uiMenuFrame, bg=Style.popupBackground)
uiHelpFrame.pack(side=tk.RIGHT, expand=False)
uiHelpLbl = tk.Label(master=uiHelpFrame,bg=Style.gestures,fg=Style.blackText,text="Help")
uiHelpLbl.grid(column=0, row=0, sticky=tk.SW, ipadx=30, ipady=20)
uiHelpBtn = tk.Button(master=uiHelpFrame ,bg=Style.gestures,fg=Style.blackText,text="Help")
uiHelpBtn.grid(column=0, row=1, sticky=tk.SW, ipadx=30, ipady=20)

# Help UI #

## Camera UI ##

uiDeviceCamera = tk.Label(master=uiMasterFrame,bg= Style.popupBackground)
uiDeviceCamera.grid(column=3, row=0, rowspan= 2, sticky=tk.EW)
#uiDeviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

uiMasterFrame.grid_forget()

## TEST MATERIAL ##
model_path = 'gesture_recognizer.task'
with open(model_path,'rb') as file:
    model_data = file.read()

looper = FrameLoop.GestureVision(uiRoot,uiDeviceCamera,uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget
# functions = Functions.editFunctions(reference to image, reference to canvas etc.)

## TEST MATERIAL ##

if __name__ == "__main__":
    uiRoot.mainloop()
    

