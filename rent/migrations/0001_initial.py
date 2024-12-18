# Generated by Django 5.1.4 on 2024-12-11 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('status', models.CharField(choices=[('created', 'Created'), ('waiting_dropoff', 'Waiting Dropoff'), ('waiting_pickup', 'Waiting Pickup'), ('delivered', 'Delivered')], default='created', max_length=15)),
                ('size', models.CharField(choices=[('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('locker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.locker')),
            ],
        ),
    ]
