# Generated by Django 3.0.3 on 2020-03-08 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentmemberships', '0004_auto_20200308_0705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentfuturesubscription',
            old_name='fututremembershiptype',
            new_name='futuremembershiptype',
        ),
    ]
