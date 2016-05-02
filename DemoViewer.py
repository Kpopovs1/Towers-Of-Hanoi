from tkinter import * 
from tkinter.ttk import *

#The demo viewer creates the GUI for hanoi demo.
#GUI events are handled through callbacks to controller

#It shows discs moving, according to the steps calculated by the controller


# We declare some constants:
#side margin
S_MARGIN = 50

#bottom margin 
B_MARGIN = 50

DISC_HEIGHT = 30

#the width of the smallest disc
MIN_DISC_WIDTH = 60

#the difference in width between two consecutive discs
DISC_WIDTH_DIFF = 30

#the distance between the bases of the poles
POLE_DIS = 100

#how thick the pole and base should be
LINE_WIDTH = 10

class DemoViewer:
    def __init__(self, root):
        self.root = root
        self.createDemoFrame()

    #------------------CALLBACK SETTERS--------------------
    #Controller calls these functions to set callbacks so that it will be 
    #notified of GUI events."func" is a controller functoin

    def setReturnCallBack(self, func):
        self.returnCallBack = func

    def setStartCallBack(self, func):
        self.startCallBack = func

    def setStopCallBack(self, func):
        self.stopCallBack = func

    #------------------SET UP INITIAL VIEW ---------------------
    #create the Hanoi Demo panel, with a blank canvas for graphics
    #and a control panel on the bottom
        
    def createDemoFrame(self):

        #--------------- create Canvas -------------------------
        self.topFrame = Frame(self.root)
        self.topFrame.pack()

        self.__canvas =  Canvas(self.topFrame, height = 300, width = 600)
        self.__canvas.pack()

        #----------------- Buttons -----------------
        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack()

        #a label for disc number
        self.discNumLabel = Label(self.bottomFrame, \
                                    text = "Number of Discs: ")
        self.discNumLabel.pack(side = "left")

        self.discNumVar = IntVar()
        self.discNumVar.set(3)
        self.discNumValue = Label(self.bottomFrame, \
                                  textvariable = self.discNumVar, \
                                  width = 3, relief = SUNKEN)
        self.discNumValue.pack(side = "left")

        #buttons to select disc number
        self.discNumPlus = Button(self.bottomFrame, text = "+",\
                                    command = self.addDiscNum)
        self.discNumPlus.pack(side = "left")
        self.discNumMinus = Button(self.bottomFrame, text = "-",\
                                     command = self.minusDiscNum)
        self.discNumMinus.pack(side = "left")

        #a speed scale, allows user to decide how fast the discs move
        self.speedScaleLabel = Label(self.bottomFrame, \
                                       text = "Choose speed: ")
        self.speedScaleLabel.pack(side = "left")        

        self.speedScale = Scale(self.bottomFrame, from_ = 1, to = 5,\
                                  value = 1, orient = HORIZONTAL)
        self.speedScale.pack(side = "left")

        #the startStop Button starts or stops and demo
        self.startStopButton = Button(self.bottomFrame, text = "Start Demo",\
                                      command = self.startDemo)
        self.startStopButton.pack(side = "left")

        #the return button, allows user to return to the main menu
        self.returnButton = Button(self.bottomFrame, text = "Return",\
                                     command = self.mainMenu)
        self.returnButton.pack(side = "right")

    #------------------- SET UP DEMO VIEW -------------------
        
    # calls class methods to resize canvas, draw the poles and disc in staring position
    def setupView(self, discNum, state, discInfo):
        self.drawCanvas(discNum)
        self.drawPoles()
        self.drawDiscs(state, discInfo)

    # resize the canvas according to the number of discs
    def drawCanvas(self, discNum):
        self.__discNum = discNum
        self.__maxDiscWidth = MIN_DISC_WIDTH + DISC_WIDTH_DIFF * (discNum-1)

        self.__poleHeight = (DISC_HEIGHT * discNum) + 75
        
        self.__baseLength = self.__maxDiscWidth + 75

        self.__canvasWidth = (2 * POLE_DIS) + (2 * S_MARGIN) + \
                             (3 * self.__baseLength)
                       
        self.__canvasHeight = (DISC_HEIGHT * discNum) + 300
        
        self.__canvas.delete(ALL)

        self.__canvas.config(width = self.__canvasWidth,\
                               height = self.__canvasHeight)

    # draw poles according to disc number
    def drawPoles(self):
        y0 = self.__canvasHeight - B_MARGIN
        y1 = self.__canvasHeight - (B_MARGIN + self.__poleHeight)
        
        
        #--------- drawing bases ----------
        baseXCoord = []
        baseTagList = ["B1", "B2", "B3"]

        #calculate the left end coordinate of bases
        for num in range(3):
            baseXCoord.append(S_MARGIN + num * (self.__baseLength + POLE_DIS))

        for idx in range(len(baseXCoord)):
            self.__canvas.create_line(baseXCoord[idx], y0, \
                                      baseXCoord[idx] + self.__baseLength, y0, \
                                    width = LINE_WIDTH, tag = baseTagList[idx])

        
        #----------- draw poles ------------
        poleTagList = ["P1", "P2", "P3"]
        poleXCoord = []

        #calculate the center of each base, where to draw the poles
        for elem in baseTagList:
            poleXCoord.append((self.__canvas.bbox(elem)[0] + \
                               self.__canvas.bbox(elem)[2])/2)

        #draw    
        for idx in range(len(poleXCoord)):
            self.__canvas.create_line(poleXCoord[idx], y1 ,\
                                    poleXCoord[idx] , y0, width = LINE_WIDTH,\
                                      tag = poleTagList[idx])

    # draw discs
    def drawDiscs(self, state, discDict):

        #the state dict is a dictionary that holds disc info:
        # which discs are which pole, size, coloe, order of the disc
        self.__discDict = discDict

        
