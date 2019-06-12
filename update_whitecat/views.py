from django.shortcuts import render
import os
from .models import *
import MySQLdb
import paramiko
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


zips_path = 'F:\\iworker工作文件\\日常更新zips'
remote_dir = '/data/website/iworker2/'


def tar_zips():
    pass


def upload_zip(host, user, password, port, zip_file):
    print(host, user, password, port, zip_file)
    t = paramiko.Transport((host, int(port)))
    t.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    local_file = os.path.join(zips_path, zip_file, )
    print(local_file)
    remote_file = os.path.join(remote_dir, zip_file)
    print(remote_file)
    try:
        sftp.put(local_file, remote_file)
    except FileNotFoundError as e:
        sftp.mkdir(remote_dir)
        sftp.put(local_file, remote_file)
    t.close()


@csrf_exempt
def show_zips(request):
    zip_items = []
    pro_list = []
    db = MySQLdb.connect('192.168.1.111', 'root', 'root', 'django_admin')
    cursor = db.cursor()
    cursor.execute("select pro_name from update_whitecat_program;")
    for item in cursor.fetchall():
        pro_list.append(item[0])
    cursor.close()
    db.close()
    for zip_item in os.listdir(zips_path):
        if zip_item.endswith('.zip'):
            zip_items.append(zip_item)
    context = {
        'zip_items': zip_items,
        'pro_list': pro_list,
    }
    print(context['zip_items'], pro_list)
    return render(request, 'list_zips.html', context)


@csrf_exempt
def update_zip(request):
    selected_pro, selected_zip = request.POST.get('selected_pro'), request.POST.get('selected_zip')
    pro_name_id = Program.objects.get(pro_name=selected_pro).id
    _, _, _, title, choice, ip, port, user, password = Server.objects.get(pro_name_id=pro_name_id).__dict__.values()
    print(ip, user, password, port, selected_zip)
    upload_zip(ip, user, password, port, selected_zip)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(hostname=ip, port=port, username=user, password=password)
    stdin, stdout, stderr = client.exec_command('cd %s ; unzip -o %s' % (remote_dir, selected_zip))
    context = {
        'stderr': stderr.readlines(),
        'stdout': stdout.readlines(),
    }
    client.close()
    return render(request, 'update_zip_result.html', context)
