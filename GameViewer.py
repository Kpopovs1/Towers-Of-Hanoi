from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from functools import partial

S_MARGIN = 50
B_MARGIN = 50
DISC_HEIGHT = 30
MIN_DISC_WIDTH = 60
DISC_WIDTH_DIFF = 30
POLE_DIS = 100
LINE_WIDTH = 10

class GameViewer:
    def __init__(self, root):
        self.root = root
        self.createGameFrame()
        self.needSave = False

    def setReturnCallBack(self, func):
        self.returnCallBack = func

    def setStartCallBack(self, func):
        self.startCallBack = func

    def setResumeCallBack(self, func):
        self.resumeCallBack = func

    def setUndoCallBack(self, func):
        self.undoCallBack = func

    def setSaveGameCallBack(self, func):
        self.saveGameCallBack = func

    def setDiscDropCallBack(self, func):
        self.discDropCallBack = func

    def setDiscShadeCallBack(self, func):
        self.discShadeCallBack = func

    def createGameFrame(self):
        self.topFrame = Frame(self.root)
        self.topFrame.pack()

        self.__canvas =  Canvas(self.topFrame, height = 300, width = 600)
        self.__canvas.pack()
        
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack()

        self.discNumLabel = Label(self.bottomFrame, \
                                    text = "Number of Discs: ")
        self.discNumLabel.pack(side = "left")

        self.discNumVar = IntVar()
        self.discNumVar.set(3)
        self.discNumValue = Label(self.bottomFrame, textvariable = self.discNumVar, width = 3, relief = SUNKEN)
        self.discNumValue.pack(side = "left")

        self.discNumPlus = Button(self.bottomFrame, text = "+", \
                                    command = self.addDiscNum)
        self.discNumPlus.pack(side = "left")
        self.discNumMinus = Button(self.bottomFrame, text = "-",\
                                     command = self.minusDiscNum)
        self.discNumMinus.pack(side = "left")

        self.startResetButton = Button(self.bottomFrame, text = "Start Game", command = self.startGame)
        self.startResetButton.pack(side = "left")

        self.undoButton = Button(self.bottomFrame, text = "Undo", command = self.undoStep,\
                                 state = DISABLED)
        self.undoButton.pack(side = "left")

        self.moveLabel = Label(self.bottomFrame, text = "Moves: ")
        self.moveLabel.pack(side = "left")

        self.moveVar = IntVar()
        self.moveVar.set(0)
        self.moveCount = Label(self.bottomFrame, \
                                 textvariable = self.moveVar, width = 5, relief = SUNKEN)
        self.moveCount.pack(side = "left")

    
        self.returnButton = Button(self.bottomFrame, text = "Return",\
                                     command = self.mainMenu)
        self.returnButton.pack(side = "right")
        
    def mainMenu(self):
        if self.needSave:
            result = self.saveGame()
            if result == True:
                self.saveGameCallBack()
            if result != None:
                self.returnCallBack()
                self.cleanUp()
        else:
            self.returnCallBack()
            self.cleanUp()
            
    def saveGame(self):
        result = messagebox.askyesnocancel("Save", \
                                "Do you want to save game?")
        return result

    def cleanUp(self):
        self.__canvas.delete(ALL)
        self.__canvas.config(width = 600, height = 300)
        self.startResetButton["text"] = "Start Game"
        self.undoButton.config(state = DISABLED)
        self.discNumVar.set(3)
        self.moveVar.set(0)
        self.needSave = False

    def startGame(self):
        self.undoButton.config(state = ACTIVE)
        if self.startResetButton["text"] == "Start Game":
            try:
                inFile = open("model.dat", "rb")
                result = messagebox.askyesno("Resume", "You have a saved game. Do you want to resume?")
                inFile.close()
                if result == True:
                    self.resumeCallBack()
                else:
                    self.startCallBack(self.discNumVar.get())   
            except:
                self.startCallBack(self.discNumVar.get())

            self.startResetButton["text"] = "Reset Game"

        else:
            self.startCallBack(self.discNumVar.get())
		

    def undoStep(self):
        self.undoCallBack()

    def addDiscNum(self):
        if int(self.discNumVar.get())< 8:
            self.discNumVar.set(int(self.discNumVar.get())+1)

    def minusDiscNum(self):
        if int(self.discNumVar.get()) > 3:
            self.discNumVar.set(int(self.discNumVar.get())-1)

    def setupView(self, discNum, state, discInfo):
        self.needSave = True
        self.drawCanvas(discNum)
        self.drawPoles()
        self.drawDiscs(state, discInfo)
        self.discNumVar.set(discNum)

    def drawCanvas(self, discNum):
        self.__discNum = discNum
        self.__maxDiscWidth = MIN_DISC_WIDTH + DISC_WIDTH_DIFF * (discNum-1)

        self.__poleHeight = (DISC_HEIGHT * discNum) + 75
        
        self.__baseLength = self.__maxDiscWidth + 75

        self.__canvasWidth = (2 * POLE_DIS) + (2 * S_MARGIN) + (3 * self.__baseLength)
                       
        self.__canvasHeight = (DISC_HEIGHT * discNum) + 300
        
        self.__canvas.delete(ALL)

        self.__canvas.config(width = self.__canvasWidth,\
                               height = self.__canvasHeight)
        
    def drawPoles(self):
        y0 = self.__canvasHeight - B_MARGIN
        y1 = self.__canvasHeight - (B_MARGIN + self.__poleHeight)
        
        #drawing bases
        baseXCoord = []
        baseTagList = ["B1", "B2", "B3"]
        
        for num in range(3):
            baseXCoord.append(S_MARGIN + num * (self.__baseLength + POLE_DIS))

        for idx in range(len(baseXCoord)):
            self.__canvas.create_line(baseXCoord[idx], y0, baseXCoord[idx] + self.__baseLength, y0, width = LINE_WIDTH, tag = baseTagList[idx])

        poleTagList = ["P1", "P2", "P3"]
        poleXCoord = []
        
        for elem in baseTagList:
            poleXCoord.append((self.__canvas.bbox(elem)[0] + self.__canvas.bbox(elem)[2])/2)
            
        for idx in range(len(poleXCoord)):
            self.__canvas.create_line(poleXCoord[idx], y1 , poleXCoord[idx] , y0, width = LINE_WIDTH, tag = poleTagList[idx])

    def drawDiscs(self, state, discDict):
        self.__center = (self.__canvas.bbox("P1")[0] + self.__canvas.bbox("P1")[2])/2
        self.__bottom = B_MARGIN + LINE_WIDTH/2

        self.__p1Center = (self.__canvas.bbox("P1")[0] + self.__canvas.bbox("P1")[2])/2
        self.__p2Center = (self.__canvas.bbox("P2")[0] + self.__canvas.bbox("P2")[2])/2
        self.__p3Center = (self.__canvas.bbox("P3")[0] + self.__canvas.bbox("P3")[2])/2

        self.__bottom = B_MARGIN + LINE_WIDTH/2

        self.__discDict = discDict

        for idx in range(len(state["P1"])):
            disc = state["P1"][idx]
            discWidth = self.__discDict[disc][0]/2

            self.__canvas.create_rectangle(self.__p1Center - discWidth, self.__canvasHeight -(self.__bottom + DISC_HEIGHT*(idx+1)),\
                                           self.__p1Center + discWidth, self.__canvasHeight - (self.__bottom+ DISC_HEIGHT*(idx)),\
                                           fill = self.__discDict[disc][1], tag = disc)
        for idx in range(len(state["P2"])):
            disc = state["P2"][idx]
            discWidth = self.__discDict[disc][0]/2

            self.__canvas.create_rectangle(self.__p2Center - discWidth, self.__canvasHeight -(self.__bottom + DISC_HEIGHT*(idx+1)),\
                                           self.__p2Center + discWidth, self.__canvasHeight - (self.__bottom+ DISC_HEIGHT*(idx)),\
                                           fill = self.__discDict[disc][1], tag = disc)

        for idx in range(len(state["P3"])):
            disc = state["P3"][idx]
            discWidth = self.__discDict[disc][0]/2

            self.__canvas.create_rectangle(self.__p3Center - discWidth, self.__canvasHeight -(self.__bottom + DISC_HEIGHT*(idx+1)),\
                                           self.__p3Center + discWidth, self.__canvasHeight - (self.__bottom+ DISC_HEIGHT*(idx)),\
                                           fill = self.__discDict[disc][1], tag = disc)

    def unsetDraggable(self, draggableList):
        for elem in draggableList:
            self.__canvas.tag_unbind(elem, "<Button-1>")
            self.__canvas.tag_unbind(elem, "<B1-Motion>")
            self.__canvas.tag_unbind(elem, "<ButtonRelease-1>")
    
    def setDraggable(self, draggableList):
        for elem in draggableList:
            self.__canvas.tag_bind(elem, "<Button-1>", partial(self.click, widgetName = elem))
            self.__canvas.tag_bind(elem, "<B1-Motion>", self.drag)
            self.__canvas.tag_bind(elem, "<ButtonRelease-1>",self.release)

    def getPoleNum(self, x):
        coordB1 = self.__canvas.bbox("B1")
        coordB2 = self.__canvas.bbox("B2")
        coordB3 = self.__canvas.bbox("B3")

        if x > coordB1[0] and x < coordB1[2]:
            return "P1"

        elif x > coordB2[0] and x < coordB2[2]:
            return "P2"

        elif x > coordB3[0] and x < coordB3[2]:
            return "P3"

        else:
            return ("null")
   
    def click(self, event, widgetName):
        #print(widgetName)
        self.drag_data = {'x':0, 'y':0, "Disc":None}
        self.drag_data["Disc"] = widgetName
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.__canvas.tag_raise(widgetName)
        self.startPole = self.getPoleNum(event.x)
        self.thisDisc = self.drag_data["Disc"]

    def castShade(self, disc, endPole, endNum):
        endpoleCoord = self.__canvas.bbox(endPole)
        center = (endpoleCoord[0] + endpoleCoord[2])/2
        thisDiscWidth = self.__discDict[disc][0]/2

        x0 = center - thisDiscWidth
        x1 = center + thisDiscWidth
        y0 = self.__canvasHeight - ((endNum+1) * DISC_HEIGHT + self.__bottom)
        y1 = y0 + DISC_HEIGHT

        self.__canvas.create_rectangle(x0, y0, x1, y1, tag = "shade", fill = self.__discDict[disc][2], stipple = "gray50")
        self.__canvas.tag_raise(disc)
        
    def drag(self, event):
        self.__canvas.delete("shade")
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
            
        # move the object the appropriate amount
        self.__canvas.move(self.drag_data["Disc"], dx, dy)

        self.thisDiscTag = self.__canvas.gettags(self.thisDisc)[0]
        self.endPole = self.getPoleNum(event.x)
        self.discShadeCallBack(self.thisDiscTag, self.startPole, self.endPole)
        
        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def release(self, event):
        self.__canvas.delete("shade")
        
        self.thisDiscTag = self.__canvas.gettags(self.thisDisc)[0]
        self.endPole = self.getPoleNum(event.x)
        self.discDropCallBack(self.thisDiscTag, self.startPole, self.endPole)

    def moveDisc(self, disc, end, endNum):
        endpoleCoord = self.__canvas.bbox(end)
        center = (endpoleCoord[0] + endpoleCoord[2])/2
        thisDiscWidth = self.__discDict[disc][0]/2

        x0 = center - thisDiscWidth
        x1 = center + thisDiscWidth
        y0 = self.__canvasHeight - ((endNum+1) * DISC_HEIGHT + self.__bottom)
        y1 = y0 + DISC_HEIGHT

        self.__canvas.coords(disc, x0, y0, x1, y1)

    def returnDisc(self, disc, start, startNum):
        
        startpoleCoord = self.__canvas.bbox(start)
          
        center = (startpoleCoord[0] + startpoleCoord[2])/2
        thisDiscWidth = self.__discDict[disc][0]/2

        x0 = center - thisDiscWidth
        x1 = center + thisDiscWidth
        y0 = self.__canvasHeight - (startNum * DISC_HEIGHT+self.__bottom)
        y1 = y0 + DISC_HEIGHT
        self.__canvas.coords(disc, x0, y0, x1, y1)

    def displayGameWon(self):
        self.needSave = False
        self.__canvas.create_text(self.__canvasWidth/2, \
                                  100, text = "You Won!!", font = ("papyrus", 40))
        self.startResetButton["text"] = "Start Game"
        
    def updateMoveNumber(self, moveNum):
        self.moveVar.set(moveNum)
        
    def resetMoveNumber(self):
        self.moveVar.set(0)

