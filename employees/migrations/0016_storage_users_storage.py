# Generated by Django 5.0.4 on 2025-02-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0015_notes_classfor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.IntegerField(default=1000000)),
                ('teacher', models.IntegerField(default=1000000)),
                ('clerk', models.IntegerField(default=1000000)),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='storage',
            field=models.IntegerField(default=0),
        ),
    ]
