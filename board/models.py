import re
import datetime
import math

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from sorl.thumbnail import ImageField


class Post(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=140, blank=True)
    content = models.TextField(blank=True)
    image = ImageField(upload_to='board/post_image', blank=True)
    music = models.FileField(upload_to='board/post_music', blank=True)
    parent = models.ForeignKey('self', related_name='comments', blank=True, null=True)
    total_length = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.title

    def add_comment(self, commet_length):
        self.total_length += commet_length
        self.save()
        if self.parent:
            self.parent.add_comment(commet_length)

    def last_life(self):
        if self.is_immortal():
            return 2000

        live_time = datetime.datetime.utcnow()-self.datetime.replace(tzinfo=None)
        life = 48*int(12*math.atan(len(self.content)/40.0-2)+14)
        return life - live_time.total_seconds()/3600

    def is_immortal(self):
        if self.parent:
            return True
        else:
            return self.total_length > 200


class Tag(models.Model):
    name = models.CharField(max_length=140, db_index=True, editable=False)
    background_color = models.CharField(max_length=30, default='#101010')
    content_text_color = models.CharField(max_length=30, default='#FFFFFF')
    title_text_color = models.CharField(max_length=30, default='#808080')
    anchor_text_color = models.CharField(max_length=30, default='#5F9EA0')

    posts = models.ManyToManyField(Post, related_name='tags')

    def __unicode__(self):
        return self.name


@receiver(post_save, sender=Post)
def add_post_to_tag(sender, instance, **kwargs):
    tags = re.findall('#(?P<tag>.+?)#', instance.title)
    for tag_name in list(set(tags)):
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tag.posts.add(instance)


@receiver(pre_save, sender=Post)
def calc_total_length(sender, instance, **kwargs):
    if instance.pk is None:
        if instance.image:
            l = 201
        else:
            l = int(len(instance.content))
        instance.total_length = l
        if instance.parent_id is not None:
            instance.parent.add_comment(l)


@receiver(pre_delete, sender=Post)
def delete_file(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.music.delete(False)
