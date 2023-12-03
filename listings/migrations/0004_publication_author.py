# Generated by Django 4.2.4 on 2023-10-12 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0003_publication_date_publication_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
