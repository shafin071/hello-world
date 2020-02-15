from django.db import models

from instructors.models import Instructors

from django.db.models.signals import pre_save
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from eLearning.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL


class CourseManager(models.Manager):
    def get_by_id(self, pk):
        course_detail = self.get_queryset().filter(pk=pk)
        if course_detail.count() == 1:
            return course_detail.first()
        return None

    def get_by_slug(self, slug):
        course_detail = self.get_queryset().filter(slug=slug)
        if course_detail.count() == 1:
            return course_detail.first()
        return None

    def search(self, query):
        lookup = Q(courseName__icontains=query) \
                      | Q(description__icontains=query) \
                      | Q(price__icontains=query) \
                      | Q(instructor__fullName__icontains=query) \
                      | Q(coursetag__tag__icontains=query)
        return self.filter(lookup).distinct()


class Courses(models.Model):
    courseName = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.CharField(max_length=120)
    price = models.FloatField(null=False, default=10.99)
    duration = models.FloatField(null=False, default=26)
    instructor = models.ForeignKey(Instructors, related_name='courses_by_instructor', null=True, blank=True, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True, null=True)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)

    objects = CourseManager()

    def get_absolute_url(self):
        # return "/courses/{slug}/".format(slug=self.slug)
        return reverse("courses:course_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.courseName

    class Meta:
        verbose_name_plural = "Courses"


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(course_pre_save_receiver, sender=Courses)

