
import sys
from PyQt4 import QtGui, QtCore
import paramiko
import time,os,threading,traceback


class Window( QtGui.QWidget ):
    def __init__( self ):
        super( Window, self ).__init__()
        self.setWindowTitle( "TestClient_helper" )
        self.resize( 500, 500 )
        hbox = QtGui.QHBoxLayout()
        vbox_left = QtGui.QVBoxLayout()
        vbox_right= QtGui.QVBoxLayout()
        self.list_machine = \
        [
        'sh-racka01.lsi.com', 
        'sh-racka02.lsi.com',
        'sh-racka03.lsi.com',
        'sh-racka04.lsi.com',
        'sh-racka05.lsi.com',
        'sh-racka06.lsi.com',
        'sh-racka07.lsi.com',
        'sh-racka08.lsi.com',
        'sh-racka09.lsi.com',
        'sh-racka10.lsi.com',
        'sh-racka11.lsi.com',
        'sh-racka12.lsi.com',
        'sh-racka13.lsi.com',
        'sh-racka14.lsi.com', 
        'sh-racka15.lsi.com',
        'lt-ssdt27-01.lsi.com',
        'lt-ssdt27-02.lsi.com',
        'lt-ssdt27-03.lsi.com',
        'lt-ssdt27-04.lsi.com',
        'lt-ssdt27-05.lsi.com',
        'lt-ssdt27-06.lsi.com',
        'lt-ssdt27-07.lsi.com',
        'lt-ssdt27-08.lsi.com',
        'lt-ssdt27-09.lsi.com',
        'lt-ssdt27-10.lsi.com',
        'lt-ssdt27-11.lsi.com',
        'lt-ssdt27-12.lsi.com',
        'lt-ssdt27-13.lsi.com',
        'lt-ssdt27-14.lsi.com',
        'lt-ssdt27-15.lsi.com',
        '135.24.22.205',
        'lt-ssdt26-06.lsi.com',
        'lt-ssdt26-07.lsi.com',
        'lt-ssdt26-08.lsi.com',]
        self.cb = []

        for i in self.list_machine:
            self.cb.append(QtGui.QCheckBox(i))

        for j in xrange(len(self.list_machine)):
            vbox_left.addWidget(self.cb[j])

        hbox.addLayout(vbox_left)
        hbox.addLayout(vbox_right) 

        self.button = QtGui.QPushButton( "start" )
        vbox_right.addWidget( self.button )
        self.connect( self.button, QtCore.SIGNAL( 'clicked()' ), self.OnStart )

        self.button2 = QtGui.QPushButton( "stop" )
        vbox_right.addWidget( self.button2 )
        self.connect( self.button2, QtCore.SIGNAL( 'clicked()' ), self.OnStop )

        self.button3 = QtGui.QPushButton( "restart" )
        vbox_right.addWidget( self.button3 )
        self.connect( self.button3, QtCore.SIGNAL( 'clicked()' ), self.OnRestart )

        # self.button4 = QtGui.QPushButton( "input" )
        # vbox_right.addWidget( self.button4 )
        # self.connect( self.button4, QtCore.SIGNAL( 'clicked()' ), self.OnInput)

        self.pushbutton = QtGui.QPushButton('choose')
        menu = QtGui.QMenu()
        menu.addAction('uncheckall', self.uncheckall)
        menu.addAction('choose client', self.choosegroup1)
        menu.addAction('choose enteprise', self.choosegroup2)
        menu.addAction('choose all', self.chooseall)
        self.pushbutton.setMenu(menu)
        vbox_right.addWidget( self.pushbutton )

        self.button5 = QtGui.QPushButton( "IDFY" )
        vbox_right.addWidget( self.button5 )
        self.connect( self.button5, QtCore.SIGNAL( 'clicked()' ), self.OnIDFY)

        self.button7 = QtGui.QPushButton( "PwOn" )
        vbox_right.addWidget( self.button7 )
        self.connect( self.button7, QtCore.SIGNAL( 'clicked()' ), self.OnPwOn)

        self.button8 = QtGui.QPushButton( "PwOff" )
        vbox_right.addWidget( self.button8 )
        self.connect( self.button8, QtCore.SIGNAL( 'clicked()' ), self.OnPwOff)

        self.button9 = QtGui.QPushButton( "SE" )
        vbox_right.addWidget( self.button9 )
        self.connect( self.button9, QtCore.SIGNAL( 'clicked()' ), self.OnSE)

        self.button10 = QtGui.QPushButton( "STBI" )
        vbox_right.addWidget( self.button10 )
        self.connect( self.button10, QtCore.SIGNAL( 'clicked()' ), self.OnSTBI)

        self.button11 = QtGui.QPushButton( "CDU" )
        vbox_right.addWidget( self.button11 )
        self.connect( self.button11, QtCore.SIGNAL( 'clicked()' ), self.OnCDU)

        self.button6 = QtGui.QPushButton( "input" )
        vbox_right.addWidget( self.button6 )
        self.connect( self.button6, QtCore.SIGNAL( 'clicked()' ), self.OnInputCmd)

        self.input = QtGui.QPlainTextEdit(self)
        vbox_right.addWidget( self.input )

        self.test_message = QtGui.QTextEdit(self)
        vbox_right.addWidget( self.test_message )

        self.status = QtGui.QStatusBar(self)
        vbox_right.addWidget(self.status)
        self.status.showMessage('Ready')

        self.setLayout( hbox )

        #self.cur_path = os.path.dirname(__file__)
        self.cur_path = os.path.dirname(os.path.abspath(__file__))
        self.list_folder = {
                            'Pass': 'Pass',
                            'Fail': 'Fail',
                            'Error': 'Error',
                            }
        self.CleanLogFolder()


    def choosegroup1(self):
        self.choosegroup1 = [
        'sh-racka02.lsi.com',
        'sh-racka03.lsi.com',
        'sh-racka11.lsi.com',
        'sh-racka12.lsi.com',
        'sh-racka13.lsi.com',
        'sh-racka14.lsi.com', 
        'lt-ssdt27-01.lsi.com',
        'lt-ssdt27-02.lsi.com',
        'lt-ssdt27-03.lsi.com',
        'lt-ssdt27-04.lsi.com',
        'lt-ssdt27-05.lsi.com',
        'lt-ssdt27-06.lsi.com',
        'lt-ssdt27-07.lsi.com',
        'lt-ssdt27-08.lsi.com',
        'lt-ssdt27-09.lsi.com',
        'lt-ssdt27-10.lsi.com',
        'lt-ssdt27-11.lsi.com',
        'lt-ssdt27-12.lsi.com',
        'lt-ssdt27-13.lsi.com',
        'lt-ssdt27-14.lsi.com',
        'lt-ssdt27-15.lsi.com',
        ]
        for i in xrange(len(self.list_machine)):
            if self.list_machine[i] in self.choosegroup1:
                self.cb[i].toggle()
                    
    def chooseall(self):
        for i in xrange(len(self.list_machine)):
            if not self.cb[i].isChecked():
                self.cb[i].toggle()

    def choosegroup2(self):
        pass

    def uncheckall(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                self.cb[i].toggle()

    def OnStart(self):
        self.TestClientStart()

    def OnStop(self):
        self.TestClientStop()

    def OnRestart(self):
        self.TestClientInput3('python /home/yoxu/sc/sd/testclient.py')

    # def OnInput(self):
    #     self.TestClientInput3('source /home/yoxu/.bashrc')

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

    def OnCDU(self):
        #self.TestClientInput3("ConfigDriveUnique.py")
        self.TestClientInput3("cdu")

    def OnInputCmd(self):
        self.TestClientInput3()

    def work2(self, hostname, cmd):
        sshCtl, error = self.__CtlConnect( hostname )

        if error == 0:
            
            sshChannel = sshCtl.get_transport().open_session()
            sshChannel.settimeout(5)
            sshChannel.set_combine_stderr(True)

            if cmd is None:
                cmd = str(self.input.toPlainText())
            try:
                sshChannel.exec_command(cmd)

                while not sshChannel.exit_status_ready():
                    buf1 = ''
                    while sshChannel.recv_ready():
                        buf1 += sshChannel.recv(1024)
                    time.sleep(2)

                # remember to get everything left when cmd returns
                buf2 = 'The message after exit status ready:\n'
                while sshChannel.recv_ready():
                    buf2 += sshChannel.recv(1024)

                if int(sshChannel.recv_exit_status()) == 0:
                    output, logresult = self.WriteToFile('Pass', hostname)
                    output.write( buf1,)
                    output.write( buf2,)
                    output.write("Exit status: %d" % sshChannel.recv_exit_status())
                    output.flush()
                else:
                    output, logresult = self.WriteToFile('Fail', hostname)
                    output.write(logresult)
                    output.flush()
            except Exception,err:
                errstring = traceback.format_exc()
                print errstring

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
            print 'cmd completed'
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
            self.CleanLog(location)

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