# Generated by Django 2.1.7 on 2019-06-02 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20190602_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(blank=True, default='', null=True),
        ),
    ]
