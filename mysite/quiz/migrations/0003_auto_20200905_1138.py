# Generated by Django 2.1.15 on 2020-09-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20200827_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(help_text='Enter the question text that you want displayed', verbose_name='Question'),
        ),
    ]
