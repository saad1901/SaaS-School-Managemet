# Generated by Django 5.0.4 on 2025-02-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0016_storage_users_storage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Storage',
        ),
        migrations.AddField(
            model_name='users',
            name='max_storage',
            field=models.IntegerField(default=0),
        ),
    ]
