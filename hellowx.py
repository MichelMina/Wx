import wx
import sys
#import schedulers


def Wiki_Question_Handler(Answer):
	if Answer == wx.ID_NO:
		AA=wx.MessageDialog(None,"Please click help from the menu bar then choose Wiki\nTo understand how to use the program",'Wiki',wx.OK)
		A=AA.ShowModal()
		AA.Destroy()

class Sched(wx.Frame):

	total_time = 0
	average_waiting=0
	Process=[]
	Time_Slice=0
	count = 0

	def __init__(self,parent,id):


		#Did you read the wiki?
		WikiQuestion=wx.MessageDialog(None,'Did you read the "how to use" Wiki?','Title',wx.YES_NO)
		WikiQuestion_Answer = WikiQuestion.ShowModal()
		WikiQuestion.Destroy()
		Wiki_Question_Handler(WikiQuestion_Answer)

		#Single Choice Dialogue (Choose Scheduler mode)
		select=wx.SingleChoiceDialog(None,'Please choose the type of your desired scheduler','Scheduler Choice',['FCFS','SJF Preemptive','SJF non-Preemptive','Priority preepmtive','Priority non-Preemptive','Round Robin'])
		if select.ShowModal()== wx.ID_CANCEL:
			sys.exit()
		Scheduler_Mode_Answer=select.GetStringSelection()
		select.Destroy()

		#Main Frame
		wx.Frame.__init__(self,parent,id,Scheduler_Mode_Answer+" Scheduler",size=(1000,1000))
		panel=wx.Panel(self)

		#Arrival Time things
		Arrival_Time_Static=wx.StaticText(panel,-1,'Arrival time',pos=(10,10),size=(-1,-1),style=0)
		Arrival_Time_Text=wx.TextCtrl(panel,pos=(75,8),size=(100,20))
		Arrival_Time_Text.Value='0'

		#Burst Time things
		Burst_Time_Static=wx.StaticText(panel,-1,'Burst time',pos=(10,30),size=(-1,-1),style=0)
		Burst_Time_Text=wx.TextCtrl(panel,pos=(75,28),size=(100,20))
		Burst_Time_Text.Value='0'

		#Case that takes priority
		if Scheduler_Mode_Answer != 'FCFS' and Scheduler_Mode_Answer != 'Round Robin':
			Priority_Static= wx.StaticText(panel,-1,'Priority',pos=(10,50),size=(-1,-1),style=0)
			Priority_Text= wx.TextCtrl(panel,pos=(75,48),size=(100,20))
			Priority_Text.Value='100'

		#Case Round robin
		if Scheduler_Mode_Answer == 'Round Robin':
			Priority_Static= wx.StaticText(panel,-1,'Time Slice',pos=(10,50),size=(-1,-1),style=0)
			Time_Slice_Spinner=wx.SpinCtrl(panel, -1, "", (75,48), (100,20))
			Time_Slice_Spinner.Value='1'

		#Add process button
		Add_Process=wx.Button(panel,label="Add process",pos=(200,15),size=(-1,-1))
		if Scheduler_Mode_Answer == 'FCFS':
			self.Bind(wx.EVT_BUTTON,lambda event: self.Add_Process_EVT(event,Burst_Time_Text,Arrival_Time_Text), Add_Process)
		elif Scheduler_Mode_Answer == 'SJF Preemptive' or Scheduler_Mode_Answer == 'SJF non-Preemptive' or Scheduler_Mode_Answer == 'Priority preepmtive' or Scheduler_Mode_Answer == 'Priority non-Preemptive':
			self.Bind(wx.EVT_BUTTON,lambda event: self.Add_Process_EVT_P(event,Burst_Time_Text,Arrival_Time_Text,Priority_Text), Add_Process)
		elif Scheduler_Mode_Answer == 'Round Robin':
			self.Bind(wx.EVT_BUTTON,lambda event: self.Add_Process_EVT_T(event,Burst_Time_Text,Arrival_Time_Text,Time_Slice_Spinner,panel), Add_Process)

		#Finish process addition button
		Finish=wx.Button(panel,label="Done",pos=(300,15),size=(-1,-1))
		self.Bind(wx.EVT_BUTTON,lambda event: self.Finish_EVT(event,Scheduler_Mode_Answer), Finish)

	#Normal Schedulers
	def Add_Process_EVT(self,event,Burst,Arrival):
		self.total_time=self.total_time+(int)(Burst.GetValue())
		self.Process.append(((int)(Arrival.GetValue()),(int)(Burst.GetValue())))
		self.count +=1
		Burst.Value='0'
		Arrival.Value='0'

	#Priority Schedulers
	def Add_Process_EVT_P(self,event,Burst,Arrival,Priority):
		self.total_time=self.total_time+(int)(Burst.GetValue())
		self.Process.append(((int)(Arrival.GetValue()),(int)(Burst.GetValue()),(int)(Priority.GetValue())))
		self.count +=1
		Burst.Value='0'
		Arrival.Value='0'
		Priority.Value='100'

	#Round Robin Schedulers
	def Add_Process_EVT_T(self,event,Burst,Arrival,Time_Slice_Spinner,Panel):
		self.total_time=self.total_time+(int)(Burst.GetValue())
		self.Process.append(((int)(Arrival.GetValue()),(int)(Burst.GetValue())))
		self.count +=1
		Burst.Value='0'
		Arrival.Value='0'
		wx.StaticText()
		self.Time_Slice=Time_Slice_Spinner.GetValue()
		Priority_Static= wx.StaticText(Panel,-1,' = '+(str)(self.Time_Slice),pos=(75,50),size=(-1,-1),style=0)
		Time_Slice_Spinner.Destroy()

	def Finish_EVT(self,event,Scheduler_Type):
		Tester=wx.MessageDialog(None,"Total times=" + (str)(self.total_time),'Title',wx.OK)
		Tester1 = Tester.ShowModal()
		'''if Scheduler_Type == 'FCFS':
			schedulers.fcfs(self.Process)
		elif Scheduler_Type == 'SJF Preemptive':
			schedulers.sjf_preemptive(self.Process)
		elif Scheduler_Type == 'SJF non-Preemptive':
			schedulers.sjf_non_preemptive(self.Process)
		elif Scheduler_Type == 'Priority Preemptive':
			schedulers.priority_preemptive(self.Process)
		elif Scheduler_Type == 'Priority non-Preemptive':
			schedulers.priority_non_preemptive'''
		if Tester1==wx.ID_OK:
			sys.exit()

if __name__=='__main__' :
	app=wx.PySimpleApp()
	frame=Sched(parent=None,id=-1)
	frame.Show()
	app.MainLoop()
	
