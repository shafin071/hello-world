
from django.shortcuts import render

from courses.models import Courses


def search_list_view(request):
    if request.method == 'GET':
        query = request.GET.get('q', None)
        print("query:", query)
        if query is not None:
            course_list = Courses.objects.search(query)
        else:
            course_list = Courses.objects.none()

        print("course_list:", course_list)
        context = {
            'course_list': course_list,
            'query': query,
        }
        return render(request, "courses/list.html", context)
