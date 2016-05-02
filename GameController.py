from tkinter import * 
from tkinter import messagebox
from tkinter.ttk import *
from GameViewer import *
from Model import *
import os
import pickle

#The game controller governs the overall logic of the game.
#It handles GUI events and makes major decisions such as:

# whether a move is legal
# whther game is won
# start/reset/resume/save game

# controller also enforces details like:
#1) makes sure at any given time, only the topmost discs are movable
#2) keeps a list to past moves to support "Undo"




class GameController:
    def __init__(self, root):
        self.root = root

        #create an instance of viewer GUI
        self.__viewer = GameViewer(root)

        #set callbacks in viewer to handle GUI events
        self.__viewer.setReturnCallBack(self.mainMenu)
        self.__viewer.setStartCallBack(self.startGame)        
        self.__viewer.setResumeCallBack(self.resumeGame) 
        self.__viewer.setUndoCallBack(self.undoStep) 
        self.__viewer.setDiscDropCallBack(self.canIMove) 
        self.__viewer.setDiscShadeCallBack(self.canIShade)
        self.__viewer.setSaveGameCallBack(self.saveGame)

    #------------------GENERAL HANDLERS--------------------
    #These handlers perform general actions such as start/reset/save game

    #Narrative: returns to main menu
    #Precondition: "Return" button is clicked in GUI
    #Postcondition: return to main menu
    def mainMenu(self):
        self.returnCallBack()

    #Narrative: saves game by pickling the model
    #Precondition: user chooses to save an unfinished game
    #Postcondition: game is saved/error message shown
    def saveGame(self):
        try:
            outFile = open("model.dat", "wb")
            pickle.dump(self.__model, outFile)
            outFile.close()
        except:
            messagebox.showerror("Error", "Sorry, your game could not be saved.")

    #Narrative: start a new game/reset a game
    #Precondition: "Start"/"Reset" is clicked; receive disc number
    #Postcondition: game started/reset
    def startGame(self, discNum):
        
        #create a model
        self.__model = Model(discNum)
        self.setupGame(discNum)

    #Narrative: resume game
    #Precondition: the user chooses to resume a game in GUI
    #Postcondition: saved game is resumed/error message shown  
    def resumeGame(self):
        
        #call function to unpickle model
        self.loadGame()
        self.setupGame(self.__model.getDiscNum())
        self.__viewer.updateMoveNumber(self.__model.getMoves())
        

    #-------------- SPECIFIC HANDLERS FOR GAME LOGIC----------------
    # These handlers respond to specific game events

    #GENERAL LOGIC:
    #1) When a disc is clicked on, dragged to, and released at a certain point,
    #the viewer does a callback to controller

    #2) The controller decides whether a move is legal

    #3) If the move is legal, the disc is placed there, and model updated.

    #4) Otherwise, the disc is returned to its staring peg and nothing is recorded


    #Narrative: decide whether a move is legal
    #Precondition: whenever a disc is released; viewer calls back with args
    #Postcondition: if move legal: disc moved to new location, model updated
       #            otherwise: disc returned to original position
    def canIMove(self, disc, startPole, endPole):

        #get number of discs on the starting pole
        startNum = self.__model.getPoleDiscNum(startPole)

        #if disc is released in the middle of nowhere, return it
        if endPole == "null":
            self.__viewer.returnDisc(disc, startPole, startNum)

        #if the disc is released near a pole           
        else:

            #check with model.
            #if the move is legal, place the disc there
            if self.__model.isMoveLegal(disc, startPole, endPole) == True:

                #tells viewer to place it there
                endNum = self.__model.getPoleDiscNum(endPole)
                self.__viewer.moveDisc(disc, endPole, endNum)

                #updates model
                self.__model.update(disc, startPole, endPole)

                #records the move
                self.__lastMoves.append([disc, startPole, endPole])

                #updates move number in viewer
                self.__viewer.updateMoveNumber(self.__model.getMoves())

                #check with model: if game won, call a class method
                if self.__model.isGameWon() == True:
                    self.gameWon()

                #if game not won, reset the which discs are movable during this new round
                else:
                    self.__viewer.unsetDraggable(self.draggableList)
                    self.setDraggable()

            #if the move is not legal, return disc to starting position
            else:
                self.__viewer.returnDisc(disc, startPole, startNum)

    #Narrative: undo a step
    #Precondition:
    #Postcondition:
    def undoStep(self):
        if len(self.__lastMoves) > 0:
            disc = self.__lastMoves[-1][0]
            endPole = self.__lastMoves[-1][1]
            endNum = self.__model.getPoleDiscNum(endPole)
            
            self.__viewer.moveDisc(disc, endPole, endNum)
            
            self.__model.undo(self.__lastMoves[-1])
            self.__viewer.updateMoveNumber(self.__model.getMoves())

            del self.__lastMoves[-1]
            self.setDraggable()
    #Narrative:
    #Precondition:
    #Postcondition:#trivial
    def canIShade(self, disc, startPole, endPole):
        if endPole == "null":
            return
        else:
            if self.__model.isMoveLegal(disc, startPole, endPole) == True:
                endNum = self.__model.getPoleDiscNum(endPole)
                self.__viewer.castShade(disc, endPole, endNum)


    #----------------OTHER FUNCTIONS---------------------  
    def setupGame(self, discNum):
        self.isWon = False
        #create a list to keep track of moves, to support undo
        self.__lastMoves = []

        self.deleteSavedGame()
        self.__viewer.setupView(discNum,self.__model.getState(), self.__model.getDiscDict())
        self.setDraggable()

    def setDraggable(self):
        self.pole1 = self.__model.getPoleState("P1")
        self.pole2 = self.__model.getPoleState("P2")
        self.pole3 = self.__model.getPoleState("P3")

        self.draggableList = []

        if len(self.pole1) != 0:
           self.draggableList.append(self.pole1[-1])
        if len(self.pole2) != 0:
           self.draggableList.append(self.pole2[-1])
        if len(self.pole3) != 0:
           self.draggableList.append(self.pole3[-1])
        
        self.__viewer.setDraggable(self.draggableList)

    def deleteSavedGame(self):
        try:
            os.remove("model.dat")
        except:
            print("can not remove model.dat")

    def loadGame(self):
        try:
            inFile = open("model.dat", "rb")
            self.__model = pickle.load(inFile)
            inFile.close()
        except:
            messagebox.showerror("Error", "Failed to resume.")
            #self.__model = None
            
    def gameWon(self):
        self.isWon = True
        self.__viewer.unsetDraggable(self.draggableList)
        self.__viewer.displayGameWon()
           
    def addReturnCallBack(self, func):
        self.returnCallBack = func
        
 
            
        
