# Generated by Django 3.1.1 on 2020-11-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0015_auto_20201101_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riverraftinggroup',
            name='presentation',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Presentation'),
        ),
    ]
