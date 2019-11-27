# Generated by Django 2.2.7 on 2019-11-17 15:14

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailimages', '0001_squashed_0021'),
        ('home', '0011_homepage_about_us_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyServices',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('title_field', models.CharField(blank=True, help_text='Оглавление перед главным текстом', max_length=128)),
                ('main_text', wagtail.core.fields.RichTextField(help_text='Главный текст о предоставляемой услуге')),
                ('image', models.ForeignKey(blank=True, help_text='Изображение', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Наши услуги',
                'verbose_name_plural': 'Наши услуги',
            },
            bases=('wagtailcore.page',),
        ),
    ]
