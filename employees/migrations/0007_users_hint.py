# Generated by Django 5.0.4 on 2025-02-03 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_alter_files_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='hint',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
