from __future__ import unicode_literals

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey

from taggit.models import Tag, TaggedItemBase

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, PageChooserPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel

class WorkPage(Page):

    introduction = RichTextField()
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    subtitle = models.CharField(blank=True, max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return "%s" % self.subtitle

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'    

    parent_page_types = ['WorksIndexPage']

    subpage_types = []


class WorksIndexPage(RoutablePageMixin, Page):

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    works_section = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='',
        verbose_name='Секция проектов'
    )    

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        PageChooserPanel('works_section'),
    ]

    subpage_types = ['WorkPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self, request):
        context = super(WorksIndexPage, self).get_context(request)
        context['posts'] = WorkPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        return context


    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

