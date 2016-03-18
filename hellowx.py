import wx

class bucky(wx.Frame):
	
	def __init__(self,parent,id):
		#Main things
		wx.Frame.__init__(self,parent,id,'Anything for now',size=(1000,500))
		panel=wx.Panel(self)

		#Buttons
		button=wx.Button(panel,label="exit",pos=(130,10),size=(60,60))
		button.SetForegroundColour('green')
		button.SetBackgroundColour('blue')
		self.Bind(wx.EVT_BUTTON,self.closebutton, button)
		self.Bind(wx.EVT_CLOSE, self.closewindow)

		#Menubar and statusbar
		status=self.CreateStatusBar()
		menubar=wx.MenuBar()
		first=wx.Menu()
		second=wx.Menu()
		first.Append(wx.NewId(),"New ndow","This is a new window")
		first.Append(wx.NewId(),"Open...","Tndow")
		menubar.Append(first,"File")
		menubar.Append(second,"Edit")
		self.SetMenuBar(menubar)


		#Message Dialog yes/no question
		box=wx.MessageDialog(None,'Did you read the how to use Wiki?','Title',wx.YES_NO)
		answer = box.ShowModal()
		box.Destroy()

		#Text box to take entry
		textbox=wx.TextEntryDialog(None, "Please enter something", "Title", 'Click to enter')
		if textbox.ShowModal()==wx.ID_OK:
			answer2=textbox.GetValue()

		#Single Choice Dialogue
		select=wx.SingleChoiceDialog(None,'Which mode?','Mode Choice',['LIFO','FIFO','What so ever'])
		
		
		if select.ShowModal()==wx.ID_OK:
			answer3 = select.GetStringSelection()

		#Image Button
		#pic=wx.Image("1.bmp",wx.BITMAP_TYPE_BMP).ConvertToBitmap()
		#self.button123=wx.BitmapButton(panel,-1, pic, pos=(150,150))
		#self.Bind(wx.EVT_BUTTON, self.closebutton, self.button123)

		#Slider
		slider = wx.Slider(panel,-1 , 50, 1, 100, pos=(300,0), size=(250,-1), style=wx.SL_AUTOTICKS | wx.SL_LABELS)
		slider.SetTickFreq(20, 1)

		#Spinner
		spinner= wx.SpinCtrl(panel, -1, "", (500,250), (100,-1))
		spinner.SetRange(1,100)
		spinner.SetValue(100)

		#Checkbox
		CHKBX=wx.CheckBox(panel, -1, "TEST",(50,200),(100,-1))

		#Test in static text
		tester=(str)(slider.GetValue())
		statictextbox=wx.StaticText(panel,-1, tester, (600,0))


		#List boxes
		MyList=['Hello','List','Boxes']
		container = wx.ListBox(panel, -1, (800,50), (80,-1), MyList, wx.LB_SINGLE)
		container.SetSelection(2)

	def closebutton(self,event):
		self.Close(True)
		
	def closewindow(self,event):
		self.Destroy()
		
if __name__=='__main__' :
	app=wx.PySimpleApp()
	frame=bucky(parent=None,id=-1)
	frame.Show()
	app.MainLoop()
	
	