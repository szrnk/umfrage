# Generated by Django 2.0.9 on 2019-01-10 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correspondents', '0005_auto_20190110_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='contact_name',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
