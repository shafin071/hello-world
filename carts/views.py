import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, View

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile, Card
from courses.models import Courses
from orders.models import Order
from students.forms import LoginForm

from .models import Cart

import stripe
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")



class CartRefreshAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        courses = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.courseName,
            "price": x.price}
            for x in cart_obj.courses.all()]

        data = {
            "courses": courses,
            "total": cart_obj.total,
        }
        return Response(data)



class CartHomeView(ListView):
    model = Cart
    template_name = "carts/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CartHomeView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['course_list'] = Courses.objects.all()
        return context



# Runs every time "add to cart" or "remove" button is clicked
class CartUpdateView(UpdateView):

    def post(self, request, *args, **kwargs):
        course_id = request.POST.get('course_id')
        if course_id is not None:
            try:
                course_obj = Courses.objects.get(id=course_id)
            except Courses.DoesNotExist:
                print("Course with that id does not exist:", course_id)
                return redirect("cart:home")
            cart_obj, new_obj = Cart.objects.new_or_get(request)
            if course_obj in cart_obj.courses.all():
                cart_obj.courses.remove(course_obj)
                course_added = False
            else:
                cart_obj.courses.add(course_obj)
                course_added = True
            request.session['cart_items'] = cart_obj.courses.count()
            if request.is_ajax():
                json_data = {
                    "added": course_added,
                    "removed": not course_added,
                    "cartItemCount": cart_obj.courses.count(),
                }
                return JsonResponse(json_data)

        return redirect("cart:home")




class CheckoutHome(View, LoginRequiredMixin):
    http_method_names = ['get']
    login_url = 'students:login'

    def get(self, request, *args, **kwargs):
        cart_obj, cart_created = Cart.objects.new_or_get(request)

        # if the cart is created in this view OR has no courses added,
        # redirect to cart:home where the cart will be displayed
        if cart_created or cart_obj.courses.count() == 0:
            return redirect("cart:home")

        billing_address_id = request.session.get("billing_address_id", None)

        user = request.user
        billing_profile, address_qs, use_address, card_obj = None, None, None, None
        login_form = LoginForm()

        if user.is_authenticated:
            billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
                user=user, email=user.email)


        order_obj, new_order_obj = Order.objects.new_or_get(billing_profile, cart_obj)

        card_obj = Card.objects.filter(billing_profile=billing_profile).last()
        address_qs = Address.objects.filter(billing_profile=billing_profile).distinct('address_line_1')

        if billing_address_id:
            try:
                use_address = Address.objects.get(id=billing_address_id)
            except Exception as ex:
                print("Exception in checkout_home:", ex)

        else:
            try:
                use_address = Address.objects.get(active=True)
            except MultipleObjectsReturned:
                use_address = Address.objects.filter(active=True).last()
            except Exception as ex:
                use_address = None

        order_obj.billing_address = use_address
        order_obj.timestamp = datetime.datetime.now()
        order_obj.save()

        address_form = AddressForm(instance=order_obj.billing_address)

        context = {
            'cart_obj': cart_obj,
            "billing_profile": billing_profile,
            "login_form": login_form,
            "address_form": address_form,
            "address_list": address_qs,
            "order": order_obj,
            "card_obj": card_obj,
            "publish_key": STRIPE_PUB_KEY
        }
        return render(request, "carts/checkout.html", context)



class CheckoutDoneView(View, LoginRequiredMixin):
    http_method_names = ['post']
    login_url = 'students:login'

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            msg = ''

            cart_obj, cart_created = Cart.objects.new_or_get(request)
            course_obj = cart_obj.courses.all()

            user = request.user
            billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
                user=user, email=user.email)

            if billing_profile is not None:
                order_obj, new_order_obj = Order.objects.new_or_get(billing_profile, cart_obj)
                if order_obj:
                    if order_obj.billing_address is None:
                        msg = "Please enter a billing address"
                        messages.error(request, msg)
                        return redirect("cart:checkout")
                    else:
                        order_obj.timestamp = datetime.datetime.now()
                        order_obj.save()
                card_obj = Card.objects.filter(billing_profile=billing_profile).last()
                if card_obj is None:
                    msg = "Please enter payment method"
                    messages.error(request, msg)
                    return redirect("cart:checkout")

            else:
                msg = "Billing profile doesn't exist. Please sign up"

            try:
                del request.session["billing_address_id"]
            except Exception as ex:
                print("Exception:", ex)

            payment_error_msg, charge_successful = BillingProfile.objects.create_charge(billing_profile)

            if charge_successful:
                is_done = order_obj.check_done()
                if is_done:
                    order_obj.mark_paid()

                    for course in course_obj:
                        course.students.add(user)

                    request.session['cart_items'] = 0
                    del request.session['cart_id']
                    return render(request, "carts/checkout-done.html", {"message": messages})

                else:
                    messages.error(request, payment_error_msg)
                    return redirect("cart:checkout")

            else:
                messages.error(request, msg)
                return redirect("cart:checkout")

        else:
            return redirect("cart:checkout")


