from MainController import *


def main():
    root = Tk()
    controller = MainController(root)
    
    #make the window not resizable
    root.resizable(width = False, height = False)
    
    root.mainloop()
    
main()
        
