# Generated by Django 4.1.7 on 2023-02-25 19:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pet_profile', '0013_remove_pet_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='id',
            field=models.CharField(default=uuid.uuid1, max_length=261),
        ),
    ]
