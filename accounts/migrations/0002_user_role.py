# Generated by Django 2.2.17 on 2020-12-12 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'customer'), ('booker', 'booker')], default='customer', max_length=20),
        ),
    ]