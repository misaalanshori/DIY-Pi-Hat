class baseApp:
    def __init__(self, dispObj, globalVar, font, buttonPool):
        self.display = dispObj
        self.globalVar = globalVar
        self.font = font
        self.buttonPool = buttonPool

        self.renderDelay = None
        self.appJoined = False
        self.keybinds = {
            "menu": {"pressCall": self.leaveApp},
        }
        
    def render(self):
        pass

    def internalRender(self):
        self.appJoined = False # Undoes the join app, as placeholder for the app. replace this with subclass internal render
        self.buttonPool.resetCallbacks()
        
    def joinApp(self):
        self.appJoined = True
        self.buttonPool.clearCallbacks()
        self.buttonPool.update(self.keybinds)
        print(self.buttonPool._buttonPoller__originalCalls)
        self.internalRender()

    def leaveApp(self):
        self.buttonPool.resetCallbacks()
        self.appJoined = False
    
    def refresh(self):
        pass


# class appMenu:
#     def __init__(self, menu):
#         self.menu = menu
#         self.selectedItem = 0
#         self.menuDepth
    
#     def render(self, drawer):
#         draer        
