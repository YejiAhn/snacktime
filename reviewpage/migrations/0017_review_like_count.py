# Generated by Django 2.2 on 2019-08-10 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewpage', '0016_remove_review_emoticon'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='like_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]