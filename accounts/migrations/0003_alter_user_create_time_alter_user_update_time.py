# Generated by Django 5.1.6 on 2025-04-03 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_user_create_time_alter_user_update_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="create_time",
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="update_time",
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
