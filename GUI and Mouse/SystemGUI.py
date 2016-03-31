from pubsub import pub
import Tkinter as Tk

########################################################################
class OtherFrame(Tk.Toplevel):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        Tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title("otherFrame")
        
        # create the button
        btn = Tk.Button(self, text="Close", command=self.onClose)
        btn.pack()
    
    #----------------------------------------------------------------------
    def onClose(self):
        """
            closes the frame and sends a message to the main frame
            """
        self.destroy()
        pub.sendMessage("otherFrameClosed", arg1="data")

########################################################################
class StartScreen(object):
    """"""
    
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
        self.frame = Tk.Frame(parent, width = w, height = h, bg = 'red')
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(columnspan = 4)
        
        
        welcomeLabel = Tk.Label(self.frame, text = "Welcome!", width = 45)
        calibrateButton = Tk.Button(self.frame, text="Calibrate", command=self.openFrame)
        quitButton = Tk.Button(self.frame, text="Quit", command=self.quitScreen)
       
       #welcomeLabel.columnconfigure(0, weight=1)
        welcomeLabel.grid(row = 0, columnspan =4)
        
        calibrateButton.grid(row = 1, column = 2)
        quitButton.grid(row = 1, column = 3)
        
        pub.subscribe(self.listener, "otherFrameClosed")
    
    #----------------------------------------------------------------------
    def listener(self, arg1, arg2=None):
        """
            pubsub listener - opens main frame when otherFrame closes
            """
        self.show()
    
    #----------------------------------------------------------------------
    def hide(self):
        """
            hides main frame
            """
        self.root.withdraw()
    
    #----------------------------------------------------------------------
    def openFrame(self):
        """
            opens other frame and hides main frame
            """
        self.hide()
        subFrame = OtherFrame()
    
    #----------------------------------------------------------------------
    def show(self):
        """
            shows main frame
            """
        self.root.update()
        self.root.deiconify()
    
    #---------------------------------------------------------------------
    def quitScreen(self):
        self.root.destroy()


#----------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk.Tk()
    app = StartScreen(root)
    root.mainloop()