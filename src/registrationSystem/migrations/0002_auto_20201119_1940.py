# Generated by Django 3.1.3 on 2020-11-19 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RiverRaftingRaffleState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('open', 'Open'), ('drawn', 'Drawn'), ('closed', 'Closed')], max_length=20)),
            ],
            options={
                'verbose_name': 'The River Rafting Raffle',
                'verbose_name_plural': 'The River Rafting Raffle',
            },
        ),
        migrations.AddField(
            model_name='interestcheck',
            name='is_utn_member',
            field=models.BooleanField(default=False),
        ),
    ]
