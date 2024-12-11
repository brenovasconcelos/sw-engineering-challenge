# Generated by Django 5.1.4 on 2024-12-11 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bloq', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='closed', max_length=6)),
                ('is_occupied', models.BooleanField(default=False)),
                ('bloq_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bloq.bloq')),
            ],
        ),
    ]