from django.contrib import admin
from .models import Program, Server
# Register your models here.


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    fields = ['pro_name']
    list_display = ['pro_name']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    fields = ['pro_name', 'title', 'choice', 'ip', 'user', 'password', 'port']
    list_display = ['pro_name', 'title', 'choice']
