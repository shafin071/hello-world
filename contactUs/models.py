from django.db import models


class Contact(models.Model):
    fullname = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    message = models.CharField(max_length=120)

    def __str__(self):
        return str(self.fullname)
