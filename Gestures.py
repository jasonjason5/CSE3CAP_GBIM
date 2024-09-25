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
        SAVEFILE = "Save File"
        OPENFILE = "Open File"
        HELP = "Help"
        UNDO = "Undo"
        REDO = "Redo"
        
        def gesture_help(cls):
            gestureHelp = {
                    Gesture.ROTATE: "Rotate: Use this gesture to rotate the image clockwise or counterclockwise.",
                    Gesture.CROP: "Crop: Used to enter and exit crop mode. Once in crop mode, utilise the resize gesture to position and scale the image under the crop visualisation.",
                    Gesture.RESIZE: "Resize: Shift the L shape of your fingers left or right to adjust the size of the image.",
                    Gesture.TRANSLATE: "Translate: Move the image around by moving your hand in the desired direction.",
                    Gesture.CONTRAST: "Contrast: Adjust the contrast of the image by moving your hand up or down.",
                    Gesture.BRIGHTNESS: "Brightness: Change the brightness of the image by raising or lowering your hand.",
                    Gesture.POINTER: "Pointer: Use this gesture to control the cursor with your hand movements. Activate it to click and interact with elements.",
                    Gesture.PEN: "Pen: Draw or write on the image using a finger, simulating a pen effect.",
                    Gesture.SAVEFILE: "Save File: Use this gesture to save the current image or project.",
                    Gesture.OPENFILE: "Open File: Use this gesture to open a new image file from your device.",
                    Gesture.HELP: "Help: Use this gesture to bring up the help menu or information about gestures.",
                    Gesture.UNDO: "Undo: Use this gesture to undo the previous editing step.",
                    Gesture.REDO: "Redo: Use this gesture to redo the previous editing step."
            }
            return gestureHelp[cls]
        def gesture_image(cls):
            gestureImage = {
                    Gesture.ROTATE: "Resources\RotateUI.gif",
                    Gesture.CROP: "Resources\CropUI.gif",
                    Gesture.RESIZE: "Resources\ResizeUI.gif",
                    Gesture.TRANSLATE :"Resources\TranslateUI.gif",
                    Gesture.CONTRAST :"Resources\ContrastUI.gif",
                    Gesture.BRIGHTNESS: "Resources\BrightnessUI.gif",
                    Gesture.POINTER: "Resources\PointerUI.gif",
                    Gesture.PEN: "Resources\PenUI.gif",
                    Gesture.SAVEFILE: "Resources\SaveUI.gif",
                    Gesture.OPENFILE: "Resources\OpenUI.gif",
                    Gesture.HELP: "Resources\HelpUI.gif",
                    Gesture.UNDO: "Resources\\UndoUI.gif",
                    Gesture.REDO: "Resources\RedoUI.gif"
            }
            return gestureImage[cls]
        
        def gesture_help_image(cls):
            gestureHelpImage = {
                    Gesture.ROTATE: "Resources\Rotate.gif",
                    Gesture.CROP: "Resources\Crop.gif",
                    Gesture.RESIZE: "Resources\Resize.gif",
                    Gesture.TRANSLATE :"Resources\Translate.gif",
                    Gesture.CONTRAST :"Resources\Contrast.gif",
                    Gesture.BRIGHTNESS: "Resources\Brightness.gif",
                    Gesture.POINTER: "Resources\Pointer.gif",
                    Gesture.PEN: "Resources\Pen.gif",
                    Gesture.SAVEFILE: "Resources\Save.gif",
                    Gesture.OPENFILE: "Resources\Open.gif",
                    Gesture.HELP: "Resources\Help.gif",
                    Gesture.UNDO: "Resources\\Undo.gif",
                    Gesture.REDO: "Resources\Redo.gif"
            } 
            return gestureHelpImage[cls]
       
        def return_enums(cls):
            enums = []
            for member in cls:  
                enums.append(member)
            return enums
        
        def string_to_enum(string):
            string = string.replace(" ", "")
            string = string.upper()
            return Gesture.__members__.get(string)
        
        def get_gesture_from_imagepath(cls, image_path):
            for member in cls:
                 string = Gesture.gesture_image(member)
                 if(string == image_path):
                      return member.value



#list = Gesture.return_enums(Gesture)
#print (list)
#print (list[0])
#print(Gesture.BRIGHTNESS.value + " = " +Gesture.gesture_help(Gesture.BRIGHTNESS))
print (Gesture.get_gesture_from_imagepath(Gesture, "Resources\RedoUI.gif"))
#print(Gesture.string_to_enum("Help"))

#print(Gesture.gesture_image(Gesture.HELP))