from django.db import models

# Create your models here.

class Book(models.Model):
    """
    Model for storing a Book
    """
    book_name = models.CharField(max_length = 256)
    author = models.CharField(max_length = 256)
    book_id = models.CharField(max_length = 256)
    copies = models.IntegerField(default = 0)

    def __str__(self):
        return self.book_name
