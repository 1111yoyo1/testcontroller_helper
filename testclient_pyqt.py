
import sys
from PyQt4 import QtGui, QtCore
import paramiko
import time,os

#date = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
#output = open('log_%s.log' % date ,'w')
#output = open('log1.log' ,'w')
#output.write("%s" % time.ctime())
#output.flush()

# class SubWindow(QtGui.QDialog):
#     def __init__(self):
#         super(SubWindow , self).__init__()     
#         label = QtGui.QLabel("Hey, subwindow here!",self);

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

        self.button6 = QtGui.QPushButton( "input" )
        vbox_right.addWidget( self.button6 )
        self.connect( self.button6, QtCore.SIGNAL( 'clicked()' ), self.OnForceDownload)

        # self.input = QtGui.QTextEdit(self)
        # vbox_right.addWidget( self.input )
        #self.test_message.resize(400,200)

        self.input = QtGui.QPlainTextEdit(self)
        vbox_right.addWidget( self.input )

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
        self.TestClientInput3('source /home/yoxu/.bashrc')

    def OnIDFY(self):
        self.TestClientInput3("IdentifyDevice.py")

    def OnSTBI(self):
        self.TestClientInput3("StandbyImmediate.py")

    def OnPwOn(self):
        self.TestClientInput3("PowerOn.py")

    def OnPwOff(self):
        self.TestClientInput3("PowerOff.py")

    def OnSE(self):
        self.TestClientInput3("SecurityErase.py --mode=1")

    def OnCDU(self):
        self.TestClientInput3("ConfigDriveUnique.py")

    def OnForceDownload(self):
        #self.TestClientInput("ForceDownload.py;PowerOff.py;PowerOn.py;sleep 10;IdentifyDevice.py")
        #self.TestClientInput("python /home/yoxu/sc/sd/sd3.py --bn=877857")
        self.TestClientInput3()

    def TestClientInput2(self, cmd = None):
        self.test_message.clear()
        #output.write('')
        #output.flush()
        #s = SubWindow()
        #s.exec_()
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
                    print stdout
                    print stdin
                    #error = stderr.read() 
                    #output1 = stdout.read()
                    # error = stderr.read()
                    # if error is not None:
                    #     self.test_message.append(error) 
                    #print 1
                    ssh.close()
                except:
                    #print 2
                    pass
                finally:
                    #read_log = open('log1.log','rU')
                    # str1 = ''
                    # for files in read_log:
                    #     str1 += files
                    #print str1
                    #self.test_message.append(output1.replace('\x00','')) 
                    self.test_message.append(self.list_machine[i]+' '+ cmd + " excuted")

    def TestClientInput(self, cmd = None):
        self.test_message.clear()
        paramiko.util.log_to_file('paramiko.log')
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(self.list_machine[i],22,"yoxu", "YXyx2345")
                ssh.use_sudo = True
                if cmd is None:
                    cmd = self.input.toPlainText()
                #cmdlist = ['source /home/yoxu/.bashrc', cmd]
                cmdlist = ['source /home/yoxu/.bashrc',
                'source /mnt/ssdt/.system/Util/SetSsdtEnvironments.sh /home/yoxu/Test_Tip',
                cmd]
                # try:
                #     chl=ssh.invoke_shell(term='vterm', width=8000, height=20000)
                #     for cmds in cmdlist :
                #         chl.sendall(cmd+"\n")
                #         while not chl.recv_ready():
                #             time.sleep(2)
                #         time.sleep(30)
                #         data=chl.recv(20480)
                #         print data 
                #     ssh.close()
                # except Exception as e:
                #     print Exception
                # finally:
                #     self.test_message.append(self.list_machine[i]+' '+ cmd + " excuted")
                chl=ssh.invoke_shell(term='vterm', width=80, height=24)
                for cmds in cmdlist :
                    chl.sendall(cmd+"\n")
                    # while not chl.recv_ready():
                    #     time.sleep(10)
                    time.sleep(10)
                    data=chl.recv(1)
                    print data 
                ssh.close()

    def TestClientInput3(self, cmd = None):
        #self.test_message.clear()
        #paramiko.util.log_to_file('paramiko.log')
        for i in xrange(len(self.list_machine)):
            if self.cb[i].isChecked():
                self.__CtlConnect(self.list_machine[i])
                self.LinkSSDTTestTipEnv()
                if cmd is None:
                    stdin,stdout,stderr=sshCtl.exec_command(''+self.input.toPlainText()+'')
                else:
                    stdin,stdout,stderr=sshCtl.exec_command(cmd)
                content = stdout.read()
                output.write(content)
                output.flush()
                os.fsync(output.fileno())
                content_err = stderr.read()
                if content_err is not None:
                    output.write(content_err)
                    output.flush()
                    os.fsync(output.fileno())

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
                    #ssh.close()
                except:
                    pass
                finally:
                    self.test_message.append( self.list_machine[i]+" Started")
                cmdlist = ['su;TestClient.py start']
                chl=ssh.invoke_shell(term='vterm', width=8000, height=20000)
                for cmds in cmdlist :
                        #print cmds
                    chl.sendall(cmds+"\n")

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
                #ssh.close()
                if len(stderr.readlines()) == 0:
                    self.test_message.append(self.list_machine[i]+" Stopped")
                else:
                    self.test_message.append(str_error)
                # cmdlist = ['su;TestClient.py stop;declare -x SSDT_FIRMWARE_ROOT="/mnt/ssdt/firmware_mil"']
                # chl=ssh.invoke_shell(term='vterm', width=8000, height=20000)
                # for cmds in cmdlist :
                #         #print cmds
                #     chl.sendall(cmds+"\n")


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
                #ssh.close()
                # cmdlist = ['su;TestClient.py stop']
                # chl=ssh.invoke_shell(term='vterm', width=8000, height=20000)
                # for cmds in cmdlist :
                #         #print cmds
                #     chl.sendall(cmds+"\n")

    def __CtlConnect(self,host):

        global sshCtl
        #print "%s SSDT Test Machine   : %s" % (__GetTime(), host)   
        try:
            
            ctlUser = 'yoxu'
            ctlPasswd = 'YXyx2345'
            ctlPort=22
            paramiko.util.log_to_file('paramiko.log', level=10)
            sshCtl=paramiko.SSHClient()
            sshCtl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshCtl.connect(hostname=host,port=ctlPort, username=ctlUser,password=ctlPasswd)
        except:
            #print "%s Connection to SSDT machine failed. Test stopped." % __GetTime()
            #output.write("%s Connection to SSDT machine failed. Test stopped.\n" % __GetTime())
            raise Exception('Connection to SSDT machine failed.')

    def LinkSSDTTestTipEnv(self):
        logEnd = 0
        output.write("%s: Check the PARAMIKO LINK First\n" % time.ctime())
        output.flush()
        try:
            f = open('paramiko.log','r')
        except:
            output.write("Failed to open paramiko.log\n")
            output.flush()
            raise

        content = f.readlines()
        f.close()
        
        # for c in content:
        #     if c.find('Authentication (password) successful!') != -1:
        #         output.write("\t>>>Successfully Log into SSDT Slave\n")
        #         output.flush()
        #         logEnd = 1

        # if logEnd == 0:
        #         output.write("\t>>>Failed to Log into SSDT Slave\n\n\n\tPLEASE CHECK HOSTNAME and PASSWORD\n\n\n")
        #         output.flush()
        #         raise
        
        # output.write("%s: Check the SSDT Environment for TestTip\n" % time.ctime())
        # output.flush() 
        stdin,stdout,stderr=sshCtl.exec_command('source .bashrc; source /mnt/ssdt/.system/Util/SetSsdtEnvironments.sh /home/yoxu/Test_Tip')
        content = stdout.read()
        # if content.find('Test_Tip') != -1:
        #     output.write("\t>>>Successfully Change to TestTip\n")
        #     output.flush()
        # else:
        #     output.write("\tENVIRONMENT ERROR!!!\n\tPLEASE CHECK!!!\n")
        #     output.flush()
        #     raise

    def input(self,cmd):
        #stdin,stdout,stderr=sshCtl.exec_command('pwd;cd;source .bashrc;python /home/yoxu/sc/sd/sd3.py --bl=f1g')
        #stdin,stdout,stderr=sshCtl.exec_command('pwd;cd;source .bashrc;'+self.input.toPlainText()+'')
        pre_cmd = 'pwd;cd;pwd;source .bashrc;'
        if cmd is None:
            stdin,stdout,stderr=sshCtl.exec_command(pre_cmd + self.input.toPlainText()+'')
        else:
            stdin,stdout,stderr=sshCtl.exec_command(pre_cmd + cmd)
        content = stdout.read()
        output.write(content)
        output.flush()
        os.fsync(output.fileno())
        content_err = stderr.read()
        if content_err is not None:
            output.write(content_err)
            output.flush()
            os.fsync(output.fileno())

output = open('1.log' ,'w')
#output.write("SSDT Automation %s: Start to Log Test Progress\n\n\n" % time.ctime())
#output.flush()

app = QtGui.QApplication( sys.argv )
win = Window()
win.show()
app.exec_()