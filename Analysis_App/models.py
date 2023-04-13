from django.db import models
import pandas as pd


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

    def read_excel(self):
        file_path = self.file_data.path
        df = pd.read_excel(file_path)
        return df
