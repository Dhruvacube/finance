from django.forms import ModelForm

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
