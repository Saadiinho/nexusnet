# Generated by Django 4.2.3 on 2023-11-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0008_remove_user_coins_remove_user_review_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default='default_profile_image.jpg', upload_to=''),
        ),
    ]