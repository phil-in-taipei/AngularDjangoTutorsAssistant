from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


def calculate_expiration_date(expiration_period, purchase_date=None):
    if purchase_date is None:
        purchase_date = date.today()

    # Tutoring expiration periods — count from first day of next month
    if expiration_period in ('6_months', '12_months', '24_months'):
        # Get the first day of the next month
        if purchase_date.month == 12:
            first_of_next_month = date(purchase_date.year + 1, 1, 1)
        else:
            first_of_next_month = date(purchase_date.year, purchase_date.month + 1, 1)

        period_map = {
            '6_months': relativedelta(months=6),
            '12_months': relativedelta(months=12),
            '24_months': relativedelta(months=24),
        }
        # Subtract one day so expiration falls on the last day of the final month
        # e.g. 6 months from July 1 = January 1, minus one day = December 31
        return first_of_next_month + period_map[expiration_period] - timedelta(days=1)

    # Group class expiration periods — count from Sunday of next week
    elif expiration_period in ('12_weeks', '30_weeks', '60_weeks'):
        # weekday() returns 0=Monday through 6=Sunday
        # Days until next Sunday: if today is Sunday (6), next Sunday is 7 days away
        days_until_next_sunday = (6 - purchase_date.weekday()) % 7
        if days_until_next_sunday == 0:
            days_until_next_sunday = 7
        next_sunday = purchase_date + timedelta(days=days_until_next_sunday)

        period_map = {
            '12_weeks': timedelta(weeks=12),
            '30_weeks': timedelta(weeks=30),
            '60_weeks': timedelta(weeks=60),
        }
        # Subtract one day so expiration falls on the Saturday at end of final week
        return next_sunday + period_map[expiration_period] - timedelta(days=1)

    else:
        # Company classes have free-text expiration periods
        # Set to today so the constraint is satisfied and the admin
        # is prompted to update it manually
        return date.today()
