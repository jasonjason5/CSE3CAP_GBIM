## PUT UI AND MODULE CALL LOGIC IN HERE ##
import MPRecognition
import FrameLoop
import Functions

import tkinter as tk



## Instead of using a different class to create the UI, it will be easier (both logistically and layout-wise) to just write the UI in here.
## Get rid of all the testing stuff when you're ready to put the UI down. This was just a test to see if I could get things passing properly between class modules.


## TEST UI ##

root = tk.Tk()
root.title("Gesture Based Image Manipulation")
root.geometry("1280x720")

deviceCamera = tk.Label(master=root)
deviceCamera.place(relx=1.0,rely=1.0,x=0,y=0,anchor='se')

detectedGesture = tk.Label(master=root,height=5,width=200,bg='black',fg='white',text="Gesture")
detectedGesture.place(relx=0.5,rely=0.1,anchor='center')

## TEST UI


## TEST MATERIAL ##
model_path = 'gesture_recognizer.task'
with open(model_path,'rb') as file:
    model_data = file.read()

looper = FrameLoop.GestureVision(root,deviceCamera,detectedGesture,model_data) ##instantiates gesturevision object (frameloop), passes references to ui root and device camera widget

def startCamera():
    looper.updateFrame()
    

startButton = tk.Button(master=root,text="Start Camera",command = startCamera)
startButton.place(relx=0.5,rely=0.9,anchor='center')

## TEST MATERIAL ##

if __name__ == "__main__":
    root.mainloop()
    