import wx
import sys
def Wiki_Question_Handler(Answer):
	if Answer == wx.ID_NO:
		AA=wx.MessageDialog(None,"Please click help from the menu bar then choose Wiki\nTo understand how to use the program",'Wiki',wx.OK)
		A=AA.ShowModal()
		AA.Destroy()




class bucky(wx.Frame):

	total_time = 0
	average_waiting=0

	def __init__(self,parent,id):


		#Did you read the wiki?
		WikiQuestion=wx.MessageDialog(None,'Did you read the "how to use" Wiki?','Title',wx.YES_NO)
		WikiQuestion_Answer = WikiQuestion.ShowModal()
		WikiQuestion.Destroy()
		Wiki_Question_Handler(WikiQuestion_Answer)

		#Single Choice Dialogue (Choose Scheduler mode)
		select=wx.SingleChoiceDialog(None,'Please choose the type of your desired scheduler','Scheduler Choice',['FCFS','SJF','Priority','Round Robin'])
		if select.ShowModal()== wx.ID_CANCEL:
			sys.exit()
		Scheduler_Mode_Answer=select.GetStringSelection()
		select.Destroy()



		#Main Frame
		wx.Frame.__init__(self,parent,id,Scheduler_Mode_Answer+" Scheduler",size=(1000,500))
		panel=wx.Panel(self)

		#Arrival Time things
		Arrival_Time_Static=wx.StaticText(panel,-1,'Arrival time',pos=(10,10),size=(-1,-1),style=0)
		Arrival_Time_Text=wx.TextCtrl(panel,pos=(75,8),size=(100,20))
		Arrival_Time_Text.Value='0'

		#Burst Time things
		Burst_Time_Static=wx.StaticText(panel,-1,'Burst time',pos=(10,30),size=(-1,-1),style=0)
		Burst_Time_Text=wx.TextCtrl(panel,pos=(75,28),size=(100,20))
		Burst_Time_Text.Value='0'

		#Add process button
		Add_Process=wx.Button(panel,label="Add process",pos=(200,15),size=(-1,-1))
		Add_Process.SetForegroundColour('red')
		Add_Process.SetBackgroundColour('yellow')
		self.Bind(wx.EVT_BUTTON,lambda event: self.Add_Process_EVT(event,Burst_Time_Text,Arrival_Time_Text), Add_Process)

		#Finish process addition button
		Finish=wx.Button(panel,label="Done",pos=(300,15),size=(-1,-1))
		self.Bind(wx.EVT_BUTTON,self.Finish_EVT, Finish)

	def Add_Process_EVT(self,event,Burst,Arrival):
		self.total_time=self.total_time+(int)(Burst.GetValue())
		Burst.Value='0'
		Arrival.Value='0'


	def Finish_EVT(self,event):
		Tester=wx.MessageDialog(None,"Total times=" + (str)(self.total_time),'Title',wx.OK)
		Tester1 = Tester.ShowModal()
		if Tester1==wx.ID_OK:
			sys.exit()

if __name__=='__main__' :
	app=wx.PySimpleApp()
	frame=bucky(parent=None,id=-1)
	frame.Show()
	app.MainLoop()
	
