# Generated by Django 3.1.2 on 2020-11-02 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_market', '0003_auto_20201030_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategory',
            old_name='pic',
            new_name='subcategory_image',
        ),
    ]
