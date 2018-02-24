from django import forms
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

# Create your models here.
class WorkPageTag(TaggedItemBase):
    content_object = ParentalKey('WorkPage', related_name='tagged_items')

class WorkIndexPage(Page):
    
        def get_context(self, request):
            context = super(WorkIndexPage, self).get_context(request)
            workpages = self.get_children().live().order_by('-first_published_at')
            context['workpages'] = workpages
            return context

        pass

class WorkPage(Page):
    intro = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=WorkPageTag, blank=True)
    work_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('work_image'),
    ]

