from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404, Http404

from carts.models import Cart
from .models import Courses


class CourseListView(ListView):
    model = Courses
    template_name = "courses/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CourseListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['course_list'] = Courses.objects.all()
        return context


class CourseDetailView(DetailView):
    template_name = "courses/detail.html"
    queryset = Courses.objects.all()

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            instance = get_object_or_404(Courses, slug=slug)
        except Exception as ex:
            raise Http404("Not found...", ex)
        return instance

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context




