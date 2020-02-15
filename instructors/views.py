from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, Http404

from .models import Instructors


class InstructorListView(ListView):
    template_name = 'instructors/instructor_list.html'
    model = Instructors



class InstructorDetailView(DetailView):
    template_name = "instructors/instructor_profile.html"
    queryset = Instructors.objects.all()

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = get_object_or_404(Instructors, slug=slug)
        except Exception as ex:
            raise Http404("Not found...", ex)

        return instance


