# Generated by Django 5.0.7 on 2024-07-23 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_photo_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
