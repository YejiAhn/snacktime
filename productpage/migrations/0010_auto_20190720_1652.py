# Generated by Django 2.1.7 on 2019-07-20 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0009_auto_20190720_0650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='product',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='liked_users',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
