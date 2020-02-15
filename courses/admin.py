from django.contrib import admin


from .models import Courses


class CourseAdmin(admin.ModelAdmin):
    list_display = ['courseName', 'instructor']

    class Meta:
        model = Courses


admin.site.register(Courses, CourseAdmin)
