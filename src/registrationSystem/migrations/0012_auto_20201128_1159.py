# Generated by Django 3.1.3 on 2020-11-28 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0011_auto_20201126_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffleentry',
            name='person_nr',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]