from django.shortcuts import render
import os
from .models import *
import MySQLdb
import paramiko
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


zips_path = 'F:\\iworker工作文件\\日常更新zips'
remote_dir = '/data/website/iworker2/'


def ssh_exec(host, port, user, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        client.connect(host, port, user, password)
        stdin, stdout, stderr = client.exec_command(command)
        print(stderr.readlines(), stdout.readlines())
        return stdin, stdout, stderr
    except Exception as err:
        return err
    finally:
        client.close()


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
    print('tar_zips: %s' % request.POST.get('tar_zips'))
    if request.POST.get('tar_zips') == '1':
        tar_command = "cd /data/website/iworker2 ; tar -cf $(date %F_%T)_st.tar.gz system themes"
        stdin, stdout, stderr = ssh_exec(ip, port, user, password, tar_command)
        if stderr:
            print('tar err: %s' % stderr)
            context = {
                'tar_result': stderr
            }
            return render(request, 'list_zips.html', context)
        else:
            return render(request, 'list_zips.html', {'tar_result': 'success'})
    else:
        upload_zip(ip, user, password, port, selected_zip)
        unzip_command = "cd %s ; unzip -o %s" % (remote_dir, selected_zip)
        stdin, stdout, stderr = ssh_exec(ip, port, user, password, unzip_command)
        context = {
            'stderr': stderr.readlines(),
            'stdout': stdout.readlines(),
        }
        print(stderr.readlines(), stdout.readlines())
        return render(request, 'update_zip_result.html', context)
