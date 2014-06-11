
import sys
from PyQt4 import QtGui, QtCore
import paramiko
import time,os,threading,traceback


class Window( QtGui.QWidget ):
    def __init__( self ):
        super( Window, self ).__init__()
        self.setWindowTitle( "hello" )
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

    def work2(self, hostname, cmd, output):
        #sshCtl = None
        sshCtl = self.__CtlConnect( hostname )

        sshChannel = sshCtl.get_transport().open_session()
        sshChannel.settimeout(5)
        sshChannel.set_combine_stderr(True)

        if cmd is None:
            cmd = str(self.input.toPlainText())
        try:
            #print cmd + " is going to be issued on " + hostname
            sshChannel.exec_command(cmd)

            while not sshChannel.exit_status_ready():
                buf = ''
                while sshChannel.recv_ready():
                    #sshChannel.recv(1024), 

                    #print sshChannel.recv(1024),  # use comma(,) to avoid additional new line

                    buf += sshChannel.recv(1024)

                    #self.test_message.append(buf)

                    #print buf

                    output.write( buf,)
                    #output.flush()
                    #os.fsync(output.fileno())
                    # num += 1
                time.sleep(2)

            # remember to get everything left when cmd returns
            buf = 'The message after exit status ready:\n'

            while sshChannel.recv_ready():

                buf += sshChannel.recv(1024)

            output.write( buf,)
            #output.flush()
            #os.fsync(output.fileno())
            if int(sshChannel.recv_exit_status()) == 0:
                output.write("Exit status: %d" % sshChannel.recv_exit_status())
                output.flush()
            else:
                cur_path = os.path.dirname(__file__)
                output_error = open(cur_path +'\\'+ 'error' +'.log' ,'w')
                output_error.write("%s encounter error " %hostname )
                output_error.flush()
            #os.fsync(output.fileno())
            #self.test_message.append(buf+'\n')
        except Exception,err:
            #pass
            errstring = traceback.format_exc()
            print errstring
            #err = 'Timeout. Should not be raised because SSH connection is alive.'
            #print err
            #self.test_message.append(errstring)
        #self.test_message.append(cmd + " completed on " + hostname + '\n')
        sshChannel.close() 
        sshCtl.close()
        output.close()


    def TestClientInput3(self, cmd = None):

        # output.write("%s: Check the PARAMIKO LINK First\n" % time.ctime())
        # output.flush()
        # os.fsync(output.fileno())

        self.test_message.clear()
        threads = []
        mutex = threading.Lock()
        try:
            for i in xrange(len(self.list_machine)):
                if self.cb[i].isChecked():
                    hostname = self.list_machine[i]
                    cur_path = os.path.dirname(__file__)
                    output = open(cur_path +'\\'+ hostname+'.log' ,'w')
                    # self.work2(hostname, cmd, output)
                    threads.append(threading.Thread(target=(self.work2), args=(hostname,cmd,output)))

            for t in threads:
                t.start()
            for t in threads:
                t.join()
            print 'cmd completed'
        except Exception, err:
            errstring = traceback.format_exc()
            print errstring
            #self.test_message.append(errstring)
        

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

    def __CtlConnect(self ,host):

        #global sshCtl
        try:
            ctlUser = 'yoxu'
            ctlPasswd = 'YXyx2345'
            ctlPort=22
            paramiko.util.log_to_file('paramiko.log', level=10)
            sshCtl=paramiko.SSHClient()
            sshCtl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshCtl.use_sudo = True
            sshCtl.connect(hostname=host,port=ctlPort, username=ctlUser,password=ctlPasswd)
        except:
            cur_path = os.path.dirname(__file__)
            output_error = open(cur_path +'\\'+ 'connect_error' +'.log' ,'w')
            output_error.write("%s connection failed " %host )
            output_error.flush()
            raise Exception('Connection to SSDT machine failed.')
        return sshCtl




app = QtGui.QApplication( sys.argv )
win = Window()
win.show()
app.exec_()