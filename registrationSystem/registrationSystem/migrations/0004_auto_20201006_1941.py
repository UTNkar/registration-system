# Generated by Django 3.1.2 on 2020-10-06 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0003_auto_20201006_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registrationSystem.user'),
        ),
    ]
