# Generated by Django 5.0.4 on 2025-01-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_users_date_of_joining_alter_users_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='file',
            field=models.FileField(default=0, upload_to='uploads/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='files',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='files',
            name='parent',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
