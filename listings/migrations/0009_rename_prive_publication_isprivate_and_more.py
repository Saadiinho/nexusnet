<<<<<<< HEAD
# Generated by Django 4.2.3 on 2023-12-02 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_rename_isprivate_publication_prive_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='prive',
            new_name='isPrivate',
        ),
        migrations.RenameField(
            model_name='publication',
            old_name='photo',
            new_name='picture',
        ),
    ]
=======
# Generated by Django 4.2.3 on 2023-12-02 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_rename_isprivate_publication_prive_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='prive',
            new_name='isPrivate',
        ),
        migrations.RenameField(
            model_name='publication',
            old_name='photo',
            new_name='picture',
        ),
    ]
>>>>>>> 710d29c1cf81e76015b4297a69c10f218c08b0b3
