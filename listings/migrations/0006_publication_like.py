# Generated by Django 4.2.3 on 2023-10-14 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_publication_isprivate'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='like',
            field=models.PositiveIntegerField(default=0),
        ),
    ]