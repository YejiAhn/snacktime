# Generated by Django 2.2 on 2019-08-10 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviewpage', '0011_auto_20190809_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='emoticon',
        ),
    ]
