from enum import Enum

class Gesture(Enum):
        ROTATE = "Rotate"
        CROP = "Crop"
        RESIZE = "Resize"
        TRANSLATE = "Translate"
        CONTRAST = "Contrast"
        BRIGHTNESS = "Brightness"
        POINTER = "Pointer"
        PEN = "Pen"
        CLOSE = "Close"
        SAVEFILE = "Save File"
        OPENFILE = "Open File"
        OPENHAND = "Open Hand"
        CLOSEDHAND = "Closed Hand"
        HELP = "Help"
        def gesture_help(cls):
            gestureHelp = {
                    Gesture.ROTATE: "Rotate: Use this gesture to rotate the image clockwise or counterclockwise.",
                    Gesture.CROP: "Crop: Draw a rectangle around the area you want to keep. This will crop the image to that selection.",
                    Gesture.RESIZE: "Resize: Pinch in or out with your fingers to adjust the size of the image.",
                    Gesture.TRANSLATE: "Translate: Move the image around by swiping your hand in the desired direction.",
                    Gesture.CONTRAST: "Contrast: Adjust the contrast of the image by moving your hand up or down.",
                    Gesture.BRIGHTNESS: "Brightness: Change the brightness of the image by raising or lowering your hand.",
                    Gesture.POINTER: "Pointer: Use this gesture to control the cursor with your hand movements. Activate it to click and interact with elements.",
                    Gesture.PEN: "Pen: Draw or write on the image using a finger or stylus, simulating a pen effect.",
                    Gesture.CLOSE: "Close: Use this gesture to close the application or current window.",
                    Gesture.SAVEFILE: "Save File: Trigger this gesture to save the current image or project.",
                    Gesture.OPENFILE: "Open File: Use this gesture to open a new image file from your device.",
                    Gesture.OPENHAND: "Open Hand: Use this gesture to indicate that you want to select or open an item.",
                    Gesture.CLOSEDHAND: "Closed Hand: This gesture is used to confirm selections or actions.",
                    Gesture.HELP: "Help: Use this gesture to bring up the help menu or information about gestures."
            }
            return gestureHelp[cls]
        def gesture_image(cls):
            gestureImage = {
                    Gesture.ROTATE: "Resources\Rotate.gif",
                    Gesture.CROP: "Resources\Crop.gif",
                    Gesture.RESIZE: "Resources\Resize.gif",
                    Gesture.TRANSLATE :"Resources\Translate.gif",
                    Gesture.CONTRAST :"Resources\Contrast.gif",
                    Gesture.BRIGHTNESS: "Resources\Brightness.gif",
                    Gesture.POINTER: "Resources\Pointer.gif",
                    Gesture.PEN: "Resources\Pen.gif",
                    Gesture.CLOSE: "Resources\Brightness.gif",
                    Gesture.SAVEFILE: "Resources\Save.gif",
                    Gesture.OPENFILE: "Resources\Open.gif",
                    Gesture.OPENHAND: "Resources\Brightness.gif",
                    Gesture.CLOSEDHAND: "Resources\Brightness.gif",
                    Gesture.HELP: "Resources\Help.gif"
            }
            return gestureImage[cls]
        def return_enums(cls):
            enums = []
            for member in cls:  
                enums.append(member)
            return enums
        
        def string_to_enum(string):
            string = string.replace(" ", "")
            string = string.upper()
            return Gesture.__members__.get(string)


#list = Gesture.return_enums(Gesture)
#print (list)
#print (list[0])
#print(Gesture.BRIGHTNESS.value + " = " +Gesture.gesture_help(Gesture.BRIGHTNESS))

#print(Gesture.string_to_enum("Help"))

#print(Gesture.gesture_image(Gesture.HELP))