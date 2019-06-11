from django.shortcuts import render
import os
from .models import *
import MySQLdb
import requests
# Create your views here.


# def get_pro_list():

def show_zips(request):
    zips_path = 'F:\\iworker工作文件\\日常更新zips'
    zip_items = []
    pro_list = []
    db = MySQLdb.connect('192.168.1.111', 'root', 'root', 'django_admin')
    cursor = db.cursor()
    cursor.execute("select pro_name from update_whitecat_program;")
    for item in cursor.fetchall():
        pro_list.append(item[0])
    cursor.close()
    for zip_item in os.listdir(zips_path):
        if zip_item.endswith('.zip'):
            zip_items.append(zip_item)
    context = {
        'zip_items': zip_items,
        'pro_list': pro_list,
    }
    print(context['zip_items'], pro_list)
    return render(request, 'list_zips.html', context)
