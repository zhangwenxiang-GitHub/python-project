from ftplib import FTP
import os
import time

class FtpClient(object):

    def __init__(self,host,port=21):
        self.ftp = FTP()
        self.host = host
        self.port = port
        self.ftp.connect(self.host,self.port)
        self.ftp.encoding = 'utf-8'

    def login(self,user,passwd):
        self.ftp.login(user,passwd)
        print(self.ftp.welcome)

    def download_file(self, local_file, remote_file):  # 下载单个文件
        file_handler = open(local_file, 'wb')
        #print(file_handler)
        # self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)#接收服务器上文件并写入本地文件
        self.ftp.retrbinary('RETR ' + remote_file, file_handler.write)
        file_handler.close()
        return True

    def download_file_tree(self, local_dir, remote_dir):  # 下载整个目录下的文件
        print("远程文件夹remoteDir:", remote_dir)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        self.ftp.cwd(remote_dir)
        remote_names = self.ftp.nlst()
        print("远程文件目录：", remote_dir)
        for file in remote_names:
            local = os.path.join(local_dir, file)
            print("正在下载", self.ftp.nlst(file))
            if file.find(".") == -1:
                if not os.path.exists(local):
                    os.makedirs(local)
                self.download_file_tree(local, file)
            else:
                self.download_file(local, file)
        self.ftp.cwd("..")
        return

    def close(self):
        self.ftp.quit()

if __name__ == "__main__":
    ftp = FtpClient('192.168.2.200')
    ftp.login('pi', '123')
    # data = str(time.strftime("%m%d"))
    local_path = 'test'
    romte_path = '/ftp/test/'
    ftp.download_file_tree(local_path,romte_path)  # 从目标目录下载到本地目录d盘
    ftp.download_file('test.txt','test.txt')
    ftp.close()
    print("下载完成")