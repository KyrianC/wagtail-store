from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(max_value=25, initial=1)
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
