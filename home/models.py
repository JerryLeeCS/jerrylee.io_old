from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from blog.models import BlogIndexPage
from works.models import WorkIndexPage

class HomePage(Page):
    
    instagramURL = models.URLField(blank=True, null=True)
    
    snapchatURL = models.URLField(blank=True, null=True)

    resume_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    def get_context(self,request):
        context = super(HomePage, self).get_context(request)

        blog = BlogIndexPage.objects.get(title="Blog")
        works = WorkIndexPage.objects.get(title="Works")
        
        context['blog'] = blog
        context['works'] = works
        
        return context
    
    content_panels = Page.content_panels + [
        FieldPanel('instagramURL'),
        FieldPanel('snapchatURL'),
        DocumentChooserPanel('resume_file'),
        ImageChooserPanel('background_image'),  
    ]

    pass

