# Generated by Django 2.2.6 on 2022-03-16 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangePassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_password', models.CharField(max_length=20)),
                ('new_password', models.CharField(max_length=20)),
                ('confirm_new_password', models.CharField(max_length=20)),
            ],
        ),
    ]
