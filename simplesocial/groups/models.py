from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()

class Group(models.Model):
    name = models.CharField(unique=True,max_length= 256)
    slug = models.SlugField(unique=True,allow_unicode=True)
    description = models.TextField(blank=True,default='')
    decription_html = models.TextField(editable=False,default='',blank=True)
    members= models.ManyToManyField(User,through='GroupMember')

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})
    class Meta():
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships',on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name ='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        self.user.username
    class Meta():
        unique_together = ('group','user')
