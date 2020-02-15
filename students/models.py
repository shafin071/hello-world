from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User, AbstractBaseUser
from django.urls import reverse
from django.utils.text import slugify
from students.utils import unique_slug_generator





class StudentProfile(models.Model):
    user = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    avatar = models.ImageField(upload_to='student_profile/', null=True, blank=True)
    description = models.CharField(max_length=120, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("students:student_profile_view", kwargs={"slug": self.slug})


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        print("creating billing profile")
        StudentProfile.objects.get_or_create(user=instance)


def user_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(user_slug_pre_save_receiver, sender=StudentProfile)
post_save.connect(user_created_receiver, sender=User)


