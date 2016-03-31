from pubsub import pub
import Tkinter as Tk

########################################################################
class StartScreen(object):

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
    
        w = 400
        h = 200
        x = (screenwidth / 2) - (w / 2)
        y = (screenheight / 2) - (h / 2)
    
        self.root = parent
        self.root.title("Welcome")
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.focus_force()
        self.frame = Tk.Frame(parent, width = w, height = h)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(rowspan = 5, columnspan = 4)
        self.buttonFrame = Tk.Frame(parent, width = w)
        self.buttonFrame.grid(row = 5, rowspan = 1, columnspan = 4, sticky = 'S')
        
        
        welcomeLabel = Tk.Label(self.frame, text = "Welcome!", width = 44)
        calibrateButton = Tk.Button(self.buttonFrame, text="Calibrate", command=self.openCalFrame)
        quitButton = Tk.Button(self.buttonFrame, text="Quit", command=self.quitScreen)
        welcomeLabel.grid(row = 0, columnspan =4)
        
        calibrateButton.grid(row = 1, column = 2)
        quitButton.grid(row = 1, column = 3)
    
    #----------------------------------------------------------------------
    #When the calibrate button is pressed
    def openCalFrame(self):
        self.hide()
        subFrame = CalibrationFrame()
    
    def hide(self):
        self.root.withdraw()
    
    #---------------------------------------------------------------------
    #When the quit button is pressed
    def quitScreen(self):
        self.root.destroy()

########################################################################
#The frame shown to allow the user to calibrate the system
class CalibrationFrame(Tk.Toplevel):
    #----------------------------------------------------------------------
    #GUI setup
    def __init__(self):
        """Constructor"""
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        
        Tk.Toplevel.__init__(self)
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(screenwidth, screenheight))
        
        canvasFrame = Tk.Frame(self, width = screenwidth, height = (screenheight - 100))
        instructionFrame = Tk.Frame(self, width = screenwidth, height = 50)
        self.canvas = Tk.Canvas(canvasFrame, width = screenwidth, height = (screenheight - 100))
        
        # create the button
        calibrateButton = Tk.Button(instructionFrame, text="Start Calibration", command=self.ovalChange)
        exitButton = Tk.Button(instructionFrame, text="Quit", command=self.quitCal)
        
        canvasFrame.grid()
        instructionFrame.grid(row = 1)
        
        self.canvas.grid()
        
        calibrateButton.grid(column = 0)
        exitButton.grid(column = 1, row = 0)
        
        pub.subscribe(self.listener, "userFrameClosed")
    
    #----------------------------------------------------------------------
    #Called when exit is pressed
    def quitCal(self):
        self.quit()
        self.destroy()
    
    #--------------------------------------------------------------------
    #When the calibration button is pressed
    def ovalChange(self):
        print "Calibration here"
        self.openUserFrame()
    
    #Open the user frame
    def openUserFrame(self):
        self.hide()
        subFrame = UserFrame()
   
   #Hide the calibration frame
    def hide(self):
        self.withdraw()
    
    #----------------------------------------------------------------------
    #When the user frame is closed, show the calibration screen
    def listener(self, arg1, arg2=None):
        print'Show calScreen'
        self.show()
    
    #Update the frame
    def show(self):
        self.update()
        self.deiconify()

########################################################################
#The frame shown when the user is interacting wiht the computer
class UserFrame(Tk.Toplevel):
    
    #----------------------------------------------------------------------
    #GUI setup
    def __init__(self):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        
        Tk.Toplevel.__init__(self)
        w = 230
        h = 200
        x = screenwidth - (w + 10)
        y = screenheight - (h + 60)
        
        self.title("User Frame")
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        #Create button frame
        self.buttonFrame = Tk.Frame(self, width = w, height = h)
        self.buttonFrame.grid()
        #Create buttons
        recalibrateButton = Tk.Button(self.buttonFrame, text = "Recalibrate", command = self.recalibrate)
        quitButton = Tk.Button(self.buttonFrame, text = "Quit", command = self.quit)
        recalibrateButton.grid(row = 0, column = 0)
        quitButton.grid(row = 0, column = 1)
    
    #----------------------------------------------------------------------
    #Called when quit is pressed
    def quitCal(self):
        self.destroy()
    
    #----------------------------------------------------------------------
    #Called when re-calibrate button is pressed
    #Send a message to pub to start the calibration again
    def recalibrate(self):
        self.destroy()
        pub.sendMessage("userFrameClosed", arg1="data")

########################################################################


#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    app = StartScreen(root)
    root.mainloop()