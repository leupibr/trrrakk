# Generated by Django 2.1.5 on 2019-02-09 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_template_templaterecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templaterecord',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='templaterecord',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
