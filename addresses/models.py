from django.db import models
from django_countries.fields import CountryField

from billing.models.billing_profile_models import BillingProfile


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, related_name='billing_address', on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = CountryField(multiple=False)
    state = models.CharField(max_length=120)
    postal_code = models.IntegerField(null=False, blank=False)
    active = models.BooleanField(default=False, verbose_name='Default address')

    objects = models.Manager()

    def __str__(self):
        return "{}-{}".format(self.billing_profile, self.address_line_1)

    def get_address(self):
        return "{line1},\n{line2}\n{city},\n{state} {postal}\n".format(
            line1=self.address_line_1,
            line2=self.address_line_2 or "",
            city=self.city,
            state=self.state,
            postal=self.postal_code,
            country=self.country
        )

    class Meta:
        verbose_name_plural = 'Addresses'



