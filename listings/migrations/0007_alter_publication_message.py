# Generated by Django 4.2.4 on 2023-10-15 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_publication_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='message',
            field=models.TextField(max_length=1000),
        ),
    ]
