from tkinter import * 
from tkinter.ttk import *
from DemoController import *
from GameController import *
from Help import *

#The Main Controller doesn't do much: it creates frames to hold
#1) the main menu,
#2) a game panel,
#3) a demo panel.
#4) a top window for instruction
#and responds to events to decide what to display or to exit.

LABEL_NORM_FONT = ("papyrus", 15)
LABEL_ACTIVE_FONT = ("papyrus", 17)

class MainController:
    def __init__(self, root):
        self.root = root
        self.root.title("The Towers of Hanoi")

        #create the menu page, create and pack images and widgets
        self.mainFrame = Frame(self.root, borderwidth = 15)
        self.mainFrame.pack()

        self.title = Label(self.mainFrame, text = "The Towers of Hanoi",\
                            font = ("papyrus", 30, "bold"))
        self.title.grid(row = 0, column = 0, columnspan = 2)
        
        self.background = PhotoImage(file = "hanoi1.gif")
        self.imageLabel = Label(self.mainFrame, image = self.background)
        self.imageLabel.grid(row = 1, column = 0)
        
        self.buttonFrame = Frame(self.mainFrame)
        self.buttonFrame.grid(row = 1, column = 1)
        
        #-----------------------------------------------
        #we used labels, and binded them to events so that
        #they function just like buttons
        self.gameLabel = Label(self.buttonFrame, text = "Game Mode",\
                                font = LABEL_NORM_FONT)

        #"<Button_1">: when users clicks a widget
        self.gameLabel.bind("<Button-1>", self.gamePanel)

        #"<Enter>": when the cursor moves into the widget
        self.gameLabel.bind("<Enter>", self.activate)

        #"<Leave>": when cursor leaves widget
        self.gameLabel.bind("<Leave>", self.deactivate)
        self.gameLabel.pack(side = "top")

        self.demoLabel = Label(self.buttonFrame, text = "Demo Mode",\
                                   font = LABEL_NORM_FONT)
        self.demoLabel.bind("<Button-1>", self.demoPanel)
        self.demoLabel.bind("<Enter>", self.activate)
        self.demoLabel.bind("<Leave>", self.deactivate)
        self.demoLabel.pack()

        self.ruleLabel = Label(self.buttonFrame, text = "Game Rules",\
                                   font = LABEL_NORM_FONT)
        self.ruleLabel.bind("<Button-1>", self.showHelp)
        self.ruleLabel.bind("<Enter>", self.activate)
        self.ruleLabel.bind("<Leave>", self.deactivate)
        self.ruleLabel.pack()

        self.exitLabel = Label(self.buttonFrame, text = "Exit",\
                                   font = LABEL_NORM_FONT)
        self.exitLabel.bind("<Button-1>", self.exitGame)
        self.exitLabel.bind("<Enter>", self.activate)
        self.exitLabel.bind("<Leave>", self.deactivate)
        self.exitLabel.pack()
        #-------------------------------------------------

        #create a frame to hold the demo panel(not displayed yet)
        self.demoFrame = Frame(self.root)

        #create an instance of demo controller
        #which creates a demo panel rooted in demo frame
        self.createDemoFrame(self.demoFrame)
        
        #--------------------------------------------------
        #create a frame to hold the game panel(not displayed yet)
        self.gameFrame = Frame(self.root)

        #call function to create an instance of game controller
        #which creates a game panel rooted in game frame
        self.createGameFrame(self.gameFrame)

    #Narrative: unpacks all frames from root window with try-except
    #Precondition: called
    #Postcondition: everything cleared from window, so that the calling function
        #may display the right frame
    def hideAll(self):

        #the .winfo_children function returns a list of all the children
        #widgets rooted in a parent window
        for w in self.root.winfo_children():
            try:

                #pack_forget() hides a widget from view
                w.pack_forget()

            #the pass statement doesn't do anything, simply moves onto
            #the next iteration
            except:
                pass

    #Narrative: display the game frame (unpack all, then pack game frame)
    #Precondition: "Game Mode" label is clicked
    #Postcondition: the game panel is displayed
    def gamePanel(self, event):
        self.hideAll()
        self.gameFrame.pack()

    #Narrative: display the demo frame (unpack all, then pack demo frame)
    #Precondition: "Demo Mode" label is clicked
    #Postcondition: the demo panel is displayed
    def demoPanel(self, event):
        self.hideAll()
        self.demoFrame.pack()

    #Narrative: create an instance of game controller
    #Precondition: called; a root frame passed in
    #Postcondition: an instance of game controller is created
    def createGameFrame(self, frame):
        self.gameController = GameController(frame)

        #add callback funtion so that user can return from game to main menu
        self.gameController.addReturnCallBack(self.mainMenu)

    #Narrative: create an instance of demo controller
    #Precondition: called, a root frame passed in
    #Postcondition: an instance of demo controller is created
    def createDemoFrame(self, frame):
        self.demoController = DemoController(frame)

        #add callback funtion so that user can return from demo to main menu
        self.demoController.addReturnCallBack(self.mainMenu)

    #Narrative: shows a top window for instructions
    #Precondition: "Help" label is clicked
    #Postcondition: the top window is displayed
    def showHelp(self, event):
        self.helpWindow = Toplevel()
        self.help = Help(self.helpWindow)

    #Narrative: display the main menu, (unpack all, pack main Frame)
    #Precondition: called
    #Postcondition: main menu is displayed
    def mainMenu(self):
        self.hideAll()
        self.mainFrame.pack()

    #Narrative: exit the game by destroying the tkinter root window
    #Precondition: "Exit" label is clicked
    #Postcondition: the window is destroyed, program ends
    def exitGame(self, event):
        self.root.destroy()

    #Narrative: changes a widget when cursor moves over it
    #Precondition: when the cursor moves into a widget
    #Postcondition: the widget changes color and becomes larger
    def activate(self, event):

        #evenr.widget returns the widget at which the event happened
        event.widget.config(foreground = "red", font = LABEL_ACTIVE_FONT)

    #Narrative: changes a widget back when cursor leaves it
    #Precondition: when the cursor leaves a widget
    #Postcondition: the widget returns to normal state
    def deactivate(self, event):
        event.widget.config(foreground = "black", font = LABEL_NORM_FONT)
          
