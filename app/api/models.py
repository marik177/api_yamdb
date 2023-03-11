from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='genres')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='categories')

    def __str__(self):
        return self.name


class Review(models.Model):
    SCORE_CHOICES = zip(range(1, 11), range(1, 11))
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField(choices=SCORE_CHOICES, default=1)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации отзыва')

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации комментария')
