from django.db import models

from api.validators import (
    score_validator,
    validate_year
)
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )


class Genre(models.Model):
    """Жанры"""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        db_index=True,
        validators=(validate_year,)
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class Review(models.Model):
    text = models.TextField(
        help_text="Введите текст отзыва",
        verbose_name="Текст отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[score_validator],
        verbose_name="Оценка произведения",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отзыва",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение с отзывом",
    )

    class Meta:
        ordering = ("-pub_date",)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв с комментарием",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="author",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата комментария",
    )
    text = models.TextField(verbose_name="Текст комментария", )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:10]
