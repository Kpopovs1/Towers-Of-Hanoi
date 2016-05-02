from tkinter import * 
from tkinter.ttk import *
from WorkingThread import *
from DemoViewer import *
from Model import *

#The demo controller governs the visualization of Hanoi solution:
#The controller creates a viewer and a model

#General Algorithm:

#Solves Hanoi (n) by recursion
#Recursion is put into a separate thread so GUI events doesn't have to wait
#until recursion is all done
#Each time a move is calculated: the controller tells viewer to display,
#and model to updated

class DemoController:
    def __init__(self, root):
        self.root = root

        #creates an instance of demo viewer: a blank canvas on top
        #and control panel at bottom
        self.__viewer = DemoViewer(root)

        #set callbacks in the viewer, so that viewer can communicate back 
        self.__viewer.setReturnCallBack(self.mainMenu)
        self.__viewer.setStartCallBack(self.startDemo)        
        self.__viewer.setStopCallBack(self.stopDemo)


    #--------------------HANDLERS------------------
    # These functions responds to GUI events

    #Narrative: prepare for demo animation, create a model, set up viewer
        # and create a thread that runs the animation
    #Precondition: "Start Demo" is clicked,
        #disc number is received from viewer
    #Postcondition: everything set up and the animation thread begins
    def startDemo(self, discNum):
        self.__model = Model(discNum)

        #tells viewer to draw poles and discs
        self.__viewer.setupView(discNum,self.__model.getState(), \
                                self.__model.getDiscDict())

        #create a different thread to do animation
        self.__thrd = WorkingThread(self.solveHanoi,(discNum, "P1","P2","P3"))

        #begins animation
        self.__thrd.run()

    #Narrative: stop the animation by calling the thread's stop method, which
        #changed the condition flag
    #Precondition: "Stop Demo" is clicked in viewer
    #Postcondition: animation thread is stopped
    def stopDemo(self):
        self.__thrd.stop()

    #call the return callback
    def mainMenu(self):
        self.returnCallBack()


    #---------------- CALLBACK SETTER-------------------
    #used by main controller to create a callback

    #returns to the main menu
    def addReturnCallBack(self, func):
        self.returnCallBack = func


    #---------------- THE RECURSIVE SOLVER --------------------
    # solves the hanoi puzzle by recursion with the condition that
        #the thread is not stopped
    # after move is calculated, the controller calls viewer and model to update 

    #NOTE: solveHanoi runs in a separate thread so that GUI events can still
        #get through
    
    def solveHanoi(self, n, start, temp, end):
        
        # check if the thread is stopped
        if not self.__thrd.isStopped():
            if n > 0:
                self.solveHanoi(n-1, start, end, temp)

                #again, check if the thread is stopped
                if not self.__thrd.isStopped():

                    #call the function to display; the try/except handles
                    #when user abruptly closes the window
                    try:
                        self.move(n, start, end)
                    except:
                        return
                    
                    self.solveHanoi(n-1, temp, start, end)
        
    #called by the recursive solver.
    #Tells demo viewer to display each move on canvas
    #Tell model to update
    def move(self, n, start, end):
        
        #reformat the tower number into a tag so the the viewer canvas can
        #find it
        n = "D"+str(n)

        #get the number of discs on the destination pole so that the viewer
        #will know how high to put it
        endNum = self.__model.getPoleDiscNum(end)

        #calls viewer's animation function
        self.__viewer.animate(n, start, end, endNum)

        #updates model
        self.__model.update(n, start, end)