from django.db import models

# Create your models here.


class Program(models.Model):
    pro_name = models.CharField(max_length=50, null=False, verbose_name='私有云项目名称')

    def __str__(self):
        return self.pro_name


# TODO_CHOICE = (
#    ('Update_Zip', 'update_zip'),
#    ('Update_Sql', 'update_sql'),
# )


class Server(models.Model):
    pro_name = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name='私有云项目名称')
    # title = models.CharField(max_length=150, null=False)
    # choice = models.CharField(max_length=50, choices=TODO_CHOICE, null=False)
    ip = models.GenericIPAddressField(null=False)
    port = models.CharField(max_length=10, default=22, null=False)
    user = models.CharField(max_length=30, default='root', null=False)
    password = models.CharField(max_length=50, null=False)

    # def __str__(self):
    #     return self.pro_name.name


class SqlServer(models.Model):
    pro_name = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name='私有云项目名称')
    ip = models.GenericIPAddressField(null=False)
    port = models.CharField(max_length=10, default=22, null=False)
    user = models.CharField(max_length=30, default='root', null=False)
    password = models.CharField(max_length=50, null=False)
    mysql_user = models.CharField(max_length=10, default='root', null=False)
    mysql_password = models.CharField(max_length=50, null=False)

    # def __str__(self):
    #     return self.pro_name.name
