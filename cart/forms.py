from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(max_value=25)
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
