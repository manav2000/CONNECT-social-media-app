# Generated by Django 3.1.1 on 2020-10-02 04:39

import connect.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, storage=connect.storage_backends.PublicMediaStorage(), upload_to='avatars/'),
        ),
    ]
