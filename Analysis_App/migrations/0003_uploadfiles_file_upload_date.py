# Generated by Django 4.1 on 2023-04-12 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analysis_App', '0002_registeruser_remove_uploadfiles_file_upload_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadfiles',
            name='file_upload_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]