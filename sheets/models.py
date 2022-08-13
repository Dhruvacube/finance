from datetime import date
from decimal import Decimal

from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class Banks(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    amount_deposited = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.01"))])
    amount_threshold = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.01"))])
    recurring_next_month = models.BooleanField(
        default=False,
        verbose_name=_("Recurring credit next month?"),
        help_text=_(
            "If checked, below credit will be automatically at at the"
            " start of next month. This is particularly useful for salary adjustments"
        ),
    )
    recurring_credit = models.DecimalField(null=True, blank=True,default=0.00,decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.00"))])
    color = ColorField(default='#ffffff')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")

    def __str__(self):
        return self.name
    
    @property
    def display_color(self):
        account_percentage = abs(self.amount_threshold / self.amount_deposited)
        if account_percentage < 0.75 and account_percentage > 0.5:
            return "#08cf3d"
        if account_percentage < 0.5 and account_percentage > 0.25:
            return "#ffc000"
        if account_percentage < 0.25:
            return "#ff0000"

    class Meta:
        verbose_name_plural = "Banks"
    
    def get_absolute_url(self):
        return reverse('sheets:banks')


class Category(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField(default="#FFFFFF")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "sheets:categories",
        )
    
    class Meta:
        verbose_name_plural = "Categories"


class Expense(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    date = models.DateField(default=date.today)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    repeat_next_month = models.BooleanField(
        default=False,
        verbose_name=_("Repeat next month?"),
        help_text=_(
            "If checked, this expense will be automatically duplicated at the"
            " start of next month. This is particularly useful for monthly"
            " subscriptions."
        ),
    )
    image = models.ImageField(upload_to="expenses", blank=True, null=True)
    bank = models.ForeignKey(Banks, related_name="expenses", on_delete=models.PROTECT)

    def __str__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        bank_model = self.bank
        bank_model.amount_deposited -= self.amount
        bank_model.save()
        super(Expense, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "sheets:sheet",
            kwargs={"year": self.date.year, "month": self.date.month},
        )

