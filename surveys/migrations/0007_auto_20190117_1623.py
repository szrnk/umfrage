# Generated by Django 2.0.9 on 2019-01-17 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20190117_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]