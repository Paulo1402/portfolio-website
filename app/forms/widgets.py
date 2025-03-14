from datetime import datetime

from django import forms


class MonthYearField(forms.DateField):
    """Custom DateField that accepts 'YYYY-MM' and converts it to 'YYYY-MM-01'."""

    def to_python(self, value):
        if not value:
            return None

        try:
            return datetime.strptime(value, "%Y-%m").date().replace(day=1)
        except ValueError:
            raise forms.ValidationError("Invalid date format. Please use YYYY-MM.")


class MonthYearWidget(forms.DateInput):
    input_type = "month"
