from django.contrib import admin


from .models import Contact


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email')


admin.site.register(Contact, ContactsAdmin)
