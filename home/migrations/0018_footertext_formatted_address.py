# Generated by Django 2.2.7 on 2019-11-27 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20191119_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='footertext',
            name='formatted_address',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
