from django.db import models
from django.urls import reverse

class Section(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    bodytext = models.TextField(blank=True)
    code = models.TextField(blank=True)
    image = models.ImageField(upload_to='sections/%Y/%m/%d', blank=True)

    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Article(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='created')
    description = models.TextField()
    requisites = models.TextField()
    image = models.ImageField(upload_to='articles/%Y/%m/%d', blank=True)
    img_height = models.IntegerField(default=100)
    img_width = models.IntegerField(default=100)
    sections = models.ManyToManyField(Section, through='SectionOrder')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)
    objects = models.Manager() # The default manager.

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.created.year, self.created.month, self.created.day, self.slug])

class SectionOrder(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return '{}_{}'.format(self.article.__str__(), self.section.__str__())

