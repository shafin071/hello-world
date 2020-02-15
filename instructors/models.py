from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from .utils import unique_slug_generator


class InstructorManager(models.Manager):
    def get_by_id(self, pk):
        course_detail = self.get_queryset().filter(pk=pk)
        if course_detail.count() == 1:
            return course_detail.first()
        return None

    def get_by_slug(self, slug):
        instructor_profile = self.get_queryset().filter(slug=slug)
        if instructor_profile.count() == 1:
            return instructor_profile.first()
        return None


class Instructors(models.Model):
    fullName = models.CharField(max_length=120)
    email = models.EmailField()
    experience = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to='instructors/', null=True, blank=True)

    objects = InstructorManager()

    def get_absolute_url(self):
        return reverse("instructors:instructor_profile", kwargs={"slug": self.slug})

    def __str__(self):
        return self.fullName

    class Meta:
        verbose_name_plural = "Instructors"


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Instructors)