# Generated by Django 2.2.7 on 2019-11-15 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_footertext_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footertext',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
