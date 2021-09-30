from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# Create your models here.


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=50)
    name_en = models.CharField('カテゴリ名英語', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def post_count(self):
        n = Post.objects.filter(category=self).count()
        return n

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    title = models.CharField('タイトル', max_length=50)
    content = RichTextUploadingField('内容', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    thumbnail = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    
    def like_count(self):
        n = Like.objects.filter(post=self).count()
        return n

    def dislike_count(self):
        n = DisLike.objects.filter(post=self).count()
        return n

    def get_previous_by_pk(self):
        queryset = type(self).objects.filter(pk__lt=self.pk).order_by('pk').last()
        if queryset:
            return queryset
        else:
            raise self.DoesNotExist("%s matching query does not exist." % self.__class__._meta.object_name)

    def get_next_by_pk(self):
        queryset = type(self).objects.filter(pk__gt=self.pk).order_by('pk').first()
        if queryset:
            return queryset
        else:
            raise self.DoesNotExist("%s matching query does not exist." % self.__class__._meta.object_name)

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name="投稿",
        on_delete=models.PROTECT)
    user = models.ForeignKey(
        User,
        verbose_name="LIKEしたユーザー",
        on_delete=models.PROTECT)


class DisLike(models.Model):
    post = models.ForeignKey(
        Post,
        verbose_name="投稿",
        on_delete=models.PROTECT)
    user = models.ForeignKey(
        User,
        verbose_name="DisLIKEしたユーザー",
        on_delete=models.PROTECT)
