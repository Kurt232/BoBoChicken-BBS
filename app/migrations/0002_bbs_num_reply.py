# Generated by Django 4.1 on 2022-12-02 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bbs',
            name='num_reply',
            field=models.IntegerField(default=0),
        ),
    ]
