# Generated by Django 3.1.1 on 2020-10-29 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0006_auto_20201029_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='riverraftinguser',
            name='lifevest_size',
            field=models.CharField(choices=[('XL', 'XL'), ('L', 'L'), ('M', 'M'), ('S', 'S'), ('XS', 'XS')], default='M', max_length=5),
            preserve_default=False,
        ),
    ]