from django import forms
from .models import Order, Refund


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "address",
            "postal_code",
            "city",
            "State",
        )


class OrderRetrieveForm(forms.Form):
    id = forms.UUIDField(required=True)


class OrderRefundForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.Textarea)
    images = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
