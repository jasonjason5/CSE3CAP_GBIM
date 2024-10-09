from enum import Enum

class Gesture(Enum):
        """
        Class of tupe enum that holds all of the available gestures.
        includes functions to return the help text and images for all gestures.

        """
        ROTATE = "Rotate"
        CROP = "Crop"
        RESIZE = "Resize"
        TRANSLATE = "Translate"
        CONTRAST = "Contrast"
        BRIGHTNESS = "Brightness"
        POINTER = "Pointer"
        PEN = "Pen"
        HELP = "Help"
        UNDO = "Undo"
        REDO = "Redo"
        SAVEFILE = "Save File"
        OPENFILE = "Open File"
        
        def gesture_help(cls :Enum) -> str:
            """
            Returns the help text of the gesture inputted to the function

            :type cls: Gesture that you require the help text for
            :param cls: Enum of type Gesture
            :return: Returns the help text
            :rtype: String

            :Example:
            >>> print(Gesture.gesture_help(Gesture.BRIGHTNESS))
            Brightness: Change the brightness of the image by raising or lowering your hand.
            """
            gestureHelp = {
                    Gesture.ROTATE: "Rotate: Use this gesture to rotate the image clockwise or counterclockwise.",
                    Gesture.CROP: "Crop: Used to enter and exit crop mode. Once in crop mode, utilise the resize gesture to position and scale the image under the crop visualisation.",
                    Gesture.RESIZE: "Resize: Shift the L shape of your fingers left or right to adjust the size of the image.",
                    Gesture.TRANSLATE: "Translate: Move the image around by moving your hand in the desired direction.",
                    Gesture.CONTRAST: "Contrast: Adjust the contrast of the image by moving your hand up or down.",
                    Gesture.BRIGHTNESS: "Brightness: Change the brightness of the image by raising or lowering your hand.",
                    Gesture.POINTER: "Pointer: Use this gesture to control the cursor with your hand movements. Activate it to click and interact with elements.",
                    Gesture.PEN: "Pen: Draw or write on the image using a finger, simulating a pen effect.",
                    Gesture.HELP: "Help: Use this gesture to bring up the help menu or information about gestures.",
                    Gesture.UNDO: "Undo: Use this gesture to undo the previous editing step.",
                    Gesture.REDO: "Redo: Use this gesture to redo the previous editing step.",
                    Gesture.SAVEFILE: "Save File: Use this gesture to save the current image or project.",
                    Gesture.OPENFILE: "Open File: Use this gesture to open a new image file from your device."
            }
            return gestureHelp[cls]
        def gesture_image(cls :Enum) -> str:
            """
            Returns the path of the image for function menu of the gesture inputted to the function

            :type cls: Gesture that you require the function menu image of
            :param cls: Enum of type Gesture
            :return: Returns the path of the the image
            :rtype: String

            :Example:
            >>> print(Gesture.gesture_image(Gesture.HELP))
            Resources\Helpui.gif
            """
            gestureImage = {
                    Gesture.ROTATE: "Resources\RotateUI.gif",
                    Gesture.CROP: "Resources\CropUI.gif",
                    Gesture.RESIZE: "Resources\ResizeUI.gif",
                    Gesture.TRANSLATE :"Resources\TranslateUI.gif",
                    Gesture.CONTRAST :"Resources\ContrastUI.gif",
                    Gesture.BRIGHTNESS: "Resources\BrightnessUI.gif",
                    Gesture.POINTER: "Resources\PointerUI.gif",
                    Gesture.PEN: "Resources\PenUI.gif",
                    Gesture.HELP: "Resources\Helpui.gif",
                    Gesture.UNDO: "Resources\\Undoui.gif",
                    Gesture.REDO: "Resources\Redoui.gif",
                    Gesture.SAVEFILE: "Resources\SaveUI.gif",
                    Gesture.OPENFILE: "Resources\OpenUI.gif"
            }
            return gestureImage[cls]
        
        def gesture_help_image(cls :Enum) -> str:
            """
            Returns the path of the the gif for the help window of the gesture inputted to the function

            :type cls: Gesture that you require the help window gif of
            :param cls: Enum of type Gesture
            :return: Returns the path of the the gif
            :rtype: String

            :Example:
            >>> print(Gesture.gesture_help_image(Gesture.HELP))
            Resources\Help.gif
            """            
            gestureHelpImage = {
                    Gesture.ROTATE: "Resources\Rotate.gif",
                    Gesture.CROP: "Resources\Crop.gif",
                    Gesture.RESIZE: "Resources\Resize.gif",
                    Gesture.TRANSLATE :"Resources\Translate.gif",
                    Gesture.CONTRAST :"Resources\Contrast.gif",
                    Gesture.BRIGHTNESS: "Resources\Brightness.gif",
                    Gesture.POINTER: "Resources\Pointer.gif",
                    Gesture.PEN: "Resources\Pen.gif",
                    Gesture.HELP: "Resources\Help.gif",
                    Gesture.UNDO: "Resources\\Undo.gif",
                    Gesture.REDO: "Resources\Redo.gif",
                    Gesture.SAVEFILE: "Resources\Save.gif",
                    Gesture.OPENFILE: "Resources\Open.gif"
            } 
            return gestureHelpImage[cls]
       
        def return_enums(cls) -> list:
            """
            Returns the full list of gestures

            :type cls: The Gesture class
            :param cls: The Gesture class
            :return: a list of all Gesture:Enums
            :rtype: GestureList

            :Example:
            >>> print(Gesture.return_enums(Gesture))
            [<Gesture.ROTATE: 'Rotate'>, <Gesture.CROP: 'Crop'>, ...etc
            """         
            enums = []
            for member in cls:  
                enums.append(member)
            return enums
        
        def string_to_enum(string: str) ->Enum:
            """
            Takes in a string eg: "Rotate","crop" and returns the Gesture:Enum assosiated

            :type string: The Gesture string
            :param string: str
            :return: the Gesture:Enum assosiated with the string
            :rtype: GestureEnum

            :Example:
            >>> print(Gesture.string_to_enum("Help"))
            Gesture.HELP
            """  
            string = string.replace(" ", "")
            string = string.upper()
            return Gesture.__members__.get(string)
        
        def get_gesture_from_imagepath(cls, image_path) ->Enum:
            """
            Takes in a image path string eg "Resources\Penui.gif","Resources\Redoui.gif" and returns the GestureEnum assosiated

            :type image_path: The imagepath string
            :param image_path: str
            :return: the Gesture:Enum assosiated with image_path
            :rtype: GestureEnum

            :Example:
            >>> print(Gesture.get_gesture_from_imagepath(Gesture, "Resources\SaveUI.gif"))
            Save File
            """  
            for member in cls:
                 string = Gesture.gesture_image(member)
                 if(string == image_path):
                      return member.value
