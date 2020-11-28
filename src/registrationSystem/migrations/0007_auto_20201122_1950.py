# Generated by Django 3.1.3 on 2020-11-22 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0006_riverraftingteam_join_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riverraftingteam',
            name='environment_raft',
            field=models.BooleanField(default=False, verbose_name='I want an environmentally friendly raft'),
        ),
        migrations.AlterField(
            model_name='riverraftinguser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
