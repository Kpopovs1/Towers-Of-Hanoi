from threading import *

#A thread class, instances have a isTerminate attribute as a flag,
#and a stop method

#the flag is an Event() object

#multi-thredding

#when the stop method is called, the flag is set to True
#so that the recursive algorithm which continuously checks for the flag will
#know to end

class WorkingThread(Thread):
    def __init__(self, func, args):
        Thread.__init__(self, target = func, args = args)
        self.__isTerminate = Event()

    #Narrative: set the flag to true
    #Precondition: called
    #Postcondition: flag is set to true
    def stop(self):
        self.__isTerminate.set()

    #Narrative: get the current value of flaf
    #Precondition: called
    #Postcondition: value of flag is returned
    def isStopped(self):
        return self.__isTerminate.isSet()
            
        
        
        
        
    
