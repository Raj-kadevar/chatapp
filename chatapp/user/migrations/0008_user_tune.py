# Generated by Django 4.2.8 on 2024-01-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_chat_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tune',
            field=models.FileField(blank=True, default='audio/beep.mp3', null=True, upload_to=''),
        ),
    ]
