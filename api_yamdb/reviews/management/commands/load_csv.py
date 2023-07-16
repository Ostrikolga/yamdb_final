from django.core.management.base import BaseCommand
import csv
import os

from django.conf import settings
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User


class Command(BaseCommand):
    """Загрузка данных из csv-файлов"""

    help = 'Загрузка данных из csv-файлов'

    def load_category(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/category.csv'),
                  'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                Category.objects.get_or_create(
                    id=row[0], name=row[1], slug=row[2]
                )

    def load_genre(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/genre.csv'),
                  'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                if row[0] != 'id':
                    Genre.objects.get_or_create(
                        id=row[0], name=row[1], slug=row[2]
                    )

    def load_titles(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/titles.csv'),
                  'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                Title.objects.get_or_create(
                    id=row[0], name=row[1], year=row[2], category_id=row[3]
                )

    def load_comments(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/comments.csv'),
                  'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                Comment.objects.get_or_create(
                    id=row[0], review_id=row[1], text=row[2], author_id=row[3]
                )

    def load_review(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/review.csv'),
                  'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                Review.objects.get_or_create(
                    id=row[0], title_id=row[1], text=row[2],
                    author_id=row[3], score=row[4]
                )

    def load_users(self):
        with open(os.path.join(settings.BASE_DIR, 'static/data/users.csv'),
                  'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip the headers
            for row in reader:
                User.objects.get_or_create(
                    id=row[0], username=row[1], email=row[2], role=row[3],
                    bio=row[4], first_name=row[5], last_name=row[6]
                )

    def handle(self, *args, **options):
        self.load_users()
        self.load_category()
        self.load_genre()
        self.load_titles()
        self.load_review()
        self.load_comments()
