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

uiRoot = tk.Tk()
uiRoot.title("Gesture Based Image Manipulation")
uiRoot.geometry("1280x720")

uiRootFrame = tk.Frame(master=uiRoot,bg= Style.workspaceBackground)
uiRootFrame.place(relheight=1, relwidth=1)

uiDeviceCamera = tk.Label(master=uiRoot,bg= Style.workspaceBackground)
uiDeviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

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

uiPreimportFrame = tk.Frame(master=uiRootFrame,height=219, bg=Style.popupBackground)
uiPreimportFrame.place(relx=.5, rely=.8,relheight=1, relwidth=1, anchor='n')

uiPreimportOpenFileBtn = tk.Button(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Open File")
uiPreimportOpenFileBtn.place(relx=0.5, rely= 0.1, anchor='center')

uiPreimportOpenFileLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Open File")
uiPreimportOpenFileLbl.place(relx=0.1, rely= 0.1, anchor='w')

uiPreimportOpenConfirmLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Confirm")
uiPreimportOpenConfirmLbl.place(relx=0.2, rely= 0.1, anchor='w')

## Pre import UI ##

## Help UI #
uiHelpFrame = tk.Frame(master=uiRootFrame,height=219, bg=Style.popupBackground)
uiHelpFrame.place(relx=.5, rely=.8,relheight=1, relwidth=1, anchor='n')

uiHelpBtn = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Help")
uiHelpBtn.place(relx=0.7, rely= 0.2, anchor='e')

uiHelpLbl = tk.Label(master=uiPreimportFrame,bg=Style.gestures,fg=Style.blackText,text="Help")
uiHelpLbl.place(relx=0.7, rely= 0.1, anchor='e')

# Help UI #


## TEST MATERIAL ##
model_path = 'gesture_recognizer.task'
with open(model_path,'rb') as file:
    model_data = file.read()

looper = FrameLoop.GestureVision(uiRoot,uiDeviceCamera,uiDetectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget
# functions = Functions.editFunctions(reference to image, reference to canvas etc.)

## TEST MATERIAL ##

if __name__ == "__main__":
    uiRoot.mainloop()
    

