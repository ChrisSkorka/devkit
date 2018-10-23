import wx

#creates a wx.App instance and then when called starts the application
#------------------------------------------------------------------------------	
class App():
	def __init__(self):
		self.app = wx.App()
		self.windows = []

	def add(self, window):
		self.windows.append(window.getFrame(self.app))

	def show(self):
		self.app.MainLoop()

class ListWindow:
	def __init__(self, title="IO", state=None):
		self.fields = []
		self.title = title
		self.state = state

	def add(self, io):
		io.state = self.state
		self.fields.append(io)

	def getFrame(self, app):
		return ListFrame(app, self.title, self.fields)

	def show(self):
		self.app = wx.App()
		self.app.add(self)
		self.app.show()

class ListFrame(wx.Frame):
	def __init__(self, parent, title, fields):
		wx.Frame.__init__(self, None, title=title)

		self.panel = wx.Panel(self)
		self.sizer = wx.GridBagSizer(hgap=5, vgap=5)

		row = 0
		for field in fields:
			txt = wx.StaticText(self.panel, label = field.name)
			view = field.createWxWidget(self.panel)
			view.SetMinSize((300, 0))

			self.sizer.Add(txt, pos = (row, 0), flag = wx.EXPAND)
			self.sizer.Add(view, pos = (row, 1), flag = wx.EXPAND)

			row += 1

		self.panel.SetSizerAndFit(self.sizer)
		self.Fit()
		self.Show()