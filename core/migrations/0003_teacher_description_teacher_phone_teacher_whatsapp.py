# Generated by Django 5.1 on 2024-09-29 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_teacher_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='description',
            field=models.TextField(default='Некое описание', max_length=1000),
        ),
        migrations.AddField(
            model_name='teacher',
            name='phone',
            field=models.CharField(default='+996999087108', max_length=30),
        ),
        migrations.AddField(
            model_name='teacher',
            name='whatsapp',
            field=models.CharField(default='+996999087108', max_length=30),
        ),
    ]
