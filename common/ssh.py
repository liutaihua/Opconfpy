import paramiko
import os, time
import commands

id_rsa = '/opt/web/gifonc/ssh/webistrano.pkey'
def sftpFile(host,LocalPath,RemotePath,user = 'root',passwd = 'XXXXXXXXXXX',port = 58422):
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~",".ssh","known_hosts")))
        privatekeyfile = os.path.expanduser('%s'%id_rsa)
        mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
        ssh.connect(host,username=user,pkey=mykey,port=58422)
        sftp = ssh.open_sftp()
        sftp.put('%s'%LocalPath,'%s'%RemotePath)
        time.sleep(3)
        sftp.close()
        ssh.close()
    except paramiko.SSHException:
        ssh.close()

def sshCommand(host,cmd,user='root',passwd='XXXXXXXXXX',myport=58422):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekeyfile = os.path.expanduser('%s'%id_rsa)
    mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    ssh.connect(host,port=myport,username=user,pkey=mykey)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    f = open('/tmp/_tmpfile','w')
    for i in stdout:
        f.write(i)
    f.close()
    s = commands.getoutput('cat /tmp/_tmpfile')
#    stdout = "Successful on:[%s],exec_commands: [%s]"%(host,cmd) + " result is: " + str(a)
    return s
