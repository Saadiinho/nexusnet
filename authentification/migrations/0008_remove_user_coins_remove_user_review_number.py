# Generated by Django 4.2.4 on 2023-10-12 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_remove_user_role_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='coins',
        ),
        migrations.RemoveField(
            model_name='user',
            name='review_number',
        ),
    ]