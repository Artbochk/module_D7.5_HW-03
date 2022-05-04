from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import signals


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.name}'


class NewsArticle(models.Model):
    name = models.CharField(max_length=128)
    news_data = models.DateField(auto_now_add=True)
    news_text = models.TextField()
    author = models.CharField(max_length=64)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.news_data} {self.name} {self.news_text} {self.author} {self.postCategory}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserCategory(models.Model):
    userThrough = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


# def user_post_save(sender, instance, signal, *args, **kwargs):
#         # Send email
#         user_greeting.delay(instance.pk)
#
#
# signals.post_save.connect(user_post_save, sender=User)





# class Appointment(models.Model):
#     date = models.DateField(
#         default=datetime.utcnow,
#     )
#     client_name = models.CharField(
#         max_length=200
#     )
#     message = models.TextField()
#
#     def __str__(self):
#         return f'{self.client_name}: {self.message}'

