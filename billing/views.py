from django.conf import settings
from django.http import HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BillingProfile, Card

import stripe
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        user = self.request.user
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
            user=user, email=user.email)

        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)

        new_card_obj = None

        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)

        return Response({
            "message": "Success! Your card was added.",
            "brand": new_card_obj.brand,
            "last4": new_card_obj.last4,
            "exp_month": new_card_obj.exp_month,
            "exp_year": new_card_obj.exp_year,
        })




