# Generated by Django 3.2.20 on 2023-07-25 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coins',
            field=models.PositiveBigIntegerField(default=3),
            preserve_default=False,
        ),
    ]
