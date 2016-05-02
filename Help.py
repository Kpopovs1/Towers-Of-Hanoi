from tkinter import *
from tkinter.ttk import *

##create a list of frames, show based on current page count

BACKGRD_COLOR = "orange"
FOREGRD_COLOR="royal blue"
FONT = ("papyrus", 12)

class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("%dx%d%+d%+d" % (400, 400, 0, 0))
        self.root.resizable(width = False, height = False)
        self.root.pack_propagate(False)
        self.root.title("Game Rules")
        #self.root.configure(background="orange")
        self.topFrame = Frame(self.root)
        self.topFrame.pack()
        
        
        self.titleFrame = Frame(self.topFrame)
        self.titleFrame.pack()

        self.title = Label(self.titleFrame, \
                           text = "Welcome to \nThe Towers of Hanoi!", \
                           font = ("papyrus", 18, "bold"), justify = CENTER)
        self.title.pack()
        self.label0 = Label(self.titleFrame, \
                            text = "In Game Mode: select the number of discs \nin your tower and start game.",\
                            font = ("papyrus",15), justify = CENTER)
        self.label0.pack()
        self.startImage = PhotoImage(file = "start.png")
        self.imageLabel = Label(self.titleFrame, image = self.startImage)
        self.imageLabel.pack(side = "bottom")

        
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side = "bottom")
        
        self.previousButton = Button(self.bottomFrame, text = "<Previous",\
                            command = self.showPrev, state = DISABLED)
        self.previousButton.pack(side = "left")
        self.nextButton = Button(self.bottomFrame, text = "Next>",\
                    command = self.showNext)
        self.nextButton.pack(side = "left")
        self.returnButton = Button(self.bottomFrame, text = "Return",\
                    command = self.mainMenu)
        self.returnButton.pack(side = "left")

        self.currentPageNum = 0

        self.pages = [self.titleFrame]
        self.createFirstPage()
        self.createSecondPage()
        self.createThirdPage()
        self.createLastPage()

    def mainMenu(self):
        self.hideAll()
        self.titleFrame.pack()
        self.previousButton.config(state = DISABLED)
        self.root.destroy()

    def createFirstPage(self):
        self.frame2 = Frame(self.topFrame)
        self.label2 = Label(self.frame2, text = "Your Objective:",\
                            font = ("papyrus", 20, "bold"))
        self.label2.pack()
        self.label3 = Label(self.frame2,\
                        text = "To move the entire tower to the rightmost pole \nin as few moves as possible,\nby click and drag, one disc at a time",\
                           font = ("papyrus", 15), justify = CENTER)
       
        self.label3.pack()

        self.moveImage = PhotoImage(file = "move.png")
        self.moveImageLabel = Label(self.frame2, image = self.moveImage)
        self.moveImageLabel.pack()

        self.pages.append(self.frame2)

    def createSecondPage(self):
        self.frame3 = Frame(self.topFrame)

        self.label5 = Label(self.frame3, \
                            text = "One Simple Rule:", font = ("papyrus", 20, "bold"))
                            
        
        self.label7 = Label(self.frame3, text = "You can't place larger discs on top of \nsmaller ones.", font = ("papyrus", 15), justify  = CENTER)
        self.label5.pack()

        self.label7.pack()
        
        self.wrongImage = PhotoImage(file = "wrong.png")
        self.wrongImageLabel=Label(self.frame3,image = self.wrongImage)
        self.wrongImageLabel.pack()
        self.pages.append(self.frame3)

    def createThirdPage(self):
        self.frame4 = Frame(self.topFrame)

        self.label8 = Label(self.frame4, \
                            text = "For Solution:", font = ("papyrus", 20, "bold"))
                            
        
        self.label9 = Label(self.frame4, text = "Go to Demo Mode and choose disc number \nin the same way", font = ("papyrus", 15), justify  = CENTER)
        self.label8.pack()

        self.label9.pack()
        
        self.image = PhotoImage(file = "demo.gif")
        self.imageLabel=Label(self.frame4,image = self.image)
        self.imageLabel.pack()
        self.pages.append(self.frame4)

    def createLastPage(self):
        self.frame5 = Frame(self.topFrame)
        self.label10 = Label(self.frame5, text = "Enjoy!!",\
                             font = ("papyrus", 25, "bold"))
        self.label10.pack()
        self.pages.append(self.frame5)


    def hideAll(self):
        for w in self.topFrame.winfo_children():
            try:
                w.pack_forget()
            except:
                pass
            
    def showNext(self):
        self.hideAll()
        self.currentPageNum += 1

        if self.currentPageNum > 0:
            self.previousButton.config(state = ACTIVE)
            
        if self.currentPageNum >= len(self.pages) - 1:
            self.nextButton.config(state = DISABLED)
            self.pages[-1].pack()

        else:    
            self.pages[self.currentPageNum].pack()
            
    def showPrev(self):
        self.hideAll()
        self.currentPageNum -= 1

        if self.currentPageNum < len(self.pages) - 1:
            self.nextButton.config(state = ACTIVE)
            
        if self.currentPageNum <= 0:
            self.previousButton.config(state = DISABLED)
            
            self.pages[0].pack()

        else:    
            self.pages[self.currentPageNum].pack()


##def main():
##    root = Tk()
##    helper = Help(root)
##    
##main()
##    
##        
