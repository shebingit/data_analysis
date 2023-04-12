from django.db import models


# User upload file

class RegisterUser(models.Model):
    name=models.CharField(max_length=255,default='',null=True)
    email=models.CharField(max_length=255,default='',null=True)
    pasword=models.CharField(max_length=255,default='',null=True)

class UploadFiles(models.Model):
    reg_id=models.ForeignKey(RegisterUser, on_delete=models.CASCADE, null=True,default='')
    file_Name=models.CharField(max_length=255,default='',null=True)
    file_upload_date=models.DateField(auto_now=True,  null=True, blank=True)
    file_data=models.FileField(upload_to='files/',blank=True,null=True)
