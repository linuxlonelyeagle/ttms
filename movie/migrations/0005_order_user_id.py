# Generated by Django 4.0.4 on 2022-06-05 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.IntegerField(default=3),
        ),
    ]
