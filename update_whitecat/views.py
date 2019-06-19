from django.shortcuts import render, HttpResponse
import os
from .models import *
import MySQLdb
import paramiko
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


zips_path = 'F:\\iworker工作文件\\日常更新zips'
sqls_path = 'F:\\iworker工作文件\\日常更新sqls'
remote_dir = '/data/website/iworker2/'


def ssh_exec(host, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password)
    return client


def upload_file(host, user, password, port, file, file_path, remote_path):
    t = paramiko.Transport((host, int(port)))
    t.connect(username=user, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    local_file = os.path.join(file_path, file, )
    remote_file = os.path.join(remote_path, file)
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
    return render(request, 'list_zips.html', context)


@csrf_exempt
def show_sqls(request):
    zip_items = []
    pro_list = []
    db = MySQLdb.connect('192.168.1.111', 'root', 'root', 'django_admin')
    cursor = db.cursor()
    cursor.execute("select pro_name from update_whitecat_program;")
    for item in cursor.fetchall():
        pro_list.append(item[0])
    cursor.close()
    db.close()
    for sql_item in os.listdir(sqls_path):
        if sql_item.endswith('.sql'):
            zip_items.append(sql_item)
    context = {
        'sql_items': zip_items,
        'pro_list': pro_list,
    }
    return render(request, 'list_sqls.html', context)


@csrf_exempt
def update_zip(request):
    selected_pro, selected_zip = request.POST.get('selected_pro'), request.POST.get('selected_zip')
    pro_name_id = Program.objects.get(pro_name=selected_pro).id
    _, _, _, ip, port, user, password = Server.objects.get(pro_name_id=pro_name_id).__dict__.values()
    file_path = 'F:\\iworker工作文件\\日常更新zips'
    remote_path = '/data/website/iworker2/'
    if request.POST.get('tar_zips') == '1':
        tar_command = "cd /data/website/iworker2 ; tar -cf $(date +%F_%H_%M_%S)_st.tar.gz system themes"
        client = ssh_exec(ip, port, user, password)
        stdin, stdout, stderr = client.exec_command(tar_command)
        if stderr.readlines():
            tar_result = 'tar_failed'
        else:
            tar_result = 'success'
        client.close()
    if request.POST.get('tar_zips') != '1' or tar_result == 'success':
        upload_file(ip, user, password, port, selected_zip, file_path, remote_path)
        unzip_command = "cd %s ; unzip -o %s" % (remote_dir, selected_zip)
        client = ssh_exec(ip, port, user, password)
        stdin, stdout, stderr = client.exec_command(unzip_command)
        if ('tar_result' in locals() or 'tar_result' in globals()) and tar_result == 'success':
            context = {
                'stderr': stderr.readlines(),
                'stdout': stdout.readlines(),
                'tar_result': tar_result,
            }
        else:
            context = {
                'stderr': stderr.readlines(),
                'stdout': stdout.readlines()
            }
        client.close()
        return render(request, 'update_zip_result.html', context)
    else:
        return HttpResponse(tar_result)


@csrf_exempt
def update_sql(request):
    selected_pro, selected_sql = request.POST.get('selected_pro'), request.POST.get('selected_sql')
    pro_name_id = Program.objects.get(pro_name=selected_pro).id
    _, _, _, ip, port, user, password, mysql_user, mysql_password = SqlServer.objects.get(pro_name_id=pro_name_id).\
        __dict__.values()
    file_path = 'F:\\iworker工作文件\\日常更新sqls'
    remote_path = '/tmp/'
    print(selected_pro, selected_sql)
    upload_file(ip, user, password, port, selected_sql, file_path, remote_path)
    update_sql_command = "source /etc/profile; mysql -u%s -p%s < /tmp/%s" % (mysql_user, mysql_password, selected_sql)
    client = ssh_exec(ip, port, user, password)
    stdin, stdout, stderr = client.exec_command(update_sql_command)
    # print(stdout.readlines(), stderr.readlines())
    err = stderr.readlines()[0]
    if not err.startswith('Warning'):
        return HttpResponse(stderr.readlines())
    else:
        return HttpResponse("update %s success \n%s \n%s" % (selected_sql, stdout.readlines(), err))
