## PUT UI AND MODULE CALL LOGIC IN HERE ##
import MPRecognition
import FrameLoop
import Functions
import Style
import tkinter as tk



## Instead of using a different class to create the UI, it will be easier (both logistically and layout-wise) to just write the UI in here.
## Get rid of all the testing stuff when you're ready to put the UI down. This was just a test to see if I could get things passing properly between class modules.

def killStartFrame():
    uiStartFrame.destroy()

def startCamera():
    killStartFrame()
    looper.updateFrame()


## Static UI ##
global uiRoot;

# Minimum size of window
min_width = 320
min_height = 320

uiRoot = tk.Tk()
uiRoot.title("Gesture Based Image Manipulation")
uiRoot.geometry("1280x720")
uiRoot.minsize(min_width, min_height)
#uiRoot.attributes('-alpha',0.5)

# Root frame, holds all other frames
uiRootFrame = tk.Frame(master=uiRoot,bg= Style.workspaceBackground)
uiRootFrame.place(relheight=1, relwidth=1)

# master frame, Holds the camera frame, menu frame, and current gesture frame
uiMasterFrame = tk.Frame(master=uiRootFrame, bg=Style.workspaceBackground)
uiMasterFrame.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)

uiMasterFrame.columnconfigure(0, weight = 4)
uiMasterFrame.columnconfigure(1, weight = 1)

uiMasterFrame.rowconfigure(0, weight = 1)
uiMasterFrame.rowconfigure(1, weight = 2)

# menu frame, holds the gesture help, open file, action history, gesture function list
uiMenuFrame = tk.Frame(master=uiMasterFrame, bg=Style.popupBackground)
uiMenuFrame.grid(column=0, row=1, sticky=tk.S)

uiDetectedGesture = tk.Label(master=uiRoot,height=5,width=200,bg='black',fg=Style.whiteText,text="Gesture")
uiDetectedGesture.place(relx=0.5,rely=0.1,anchor='center')
## Static UI ##

## Splash Start UI ##

uiStartFrame = tk.Frame(master=uiRootFrame, height=100,width=500, bg=Style.popupBackground)
uiStartFrame.place(relx=0.5,rely=0.5,anchor='center')

uiStartWelcome = tk.Label(master=uiStartFrame,bg=Style.popupBackground, fg=Style.whiteText,text="Welcome to [Application Name]!")
uiStartWelcome.place(relx=0.5,rely=0.3,anchor='center')

uiStartButton = tk.Button(master=uiStartFrame,text="Start Device Camera", bg=Style.gestures, fg=Style.blackText, command = startCamera)
uiStartButton.place(relx=0.5,rely=0.7,anchor='center')

## Splash Start UI ##



## Pre import UI ##

uiPreimportFrame = tk.Frame(master=uiMenuFrame)
uiPreimportFrame.pack(side=tk.LEFT, expand=True)
#uiPreimportFrame.columnconfigure(0, weight=1)
#uiPreimportFrame.rowconfigure(0, weight=1)

uiPreimportOpenFileLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Open File")
uiPreimportOpenFileLbl.grid(column=0, row=0, sticky=tk.SW, ipadx=30, ipady=30)

uiPreimportOpenConfirmLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Confirm")
uiPreimportOpenConfirmLbl.grid(column=1, row=0, sticky=tk.SW, ipadx=30, ipady=30)

uiPreimportOpenOrLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="OR")
uiPreimportOpenOrLbl.grid(column=2, row=0, sticky=tk.SW, ipadx=30, ipady=30)

uiPreimportOpenFileBtn = tk.Button(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Open File")
uiPreimportOpenFileBtn.grid(column=3, row=0, sticky=tk.SW, ipadx=30, ipady=30)

#.pack(side=tk.LEFT, expand=False, ipadx=20, ipady=20

## Pre import UI ##

## Help UI #
uiHelpFrame = tk.Frame(master=uiMenuFrame, bg=Style.popupBackground)
uiHelpFrame.pack(side=tk.LEFT, expand=True)

uiHelpLbl = tk.Label(master=uiHelpFrame,bg=Style.gestures,fg=Style.blackText,text="Help")
uiHelpLbl.pack(side=tk.TOP, expand=False, ipadx=40, ipady=20)

uiHelpBtn = tk.Button(master=uiHelpFrame ,bg=Style.gestures,fg=Style.blackText,text="Help")
uiHelpBtn.pack(side=tk.TOP, expand=False, ipadx=40, ipady=20)

# Help UI #

## Camera UI ##

uiDeviceCamera = tk.Label(master=uiMasterFrame,bg= Style.workspaceBackground)
uiDeviceCamera.grid(column=1, row=0, rowspan= 2, sticky=tk.E)
#uiDeviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

## TEST MATERIAL ##
model_path = 'gesture_recognizer.task'
with open(model_path,'rb') as file:
    model_data = file.read()

looper = FrameLoop.GestureVision(uiRoot,uiDeviceCamera,uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget
# functions = Functions.editFunctions(reference to image, reference to canvas etc.)

## TEST MATERIAL ##

if __name__ == "__main__":
    uiRoot.mainloop()
    

