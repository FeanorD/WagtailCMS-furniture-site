# Generated by Django 2.2.7 on 2019-11-15 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20191114_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='footertext',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
