# Generated by Django 3.0.3 on 2020-03-18 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grades', '0005_auto_20200318_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='futuregrades',
            name='student',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
