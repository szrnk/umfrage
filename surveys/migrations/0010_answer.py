# Generated by Django 2.0.9 on 2019-01-20 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('correspondents', '0008_auto_20190117_1515'),
        ('surveys', '0009_invitation_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='correspondents.Department')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Question')),
            ],
        ),
    ]
