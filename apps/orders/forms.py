from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext as _

from apps.orders.models import Order
from apps.products.models import Product, CustomerImage, CustomerColor


class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "size",
            "color",
            "custom_image",
            "custom_color",
            "quantity",
            "update_quantity",
        ]

    size = forms.ChoiceField(widget=forms.Select(attrs={"id": "select-size"}))
    color = forms.ChoiceField(widget=forms.Select(attrs={"id": "select-sports"}))
    custom_image = forms.ChoiceField(widget=forms.Select(attrs={"id": "select-image"}))
    custom_color = forms.ChoiceField(widget=forms.Select(attrs={"id": "select-color"}))
    quantity = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"id": "product_counter", "type": "number"}),
    )
    update_quantity = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        fields = self.fields

        fields_labels = {
            "size": _("Size"),
            "color": _("Color"),
            "custom_image": _("Image"),
            "custom_color": _("Color"),
        }

        for filed_name, label in fields_labels.items():
            fields[filed_name].label = label

        # udpate choise fields
        fields_names_list = ["size", "color"]
        for field in fields_names_list:
            if (
                getattr(instance, field, None)
                and getattr(instance, field, None).count()
            ):
                fields[field].choices = [("", _("Choose an option"))] + [
                    (x.id, x.name) for x in getattr(instance, field, None).all()
                ]
            else:
                del fields[field]

        if instance.custom_image:
            fields["custom_image"].choices = [("", _("Choose an option"))] + [
                (x.id, x.name) for x in CustomerImage.objects.all()
            ]
            fields["custom_color"].choices = [("", _("Choose an option"))] + [
                (x.id, x.name) for x in CustomerColor.objects.all()
            ]
        else:
            del fields["custom_image"]
            del fields["custom_color"]

        # update quantity field
        min_quantity = instance.get_minimum_quantity().min_quantity
        max_quantity = instance.get_maximum_quantity().max_quantity

        fields["quantity"].validators.extend(
            [MinValueValidator(min_quantity), MaxValueValidator(max_quantity)]
        )
        extra = {"min": min_quantity, "max": max_quantity, "value": min_quantity}
        fields["quantity"].widget.attrs.update(extra)


class CreateOrderForm(forms.ModelForm):  # pragma: no cover

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "required": "",
                # Feel free to put inside here all the classes and IDS
                # that you need them on the frontend for the input form field
            }
        ),
    )
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"type": "text", "required": ""})
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"type": "email", "required": ""})
    )
    address = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"type": "text", "required": ""})
    )
    postal_code = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"type": "text", "required": ""})
    )
    city = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"type": "text", "required": ""})
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "type": "textarea",
                "rows": 3,
                "class": "form-control",
                "style": "background-color: #f5f5f5;",
            }
        ),
    )

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
