from django import forms
from django.contrib import admin

from app.exceptions import InvalidTransition
from order.models import Order


class OrderAdminForm(forms.ModelForm):
    """Custom form for manage orders on admin site"""
    def clean_state(self):
        """Validate state with order's change_state method when is an update"""
        if self.instance.pk:
            next_state = self.cleaned_data['state']
            try:
                self.instance.change_state(next_state)
            except InvalidTransition as error:
                raise forms.ValidationError(error.args[0])
        return self.cleaned_data['state']


class OrderAdmin(admin.ModelAdmin):
    """Custom order admin for handle objects on admin site"""
    list_display = ['id', 'client_id', 'state']
    form = OrderAdminForm

    def get_exclude(self, request, obj=None):
        """Override exclude for only set state field when the object is new"""
        if not obj:
            # If it's a new data, exclude the 'state' field
            return ("state", )
        return super().get_exclude(request, obj)


admin.site.register(Order, OrderAdmin)
