# Generated by Django 2.1.7 on 2019-07-19 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productpage', '0007_auto_20190720_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='emoticon',
            field=models.ImageField(blank=True, default='https://image.flaticon.com/icons/png/128/1742/1742384.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='PBstore',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
