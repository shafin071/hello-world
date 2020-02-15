from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed, pre_save, post_save

from courses.models import Courses

User = settings.AUTH_USER_MODEL


# A session ends when a user logs out. So if you log out and return to cart,
# the session with the current cart_id ends and a new cart_id is created
# If you create a new cart_id and then log in, the cart_id will be the same
class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id  # when you log in, your cart still stays the same
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Courses, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.pk)   # id is same as pk in the DB


def pre_save_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'pre_add' or action == 'post_add' or \
            action == 'post_remove' or action == 'post_clear':
        courses = instance.courses.all()
        total = 0
        for x in courses:
            total += Decimal(x.price)
        instance.total = total
        instance.save()


m2m_changed.connect(pre_save_cart_receiver, sender=Cart.courses.through)

