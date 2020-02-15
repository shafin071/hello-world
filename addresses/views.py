from django.utils.http import is_safe_url
from django.views.generic import CreateView, RedirectView

from billing.models.billing_profile_models import BillingProfile
from orders.models import Order

from .forms import AddressForm
from .models import Address


class CheckoutAddressCreateView(CreateView):
    form_class = AddressForm
    template_name = "carts/checkout.html"

    def form_valid(self, form):

        try:
            previous_default_address = Address.objects.get(active=True)
            previous_default_address.active = False
            previous_default_address.save()
        except:
            pass

        instance = form.save(commit=False)
        self.request.session["billing_address_id"] = instance.id
        user = self.request.user
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)

        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()
            self.request.session["billing_address_id"] = instance.id

        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        url = next_ or next_post or None
        print("url:", url)
        if is_safe_url(url, self.request.get_host()):
            return url



class CheckoutAddressReuseView(RedirectView):

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST':
            user = self.request.user
            billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
            address_id = self.request.POST.get('address_id', None)

            try:
                order_obj, new_order_obj = Order.objects.get_or_create(billing_profile=billing_profile)
            except:
                order_obj = Order.objects.filter(billing_profile=billing_profile, status="created").last()

            if address_id is not None:
                self.request.session["billing_address_id"] = address_id
                order_obj.billing_address = Address.objects.get(id=address_id)
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        """Return the URL to redirect to after processing a valid form."""
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        url = next_ or next_post or None
        if is_safe_url(url, self.request.get_host()):
            return url




