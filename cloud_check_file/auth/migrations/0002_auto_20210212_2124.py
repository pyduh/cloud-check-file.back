# Generated by Django 3.1.5 on 2021-02-13 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_extended', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invites',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_invited', to=settings.AUTH_USER_MODEL),
        ),
    ]