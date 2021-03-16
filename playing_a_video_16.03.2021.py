import wx
import wx.media
import os
#--------------------------------------------------------------------------------------------------------------------
class StaticText(wx.StaticText):
    """
    A StaticText that only updates the label if it has changed, to
    help reduce potential flicker since these controls would be
    updated very frequently otherwise.
    """
    def SetLabel(self, label):
        if label != self.GetLabel():
            wx.StaticText.SetLabel(self, label)
#----------------------------------------------------------------------
class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1,
                          style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)
        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER,
                                         szBackend=wx.media.MEDIABACKEND_DIRECTSHOW
                                         #szBackend=wx.media.MEDIABACKEND_QUICKTIME
                                         #szBackend=wx.media.MEDIABACKEND_WMP10
                                         )
        except NotImplementedError:
            self.Destroy()
            raise
        # print(dir(self.mc))
        self.video_size = parent.GetSize()
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        loadButton = wx.Button(self, -1, "Load File")
        self.Bind(wx.EVT_BUTTON, self.OnLoadFile, loadButton)
        playButton = wx.Button(self, -1, "Play")
        self.Bind(wx.EVT_BUTTON, self.OnPlay, playButton)
        self.playBtn = playButton
        pauseButton = wx.Button(self, -1, "Pause")
        
        eventButton = wx.Button(self, -1, "Event")
        self.eventBtn = eventButton
        
        next_stepButton = wx.Button(self, -1, "Close")
        self.next_stepBtn = next_stepButton
                
        self.Bind(wx.EVT_BUTTON, self.OnPause, pauseButton)
        self.Bind(wx.EVT_BUTTON, self.OnEvent, pauseButton) 
        stopButton = wx.Button(self, -1, "Back")
        self.Bind(wx.EVT_BUTTON, self.OnStop, stopButton)
        self.Bind(wx.EVT_BUTTON, self.OnEvent, eventButton)
        self.Bind(wx.EVT_BUTTON, self.on_quit, next_stepButton)
        self.slider = wx.Slider(self, -1, 0,0.0001,3000, pos=(120,680), style = wx.SL_HORIZONTAL | wx.SL_LABELS, size = (400, -1))
        self.slider.SetMinSize((self.video_size[0]-15, -1))
        self.Bind(wx.EVT_SLIDER, self.OnSeek, self.slider)
        self.st_size = StaticText(self, -1, size=(100,-1))
        self.st_len  = StaticText(self, -1, size=(100,-1))
        self.st_pos  = StaticText(self, -1, size=(100,-1))
        self.st_file = StaticText(self, -1, ".mid .mp3 .wav .au .avi .mpg", size=(200,-1))
        Bsizer = wx.BoxSizer(wx.VERTICAL)
        Lsizer = wx.BoxSizer(wx.HORIZONTAL)
        Lsizer.Add(loadButton, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        Lsizer.Add(self.st_file, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        Bsizer.Add(Lsizer)
        Bsizer.Add(self.mc, 1, wx.ALL, 5) # for .avi .mpg video files
        Bsizer.Add(self.slider)
        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(playButton, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        bsizer.Add(pauseButton, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        bsizer.Add(stopButton, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        bsizer.Add(eventButton, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        bsizer.Add(next_stepButton, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        Bsizer.Add(bsizer)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.st_size, 0, wx.ALL|wx.ALIGN_RIGHT, 7)
        sizer.Add(self.st_len, 0, wx.ALL|wx.ALIGN_RIGHT, 7)
        sizer.Add(self.st_pos, 0, wx.ALL|wx.ALIGN_RIGHT, 7)
        sizer.Add(next_stepButton, 0, wx.ALL|wx.ALIGN_RIGHT, 7)
        Bsizer.Add(sizer)
        self.SetSizer(Bsizer)
        filename = myVideo
        
        if os.path.isfile(filename):
            wx.CallAfter(self.DoLoadFile, os.path.abspath(filename))
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)
    def OnLoadFile(self, evt):
        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.DoLoadFile(path)
        dlg.Destroy()
    def DoLoadFile(self, path):
        #self.playBtn.Disable()
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            folder, filename = os.path.split(path)
            self.st_file.SetLabel('%s' % filename)
            self.mc.SetInitialSize(self.video_size)
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
    def OnMediaLoaded(self, evt):
        self.playBtn.Enable()
    def OnPlay(self, evt):
        if not self.mc.Play():
            wx.MessageBox("Unable to Play media : Unsupported format?",
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        else:
            self.mc.SetInitialSize(self.video_size)
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
    def OnPause(self, evt):        
        self.mc.Pause()
        evt.Skip()
               
    def OnStop(self, evt):
        self.mc.Stop()
    
       
    def OnSeek(self, evt):
        offset = self.slider.GetValue()
        self.mc.Seek(offset)
    def OnTimer(self, evt):
        offset = self.mc.Tell()
        offset_hours = offset//3600000
        offset_minutes = offset//60000 - offset_hours*60
        offset_seconds = offset//1000 - offset_minutes*60
        total_hours = self.mc.Length()//3600000
        total_minutes = self.mc.Length()//60000 - total_hours*60
        total_seconds = self.mc.Length()//1000 - total_minutes*60
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s ms' % self.mc.Length())
        self.st_len.SetLabel('length: %d : %d : %d' % (total_hours, total_minutes, total_seconds))
        self.st_pos.SetLabel('time: %d : %d : %d ' % (offset_hours,  offset_minutes, offset_seconds))
    def OnEvent(self, evt):
        offset = float(self.slider.GetValue())
        print(offset)
        evt.Skip()
        
        offset_sec=offset//1000        
        offset_minute=offset_sec//60       
        offset_hour=offset_minute//60
        
        offset_sec_0=offset_sec-offset_minute*60        
        offset_minute_0=offset_minute-offset_hour*60
        offset_hour_0=offset_hour
        
        offset_hour_0=str(int(offset_hour_0))
        if int(offset_hour_0)<10:
            offset_hour_0='0'+str(int(offset_hour_0))
        offset_minute_0=str(int(offset_minute_0))
        if int(offset_minute_0)<10:
            offset_minute_0='0'+str(int(offset_minute_0))
        offset_sec_0=str(int(offset_sec_0))
        if int(offset_sec_0)<10:
            offset_sec_0='0'+str(int(offset_sec_0))
        offset_0=offset_hour_0+offset_minute_0+offset_sec_0
        offset_0=offset_0[(len(offset_0)-6):]
        print (offset_0)
        text_file=open("intercode.txt", "w", encoding='utf-8')
        text_file.write(offset_0)
        text_file.close() 
    def ShutdownDemo(self):
        self.timer.Stop()
        del self.timer
    def on_quit(self,evt):
        print ('close')       
        self.Destroy()
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------
ictal_episode_code=''
text_file=open("ictal_episode_code.txt", "w", encoding='utf-8')
text_file.write(ictal_episode_code)
text_file.close()
read_code=''
while read_code=='':
    text_file=open("ictal_episode_code.txt", "r", encoding='utf-8')
    read_code=text_file.read(40)
    text_file.close()
    print("perpetum mobile")
ictal_episode_code=read_code

videoplayer=''
text_file=open("video-player_go_no_go.txt", "w", encoding='utf-8')
text_file.write(str(videoplayer))
text_file.close()
read_video=''
while read_video=='':
    text_file=open("video-player_go_no_go.txt", "r", encoding='utf-8')
    read_video=text_file.read(10)
    text_file.close()
    print('mobile perpetum')
if read_video=='0':
    quit()
if read_video=='1':
    # CHOOSE VIDEO HERE
    myVideo=r"C:\Users\maric\Downloads\marik_newer\\"+ictal_episode_code+".wmv"
        
    app = wx.App(0)
    frame = wx.Frame(None, size=(640, 480))
    panel = TestPanel(frame)
    frame.Show()
    app.MainLoop()


