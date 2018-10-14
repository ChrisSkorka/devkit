import wx, devkit.Threads, math, time

class Context():
	def __init__(self, dc):
		#self.context = wx.GraphicsContext.Create(dc)
		#self.context.SetAntialiasMode(wx.ANTIALIAS_DEFAULT)
		self.context = dc
		self.context.SetBackgroundMode(wx.TRANSPARENT)

		self.pen = wx.Pen(wx.Colour(0, 0, 0, 0), 1)
		self.brush = wx.Brush(wx.Colour(0, 0, 0, 0))
		self.context.SetPen(self.pen)
		self.context.SetBrush(self.brush)

	def Flush(self):
		self.context.Flush()

	def getSize(self):
		return self.context.GetSize()

	def setFillColor(self, *color):
		#self.context.SetBrush(wx.Brush(wx.Colour(*color)))
		self.brush.SetStyle(wx.BRUSHSTYLE_SOLID)
		self.brush.SetColour(wx.Colour(*color))
		self.context.SetBrush(self.brush)

	def setStrokeColor(self, *color):
		#self.context.SetPen(wx.Pen(wx.Colour(*color)))
		self.pen.SetStyle(wx.PENSTYLE_SOLID)
		self.pen.SetColour(wx.Colour(*color))
		self.context.SetPen(self.pen)

	def setStrokeWidth(self, width):
		#self.context.SetPen(wx.Pen(wx.Colour(*color)))
		self.pen.SetStyle(wx.PENSTYLE_SOLID)
		self.pen.SetWidth(width)
		self.context.SetPen(self.pen)

	def clearFill(self):
		#self.context.SetBrush(wx.Brush(wx.Colour(0, 0, 0, 0)))
		self.brush.SetStyle(wx.BRUSHSTYLE_TRANSPARENT)
		self.context.SetBrush(self.brush)

	def clearStroke(self):
		#self.context.SetPen(wx.Pen(wx.Colour(0, 0, 0, 0), 0))
		self.pen.SetStyle(wx.PENSTYLE_TRANSPARENT)
		self.context.SetPen(self.pen)

	def setTools(self, fill=None, stroke=None, strokeWidth=None):
		if fill != None:
			self.setFillColor(fill)

		if stroke != None:
			self.setStrokeColor(stroke)	

		if strokeWidth != None:
			self.setStrokeWidth(strokeWidth)	

	def clear(self, color=(255, 255, 255)):
		self.setTools(fill=color, stroke=color, strokeWidth=0)
		self.context.DrawRectangle(0, 0, *self.context.GetSize())

	def rect(self, x, y, width, height, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawRectangle(x, y, width, height)

	def roundRect(self, x, y, width, height, r, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawRoundedRectangle(x, y, width, height, r)

	def oval(self, x, y, rx, ry, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawEllipse(x-rx, y-ry, 2*rx, 2*ry)

	def ovalInRect(self, x, y, width, height, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawEllipse(x, y, width, height)

	def circle(self, x, y, r, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawEllipse(x-r, y-r, 2*r, 2*r)

	def arcPointToPoint(self, xPoint1, yPoint1, xPoint2, yPoint2, xCenter, yCener, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawArc(xPoint1, yPoint1, xPoint2, yPoint2, xCenter, yCener)

	def arc(self, x, y, r, starAngle, endAngle, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		xCenter, yCener = x, y
		xPoint1, yPoint1 = x + math.cos(endAngle) * r, y + math.sin(endAngle) * r
		xPoint2, yPoint2 = x + math.cos(starAngle) * r, y + math.sin(starAngle) * r

		self.context.DrawArc(xPoint1, yPoint1, xPoint2, yPoint2, xCenter, yCener)

	def point(self, x, y, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawPoint(x, y)

	def line(self, x1, y1, x2, y2, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawLine(x1, y1, x2, y2)

	def polygon(self, points, offset=(0, 0), fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawPolygon(points, *offset)

	def text(self, x, y, text, fill=None, stroke=None, strokeWidth=None):
		self.setTools(fill, stroke, strokeWidth)

		self.context.DrawText(text, x, y)

	def bitmap(self, x, y, bitmap):

		#drawable = wx.Bitmap.NewFromPNGData(bitmap, size)
		self.setStrokeWidth(1)

		for i in range(len(bitmap)):
			row = bitmap[i]
			for j in range(len(row)):
				self.setStrokeColor(row[j])
				self.context.DrawPoint(i+x, j+y)


		#self.context.DrawBitmap(drawable, x, y)

class CanvasFrame(wx.Frame):

	def __init__(self, 
			parent, 
			size, 
			title, 
			onDraw, 
			state, 
			onLeftUp, 
			onLeftDown, 
			onRightUp,
			onRightDown,
			onMiddleUp, 
			onMiddleDown, 
			onMouseMove):

		wx.Frame.__init__(self, None, title=title, size=size)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
		self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
		self.Bind(wx.EVT_RIGHT_UP, self.onRightUp)
		self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
		self.Bind(wx.EVT_MIDDLE_UP, self.onMiddleUp)
		self.Bind(wx.EVT_MIDDLE_DOWN, self.onMiddleDown)
		self.Bind(wx.EVT_MOTION, self.onMouseMove)

		self.onDraw = onDraw
		self.leftUp = onLeftUp
		self.leftDown = onLeftDown
		self.rightUp = onRightUp
		self.rightDown = onRightDown
		self.middleUp = onMiddleUp
		self.middleDown = onMiddleDown
		self.mouseMove = onMouseMove

		self.state = state
		self.parent = parent
		self.lastDraw = time.time()
		self.created = time.time()
		self.lastMousePosition = (0, 0)

	def onLeftUp(self, event):
		position = event.GetPosition()
		if self.leftUp != None:
			self.leftUp(position.x, position.y, self.parent, self.state)

	def onLeftDown(self, event):
		position = event.GetPosition()
		if self.leftDown != None:
			self.leftDown(position.x, position.y, self.parent, self.state)

	def onRightUp(self, event):
		position = event.GetPosition()
		if self.rightUp != None:
			self.rightUp(position.x, position.y, self.parent, self.state)

	def onRightDown(self, event):
		position = event.GetPosition()
		if self.rightDown != None:
			self.rightDown(position.x, position.y, self.parent, self.state)

	def onMiddleUp(self, event):
		position = event.GetPosition()
		if self.middleUp != None:
			self.middleUp(position.x, position.y, self.parent, self.state)

	def onMiddleDown(self, event):
		position = event.GetPosition()
		if self.middleDown != None:
			self.middleDown(position.x, position.y, self.parent, self.state)

	def onMouseMove(self, event):
		position = event.GetPosition()
		if self.mouseMove != None:
			self.mouseMove(position.x, position.y, *self.lastMousePosition, self.parent, self.state)

		self.lastMousePosition = (position.x, position.y)

	def OnPaint(self, event=None):
		#dc = wx.PaintDC(self)
		dc = wx.BufferedPaintDC(self)
		context = Context(dc)
		
		now = time.time()
		deltaTime = now - self.lastDraw
		age = now - self.created
		self.lastDraw = now

		if self.onDraw != None:
			self.onDraw(context, age, deltaTime, self.parent, self.state)

		#context.Flush()
		del dc

class Canvas:

	def __init__(self, 
			size = (1280, 720), 
			title = "Graphics Output", 
			onDraw=None, 
			fps=None, 
			state=None, 
			onLeftUp=None, 
			onLeftDown=None, 
			onRightUp=None,
			onRightDown=None,
			onMiddleUp=None, 
			onMiddleDown=None, 
			onMouseMove=None):
		
		self.onDraw = onDraw
		self.fps = fps
		self.state = state
		self.title = title
		self.onLeftUp=onLeftUp
		self.onLeftDown=onLeftDown
		self.onRightUp=onRightUp
		self.onRightDown=onRightDown
		self.onMiddleUp=onMiddleUp
		self.onMiddleDown=onMiddleDown 
		self.onMouseMove=onMouseMove
		
		self.size = size
		self.width, self.height = self.size

	def updateLoop(self):

		delay = 1/self.fps

		time.sleep(0.1)
		while self.frameShown:
			self.frame.Refresh(False)
			time.sleep(delay)

	def getFrames(self):
		
		self.frame = CanvasFrame(self, 
			self.size, 
			self.title, 
			self.onDraw, 
			self.state, 
			self.onLeftUp, 
			self.onLeftDown, 
			self.onRightUp, 
			self.onRightDown, 
			self.onMiddleUp,  
			self.onMiddleDown,  
			self.onMouseMove)

		self.frame.Show()
		self.frame.SetFocus()
		self.frame.Bind(wx.EVT_CLOSE, self.exitApp)
		self.frame.Refresh(False)

		if self.fps != None:

			self.frameShown = True
			Threads.newThread(self.updateLoop)
			#Threads.newThread(self.app.MainLoop())

		return [self.frame]

	def show(self):

		self.app = wx.App()
		self.getFrames()
		self.app.MainLoop()

	def exitApp(self, event):
		self.frameShown = False
		self.frame.Destroy()

	def update(self):
		self.frame.Refresh(False)



def exampleOnDraw(context, time, deltaTime, canvas, state):
	print("On Draw", time, deltaTime)

def exampleOnLeftUp(x, y, canvas, state):
	print("Left Up", x, y)
	
def exampleOnLeftDown(x, y, canvas, state):
	print("Left Down", x, y)

def exampleOnRightUp(x, y, canvas, state):
	print("Right Up", x, y)

def exampleOnRightDown(x, y, canvas, state):
	print("Right Down", x, y)

def exampleOnMiddleUp(x, y, canvas, state):
	print("Right Up", x, y)

def exampleOnMiddleDown(x, y, canvas, state):
	print("Right Down", x, y)

def exampleOnMouseMove(x, y, xLast, yLast, canvas, state):
	print("Mouse Move", x, y, xLast, yLast)

if __name__ == "__main__":

	canvas = Canvas(size=(1280, 720), 
		title="Canvas", 
		onDraw=exampleOnDraw, 
		fps=1, 
		state=None, 
		onLeftDown=exampleOnLeftDown, 
		onLeftUp=exampleOnLeftUp, 
		onRightDown=exampleOnRightDown, 
		onRightUp=exampleOnRightUp, 
		onMiddleDown=exampleOnMiddleDown, 
		onMiddleUp=exampleOnMiddleUp, 
		onMouseMove=exampleOnMouseMove)

	canvas.show()