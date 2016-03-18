import wx
import sys
def Wiki_Question_Handler(Answer):
	if Answer == wx.ID_NO:
		AA=wx.MessageDialog(None,"Please click help from the menu bar then choose Wiki\nTo understand how to use the program",'Wiki',wx.OK)
		A=AA.ShowModal()
		AA.Destroy()

class bucky(wx.Frame):

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


		#Test in static text
		tester=(str)(Scheduler_Mode_Answer)
		statictextbox=wx.StaticText(panel,-1, tester, (600,0))
if __name__=='__main__' :
	app=wx.PySimpleApp()
	frame=bucky(parent=None,id=-1)
	frame.Show()
	app.MainLoop()
	
