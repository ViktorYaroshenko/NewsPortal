from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        _1 = self.post_set.all().aggregate(Sum('post_rating'))['post_rating__sum'] * 3
        _2 = self.user.comment_set.all().aggregate(Sum('comment_rating'))['comment_rating__sum']
        _3 = self.post_set.all().aggregate(Sum('comment__comment_rating'))['comment__comment_rating__sum']
        self.author_rating = _1+_2+_3
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscriptions', related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    article = 'Статья'
    news = 'Новость'
    TYPES = [(article, 'Статья'),
             (news, 'Новость')
             ]
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TYPES, default=news)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_rating = models.IntegerField(default=0)
    category = models.ManyToManyField('Category', through='PostCategory')

    def __str__(self):
        return f'{self.title}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_rating = models.IntegerField(default=0)
    time_in = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscriptions(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f'Пользователь {self.user.username} подписан на категорию {self.category.name}'
