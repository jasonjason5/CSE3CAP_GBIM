## PUT EDITING FUNCTIONS IN HERE ##
## Hey Harry. Thought I'd put some thoughts in here. I think the most logical way to go about this would be to have this as a class we can instantiate in Main
## Something like class editFunction(self):, that way we could store variables we need to keep track of i.e image start size, start position etc.
## within the properties of the class, and stop them from being changed everytime a function (The edit operations) from this class is called on each frame 
##
## For example - Resize. We have functions(self,image) (an object of this class) in Main. We pass the image into it and store all the important information
## Then when a gesture is done being detected from MPRecognition, we pass the gesture's name to the FrameLoop and FrameLoop.callFunction("Whatever gesture was detected")
## callFunction will go through if/else to find the right one, and then call the appropriate method of from the object of this class i.e editFunction.resize()
##
## then, the method has the results (hand landmarks) and the initial photo information that will be an unchanging reference point for the duration needed. Since it will be called every
## frame we have the realtime update as long as the image is placed back on the tkinter canvas at the end of each frame's call. Since we have the hand landmarks,
## we've got all the math we need.
##
##
## Feel free to experiment or do it in whatever way makes the most sense though - just thought I'd give you my idea as a starting point
##
##
##
##