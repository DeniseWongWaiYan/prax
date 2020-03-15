# Generated by Django 3.0.3 on 2020-03-15 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutors', '0002_auto_20200315_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishStudentMembershipType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('english_membership_type', models.CharField(choices=[('Smile School English Full', 'English Full'), ('Smile School English Basic', 'English Basic'), ('No Smile School English', 'English No')], default='No Smile School English', max_length=30)),
                ('price', models.IntegerField(default=15)),
                ('stripe_plan_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='FutureStudentMembershipType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('future_membership_type', models.CharField(choices=[('Smile School Future', 'Future'), ('No Smile School Future', 'Future No')], default='No Smile School Future', max_length=30)),
                ('price', models.IntegerField(default=15)),
                ('stripe_plan_id', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='StudentMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(max_length=40)),
                ('englishmembership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentmemberships.EnglishStudentMembershipType')),
                ('englishtutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tutors.Tutors')),
                ('futuremembership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentmemberships.FutureStudentMembershipType')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentFutureSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscription_id', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=False)),
                ('futuremembershiptype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentmemberships.StudentMembership')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnglishSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscription_id', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=False)),
                ('englishmembershiptype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentmemberships.StudentMembership')),
            ],
        ),
    ]
