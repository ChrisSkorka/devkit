import wx

#creates a wx.App instance and then when called starts the application
#------------------------------------------------------------------------------	
class App():
	def __init__(self):
		self.app = wx.App()

	def show(self):
		self.app.MainLoop()