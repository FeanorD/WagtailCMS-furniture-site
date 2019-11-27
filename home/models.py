from django.db import models

from wagtail.core.models import Page

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.snippets.models import register_snippet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    FieldRowPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtailgmaps.edit_handlers import MapFieldPanel

from wagtailcaptcha.models import WagtailCaptchaEmailForm

@register_snippet
class FooterText(models.Model):

    address = models.CharField(
        max_length=128,
        blank=True,
        help_text='Адрес компании'
    )
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        # blank = True,
    )

    formatted_address = models.CharField(
        max_length=255,
        blank=True,
    )

    panels = [
        FieldPanel('address'),
        FieldPanel('email'),
        FieldPanel('phone'),
        MapFieldPanel('formatted_address'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'


class HomePage(Page):
    """The Home Page"""
    max_count = 1

    some_text = RichTextField()
    title_field = models.CharField(
        max_length=128
    )

    image_about = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Изображение на ссылке на страницу О нас'
    )
    image_news = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Изображение на ссылке на страницу Новости'
    )
    image_works = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Изображение на ссылке на страницу Проектов'
    )


    slideshow_section = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='featured section for the homepage. Will display up to '
        'six child items.',
        verbose_name='Секция слайдшоу'
    )
    slideshow_section_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )

    about_us_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Ссылка на страницу О компании',
        help_text='Выбрать страницу О компании'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('some_text'),
            FieldPanel('title_field'),
            ImageChooserPanel('image_about'),
            ImageChooserPanel('image_news'),
            ImageChooserPanel('image_works'),
        ], heading="Секция тела страницы"),
        MultiFieldPanel([
            FieldPanel('slideshow_section_title'),
            PageChooserPanel('slideshow_section'),
        ], heading='Секция Слайдшоу'),
        MultiFieldPanel([
            PageChooserPanel('about_us_link'),
        ], heading="Секция ссылок на другие страницы")
    ]

    def __str__(self):
        return self.title_field

    class Meta:
        verbose_name = "Домашняя страница"

    # subpage_types = []

class HomePageSlides(Page):
    subpage_types = ['Slide']

    def get_slides(self):
        return Slide.objects.live().descendant_of(
            self).order_by('-first_published_at') 

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(HomePageSlides, self).get_context(request)

        # BreadPage objects (get_breads) are passed through pagination
        breads = self.get_slides

        context['slides'] = slides

        return context               

class Slide(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Изображение на слайде'
    )
    caption_field = models.CharField(
        max_length=64, 
        default=None
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('caption_field'),
            ImageChooserPanel('image'),
        ], heading='Слайд'),
    ]

    parent_page_types = ['HomePageSlides']

    class Meta:
        verbose_name = 'Слайды'
        verbose_name_plural = 'Слайды'

class AboutPage(Page):
    """
    A generic content page for About Us
    """
    title_field = models.CharField(
        max_length=128,
        blank=True,
        help_text='Оглавление перед главным текстом'
    )
    main_text = RichTextField(
        help_text = 'Главный текст о нашей компании'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Изображение'
    )
    image_text = RichTextField(
        help_text = 'Текст под фото'
    )    

    services_section = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='дополнительная секция для ссылок на предоставляемые услуги',
        verbose_name='Секция наших услуг'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('title_field'),
            FieldPanel('main_text'),
            FieldPanel('image_text'),
            ImageChooserPanel('image'),
            PageChooserPanel('services_section'),
        ])
    ]

    def __str__(self):
        return "%s" % self.title_field

    def get_services(self):
        return Slide.objects.live().descendant_of(
            self).order_by('-first_published_at') 

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(AboutPage, self).get_context(request)
        services = self.get_services
        context['services'] = services

        return context               

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    subpage_types = ['ServicePage']

class ServicePage(Page):
    """
    A generic content page for Service which company provides
    """
    title_field = models.CharField(
        max_length=128,
        blank=True,
        help_text='Оглавление перед главным текстом'
    )
    main_text = RichTextField(
        help_text = 'Главный текст о предоставляемой услуге'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Изображение'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('title_field'),
            FieldPanel('main_text'),
            ImageChooserPanel('image'),
        ])
    ]

    def __str__(self):
        return "%s" % self.title_field

    class Meta:
        verbose_name = 'Наши услуги'
        verbose_name_plural = 'Наши услуги'

    parent_page_types = ['AboutPage']

class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', related_name='form_fields', on_delete=models.CASCADE)


class ContactPage(WagtailCaptchaEmailForm):
    thank_you_text = RichTextField(blank=True)

    formatted_address = models.CharField(
        max_length=255,
        blank=True,
    )
    latlng_address = models.CharField(
        max_length=255,
        blank=True,
    )

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MapFieldPanel('formatted_address'),
        MapFieldPanel('latlng_address', latlng=True),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]