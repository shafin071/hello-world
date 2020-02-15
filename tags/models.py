from django.db import models

from courses.models import Courses


class CourseTag(models.Model):
    tag = models.CharField(max_length=120)
    course = models.ManyToManyField(Courses, blank=True)

    def __str__(self):
        return self.tag

