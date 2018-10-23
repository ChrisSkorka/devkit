import wx
from devkit.App import App

class Output:
	def __init__(self, name, value):
		self.name = name
		self.value = value
		self.state = None
		self.view = None

	def setValue(self, value):
		self.value = value
		if self.view != None:
			self.updateWidget()

	def updateWidget(self):
		pass

	def createWxWidget(self):
		pass

class Dictionary(Output):
	def __init__(self, name, values={}):
		Output.__init__(self, name, None)
		self.sizer = wx.GridBagSizer(hgap=5, vgap=5)
		self.value = values

	def updateWidget(self):
		row = 0
		for key in self.value:
			label = wx.StaticText(self.view, label=str(key) + ":")
			value = wx.StaticText(self.view, label=str(self.value[key]))

			self.sizer.Add(label, pos=(row, 0), flag=wx.EXPAND)
			self.sizer.Add(value, pos=(row, 1), flag=wx.EXPAND)
			print(key, self.value[key])

			row += 1

		self.view.SetSizerAndFit(self.sizer)
		# self.Fit()
		# self.Show()

	def createWxWidget(self, panel):
		self.view = wx.Panel(panel)
		self.sizer = wx.GridBagSizer(hgap=5, vgap=5)
		self.updateWidget()

		return self.view
