import wx
import sys
import schedulers
import pygame


def Wiki_Question_Handler(Answer):
    if Answer == wx.ID_NO:
        FPS = 60
        pygame.init()
        clock = pygame.time.Clock()
        pygame.mixer.quit()
        movie = pygame.movie.Movie('test.mpg')
        screen = pygame.display.set_mode(movie.get_size())
        movie_screen = pygame.Surface(movie.get_size()).convert()
        movie.set_display(movie_screen)
        movie.play()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    movie.stop()
                    playing = False

            screen.blit(movie_screen, (0, 0))
            pygame.display.update()
            clock.tick(FPS)

    pygame.quit()


class Sched(wx.Frame):
    total_time = 0
    average_waiting = 0
    Process = []
    Time_Slice = 0
    count = 0

    def __init__(self, parent, id):

        # Did you read the wiki?
        WikiQuestion = wx.MessageDialog(None, 'Did you read the "how to use" Wiki?', 'Title', wx.YES_NO)
        WikiQuestion_Answer = WikiQuestion.ShowModal()
        WikiQuestion.Destroy()
        Wiki_Question_Handler(WikiQuestion_Answer)

        # Single Choice Dialogue (Choose Scheduler mode)
        select = wx.SingleChoiceDialog(None, 'Please choose the type of your desired scheduler', 'Scheduler Choice',
                                       ['FCFS', 'SJF Preemptive',
                                        'SJF non-Preemptive', 'Priority preepmtive', 'Priority non-Preemptive',
                                        'Round Robin'])
        if select.ShowModal() == wx.ID_CANCEL:
            sys.exit()
        Scheduler_Mode_Answer = select.GetStringSelection()
        select.Destroy()

        # Main Frame
        image = 'roses.png'
        self.bmp1 = wx.Image(image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.Width = self.bmp1.GetWidth()
        self.Hight = self.bmp1.GetHeight()
        wx.Frame.__init__(self, parent, id, Scheduler_Mode_Answer + " Scheduler", size=(self.Width, self.Hight),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        wx.Frame.BackgroundColour = "black"
        panel.SetBackgroundColour('green')
        self.bitmap1 = wx.StaticBitmap(self, -1, self.bmp1, (0, 0))
        panel = self.bitmap1

        # OS scheduler edited text
        OS = '0.png'
        OS_im = wx.Image(OS, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.StaticBitmap(self, -1, OS_im, (0, 0))

        """ Arrival time objects """
        # Arrival Time static text
        wx.StaticBitmap(self, -1, wx.Image('1.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), (0, 120))
        # Arrival Time text
        Arrival_Time_Text = wx.TextCtrl(panel, pos=(250, 137), size=(100, 32), style=wx.BORDER_NONE)
        # Changing arrival time font
        Arrival_Time_Text.SetFont(
            wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.BOLD, False, u'Viner Hand ITC'))
        # Setting default Value
        Arrival_Time_Text.Value = '0'
        # Arrival_Time_Static = wx.StaticText(panel, -1, 'Arrival time', pos=(10, 10), size=(-1, -1), style=0)

        """ Burst Time objs """
        # Burst time static text
        wx.StaticBitmap(self, -1, wx.Image('2.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), (5, 188))
        # Burst time Text
        Burst_Time_Text = wx.TextCtrl(panel, pos=(250, 187), size=(100, 32), style=wx.BORDER_NONE)
        Burst_Time_Text.Value = '0'
        # Changing font
        Burst_Time_Text.SetFont(
            wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.BOLD, False, u'Viner Hand ITC'))
        # Burst_Time_Static = wx.StaticText(panel, -1, 'Burst time', pos=(10, 30), size=(-1, -1), style=0)

        # Case that takes priority
        if Scheduler_Mode_Answer == 'Priority preepmtive' or Scheduler_Mode_Answer == 'Priority non-Preemptive':
            # Priority time image
            wx.StaticBitmap(self, -1, wx.Image('3.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), (5, 240))
            # Priority text control
            Priority_Text = wx.TextCtrl(panel, pos=(250, 237), size=(100, 32), style=wx.BORDER_NONE)
            # Change font
            Priority_Text.SetFont(
                wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.BOLD, False, u'Viner Hand ITC'))
            Priority_Text.Value = '100'

        # Case Round robin
        if Scheduler_Mode_Answer == 'Round Robin':
            wx.StaticBitmap(self, -1, wx.Image('4.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap(), (5, 240))
            Time_Slice_Spinner = wx.SpinCtrl(panel, -1, "", (230, 247), (100, 32))
            # Change font
            Time_Slice_Spinner.SetFont(
                wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.BOLD, False, u'Viner Hand ITC'))
            Time_Slice_Spinner.SetValue(50)

        """ ADD Button """
        # Add process button
        Add_Process = wx.BitmapButton(panel, -1, wx.Image("Add.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
                                      pos=(380, 135), style=wx.BORDER_NONE)
        # Add button action event handlers
        if Scheduler_Mode_Answer == 'FCFS' or Scheduler_Mode_Answer == 'SJF preepmtive' or Scheduler_Mode_Answer == 'SJF non-Preemptive':
            self.Bind(wx.EVT_BUTTON, lambda event: self.Add_Process_EVT(event, Burst_Time_Text, Arrival_Time_Text),
                      Add_Process)

        elif Scheduler_Mode_Answer == 'Priority preepmtive' or Scheduler_Mode_Answer == 'Priority non-Preemptive':
            self.Bind(wx.EVT_BUTTON,
                      lambda event: self.Add_Process_EVT_P(event, Burst_Time_Text, Arrival_Time_Text, Priority_Text),
                      Add_Process)

        elif Scheduler_Mode_Answer == 'Round Robin':
            self.Bind(wx.EVT_BUTTON, lambda event: self.Add_Process_EVT_T(event, Burst_Time_Text, Arrival_Time_Text,
                                                                          Time_Slice_Spinner, panel), Add_Process)
        """Finish Button"""
        # Finish process addition button
        self.Finish = wx.BitmapButton(panel, -1, wx.Image("Schedule.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap(),
                                      pos=(480, 125), style=wx.BORDER_NONE)
        self.Bind(wx.EVT_BUTTON, lambda event: self.Finish_EVT(event, Scheduler_Mode_Answer), self.Finish)

        """HELP ME! button """
        HELP = wx.BitmapButton(panel, -1, wx.Image("help.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap(), pos=(1200, 5),
                               style=wx.BORDER_NONE)
        self.Bind(wx.EVT_BUTTON, lambda event: self.Play_Video(event), HELP)
        self.Panel1 = panel

    # Normal Schedulers
    def Add_Process_EVT(self, event, Burst, Arrival):
        self.Process.append((self.count, float(Arrival.GetValue()), float(Burst.GetValue())))
        Burst.Value = '0'
        Arrival.Value = '0'
        self.count += 1

    # Priority Schedulers
    def Add_Process_EVT_P(self, event, Burst, Arrival, Priority):
        self.Process.append((self.count, float(Arrival.GetValue()), float(Burst.GetValue()), int(Priority.GetValue())))
        self.count += 1
        Burst.Value = '0'
        Arrival.Value = '0'
        Priority.Value = '100'

    # Round Robin Schedulers
    def Add_Process_EVT_T(self, event, Burst, Arrival, Time_Slice_Spinner, Panel):
        self.Process.append((self.count, float(Arrival.GetValue()), float(Burst.GetValue())))
        self.count += 1
        Burst.Value = '0'
        Arrival.Value = '0'
        # wx.StaticText()
        if Time_Slice_Spinner:
            self.Time_Slice = Time_Slice_Spinner.GetValue()
        Quantum = wx.StaticText(Panel, -1, ' = ' + (str)(self.Time_Slice), pos=(230, 245), size=(-1, -1),
                                style=wx.BORDER_NONE)
        Quantum.SetFont(
            wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.BOLD, False, u'Viner Hand ITC'))
        Quantum.SetBackgroundColour("white")
        Time_Slice_Spinner.Hide()

    def Finish_EVT(self, event, Scheduler_Type):
        self.Finish.Destroy()
        if Scheduler_Type == 'FCFS':
            Av = schedulers.fcfs(self.Process)
        elif Scheduler_Type == 'SJF Preemptive':
            schedulers.sjf_preemptive(self.Process)
        elif Scheduler_Type == 'SJF non-Preemptive':
            Av = schedulers.sjf_non_preemptive(self.Process)
        elif Scheduler_Type == 'Priority Preemptive':
            schedulers.priority_preemptive(self.Process)
        elif Scheduler_Type == 'Priority non-Preemptive':
            Av = schedulers.priority_non_preemptive(self.Process)
        elif Scheduler_Type == 'Round Robin':
            Av = schedulers.round_robin_non_preemptive(self.Process, self.Time_Slice)

        image1 = "out.png"
        bmp1 = wx.Image(image1, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap21 = wx.StaticBitmap(self, -1, bmp1, (0, (self.Hight / 2) - 10))

        Average_Waiting = wx.StaticText(self.Panel1, -1, 'Average Waiting = %.2f' % Av, pos=(800, 500), size=(-1, -1),
                                        style=wx.BORDER_NONE)
        Average_Waiting.SetFont(
            wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_ITALIC, wx.BOLD, False, u'Viner Hand ITC'))
        Average_Waiting.SetBackgroundColour("white")

    def Play_Video(self, event):
        Wiki_Question_Handler(wx.ID_NO)


if __name__ == '__main__':
    app = wx.App(0)
    frame = Sched(parent=None, id=-1)
    frame.Show(True)
    app.MainLoop()
