from django import forms
from django.db import models

from modelcluster.fields import ParentalManyToManyField

from wagtail.wagtailsnippets.models import register_snippet

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

# Create your models here.

class BlogIndexPage(Page):
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        
        context['blogpages'] = blogpages
        
        return context
    pass

class BlogPage(Page):
    body = RichTextField(blank=True, null=True)
    date = models.DateField("Post date", blank=True, null=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    post_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading = "Blog information"),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('post_image'),    
        ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'