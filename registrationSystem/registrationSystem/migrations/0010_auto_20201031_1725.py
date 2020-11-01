# Generated by Django 3.1.1 on 2020-10-31 16:25

from django.db import migrations, models
import registrationSystem.models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0009_auto_20201031_1646'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='riverraftinguser',
            managers=[
                ('objects', registrationSystem.models.CommonUserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', registrationSystem.models.CommonUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Staff'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='Superuser'),
            preserve_default=False,
        ),
    ]
