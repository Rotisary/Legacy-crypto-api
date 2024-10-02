# Generated by Django 5.1.1 on 2024-10-01 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_wallet_seed_phrase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='wallet',
        ),
        migrations.AddField(
            model_name='wallet',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='users.profile'),
        ),
    ]
