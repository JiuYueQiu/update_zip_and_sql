import paramiko
import datetime
import os

hostname = '192.168.1.111'
username = 'root'
password = '123.com'
port = 22


def upload(local_dir, remote_dir):
    try:
        t = paramiko.Transport(hostname, remote_dir)
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('upload file start %s' % datetime.datetime.now())
        for root, dirs, files in os.walk(local_dir):
            for filepath in files:
                local_file = os.path.join(root, filepath)
            a = local_file.replace(local_dir, '').replace('\\', '/').lstrip('/')
            remote_file = os.path.join(remote_dir, a)
            try:
                sftp.put(local_file, remote_file)
            except Exception as e:
                sftp.mkdir(remote_dir)
                sftp.put(local_file, remote_file)
                print("upload %s to remote %s" % (local_file, remote_file))
        for name in dirs:
            local_path = os.path.join(root, name)
            a = local_path.replace(local_dir, '').replace('\\', '')
            remote_path = os.path.join(remote_dir, a)
            try:
                sftp.mkdir(remote_path)
            except Exception as e:
                print("create dir %s" % remote_path, e)
        print("upload file success %s" % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(e)

