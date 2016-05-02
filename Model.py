import sys
import pickle

DISC_HEIGHT = 30
MIN_DISC_WIDTH = 60
DISC_WIDTH_DIFF = 30

class Model:
    def __init__(self, discNum):
        self.__discNum = discNum
        self.__moves = 0
        
        self.__state = {}
        self.__state["P1"] = []

        for num in range(discNum, 0, -1):
            self.__state["P1"].append("D"+str(num))

        self.__state["P2"] = []
        self.__state["P3"] = []

        discWidthList = []
        for num in range(self.__discNum, 0, -1):
            discWidthList.append(MIN_DISC_WIDTH + (num-1) * DISC_WIDTH_DIFF)

        discTagList = []
        for num in range(self.__discNum, 0, -1):
            discTagList.append("D"+str(num))
        
        discColorList = ("black", "midnight blue", "dark violet", "cyan", \
                         "lawn green", "yellow", "dark orange", "red")

        discShadeList = ("grey", "light slate blue", "orchid", "powder blue", "pale green", "khaki", "light salmon", "firebrick1")

        self.__discDictionary = {}

        for idx in range(len(discTagList)):
            self.__discDictionary[discTagList[idx]] = [discWidthList[idx], discColorList[idx + (8-self.__discNum)], discShadeList[idx + (8-self.__discNum)]]
        print(self.__discDictionary)

    ##Narrative:get value of attribute
    ##Preconditions:called
    ##Postconditions:returns value of the attribute
    def getDiscNum(self):
        return self.__discNum

    ##Narrative:get value of attribute
    ##Preconditions:called
    ##Postconditions:returns value of the attribute
    def getMoves(self):
        return self.__moves

    ##Narrative:delete the top disc from the start pole, append it to the
    ##end pole, increase move number by 1
    ##Preconditions:called
    ##Postconditions:moves disc from start pole to end pole and
    ##increases move number by 1
    def update(self, n, start, end):
        disc = self.__state[start][-1]
        del self.__state[start][-1]
        self.__state[end].append(disc)
        self.__moves += 1

    ##Narrative:undoes a move
    ##Preconditions:called
    ##Postconditions:move is undone and move number is decreased by 1
    def undo(self, dataList):
        disc = dataList[0]
        start = dataList[1]
        end = dataList[2]

        #delete the top disc from the end pole
        del self.__state[end][-1]
        #append it to the start pole
        self.__state[start].append(disc)
        #decrease move number by 1
        self.__moves -= 1

    ##Narrative:get length value of state
    ##Preconditions:called
    ##Postconditions:returns length value of state
    def getPoleDiscNum(self, pole):
        return len(self.__state[pole])

    ##Narrative:get the value of the state of the pole
    ##Preconditions:called
    ##Postconditions:returns value 
    def getPoleState(self, pole):
        return self.__state[pole]

    ##Narrative:get value of attribute state
    ##Preconditions:called
    ##Postconditions:returns value 
    def getState(self):
        return self.__state
    
    ##Narrative:get value of attribute
    ##Preconditions:called
    ##Postconditions:returns value of the attribute
    def getDiscDict(self):
        return self.__discDictionary

    ##Narrative:get the state of the top disc from the end pole and convert the
    ##number into an integer. if it does not work, assign the max int possible
    ##to the variable. If the disc number is smaller than the number of the
    ##top disc, return True. Else, return False.
    ##Preconditions:called
    ##Postconditions:if move is legal, True is returned. Otherwise, False is
    ##returned.
    def isMoveLegal(self, disc, start, end):
        
        try:
            #get the state of the top disc from the end pole
            endPoleTopDisc = self.getPoleState(end)[-1]
            #strip the D and convert it into an integer
            endPoleTopDisc = int(endPoleTopDisc.lstrip("D"))
        except:
            #make it into the max integer python can hold
            endPoleTopDisc = int(sys.maxsize)
        #if int(number) of disc if smaller than the number of the top disc
        #at the end pole, retur True. Else is False.
        if int(disc.lstrip('D')) < endPoleTopDisc:
            return True
        else:
            return False

    ##Narrative:if pole 3 is equal to the original order of the discs in pole 1
    ##return True and the game is won. Else, return False.
    ##Preconditions:called
    ##Postconditions:if game is won, True is returned. Otherwise, False is
    ##returned.
    def isGameWon(self):
        if self.getPoleDiscNum("P3") == self.__discNum: 
            return True

        else:
            return False

def main():
    model = Model(5)
    
main()
