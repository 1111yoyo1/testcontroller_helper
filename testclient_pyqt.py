
import sys
from PyQt4 import QtGui, QtCore
import paramiko
import time,os,threading,traceback
import win32clipboard
from csvlib import *

class Window( QtGui.QWidget ):
    def __init__( self ):
        super( Window, self ).__init__()


        self.setWindowTitle( "TestClient_helper" )
        self.resize( 500, 500 )
        hbox = QtGui.QHBoxLayout()
        self.vbox_left = QtGui.QVBoxLayout()
        self.vbox_right= QtGui.QVBoxLayout()
        self.cur_path = os.path.dirname(os.path.abspath(__file__))

        self.list_machine = []

        self.hostcsv_path = r'\\cn-vmhost01.sandforce.com\\Share\\Scratch\\yoxu\\share\\testclient'
        #self.csvfile = self.cur_path + '\\' + 'host.csv'
        self.csvfile = self.hostcsv_path + '\\' + 'host.csv'

        for i in GetColumnAllElements(self.csvfile,'hostname'):
            self.list_machine.append(i)

        self.checkboxupdate()

        # self.pushbutton = QtGui.QPushButton('choose')
        # menu = QtGui.QMenu()
        # menu.addAction('Used by selection above', self.selecthost)
        # menu.addAction('uncheckall', self.uncheckall)
        # menu.addAction('choose all', self.chooseall)
        # self.pushbutton.setMenu(menu)
        # self.vbox_right.addWidget( self.pushbutton )

        self.button = QtGui.QPushButton( "start" )
        self.vbox_right.addWidget( self.button )
        self.connect( self.button, QtCore.SIGNAL( 'clicked()' ), self.OnStart )

        self.button2 = QtGui.QPushButton( "stop" )
        self.vbox_right.addWidget( self.button2 )
        self.connect( self.button2, QtCore.SIGNAL( 'clicked()' ), self.OnStop )

        self.button3 = QtGui.QPushButton( "restart" )
        self.vbox_right.addWidget( self.button3 )
        self.connect( self.button3, QtCore.SIGNAL( 'clicked()' ), self.OnRestart )

        self.pushbutton2 = QtGui.QPushButton('action')
        menu2 = QtGui.QMenu()

        menu2.addAction('IDFY', self.OnIDFY)
        menu2.addAction('PowerOn', self.OnPwOn)
        menu2.addAction('PowerOff', self.OnPwOff)
        menu2.addAction('SecurityErase', self.OnSE)
        menu2.addAction('StandbyImmediate', self.OnSTBI)
        self.pushbutton2.setMenu(menu2)
        self.vbox_right.addWidget( self.pushbutton2 )

        self.button11 = QtGui.QPushButton( "Show hostname" )
        self.vbox_right.addWidget( self.button11 )
        self.connect( self.button11, QtCore.SIGNAL( 'clicked()' ), self.OnShowhostname)

        # self.button12 = QtGui.QPushButton( "Refresh hosts" )
        # self.vbox_right.addWidget( self.button12 )
        # self.connect( self.button12, QtCore.SIGNAL( 'clicked()' ), self.Refreshosts)

        self.button6 = QtGui.QPushButton( "input" )
        self.vbox_right.addWidget( self.button6 )
        self.connect( self.button6, QtCore.SIGNAL( 'clicked()' ), self.OnInputCmd)

        self.input = QtGui.QPlainTextEdit(self)
        self.vbox_right.addWidget( self.input )

        self.test_message = QtGui.QTextEdit(self)
        self.vbox_right.addWidget( self.test_message )

        self.status = QtGui.QStatusBar(self)
        self.vbox_right.addWidget(self.status)
        self.status.showMessage('Ready')

        hbox.addLayout(self.vbox_left)
        hbox.addLayout(self.vbox_right) 
        self.setLayout( hbox )
        
        self.list_folder = {
                            'Pass': 'Pass',
                            'Fail': 'Fail',
                            'Error': 'Error',
                            }
        self.CleanLogFolder()

    def checkboxupdate(self):
        self.cb = []
        for i in self.list_machine:
            self.cb.append(QtGui.QCheckBox(i))
        for j in xrange(len(self.list_machine)):
            self.vbox_left.addWidget(self.cb[j])

        self.qcbox = QtGui.QComboBox()
        self.cb_admin = []
        for i in GetColumnAllElements(self.csvfile,'info'):
            self.cb_admin.append(str(i))
        self.target_list = list(set(self.cb_admin))
        self.qcbox.addItems(self.target_list)
        self.qcbox.addItem('uncheckall')
        self.qcbox.addItem('chooseall')
        self.vbox_right.addWidget(self.qcbox)
        self.connect( self.qcbox, QtCore.SIGNAL("currentIndexChanged(QString)"), self.selecthost )

    def Refreshosts(self):
        self.checkboxupdate()

    def selecthost(self):
        for i in xrange(len(self.list_machine)):
            self.cb[i].setEnabled(True)

        ower = self.qcbox.currentText()
        if ower == 'uncheckall':
            for i in xrange(len(self.list_machine)):
                self.cb[i].setDisabled(True)
                if self.cb[i].isChecked():
                    self.cb[i].toggle()

        elif ower == 'chooseall':
            for i in xrange(len(self.list_machine)):
                if not self.cb[i].isChecked():
                    self.cb[i].toggle()

        else:
            choosegroup = []
            for i in GetAllRowByElement(self.csvfile, 'info', ower,'hostname'):
                choosegroup.append(i)
            for i in xrange(len(self.list_machine)):
                if self.cb[i].isChecked():
                    self.cb[i].toggle()

                if self.list_machine[i] in choosegroup:
                    self.cb[i].toggle()
                else:
                    self.cb[i].setDisabled(True)

    def OnStart(self):
        self.TestClientStart()

    def OnStop(self):
        self.TestClientStop()

    def OnRestart(self):
        self.TestClientInput3('python /home/yoxu/sc/sd/testclient.py')

    def OnIDFY(self):
        self.TestClientInput3("IdentifyDevice.py ")

    def OnSTBI(self):
        self.TestClientInput3("StandbyImmediate.py")

    def OnPwOn(self):
        self.TestClientInput3("PowerOn.py --force")

    def OnPwOff(self):
        self.TestClientInput3("PowerOff.py --force")

    def OnSE(self):
        self.TestClientInput3("SecurityErase.py --mode=1")

    def OnShowhostname(self):
        self.test_message.clear()
        result=''
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                result += self.cb[i].text().split('.')[0]+'|'
        result = result[:-1]
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(str(result))
        win32clipboard.CloseClipboard()
        self.test_message.append(result)

    def OnInputCmd(self):
        self.TestClientInput3()

    def getserialparabyhost(self,hostname):
        return ' --serial='+str(GetSingleRowByElement(self.csvfile, 'hostname', hostname,'serialnumber'))

    def work2(self, hostname, cmd):
        sshCtl, error = self.__CtlConnect( hostname )

        if error == 0:
            
            sshChannel = sshCtl.get_transport().open_session()
            sshChannel.settimeout(10)
            sshChannel.set_combine_stderr(True)
            if cmd is None:
                cmd = str(self.input.toPlainText())
                #self.test_message.append(self.getserialparabyhost(hostname))
                if 's2' in cmd :
                    #print self.getserialparabyhost(hostname)
                    #self.test_message.append(self.getserialparabyhost(hostname))
                    cmd += self.getserialparabyhost(hostname)
            try:
                sshChannel.exec_command(cmd)
                buf = ''
                buf1 = ''
                buf2 = 'The message after exit status ready:\n'
                while not sshChannel.exit_status_ready():
                    while sshChannel.recv_ready():
                        buf1 += sshChannel.recv(1024)
                    time.sleep(3)
                    # if buf1 != '':
                    #     break

                # remember to get everything left when cmd returns
                while sshChannel.recv_ready():
                    buf2 += sshChannel.recv(1024)
                buf = buf1 + buf2

                #print sshChannel.recv_exit_status()
                #print int(sshChannel.recv_exit_status())

                try:
                    #self.test_message.append(str(sshChannel.recv_exit_status()))
                    if sshChannel.recv_exit_status() == 0:
                        output, logresult = self.WriteToFile('Pass', hostname)
                    else:
                        output, logresult = self.WriteToFile('Fail', hostname)
                    # output, logresult = self.WriteToFile('Pass', hostname)
                except socket.timeout:
                    output, logresult = self.WriteToFile('Fail', hostname)
                    raise socket.timeout
                output.write( buf,)
                output.flush()
                    # print 2
                    # print time.time()- timeStart
                # timeStart = time.time()
                # timeout = 15
                # while ( time.time()- timeStart ) < timeout:
                #     output, logresult = self.WriteToFile('Pass', hostname)
                # output, logresult = self.WriteToFile('Fail', hostname)
                # if sshChannel.recv_exit_status() == 0:
                #     output, logresult = self.WriteToFile('Pass', hostname)
                # else:
                #     output, logresult = self.WriteToFile('Fail', hostname)

            except Exception,err:
                errstring = traceback.format_exc()

            output.close()
            sshChannel.close() 
        sshCtl.close()
        
    def TestClientInput3(self, cmd = None):
        self.test_message.clear()
        threads = []
        mutex = threading.Lock()
        try:
            for i in xrange(len(self.list_machine)):
                if self.cb[i].isChecked():
                    hostname = self.list_machine[i]
                    threads.append(threading.Thread(target=(self.work2), args=(hostname, cmd)))

            for t in threads:
                t.start()
            for t in threads:
                t.join()
            self.test_message.append( " completed")   
            #print 'cmd completed'
        except Exception, err:
            errstring = traceback.format_exc()
            print errstring
            #self.test_message.append(errstring)
        
    def __CtlConnect(self ,hostname):

        #global sshCtl
        error = 0
        try:
            ctlUser = 'yoxu'
            ctlPasswd = 'YXyx2345'
            ctlPort=22
            paramiko.util.log_to_file('paramiko.log', level=10)
            sshCtl=paramiko.SSHClient()
            sshCtl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshCtl.use_sudo = True
            sshCtl.connect(hostname=hostname,port=ctlPort, username=ctlUser,password=ctlPasswd)
        except:
            output, logresult = self.WriteToFile('Error', hostname)
            output.write(logresult)
            output.flush()
            raise Exception('Connection to SSDT machine failed.')
            error = 1
        return sshCtl, error 

    def WriteToFile(self, resultType, hostname):
        logresult = "%s %s" %(hostname,resultType)
        folder_logname = self.cur_path +'\\%s\\%s.log' %(resultType, hostname)     
        output = open(folder_logname,'w')
        return output, logresult

    def CleanLogFolder(self):
        for types in self.list_folder.keys():
            location = self.cur_path +'\\'+self.list_folder[types]+ '\\'
            if os.path.isdir(location):
                self.CleanLog(location)
            else:
                os.mkdir(location)

    def CleanLog(self, path):
        for files in os.listdir(path):
            if files.endswith('.log'):
                os.remove(path + files)

    def TestClientStart(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.use_sudo = True
                try:
                    stdin, stdout, stderr = ssh.exec_command('su -c"source /mnt/ssdt/.system/Util/SetSsdtEnvironments.sh;export SSDT_FIRMWARE_ROOT="/mnt/ssdt/firmware_mil";TestClient.py start"', timeout=5)
                    for str_out in stdout.readlines():
                        self.test_message.append(str_out),
                    for str_error in stderr.readlines():
                        self.test_message.append(str_error) 
                    self.test_message.append(stdout.read()) 
                except:
                    pass
                finally:
                    self.test_message.append( self.list_machine[i]+" Started")
                cmdlist = ['su;TestClient.py start']
                chl=ssh.invoke_shell(term='vterm', width=8000, height=20000)
                for cmds in cmdlist :
                    chl.sendall(cmds+"\n")

    def TestClientStop(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.use_sudo = True
                stdin, stdout, stderr = ssh.exec_command('su -c "source /mnt/ssdt/.system/Util/SetSsdtEnvironments.sh;TestClient.py stop"')
                for str_out in stdout.readlines():
                    self.test_message.append(str_out),
                for str_error in stderr.readlines():
                    self.test_message.append(str_error)  
                self.test_message.append(stdout.read()) 
                if len(stderr.readlines()) == 0:
                    self.test_message.append(self.list_machine[i]+" Stopped")
                else:
                    self.test_message.append(str_error)

    def TestClientStatus(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.use_sudo = True
                stdin, stdout, stderr = ssh.exec_command('TestClient.py status', timeout=30)
                for str_out in stdout.readlines():
                    if str_out.find('Daemon running') == 8:
                        self.test_message.append(self.list_machine[i]+" Running")
                    if str_out.find("Daemon not running") == 8:
                        self.test_message.append(self.list_machine[i]+" not Running")
                for str_error in stderr.readlines():
                    self.test_message.append(str_error) 
                self.test_message.append(stdout.read())  


app = QtGui.QApplication( sys.argv )
win = Window()
win.show()
app.exec_()