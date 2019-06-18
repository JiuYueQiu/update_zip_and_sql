from django.contrib import admin
from .models import Program, Server, SqlServer
# Register your models here.


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    fields = ['pro_name']
    list_display = ['pro_name']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    fields = ['pro_name', 'ip', 'user', 'password', 'port']
    list_display = ['pro_name', 'ip', 'user', 'password', 'port']


@admin.register(SqlServer)
class SqlServerAdmin(admin.ModelAdmin):
    fields = ['pro_name', 'ip', 'user', 'password', 'port', 'mysql_user', 'mysql_password']
    list_display = ['pro_name', 'ip', 'user', 'password', 'port', 'mysql_user', 'mysql_password']

