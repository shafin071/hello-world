from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

User = settings.AUTH_USER_MODEL


import stripe
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY")



class BillingProfileManager(models.Manager):
    def create_charge(self, billing_profile):
        try:
            # charge the customer because we cannot charge the token more than once
            charge = stripe.Charge.create(
                amount=400,  # cents
                currency="usd",
                customer=billing_profile.customer_id,
            )
            message = "Success! Your card was added and charged."
            charge_successful = True


        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            message = f"{err.get('message')}"
            charge_successful = False

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            # messages.warning(self.request, "Rate limit error")
            message = "Rate limit error"
            charge_successful = False

        except stripe.error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            message = "Invalid parameters"
            charge_successful = False

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            message = "Not authenticated"
            charge_successful = False

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            message = "Network error"
            charge_successful = False

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            message = "Something went wrong. You were not charged. Please try again."
            charge_successful = False

        except Exception as e:
            message = "Something went wrong. You were not charged. Please try again."
            charge_successful = False

        return message, charge_successful


# A user email can have multiple billing profile
# but a billing profile can only have 1 email
class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
                email = instance.email
            )
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        print("creating billing profile")
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)


