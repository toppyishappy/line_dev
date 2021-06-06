# Generated by Django 2.2.17 on 2020-12-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservartionhistory',
            name='is_cancled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservartionhistory',
            name='reserved_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='reservartionhistory',
            name='location',
            field=models.TextField(default='', null=True),
        ),
    ]
