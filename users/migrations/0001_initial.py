# Generated by Django 5.2.3 on 2025-07-21 16:41

import django.db.models.deletion
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('nationality', models.CharField(blank=True, default='Nepal', max_length=15, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=6)),
                ('profile_image', models.ImageField(blank=True, default='users/default_user.png', null=True, upload_to=users.models.Profile.generateImagePath)),
                ('dob', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
