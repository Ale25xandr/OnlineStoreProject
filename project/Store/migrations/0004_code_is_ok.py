# Generated by Django 4.2.1 on 2023-08-13 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='is_ok',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
