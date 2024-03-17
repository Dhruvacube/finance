from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Category, Expense, Banks


class ExpenseForm(ModelForm):
    required_css_class = "form-group-required"

    class Meta:
        model = Expense
        fields = "__all__"


class CategoryForm(ModelForm):
    required_css_class = "form-group-required"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["color"].widget.attrs["data-jscolor"] = ""

    class Meta:
        model = Category
        fields = "__all__"


class BanksForm(ModelForm):
    required_css_class = "form-group-required"

    class Meta:
        model = Banks
        fields = "__all__"

    def clean(self):
        super().clean()
        amount_deposited = self.cleaned_data.get("amount_deposited")
        amount_threshold = self.cleaned_data.get("amount_threshold")
        if amount_threshold > amount_deposited:
            raise ValidationError(
                "Amount threshold must be less than amount deposited"
            )

        if (
            self.cleaned_data.get("recurring_next_month")
            and self.cleaned_data.get("recurring_credit") == 0
        ):
            raise ValidationError("You can't have recurring credit as 0.00")
