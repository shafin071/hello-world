from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, View

from .forms import ContactForm



class SignUpView(TemplateView):
    template_name = 'contactUs/signup.html'

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     return super().post(request, *args, **kwargs)


class SignUpPostView(View):
    # template_name = 'students/signup.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data['lastname'])
        # return data




def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Welcome to the contact page",
        "contact_form": contact_form
    }

    # check whether it's valid:
    if contact_form.is_valid():
        contact_form.save()

        fullname = contact_form.cleaned_data['fullname']
        emailFrom = contact_form.cleaned_data['email']
        subject = 'Message from eLearning.com'
        message = contact_form.cleaned_data['message']
        message_content = '%s %s' %(message, fullname)
        emailTo = [settings.EMAIL_HOST_USER]

        # Fail silently means the user will not see any errors if the email is not sent
        # send_mail(subject, message, emailFrom, emailTo, fail_silently=True)

        if request.is_ajax():
           return JsonResponse({"message": "Thank you for your submission"})

        if contact_form.errors:
            errors = contact_form.errors.as_json()
            if request.is_ajax():
                return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, 'contactUs/contact.html', context)

