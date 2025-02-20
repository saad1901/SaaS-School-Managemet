# Generated by Django 5.0.4 on 2025-01-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_users_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='date_of_joining',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
