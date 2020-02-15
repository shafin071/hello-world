from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, UpdateView


from addresses.models import Address
from addresses.forms import AddressForm
from billing.models.billing_profile_models import BillingProfile
from orders.models import Order

from .forms import LoginForm, RegisterForm, ImageUploadForm, AboutMeForm, EditProfileForm
from .models import StudentProfile

import stripe
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")

User = get_user_model()


class StudentProfileDetailView(DetailView, LoginRequiredMixin):
    template_name = "students/profile.html"
    model = StudentProfile
    login_url = 'students:login'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentProfileDetailView, self).get_context_data(**kwargs)

        student = User.objects.get(username=self.request.user)
        student_profile_obj = StudentProfile.objects.get(slug=self.kwargs.get('slug'))
        billing_profile = BillingProfile.objects.get(user=student)
        billing_address = Address.objects.filter(billing_profile=billing_profile, active=True)

        if billing_address is not None:
            active_billing_address = billing_address.last()
        else:
            active_billing_address = None

        course_list = student.enrolled_courses.all()

        # All the forms
        edit_name_form = EditProfileForm(instance=self.request.user)
        if student_profile_obj.description is None:
            placeholder = "Introduce yourself...."
        else:
            placeholder = student_profile_obj.description
        about_me_form = AboutMeForm(self.request.POST or None, initial={'description': placeholder},
                                    instance=student_profile_obj)
        image_form = ImageUploadForm(self.request.POST, self.request.FILES)
        address_change_form = AddressForm(self.request.POST or None, instance=active_billing_address)

        context['student'] = student
        context['student_profile'] = student_profile_obj
        context['course_list'] = course_list
        context['billing_address'] = active_billing_address
        context['image_form'] = image_form
        context['edit_name_form'] = edit_name_form
        context['about_me_form'] = about_me_form
        context['address_change_form'] = address_change_form

        return context



class PurchaseHistoryView(ListView, LoginRequiredMixin):
    template_name = "students/purchase_history.html"
    model = Order
    login_url = 'students:login'

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseHistoryView, self).get_context_data(*args, **kwargs)
        billing_profile = BillingProfile.objects.get(user=self.request.user)
        context['order_obj'] = Order.objects.filter(status='paid', billing_profile=billing_profile)
        return context



class ChangeNameView(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    template_name = 'students/edit_profile.html'
    model = User
    form_class = EditProfileForm
    success_message = "Your name has been updated"
    login_url = 'students:login'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('students:student_profile_view', kwargs={'slug': self.object.student_profile.slug})




class AboutMeChangeView(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    template_name = 'students/about_me.html'
    model = StudentProfile
    form_class = AboutMeForm
    success_message = "Your bio has been updated"
    login_url = 'students:login'

    def get_object(self, queryset=None):
        student_profile_slug = self.request.user.student_profile.slug
        return get_object_or_404(StudentProfile, slug=student_profile_slug)

    def get_success_url(self):
        # return reverse('students:about_me')
        return reverse('students:student_profile_view', kwargs={'slug': self.object.slug})


class AddressUpdateView(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    model = Address
    form_class = AddressForm
    success_message = "Your address has been updated"
    login_url = 'students:login'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.billing_profile = BillingProfile.objects.get(user=request.user)
            form.instance.active = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('students:student_profile_view', kwargs={'slug': self.object.billing_profile.user.student_profile.slug})


class AvatarChangeView(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    template_name = 'students/profile.html'
    model = StudentProfile
    form_class = ImageUploadForm
    success_message = "Your bio has been updated"
    warning_message = "Warning: Please upload a valid image file!"
    login_url = 'students:login'

    def get_object(self, queryset=None):
        student_profile_slug = self.request.user.student_profile.slug
        return get_object_or_404(StudentProfile, slug=student_profile_slug)

    def get_success_url(self):
        return reverse('students:student_profile_view', kwargs={'slug': self.object.slug})

    def form_invalid(self, form):
        messages.error(self.request, self.warning_message)
        return redirect("home_page")



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            # keeps user logged in after password change
            update_session_auth_hash(request, form.user)
            return redirect('students:student_profile_view')
        else:
            return redirect('students:change_password')
    else:
        form = PasswordChangeForm(user=request.user)

        context = {'form': form}
        return render(request, 'students/change_password.html', context)



def login_page(request):

    # this part comes from django authentication document
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    context = {
        "login_form": LoginForm(),
        "error": None,
        "redirect_path": redirect_path,
    }
    if request.method == 'POST':
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")


            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if is_safe_url(redirect_path, request.get_host()):
                    if redirect_path == '/students/register/' or redirect_path =='/students/profile':
                        redirect_path = '/'
                    return redirect(redirect_path)
                else:
                    return redirect("home_page")
            else:
                context["error"] = "Username/Password is incorrect"

    return render(request, "students/login.html", context)


def register_page(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST or None)

        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get("username")
            password = register_form.cleaned_data.get("password1")
            email = register_form.cleaned_data.get("email")

            next_ = request.GET.get('next')
            next_post = request.POST.get('next')
            redirect_path = next_ or next_post or None

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if is_safe_url(redirect_path, request.get_host()):
                    if redirect_path == '/students/login/' or redirect_path =='/students/profile':
                        redirect_path = "home_page"
                    return redirect(redirect_path)
                else:
                    return redirect("home_page")

    else:
        register_form = RegisterForm()

    return render(request, "students/register.html", {"register_form": register_form})



class AccountDeleteConfirmView(TemplateView):
    template_name = 'students/account_delete_confirmation.html'


class AccountDeleteView(DeleteView, SuccessMessageMixin):
    success_url = reverse_lazy('students:logout')
    success_message = "account has been deleted"
    template_name = 'students/account_delete_confirmation.html'


    def get_object(self, queryset=None):
        id_ = self.kwargs.get('pk')
        print("user:", get_object_or_404(User, id=id_))
        return get_object_or_404(User, id=id_)

    def post(self, request, *args, **kwargs):
        billing_profile = BillingProfile.objects.get(user=self.request.user)
        try:
            stripe.Customer.delete(billing_profile.customer_id)
        except:
            pass
        return super(AccountDeleteView, self).post(request, *args, **kwargs)























