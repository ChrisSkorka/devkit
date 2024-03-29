import wx
from devkit.App import App

class Input:
	def __init__(self, name, value, onUpdate):
		self.name = name
		self.value = value
		self.update = onUpdate
		self.state = None
		self.view = None

	def setValue(self, value):
		self.value = value
		if self.view != None:
			self.updateWidget()
			self.processUpdate(None)

	def updateWidget(self):
		pass

	def processUpdate(self, event):
		pass

	def onUpdate(self):
		if self.update != None:
			self.update(self, self.value, self.state)

	def createWxWidget(self):
		pass

class Button(Input):
	def __init__(self, name, onClick=None):
		Input.__init__(self, name, None, onClick)

	def updateWidget(self):
		self.view.SetValue(self.name)

	def processUpdate(self, event):
		self.onUpdate()

	def createWxWidget(self, panel):
		
		self.view = wx.Button(panel, label=self.name)
		self.view.Bind(wx.EVT_BUTTON, self.processUpdate)

		return self.view

class Slider(Input):
	def __init__(self, name, value, onUpdate=None, sMin=0, sMax=100, sSteps=1):
		Input.__init__(self, name, value, onUpdate)

		self.min = sMin
		self.max = sMax
		self.steps = sSteps
		self.valueView = None

	def updateWidget(self):
		self.view.SetValue((self.value - self.min) // self.steps)

	def processUpdate(self, event):
		self.value = self.view.GetValue() * self.steps + self.min
		self.valueView.SetLabelText(str(self.value))
		self.onUpdate()

	def createWxWidget(self, panel):

		totalSteps = (self.max - self.min) // self.steps
		
		self.valueView = wx.StaticText(panel, label=str(self.value)+"    ")
		self.view = wx.Slider(panel, value=0, minValue=0, maxValue=totalSteps)
		self.view.Bind(wx.EVT_SCROLL, self.processUpdate)

		self.updateWidget()

		self.view.SetMinSize((300, 30))

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.view)
		sizer.Add(self.valueView, wx.EXPAND)

		return sizer

class CheckBox(Input):
	def __init__(self, name, value, onUpdate=None):
		Input.__init__(self, name, value, onUpdate)

	def updateWidget(self):
		self.view.SetValue(self.value)

	def processUpdate(self, event):
		self.value = self.view.GetValue()
		self.onUpdate()

	def createWxWidget(self, panel):
		
		self.view = wx.CheckBox(panel)
		self.view.SetValue(self.value)
		self.view.Bind(wx.EVT_CHECKBOX, self.processUpdate)

		return self.view

class Text(Input):
	def __init__(self, name, value='', onUpdate=None):
		Input.__init__(self, name, value, onUpdate)

	def updateWidget(self):
		self.view.SetValue(self.value)

	def processUpdate(self, event):
		self.value = self.view.GetValue()
		self.onUpdate()

	def createWxWidget(self, panel):
		
		self.view = wx.TextCtrl(panel, value=self.value)
		self.view.Bind(wx.EVT_TEXT, self.processUpdate)

		return self.view

class Color(Input):
	def __init__(self, name, value, onUpdate=None):
		Input.__init__(self, name, value, onUpdate)

	def updateWidget(self):
		self.view.SetColour(self.value)

	def processUpdate(self, event):
		color = self.view.GetColour()
		self.value = (color.Red(), color.Green(), color.Blue(), color.Alpha())
		self.onUpdate()

	def createWxWidget(self, panel):
		
		self.view = wx.ColourPickerCtrl(panel, colour=self.value)
		self.view.Bind(wx.EVT_COLOURPICKER_CHANGED, self.processUpdate)

		return self.view

class File(Input):
	def __init__(self, name, value, onUpdate=None):
		Input.__init__(self, name, value, onUpdate)

	def updateWidget(self):
		self.view.SetPath(self.value)

	def processUpdate(self, event):
		self.value = self.view.GetPath()
		self.onUpdate()

	def createWxWidget(self, panel):
		
		self.view = wx.FilePickerCtrl(panel, path=self.value)
		self.view.Bind(wx.EVT_FILEPICKER_CHANGED, self.processUpdate)

		return self.view

class Folder(Input):
	def __init__(self, name, value, onUpdate=None):
		Input.__init__(self, name, value, onUpdate)

	def updateWidget(self):
		self.view.SetPath(self.value)

	def processUpdate(self, event):
		self.value = self.view.GetPath()
		self.onUpdate()

	def createWxWidget(self, panel):
		
		self.view = wx.DirPickerCtrl(panel, path=self.value)
		self.view.Bind(wx.EVT_DIRPICKER_CHANGED, self.processUpdate)

		return self.view

def exampleUpdate(control, value, state):
	dprint(control.name, value)

def exampleUpdateSlider(control, value, state):
	dprint(control.name, value)

	state[0].setValue(value)

if __name__ == "__main__":

	button1 = InputButton("Button", onClick=exampleUpdate)
	slider1 = InputSlider("Slider A", 10, onUpdate=exampleUpdate)
	slider2 = InputSlider("Slider B", 10, onUpdate=exampleUpdateSlider)
	slider3 = InputSlider("Slider C", 10, onUpdate=exampleUpdateSlider)
	checkbox1 = InputCheckBox("Important", True, onUpdate=exampleUpdate)
	color1 = InputColor("Color", "#0088FF", onUpdate=exampleUpdate)
	color2 = InputColor("Color", (255, 128, 0, 255), onUpdate=exampleUpdate)
	text1 = InputText("Text", "Text", onUpdate=exampleUpdate)
	file1 = InputFile("File", "Text", onUpdate=exampleUpdate)
	folder1 = InputFolder("Folder", "Text", onUpdate=exampleUpdate)

	inputs = Inputs(state=[slider1])

	inputs.addInput(button1, "Inputs")
	inputs.addInput(slider1, "Inputs")
	inputs.addInput(slider2, "Inputs")
	inputs.addInput(slider3, "Inputs")
	inputs.addInput(checkbox1, "Inputs")
	inputs.addInput(color1, "Inputs")
	inputs.addInput(color2, "Inputs")
	inputs.addInput(text1, "Inputs")
	inputs.addInput(file1, "Inputs")
	inputs.addInput(folder1, "Inputs")

	inputs.show()