##        self.__center = (self.__canvas.bbox("P1")[0] + \
##                         self.__canvas.bbox("P1")[2])/2
        self.__bottom = B_MARGIN + LINE_WIDTH/2

        self.__p1Center = (self.__canvas.bbox("P1")[0] + \
                           self.__canvas.bbox("P1")[2])/2
        self.__p2Center = (self.__canvas.bbox("P2")[0] + \
                           self.__canvas.bbox("P2")[2])/2
        self.__p3Center = (self.__canvas.bbox("P3")[0] + \
                           self.__canvas.bbox("P3")[2])/2

        self.__bottom = B_MARGIN + LINE_WIDTH/2

        
        #draw the discs on pole 1
        for idx in range(len(state["P1"])):
            disc = state["P1"][idx]
            discWidth = self.__discDict[disc][0]/2

            self.__canvas.create_rectangle(self.__p1Center - discWidth, \
                    self.__canvasHeight -(self.__bottom + DISC_HEIGHT*(idx+1)),\
                    self.__p1Center + discWidth, \
                    self.__canvasHeight - (self.__bottom+ DISC_HEIGHT*(idx)),\
                    fill = self.__discDict[disc][1], \
                    tag = disc)

        #draw the discs on pole 2
        for idx in range(len(state["P2"])):
            disc = state["P2"][idx]
            discWidth = self.__discDict[disc][0]/2

            self.__canvas.create_rectangle(self.__p2Center - discWidth, \
                    self.__canvasHeight -(self.__bottom + DISC_HEIGHT*(idx+1)),\
                    self.__p2Center + discWidth, \
                    self.__canvasHeight - (self.__bottom+ DISC_HEIGHT*(idx)),\
                    fill = self.__discDict[disc][1], tag = disc)

        #draw the discs on pole 3
        for idx in range(len(state["P3"])):
            disc = state["P3"][idx]
            discWidth = self.__discDict[disc][0]/2

            self.__canvas.create_rectangle(self.__p3Center - discWidth, \
                    self.__canvasHeight -(self.__bottom + DISC_HEIGHT*(idx+1)),\
                    self.__p3Center + discWidth, \
                    self.__canvasHeight - (self.__bottom+ DISC_HEIGHT*(idx)),\
                    fill = self.__discDict[disc][1], tag = disc)

    
    #---------------- ANIMATION FUNCTIONS -------------------

    #GENERAL ALGORITHM: the "moving" process is divide into 3 stages:
            #1) move up the start pole to a certain height (constant: MAX_Y)
            #2) move left/right to the top of the end pole
            #3) move down the end pole until it reaches the top disc on that pole

            #canvas.bbox(n) returns the current position of object with tag/id n
            # we continuously compare the current position of the disc
            # with the destination coordinates of each stage
            # move it up, down, right, or left
            # and update the canvas

            #canvas.move(tag, dx, dy) moves object with tag/id n by a displacement of dx, dy
            #canvas.update() updates the canvas

    #NOTE: canvas y coordinate is opposite of cartesian, (0,0) at upper left
            #when you move something up, you decrease its y coord
            #vice versa
            

    #move disc with tag n to the left by decreasing its x-coord
    def moveDiscLeft(self, n, speed):
        dx = -.03 * speed
        dy = 0
        self.__canvas.move(n, dx, dy)

    #move disc with tag n to the right by increasing its x-coord
    def moveDiscRight(self, n, speed):
        dx = .03 * speed
        dy = 0
        self.__canvas.move(n, dx, dy)
        
    #move disc with tag n up by decreasing its y-coord
    def liftDisc(self, n, speed):
        dx = 0
        dy = -.03 *speed
        self.__canvas.move(n, dx, dy)

    #move disc with tag n down by increasing its y-coord
    def dropDisc(self, n, speed):
        dx = 0
        dy = .03*speed
        self.__canvas.move(n, dx, dy)

    #moves the disc with tag n from start pole to end pole
    #endNum is the number of discs already on the end pole
    def animate(self, n, start, end, endNum):
        
        #-------------------get necessary coordinates----------------------
        #get speed from speed scale
        speed = self.speedScale.get()

        #get start and end x-coords
        start_x = self.__canvas.bbox(start)[0]
        end_x = self.__canvas.bbox(end)[0]

        #get the current position of the disc
        discCoord = self.__canvas.bbox(n)

        disc_x = discCoord[0]
        disc_y = discCoord[1]

        #get disc width
        thisDiscWidth = (self.__discDict[n][0])/2

        #get pole coordinate
        poleCoord = self.__canvas.bbox(end)
        newCenter = (poleCoord[0] + poleCoord[2])/2

        #get the destination coordinates
        dest_x = newCenter - thisDiscWidth
        dest_y = self.__canvasHeight-(DISC_HEIGHT * (endNum+1) + self.__bottom)

        #MAX_Y is how high a disc will go until it travels to left or right
        # 40 pixels above the tip of pole
        MAX_Y = self.__canvasHeight - (self.__bottom + self.__poleHeight + 40)


        #--------------------start moving--------------------------------
        #when a disc is moved to the right
        
        if start_x < end_x:

            #move up the start pole as long as its current y
            # is greater than MAX_Y 
            while disc_x < dest_x and disc_y > MAX_Y:
                self.liftDisc(n, speed)
                self.__canvas.update()
                disc_x = self.__canvas.bbox(n)[0]
                disc_y = self.__canvas.bbox(n)[1]
            
            #enters "moving right" stage, move right
            #as long as its current x is smaller than destination x
            while disc_x < dest_x and disc_y >= MAX_Y:
                self.moveDiscRight(n, speed)
                self.__canvas.update()
                disc_x = self.__canvas.bbox(n)[0]
                disc_y = self.__canvas.bbox(n)[1]

            #going down the end pole, move down as long as its current y
            # is less than dest_y 
            while disc_y < dest_y:
                self.dropDisc(n, speed)
                self.__canvas.update()
                disc_x = self.__canvas.bbox(n)[0]
                disc_y = self.__canvas.bbox(n)[1]

        #when a disc is moved to the left, same general steps, up-left-down
        else:

            while disc_x > dest_x and disc_y > MAX_Y:
                self.liftDisc(n, speed)
                self.__canvas.update()
                disc_x = self.__canvas.bbox(n)[0]
                disc_y = self.__canvas.bbox(n)[1]

            while disc_x > dest_x and disc_y >= MAX_Y:
                self.moveDiscLeft(n, speed)
                self.__canvas.update()
                disc_x = self.__canvas.bbox(n)[0]
                disc_y = self.__canvas.bbox(n)[1]

            while disc_y < dest_y:
                self.dropDisc(n, speed)
                self.__canvas.update()
                disc_x = self.__canvas.bbox(n)[0]
                disc_y = self.__canvas.bbox(n)[1]

    
    #-------------  HANDLERS  ------------
                
    # increase disc number when "+" button is clicked
    # maximum disc number is 8
    def addDiscNum(self):
        if int(self.discNumVar.get())< 8:
            self.discNumVar.set(int(self.discNumVar.get())+1)

    #decrease disc number when "-" button is clicked
    # minimum disc number is 3
    def minusDiscNum(self):
        if int(self.discNumVar.get()) > 3:
            self.discNumVar.set(int(self.discNumVar.get())-1)

    #start/stop demo based on what the button displays when clicked
    def startDemo(self):
        if self.startStopButton["text"] == "Start Demo":
            self.startStopButton["text"] = "Stop Demo"
            self.startCallBack(self.discNumVar.get())
            
        else:
            self.stopCallBack()

        self.startStopButton["text"] = "Start Demo"

    # go back to the main menu when "return" is clicked
    # clean up and resize canvas to initial state
    # reset buttons and disc number label etc
    def mainMenu(self):
        self.returnCallBack()
        self.__canvas.delete(ALL)
        self.__canvas.config(width = 600, height = 300)
        self.startStopButton["text"] = "Start Demo"
        self.discNumVar.set(3)


