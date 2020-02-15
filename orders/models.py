from django.db import models
from django.db.models.signals import pre_save, post_save

from addresses.models import Address
from billing.models.billing_profile_models import BillingProfile
from carts.models import Cart
from eLearning.utils import unique_order_id_generator

# left: DB values, right: display values on admin
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile,
                cart=cart_obj,
                status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile,
                    cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    order_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.order_id, self.billing_address)

    objects = OrderManager()

    def update_total(self):
        self.order_total = self.cart.total
        self.save()
        return self.order_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        order_total = self.order_total
        if billing_profile and billing_address and order_total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    # Runs when an existing cart is changed and saved
    # order will update when you refresh, NOT save
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    # runs when a new order is created and saved
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)

