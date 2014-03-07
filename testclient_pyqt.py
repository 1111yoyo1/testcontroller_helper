
import sys
from PyQt4 import QtGui, QtCore
import paramiko
import time

#date = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
#output = open('log_%s.log' % date ,'w')
#output = open('log1.log' ,'w')
#output.write("%s" % time.ctime())
#output.flush()

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
        '135.24.22.205',]
        self.cb = []

        for i in self.list_machine:
            self.cb.append(QtGui.QCheckBox(i))

        for j in xrange(len(self.list_machine)):
            vbox_left.addWidget(self.cb[j])

        hbox.addLayout(vbox_left)
        hbox.addLayout(vbox_right) 
        #self.setLayout(hbox) 

        #checkbox1.setChecked( True )
        self.button = QtGui.QPushButton( "start" )
        vbox_right.addWidget( self.button )
        self.connect( self.button, QtCore.SIGNAL( 'clicked()' ), self.OnStart )

        self.button2 = QtGui.QPushButton( "stop" )
        vbox_right.addWidget( self.button2 )
        self.connect( self.button2, QtCore.SIGNAL( 'clicked()' ), self.OnStop )

        self.button3 = QtGui.QPushButton( "status" )
        vbox_right.addWidget( self.button3 )
        self.connect( self.button3, QtCore.SIGNAL( 'clicked()' ), self.OnStatus )

        self.button4 = QtGui.QPushButton( "input" )
        vbox_right.addWidget( self.button4 )
        self.connect( self.button4, QtCore.SIGNAL( 'clicked()' ), self.OnInput)

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

        self.button6 = QtGui.QPushButton( "FD" )
        vbox_right.addWidget( self.button6 )
        self.connect( self.button6, QtCore.SIGNAL( 'clicked()' ), self.OnForceDownload)

        # self.input = QtGui.QTextEdit(self)
        # vbox_right.addWidget( self.input )
        #self.test_message.resize(400,200)

        #self.test_message = QtGui.QPlainTextEdit(self)
        #vbox_right.addWidget( self.test_message )

        self.test_message = QtGui.QTextEdit(self)
        vbox_right.addWidget( self.test_message )

        #self.test_message.resize(400,200)

        self.status = QtGui.QStatusBar(self)
        vbox_right.addWidget(self.status)
        self.status.showMessage('Ready')

        self.setLayout( hbox )

    def OnStart(self):
        self.TestClientStart()

    def OnStop(self):
        self.TestClientStop()

    def OnStatus(self):
        self.TestClientStatus()

    def OnInput(self):
        self.TestClientInput()

    def OnIDFY(self):
        self.TestClientInput("IdentifyDevice.py")

    def OnSTBI(self):
        self.TestClientInput("StandbyImmediate.py")

    def OnPwOn(self):
        self.TestClientInput("PowerOn.py")

    def OnPwOff(self):
        self.TestClientInput("PowerOff.py")

    def OnSE(self):
        self.TestClientInput("SecurityErase.py --mode=1")

    def OnCDU(self):
        self.TestClientInput("ConfigDriveUnique.py")

    def OnForceDownload(self):
        self.TestClientInput("ForceDownload.py;PowerOff.py;PowerOn.py;sleep 10;IdentifyDevice.py")

    def TestClientInput(self, cmd = None):
        self.test_message.clear()
        #output.write('')
        #output.flush()

        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.connect(self.list_machine[i],22,"yoxu", "YXyx2345")
                ssh.use_sudo = True
                if cmd is None:
                    cmd = self.input.toPlainText()
                try:
                    #stdin,stdout,stderr=ssh.exec_command('source /home/yoxu/.bashrc; source /mnt/ssdt/.system/Util/SetSsdtEnvironments.sh /home/yoxu/Test_Tip;%s' %cmd, timeout=30)
                    stdin,stdout,stderr=ssh.exec_command('source /home/yoxu/.bashrc;%s' %cmd, timeout=30)
                    output1 = stdout.read()
                    # error = stderr.read()
                    # if error is not None:
                    #     self.test_message.append(error) 
                    ssh.close()
                except:
                    pass
                finally:
                    #read_log = open('log1.log','rU')
                    # str1 = ''
                    # for files in read_log:
                    #     str1 += files
                    #print str1
                    self.test_message.append(output1.replace('\x00','')) 
                    #self.test_message.setText(str1)  
                    self.test_message.append(self.list_machine[i]+' '+ cmd + " excuted")

    def TestClientStart(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.use_sudo = True
                try:
                    stdin, stdout, stderr = ssh.exec_command('TestClient.py start', timeout=5)
                    for str_out in stdout.readlines():
                        self.test_message.append(str_out),
                    for str_error in stderr.readlines():
                        self.test_message.append(str_error) 
                    self.test_message.append(stdout.read()) 
                    ssh.close()
                except:
                    pass
                finally:
                    self.test_message.append( self.list_machine[i]+" Started")

    def TestClientStop(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.use_sudo = True
                #stdin, stdout, stderr = ssh.exec_command('su -c "/usr/local/sbin/SandForce/SetSsdtHostName.sh"')
                stdin, stdout, stderr = ssh.exec_command('su -c "source /mnt/ssdt/.system/Util/SetSsdtEnvironments.sh;TestClient.py stop"')
                #stdin, stdout, stderr = ssh.exec_command("TestClient.py stop", timeout=5)
                for str_out in stdout.readlines():
                    self.test_message.append(str_out),
                for str_error in stderr.readlines():
                    self.test_message.append(str_error)  
                self.test_message.append(stdout.read()) 
                ssh.close()
                if len(stderr.readlines()) == 0:
                    self.test_message.append(self.list_machine[i]+" Stopped")
                else:
                    self.test_message.append(str_error)

    def TestClientStatus(self):
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.connect(self.list_machine[i],22,"sfitest", "sandforce")
                ssh.use_sudo = True
                #stdin, stdout, stderr = ssh.exec_command('su -c "/usr/local/sbin/SandForce/SetSsdtHostName.sh"')
                #stdin, stdout, stderr = ssh.exec_command('su yoxu -c "TestClient.py start"')
                stdin, stdout, stderr = ssh.exec_command('TestClient.py status', timeout=30)
                for str_out in stdout.readlines():
                    if str_out.find('Daemon running') == 8:
                        self.test_message.append(self.list_machine[i]+" Running")
                    if str_out.find("Daemon not running") == 8:
                        self.test_message.append(self.list_machine[i]+" not Running")
                for str_error in stderr.readlines():
                    self.test_message.append(str_error) 
                self.test_message.append(stdout.read())  
                ssh.close()
         
app = QtGui.QApplication( sys.argv )
win = Window()
win.show()
app.exec_()