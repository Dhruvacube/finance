"""
 Command for backup database
"""

import datetime

from dateutil import relativedelta
from django.core.management.base import BaseCommand
from sheets.models import Expense, Banks


class Command(BaseCommand):
    help = "Commands to repeat the expenses and the bank recurring money"
    output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        today = datetime.datetime.today()
        last_day_of_previous_month = today.replace(day=1) - datetime.timedelta(
            days=1
        )

        for expense in Expense.objects.filter(
            repeat_next_month=True,
            date__year=last_day_of_previous_month.year,
            date__month=last_day_of_previous_month.month,
        ):
            # Trick to clone the object
            expense.pk = None
            expense.date = expense.date + relativedelta.relativedelta(months=1)
            expense.save()
        
        for bank in Banks.objects.filter(
            recurring_next_month=True,
            updated_at__year=last_day_of_previous_month.year,
            updated_at__month=last_day_of_previous_month.month,
        ):
            bank.amount_deposited += bank.recurring_credit
            bank.save()
            
        print('Done cloning expenses and recurring money of the bank')
        
