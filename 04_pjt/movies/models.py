from django.db import models

# Create your models here.
class Movie(models.Model):
    national_choices = (
        ('comedy', 'comedy'),
        ('thriller', 'thriller'),
        ('romance', 'romance'),
    )

    title = models.CharField(max_length=20)
    audience = models.IntegerField()
    release_date = models.DateField()
    genre = models.CharField(max_length=30, choices=national_choices)
    score = models.FloatField()
    poster_url = models.CharField(max_length=50)
    description = models.TextField()
    actor_image = models.ImageField(blank=True, null=True)